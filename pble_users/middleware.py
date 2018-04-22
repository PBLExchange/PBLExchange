from django.utils.translation import activate


class LanguageMiddleware(object):
    """Finds the users preferred language, and activates it."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        assert hasattr(request, 'user')
        if request.user.is_authenticated():
            lang = request.user.usersettings.language
            activate(lang)

        return self.get_response(request)
