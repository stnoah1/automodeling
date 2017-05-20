from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.DesignView.as_view(), name='home'),
]
