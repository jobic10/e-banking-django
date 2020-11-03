from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .forms import FeedbackForm
# Create your views here.


def homepage(request):
    context = {}
    return render(request, 'home/index.html', context)


def contact(request):
    form = FeedbackForm(request.POST or None)
    context = {'form': form}
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Feedback sent! We will get back to you soon :-) ')
            return redirect(reverse('contact'))
        else:
            messages.error(request, "Form errors")
    return render(request, 'home/contact.html', context)
