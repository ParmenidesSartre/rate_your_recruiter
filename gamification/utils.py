from django.db.models import Sum
from .models import UserActivity, UserLevel, Level, Leaderboard
from django.contrib.auth import get_user_model


def update_user_level(user):
    # Calculate the total points for the user
    total_points = UserActivity.objects.filter(
        user=user).aggregate(total=Sum('points'))['total'] or 0
    # Find the highest level the user qualifies for based on their points
    new_level = Level.objects.filter(
        threshold__lte=total_points).order_by('-threshold').first()
    if new_level:
        # Get or create a UserLevel instance and update it if necessary
        user_level, created = UserLevel.objects.get_or_create(user=user)
        if not created and user_level.level != new_level:
            user_level.level = new_level
            user_level.save()
        elif created:
            user_level.level = new_level
            user_level.save()


def update_leaderboard():
    # Aggregate total points for each user and order them by total points descending
    leaderboard_data = UserActivity.objects.values('user').annotate(
        total_points=Sum('points')).order_by('-total_points')
    # Update the leaderboard entries
    for idx, data in enumerate(leaderboard_data):
        user = get_user_model().objects.get(id=data['user'])
        Leaderboard.objects.update_or_create(
            user=user,
            defaults={'position': idx + 1, 'points': data['total_points']}
        )
