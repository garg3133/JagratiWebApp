from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

app_name = 'accounts'
urlpatterns = [
    path('login/', views.login_signup, name='login_signup'),
    path('complete_profile/', views.complete_profile, name='complete_profile'),
    path('logout/', views.logout_view, name='logout'),
    path('activate/<slug:uidb64>/<slug:token>/', views.account_activation, name='account_activation'),
    path('authenticate/<slug:uidb64>/<slug:token>/', views.account_authentication, name='account_authentication'),

    path('signup/success/', views.signup_success, name='signup_success'),
    path('profile_completed/', views.profile_completed, name='profile_completed'),
    path('authenticated/', views.account_authenticated, name='account_authenticated'),

    # Django Auth URLs
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    #AJAX call URLs
    path('ajax_volun_roll/', views.ajax_volunteer_rollcheck, name='volunteer_rollcheck'),

]