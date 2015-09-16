from django.conf.urls import include, url

import forum.views

urlpatterns = [
    url(r'^$', forum.views.posts, name='posts'),
    url(r'^accounts/signup/', forum.views.signup, name='signup'),
    url(r'^accounts/', include('django.contrib.auth.urls')),
]
