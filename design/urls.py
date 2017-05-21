from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='bridge'),
    url(r'^(?P<code>[^/]+)/$', views.DesignView.as_view(), name='home'),
]
