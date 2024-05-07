from django.db import models
from django.conf import settings
from django.utils.timezone import now

# Preset Levels


class Level(models.Model):
    name = models.CharField(max_length=100)
    threshold = models.PositiveIntegerField()

    def __str__(self):
        return f"Level {self.name} - Threshold: {self.threshold}"

# Preset Badges


class Badge(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

# User Level Tracking


class UserLevel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    achieved_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.user.username} - Level {self.level.name}"

# User Badge Tracking


class UserBadge(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    badge = models.ForeignKey(
        Badge, on_delete=models.CASCADE, related_name='badges', null=True, blank=True)
    awarded_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.user.username} - {self.badge.name}"

# Tracking user activities and points


class UserActivity(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=100)
    points = models.PositiveIntegerField()
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.user.username} - {self.activity_type} - {self.points} points"

# Leaderboard tracking current standings


class Leaderboard(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    position = models.PositiveIntegerField(unique=True)
    points = models.PositiveIntegerField()

    def __str__(self):
        return f"Position {self.position} - {self.user.username} - {self.points}"

    class Meta:
        ordering = ['position']
