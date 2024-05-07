from django.core.management.base import BaseCommand
from gamification.utils import update_user_level, update_leaderboard
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Updates user levels and leaderboard'

    def handle(self, *args, **options):
        User = get_user_model()
        for user in User.objects.all():
            update_user_level(user)
        update_leaderboard()
        self.stdout.write(self.style.SUCCESS(
            'Successfully updated gamification data'))
