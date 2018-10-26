from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render
from blog.models.help_request import Request
from django.template.defaulttags import register
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView, UpdateView, DeleteView
CHOICES = [(1,"Pending"), (2, "Assigned"), (3, "Resolved")]
choices = {1: "Pending", 2: "Assigned", 3: "Resolved"}
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
    
NUM_OF_POSTS = 10


def help_requests(request):
    requests_list = Request.objects.all().order_by('-pub_date')

    paginator = Paginator(requests_list, NUM_OF_POSTS)  # Show NUM_OF_PAGES posts per page
    page = request.GET.get('page')

    requests = paginator.get_page(page)
    return render(request, 'blog/helprequests.html', {'rqsts': requests, 'choices': choices })

def assign(request):
    pass

class RequestView(generic.DetailView):
    model = Request
    template_name = 'blog/request.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the username
        request = Request.objects.get(id=self.kwargs['pk'])
        context['req'] = request
        context['choices'] = choices
        return context