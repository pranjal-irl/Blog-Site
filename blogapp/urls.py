from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('article/<slug:slug>/', views.article_detail, name='article_detail'),
    path('article/<slug:slug>/like/', views.like_article, name='like_article'),
    path('article/<slug:slug>/comment/', views.add_comment, name='add_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    path('login/', views.login_view, name='login'),
    path('signup', views.signup_view, name='signup'),
]