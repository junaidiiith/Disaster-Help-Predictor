from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView

from blog.models.comment import Comment
from blog.models.post import Post

CHOICES = [
    (1, "Caution/Advice"),
    (2, "Damage"),
    (3, "Disease"),
    (4, "Information"),
    (5, "Need Help"),
    (6, "Other"),
    (7, "People Affected"),
    (8, "Support")]

class CommentCreate(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['vote']
    template_name = 'blog/create_comment.html'
    login_url = reverse_lazy('login')
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the username
        context['post'] = Post.objects.get(id=self.kwargs['pk'])
        context['choices'] = CHOICES
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post = Post.objects.get(id=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post', kwargs={'pk': self.kwargs['pk']})