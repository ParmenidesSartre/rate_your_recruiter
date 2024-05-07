from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import RecruiterReview
from gamification.models import UserActivity, Level, UserLevel


@receiver(post_save, sender=RecruiterReview)
def handle_review_activity(sender, instance, created, **kwargs):
    """Handles the creation of UserActivity instances and updates user levels when reviews are posted or updated."""
    points = 10 if created else 5
    activity_type = 'Review Posted' if created else 'Review Updated'

    # Only create activity if it's a new review or an update that hasn't yet been awarded points.
    if created or (not created and not instance.points_awarded_for_update):
        UserActivity.objects.create(
            user=instance.user, activity_type=activity_type, points=points)

        # Update that points have been awarded for this update to prevent spam
        if not created:
            instance.points_awarded_for_update = True
            instance.save(update_fields=['points_awarded_for_update'])

    update_user_level(instance.user)


def update_user_level(user):
    """Updates the user's level based on total accumulated points."""
    total_points = UserActivity.objects.filter(
        user=user).aggregate(Sum('points'))['points__sum'] or 0
    new_level = Level.objects.filter(
        threshold__lte=total_points).order_by('-threshold').first()

    if new_level:
        current_level = UserLevel.objects.filter(
            user=user).order_by('-level__threshold').first()
        if not current_level or current_level.level.threshold < new_level.threshold:
            UserLevel.objects.update_or_create(
                user=user, defaults={'level': new_level})
