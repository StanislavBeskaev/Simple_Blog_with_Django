from django.urls import path

from . import views


urlpatterns = [
    path('post_list', views.post_list_view, name='post_list'),  # Страница списка постов
    path('create_post', views.CreatePostView.as_view(), name='create_post'),  # страница создания поста
    path('post_detail/<int:pk>', views.PostDetailView.as_view(), name='post_detail'),  # страница детальной информации о посте
    path('create_posts_from_file', views.CreatePostsFromFileView.as_view(), name='create_posts_from_file')
]
