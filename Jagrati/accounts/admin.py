# from django.contrib import admin
# from django.contrib.auth import get_user_model #coz model in auth is now our custom model
# # we can also do from .models import ...?\
# from .forms import UserAdminChangeForm, UserAdminCreationForm

# # Register your models here.
# User = get_user_model()

# class UserAdmin(admin.ModelAdmin):
#     form = UserAdminChangeForm
#     add_form = UserAdminCreationForm

# admin.site.register(User, UserAdmin)

from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


# from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import User

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances

    # form = UserAdminChangeForm
    # add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'desig', 'auth')
    search_fields = ('email',)
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ('desig', 'auth', 'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('desig',)}),
        ('Permissions', {'fields': ('is_active', 'auth', 'is_staff', 'is_admin')}),
        ('Others', {'fields': ('date_joined', 'last_login')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'desig')}
        ),
    )
    
    ordering = ('email',)


admin.site.register(User, UserAdmin)



# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)