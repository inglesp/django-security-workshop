from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import PostForm
from .models import Post


@login_required
def posts(request):
    if request.method == 'POST':
        post = Post(owner=request.user)
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            messages.add_message(request, messages.INFO, 'Thanks for posting!')
            form.save()
            return HttpResponseRedirect(reverse('posts'))
    else:
        form = PostForm()

    posts = Post.objects.order_by('-created_at')

    username = request.GET.get('user')
    if username:
        posts = posts.filter(owner__username=username)

    context = {'form': form, 'posts': posts}
    return render(request, 'forum/posts.html', context)


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password2']
            form.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect(reverse('posts'))
    else:
        form = UserCreationForm()

    context = {'form': form}
    return render(request, 'registration/signup.html', context)
