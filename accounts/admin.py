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

from applications.volunteers.admin import VolunteerInline
from .forms import UserAdminCreationForm
from .models import User, Profile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances

    # form = UserAdminChangeForm
    # Will override default password checks (like password too common)
    # and validations with those specified in this form.
    # Also 'desig' field won't work without this.
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'desig', 'auth')
    search_fields = ('email',)
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ('user_permissions', 'groups')
    list_filter = ('desig', 'auth', 'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('desig',)}),
        ('Permissions', {'fields': ('is_active', 'auth', 'is_staff', 'is_superuser')}),
        ('Permissions and Groups', {'fields': ('user_permissions', 'groups')}),
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

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'get_email', 'get_desig', 'get_auth')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('user__desig', 'user__auth')
    ordering = ('-user__date_joined',)

    inlines = [VolunteerInline]

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

    def get_desig(self, obj):
        return obj.user.get_desig_display()
    get_desig.short_description = 'Designation'

    def get_auth(self, obj):
        return obj.user.auth
    get_auth.short_description = 'Auth'
    get_auth.admin_order_field = 'user__auth'
    get_auth.boolean = True