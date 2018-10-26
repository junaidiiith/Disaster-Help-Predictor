from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView, UpdateView, DeleteView

from blog.models.comment import Comment
from blog.models.post import Post
from blog.models.clasDict import classes

class PostView(generic.DetailView):
    model = Post
    template_name = 'blog/post.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the username
        comments = Comment.objects.filter(post=self.kwargs['pk'])
        votes = dict()
        for comment in comments:
            try:
                votes[classes[comment.vote]] += 1
            except:
                votes[classes[comment.vote]]  = 1 

        context['votes'] = votes
        return context


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['body']
    template_name = 'blog/create_post.html'
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.location = "None"
        form.instance.clss = 1
        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'body']
    template_name = 'blog/create_post.html'
    login_url = reverse_lazy('login')

    def test_func(self):
        return Post.objects.get(id=self.kwargs['pk']).user == self.request.user


class PostDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog:home')
    login_url = reverse_lazy('login')

    def test_func(self):
        return Post.objects.get(id=self.kwargs['pk']).user == self.request.user