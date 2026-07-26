from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_articles_view, name='home'),
    path('article/<slug:slug>/', views.article_detail, name='article_detail'),
    path('article/<slug:slug>/like/', views.like_article, name='like_article'),
    path('article/<slug:slug>/comment/', views.add_comment, name='add_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    path('login/', views.login_view, name='login'),
    path('signup', views.signup_view, name='signup'),
    path('continue_guest/', views.continue_as_guest, name='continue_guest'),
    path('htmx/login-form/', views.htmx_login_form, name='htmx_login_form'),
    path('htmx/signup-form/', views.htmx_signup_form, name='htmx_signup_form'),
    path('subscribe-notify/', views.subscribe_notification, name='subscribe_notify'),
    path('htmx/welcome-form/', views.htmx_welcome_form, name='htmx_welcome_form'),
]