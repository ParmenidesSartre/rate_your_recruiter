from django.contrib import admin
from .models import UserActivity,  UserLevel, Leaderboard, Level


class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity_type', 'points', 'created_at')
    search_fields = ('user__username', 'activity_type')
    list_filter = ('activity_type', 'created_at')


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


class LevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'threshold')
    search_fields = ('name',)


admin.site.register(UserActivity, UserActivityAdmin)
admin.site.register(UserLevel, UserLevelAdmin)
admin.site.register(Leaderboard, LeaderboardAdmin)
admin.site.register(Level, LevelAdmin)
