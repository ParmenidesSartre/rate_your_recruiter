from django.contrib import admin
from .models import UserActivity, UserBadge, UserLevel, Leaderboard, Level, Badge

# Admin for User Activities


class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity_type', 'points', 'created_at')
    search_fields = ('user__username', 'activity_type')
    list_filter = ('activity_type', 'created_at')

# Admin for User Badges


class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ('user', 'badge', 'awarded_at')
    search_fields = ('user__username', 'badge__name')
    list_filter = ('badge__name',)

# Admin for User Levels


class UserLevelAdmin(admin.ModelAdmin):
    list_display = ('user', 'level', 'achieved_at')
    search_fields = ('user__username', 'level__name')
    list_filter = ('level__name',)

# Admin for Leaderboards


class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ('user', 'position', 'points')
    search_fields = ('user__username',)
    list_filter = ('position',)
    ordering = ('position',)

# Admin for Level Presets


class LevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'threshold')
    search_fields = ('name',)

# Admin for Badge Presets


class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


# Registering models with the admin site
admin.site.register(UserActivity, UserActivityAdmin)
admin.site.register(UserBadge, UserBadgeAdmin)
admin.site.register(UserLevel, UserLevelAdmin)
admin.site.register(Leaderboard, LeaderboardAdmin)
admin.site.register(Level, LevelAdmin)
admin.site.register(Badge, BadgeAdmin)
