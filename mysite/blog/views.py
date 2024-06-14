from django.shortcuts import render
from django.views import generic
from .models import Post, Comment
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class PostListView(generic.ListView):
    model = Post
    context_object_name = "posts"
    template_name = "posts.html"
    paginate_by = 5


class PostDetailView(generic.DetailView):
    model = Post
    context_object_name = "post"
    template_name = "post.html"


def search(request):
    query = request.GET.get('query')
    post_search_results = Post.objects.filter(
        Q(title__icontains=query) | Q(content__icontains=query) | Q(author__username__icontains=query))
    return render(request, 'search.html', context={"posts": post_search_results, "query": query})


class UserPostListView(LoginRequiredMixin, generic.ListView):
    model = Post
    template_name = "user_posts.html"
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)


class UserCommentListView(LoginRequiredMixin, generic.ListView):
    model = Comment
    template_name = "user_comments.html"
    context_object_name = "comments"

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user)
