from django.core.exceptions import ValidationError

from pble_questions.models import QuestionVote, AnswerVote, CommentVote
from pblexchange.models import Setting


def post_vote(user, post, vote_type, amount):
    if user != post.author:
        v, created = vote_type.objects.get_or_create(user=user, post=post)
        if not created:
            prev_vote = v.vote
        else:
            prev_vote = 0
        v.vote += amount
        if v.vote != 0:
            if amount > 0:
                if isinstance(v, QuestionVote):
                    post.author.userprofile.points += int(Setting.get('question_up_vote_points'))
                elif isinstance(v, AnswerVote):
                    post.author.userprofile.points += int(Setting.get('answer_up_vote_points'))
                elif isinstance(v, CommentVote):
                    post.author.userprofile.points += int(Setting.get('comment_up_vote_points'))
            else:
                if isinstance(v, QuestionVote):
                    post.author.userprofile.points += int(Setting.get('question_down_vote_points'))
                elif isinstance(v, AnswerVote):
                    post.author.userprofile.points += int(Setting.get('answer_down_vote_points'))
                elif isinstance(v, CommentVote):
                    post.author.userprofile.points += int(Setting.get('comment_down_vote_points'))
        else:
            if prev_vote == 1:
                if isinstance(v, QuestionVote):
                    post.author.userprofile.points -= int(Setting.get('question_up_vote_points'))
                elif isinstance(v, AnswerVote):
                    post.author.userprofile.points -= int(Setting.get('answer_up_vote_points'))
                elif isinstance(v, CommentVote):
                    post.author.userprofile.points -= int(Setting.get('comment_up_vote_points'))
            else:
                if isinstance(v, QuestionVote):
                    post.author.userprofile.points -= int(Setting.get('question_down_vote_points'))
                elif isinstance(v, AnswerVote):
                    post.author.userprofile.points -= int(Setting.get('answer_down_vote_points'))
                elif isinstance(v, CommentVote):
                    post.author.userprofile.points -= int(Setting.get('comment_down_vote_points'))
        try:
            v.save()
            post.author.userprofile.full_clean()
            post.author.userprofile.save()
        except ValidationError:
            post.author.userprofile.points = 1
            post.author.userprofile.save()


def answer_accept(user, post):
    if user != post.author:
        if post.accepted:
            user.userprofile.points -= int(Setting.get('accepted_answer_acceptor_points'))
            user.userprofile.save()
            post.author.userprofile.points -= int(Setting.get('accepted_answer_points'))
            post.author.userprofile.save()
        else:
            user.userprofile.points += int(Setting.get('accepted_answer_acceptor_points'))
            user.userprofile.save()
            post.author.userprofile.points += int(Setting.get('accepted_answer_points')) + post.question.bounty
            post.author.userprofile.save()
    post.question.bounty = 0
    post.question.save()


def post_bounty(user, post, bounty, challenge=0):
    points = bounty + challenge
    if user.userprofile.points < bounty and user.userprofile.challenge_points < challenge:
        return
    user.userprofile.points -= bounty
    user.userprofile.challenge_points -= challenge
    user.userprofile.save()
    post.bounty = points
    post.is_challenge = challenge > 0
