from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.index, name='index'),

    path('create/', views.create, name='create'),
    path('<int:post_id>/comments/create/', views.comment_create, name='comment_create'),
    
    path('<int:post_id>/like/', views.like, name='like'),
    path('<int:post_id>/like-async/', views.like_async, name='like_async'),

    path('<int:post_id>/delete/', views.post_delete, name='post_delete'), 
    path('<int:post_id>/comment/<int:id>/delete', views.comment_delete, name='comment_delete'),
]