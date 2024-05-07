from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import RecruiterReview
from gamification.models import UserActivity, Level, UserLevel, Badge, UserBadge


@receiver(post_save, sender=RecruiterReview)
def handle_review_activity(sender, instance, created, **kwargs):
    # Points logic
    if created:
        # Add points for creating a review
        points = 10
        activity_type = 'Review Posted'
        UserActivity.objects.create(
            user=instance.user, activity_type=activity_type, points=points)
    elif not instance.points_awarded_for_update:
        # Add points for updating a review
        points = 5
        activity_type = 'Review Updated'
        UserActivity.objects.create(
            user=instance.user, activity_type=activity_type, points=points)
        # Update that points have been awarded for this update to prevent spam
        RecruiterReview.objects.filter(pk=instance.pk).update(
            points_awarded_for_update=True)

    # Update user's level based on total points
    update_user_level(instance.user)


def update_user_level(user):
    total_points = UserActivity.objects.filter(
        user=user).aggregate(Sum('points'))['points__sum']
    new_level = Level.objects.filter(
        threshold__lte=total_points).order_by('-threshold').first()
    if new_level:
        current_level = UserLevel.objects.filter(
            user=user).order_by('-level__threshold').first()
        if not current_level or current_level.level.threshold < new_level.threshold:
            UserLevel.objects.update_or_create(
                user=user, defaults={'level': new_level})


@receiver(post_save, sender=RecruiterReview)
def handle_review_activity(sender, instance, created, **kwargs):
    # Points logic
    if created:
        # Add points for creating a review
        points = 10
        activity_type = 'Review Posted'
        UserActivity.objects.create(
            user=instance.user, activity_type=activity_type, points=points)
    elif not instance.points_awarded_for_update:
        # Add points for updating a review
        points = 5
        activity_type = 'Review Updated'
        UserActivity.objects.create(
            user=instance.user, activity_type=activity_type, points=points)
        # Update that points have been awarded for this update to prevent spam
        RecruiterReview.objects.filter(pk=instance.pk).update(
            points_awarded_for_update=True)

    # Update user's level based on total points
    update_user_level(instance.user)


def update_user_level(user):
    total_points = UserActivity.objects.filter(
        user=user).aggregate(Sum('points'))['points__sum']
    new_level = Level.objects.filter(
        threshold__lte=total_points).order_by('-threshold').first()
    if new_level:
        current_level = UserLevel.objects.filter(
            user=user).order_by('-level__threshold').first()
        if not current_level or current_level.level.threshold < new_level.threshold:
            UserLevel.objects.update_or_create(
                user=user, defaults={'level': new_level})


def maybe_award_first_review_badge(user):
    if not UserBadge.objects.filter(user=user, badge__name='First Review').exists():
        first_review_badge = Badge.objects.get(name='First Review')
        UserBadge.objects.create(user=user, badge=first_review_badge)
