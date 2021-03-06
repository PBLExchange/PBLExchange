"""Custom CAS authentication backend"""
from django_cas_ng.backends import CASBackend

from django.contrib.auth import get_user_model
from django.conf import settings

from django_cas_ng.signals import cas_user_authenticated
from django_cas_ng.utils import get_cas_client

from pble_users import models as users_model
from pble_subscriptions.models import Subscription

class CustomCASBackend(CASBackend):
    # Modifications/additions are indicated by a comment '# Extra ...'
    def authenticate(self, request, ticket, service):
        """Verifies CAS ticket and gets or creates User object"""
        client = get_cas_client(service_url=service)
        username, attributes, pgtiou = client.verify_ticket(ticket)
        if attributes and request:
            request.session['attributes'] = attributes

        if not username:
            return None
        user = None
        username = self.clean_username(username)
        domain = username
        # Extra added line, to ensure it is not the full email address
        if "@" in username:
            domain = username.split('@')[1]
            username = username.split('@')[0]

        EXEMPT_USERS = []
        DISALLOWED_DOMAINS = []

        if hasattr(settings, 'EXEMPT_USERS'):
            EXEMPT_USERS += settings.EXEMPT_USERS

        if hasattr(settings, 'DISALLOWED_DOMAINS'):
            DISALLOWED_DOMAINS += settings.DISALLOWED_DOMAINS

        if domain in DISALLOWED_DOMAINS and username not in EXEMPT_USERS:
            return None

        UserModel = get_user_model()

        # Note that this could be accomplished in one try-except clause, but
        # instead we use get_or_create when creating unknown pble_users since it has
        # built-in safeguards for multiple threads.
        if settings.CAS_CREATE_USER:
            user, created = UserModel._default_manager.get_or_create(**{
                UserModel.USERNAME_FIELD: username
            })
            if created:
                # Extra parameter, attributes, added
                user = self.configure_user(user, attributes)
            else:
                self.fill_misc_info(user, attributes)
        else:
            created = False
            try:
                user = UserModel._default_manager.get_by_natural_key(username)
            except UserModel.DoesNotExist:
                pass

        if not self.user_can_authenticate(user):
            return None

        if pgtiou and settings.CAS_PROXY_CALLBACK and request:
            request.session['pgtiou'] = pgtiou

        if settings.CAS_APPLY_ATTRIBUTES_TO_USER and attributes:
            # If we are receiving None for any values which cannot be NULL
            # in the User model, set them to an empty string instead.
            # Possibly it would be desirable to let these throw an error
            # and push the responsibility to the CAS provider or remove
            # them from the dictionary entirely instead. Handling these
            # is a little ambiguous.
            user_model_fields = UserModel._meta.fields
            for field in user_model_fields:
                # Handle null -> '' conversions mentioned above
                if not field.null:
                    try:
                        if attributes[field.name] is None:
                            attributes[field.name] = ''
                    except KeyError:
                        continue
                # Coerce boolean strings into true booleans
                if field.get_internal_type() == 'BooleanField':
                    try:
                        boolean_value = attributes[field.name] == 'True'
                        attributes[field.name] = boolean_value
                    except KeyError:
                        continue

            user.__dict__.update(attributes)

            # If we are keeping a local copy of the user model we
            # should save these attributes which have a corresponding
            # instance in the DB.
            if settings.CAS_CREATE_USER:
                user.save()

        # send the `cas_user_authenticated` signal
        cas_user_authenticated.send(
            sender=self,
            user=user,
            created=created,
            attributes=attributes,
            ticket=ticket,
            service=service,
            request=request
        )
        return user

    def configure_user(self, user, attributes):
        user.username = user.username
        user.email = attributes['mail']
        user.first_name = attributes['givenName']
        user.last_name = attributes['sn']

        # create a user profile & settings
        new_user_profile = users_model.UserProfile.objects.create(user=user)
        new_user_profile.save()
        new_user_settings = users_model.UserSetting.objects.create(user=user)
        new_user_settings.save()

        # create user subscription
        new_user_subscription = Subscription.objects.create(user=user)
        new_user_subscription.save()
        return user

    def fill_misc_info(self, user, attributes):
        if not user.first_name or not user.last_name:
            user.first_name = attributes['givenName']
            user.last_name = attributes['sn']
