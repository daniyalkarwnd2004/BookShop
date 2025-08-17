from django.urls import path
from . import views
from django.contrib.auth import views as auth_view
from django.urls import reverse_lazy

app_name = "blog"

urlpatterns = [
    path('', views.home, name='home'),
    path('book/', views.list_book, name='list_book'),
    path('book/<int:id>/', views.detail_book, name='detail_book'),
    path('book/<int:book_id>/comment', views.comment_book, name='comment_book'),
    path('ticket/', views.ticket, name='ticket'),
    path('search/', views.search, name='search'),
    path('profile/', views.profile, name='profile'),
    path('about/', views.about_project, name='about'),
    path('help/', views.project_help, name='help'),
    path('terms/', views.terms_of_use, name='terms'),
    path('my_books/', views.my_library, name='my_books'),
    path('download/<int:book_id>/', views.download_book, name='download_book'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('password-change/', auth_view.PasswordChangeView.as_view(
        template_name='blog/password_change_form.html', success_url='/password-change/done/'), name='password_change'),
    path('password-change/done/', auth_view.PasswordChangeDoneView.as_view(
        template_name='blog/password_change_done.html'), name='password_change_done'),
    path('password-reset/', views.password_reset_request_view, name='password_reset'),
    path('password-reset/done/', views.password_reset_done_view, name='password_reset_done'),
    path('reset-password-confirm/<uidb64>/<token>/', views.password_reset_confirm_view, name='password_reset_confirm'),
    path('password-reset/complete/', views.password_reset_complete_view, name='password_reset_complete'),
    path('register/', views.register, name='register'),
    path('user_edit/', views.user_edit, name="user_edit")
]
