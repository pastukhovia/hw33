from django.contrib import admin

from .models import GoalCategory, Goal, Comment


class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created", "updated")
    search_fields = ("title", "user")


class GoalAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created", "updated", 'category', 'description', 'status', 'priority', 'due_date')
    search_fields = ("title", "user", 'description')


class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "created", "updated", 'text', 'goal')
    search_fields = ("goal", "user", 'text')


admin.site.register(GoalCategory, GoalCategoryAdmin)
admin.site.register(Goal, GoalAdmin)
admin.site.register(Comment, CommentAdmin)
