from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from blog.forms import DocumentForm
from django.http import HttpResponse, HttpResponseRedirect
from blog.views.identify_face import searchImage

def findMissing(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            result = searchImage(request.FILES['document'].name, form.cleaned_data['name'])
            request.session['result'] = result
            return HttpResponseRedirect(reverse('blog:myresults'))
    else:
        form = DocumentForm()
    return render(request, 'blog/findMissing.html', {
        'form': form
    })

def results(request):
	return render(request,"blog/results.html",{"result":request.session['result']})
