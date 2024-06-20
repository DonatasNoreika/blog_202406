from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse
from django.views import generic
from .models import Post, Comment
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import FormMixin
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth import password_validation
from django.contrib.auth.forms import User
from .forms import (CommentForm,
                    UserUpdateForm,
                    ProfileUpdateForm)


# Create your views here.


def search(request):
    query = request.GET.get('query')
    post_search_results = Post.objects.filter(
        Q(title__icontains=query) | Q(content__icontains=query) | Q(author__username__icontains=query))
    return render(request, 'search.html', context={"posts": post_search_results, "query": query})


@csrf_protect
def register(request):
    if request.method == "POST":
        # pasiimame reikšmes iš registracijos formos
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # tikriname, ar sutampa slaptažodžiai
        if password == password2:
            # tikriname, ar neužimtas username
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Vartotojo vardas {username} užimtas!')
                return redirect('register')
            else:
                # tikriname, ar nėra tokio pat email
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'Vartotojas su el. paštu {email} jau užregistruotas!')
                    return redirect('register')
                else:
                    try:
                        password_validation.validate_password(password)
                    except password_validation.ValidationError as e:
                        for error in e:
                            messages.error(request, error)
                        return redirect('register')

                    # jeigu viskas tvarkoje, sukuriame naują vartotoją
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f'Vartotojas {username} užregistruotas!')
                    return redirect('login')
        else:
            messages.error(request, 'Slaptažodžiai nesutampa!')
            return redirect('register')
    return render(request, 'registration/register.html')


@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        new_email = request.POST['email']
        if new_email == "":
            messages.error(request, f'El. paštas negali būti tuščias!')
            return redirect('profile')
        if request.user.email != new_email and User.objects.filter(email=new_email).exists():
            messages.error(request, f'Vartotojas su el. paštu {new_email} jau užregistruotas!')
            return redirect('profile')
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Profilis atnaujintas")
            return redirect('profile')

    u_form = UserUpdateForm(instance=request.user)
    p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, "profile.html", context=context)


class UserCommentListView(LoginRequiredMixin, generic.ListView):
    model = Comment
    template_name = "user_comments.html"
    context_object_name = "comments"

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user)


class PostListView(generic.ListView):
    model = Post
    context_object_name = "posts"
    template_name = "posts.html"
    paginate_by = 5


class PostDetailView(FormMixin, generic.DetailView):
    model = Post
    context_object_name = "post"
    template_name = "post.html"
    form_class = CommentForm

    # nurodome, kur atsidursime komentaro sėkmės atveju.
    def get_success_url(self):
        return reverse("post", kwargs={"pk": self.object.id})

    # standartinis post metodo perrašymas, naudojant FormMixin, galite kopijuoti tiesiai į savo projektą.
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    # štai čia nurodome, kad knyga bus būtent ta, po kuria komentuojame, o vartotojas bus tas, kuris yra prisijungęs.
    def form_valid(self, form):
        form.instance.post = self.object
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)


class UserPostListView(LoginRequiredMixin, generic.ListView):
    model = Post
    template_name = "user_posts.html"
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    template_name = "post_form.html"
    success_url = "/userposts/"
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Post
    template_name = "post_form.html"
    success_url = "/userposts/"
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        current_post = self.get_object()
        return current_post.author == self.request.user
