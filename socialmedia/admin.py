from django.contrib import admin
from .models import UserProfile, UserPost, Comments, UserFollower, PostLike
# Register your models here.
    
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'profession')  # Display these fields in the list view
    search_fields = ['username']  # Enable search by username
    list_filter = ('email',)  # Add a filter for email

    def get_actions(self, request):
        actions = super().get_actions(request)
        return actions

    def has_delete_permission(self, request, obj=None):
        return True  # Enable/Disable delete permission

    def has_add_permission(self, request):
        return True  # Enable/Disable add permission


class UserPostAdmin(admin.ModelAdmin):
    list_display = ('username', 'post_title', 'created_at')  # Display these fields in the list view
    search_fields = ['username']  # Enable search by username
    list_filter = ('post_title', 'username')  # Add a filter for post_title

    def get_actions(self, request):
        actions = super().get_actions(request)
        return actions

    def has_delete_permission(self, request, obj=None):
        return True  # Enable/Disable delete permission

    def has_add_permission(self, request):
        return False  # Enable/Disable add permission

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserPost, UserPostAdmin)
admin.site.register(Comments)
admin.site.register(UserFollower)
admin.site.register(PostLike)
