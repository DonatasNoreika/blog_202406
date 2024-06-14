from django.shortcuts import render
from django.views import generic
from .models import Post
from django.db.models import Q


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
    post_search_results = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query) | Q(author__username__icontains=query))
    return render(request, 'search.html', context={"posts": post_search_results, "query": query})