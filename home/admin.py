from django.contrib import admin
from .models import CustomUser, UserProfile, UserPost, Comments
# Register your models here.



class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'password')  # Display these fields in the list view
    search_fields = ['username', 'email']  # Enable search by username
    list_filter = ('password',)  # Add a filter for password

    actions = ['make_active', 'make_inactive']  # Define custom actions
    def get_actions(self, request):
        actions = super().get_actions(request)
        return actions

    def make_active(self, request, queryset):
        queryset.update(password=True)

    make_active.short_description = "Make selected items active"

    def make_inactive(self, request, queryset):
        queryset.update(password=False)

    make_inactive.short_description = "Make selected items inactive"


    def has_delete_permission(self, request, obj=None):
        return True  # Enable/Disable delete permission

    def has_add_permission(self, request):
        return True  # Enable/Disable add permission
    

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'profession')  # Display these fields in the list view
    search_fields = ['username']  # Enable search by username
    list_filter = ('email',)  # Add a filter for email

    def get_actions(self, request):
        actions = super().get_actions(request)
        return actions

    def has_delete_permission(self, request, obj=None):
        return False  # Enable/Disable delete permission

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

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserPost, UserPostAdmin)
admin.site.register(Comments)
