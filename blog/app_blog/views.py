from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic.base import View
from django.utils.translation import gettext as _

from core.handlers import get_correct_file_path_to_img_tag
from .forms import CreatePostForm, CreatePostsFromFileForm
from .models import Post
from .services.post_services import get_post_list, get_post_images, create_post, create_posts_from_file


def post_list_view(request):
    """Вью для страницы списка постов"""
    context = {'post_list': get_post_list()}
    return render(request, 'post_list.html', context)


class CreatePostView(View):
    """Вью для страницы создания поста"""

    def get(self, request):
        # Создание поста доступно только для авторизованных пользователей
        if not request.user.is_authenticated:
            raise PermissionDenied()
        create_post_form = CreatePostForm()
        context = {'form': create_post_form}
        return render(request, 'create_post.html', context)

    def post(self, request):
        if not request.user.is_authenticated:
            raise PermissionDenied()
        create_post_form = CreatePostForm(request.POST, request.FILES)
        if create_post_form.is_valid():
            create_post(user=request.user,
                        post_title=create_post_form.cleaned_data['post_title'],
                        post_content=create_post_form.cleaned_data['post_content'],
                        post_images=request.FILES.getlist('images_field')
                        )

            return redirect('post_list')

        # Если форма не прошла валидацию
        context = {'form': create_post_form}
        return render(request, 'create_post.html', context)


class PostDetailView(generic.DetailView):
    """Вью для детальной страницы поста"""
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_images'] = get_post_images(context['post'])
        avatar_path = get_correct_file_path_to_img_tag(context['post'].post_author.profile.avatar_image_file)
        context['avatar_path'] = avatar_path
        return context


class CreatePostsFromFileView(View):
    """Вью для страницы создания постов из файла"""

    def get(self, request):
        # Создание постов доступно только для авторизованных пользователей
        if not request.user.is_authenticated:
            raise PermissionDenied()
        create_posts_from_file_form = CreatePostsFromFileForm()
        context = {'form': create_posts_from_file_form}
        return render(request, 'create_posts_from_file.html', context)

    def post(self, request):
        if not request.user.is_authenticated:
            raise PermissionDenied()
        create_posts_from_file_form = CreatePostsFromFileForm(request.POST, request.FILES)
        context = {'form': create_posts_from_file_form}
        if create_posts_from_file_form.is_valid():
            is_corrects, message = create_posts_from_file(user=request.user,
                                                          posts_file=create_posts_from_file_form.cleaned_data['posts_file']
                                                          )
            context['message'] = message
            return render(request, 'create_posts_from_file.html', context)

        # Если форма не прошла валидацию
        context['message'] = _('Form is invalid')
        return render(request, 'create_posts_from_file.html', context)
