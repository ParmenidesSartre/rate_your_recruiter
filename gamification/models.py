from django.db import models
from django.conf import settings
from django.utils.timezone import now


class Level(models.Model):
    name = models.CharField(max_length=100)
    threshold = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} (Threshold: {self.threshold})"

    class Meta:
        verbose_name = "Level"
        verbose_name_plural = "Levels"


class UserLevel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    achieved_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.user.username} - {self.level.name}"

    class Meta:
        verbose_name = "User Level"
        verbose_name_plural = "User Levels"


class UserActivity(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=100)
    points = models.PositiveIntegerField()
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.user.username} - {self.activity_type} ({self.points} points)"

    class Meta:
        verbose_name = "User Activity"
        verbose_name_plural = "User Activities"


class Leaderboard(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    position = models.PositiveIntegerField(unique=True)
    points = models.PositiveIntegerField()

    def __str__(self):
        return f"#{self.position} - {self.user.username} ({self.points} points)"

    class Meta:
        verbose_name = "Leaderboard Entry"
        verbose_name_plural = "Leaderboard"
        ordering = ['position']
