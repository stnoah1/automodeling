from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView

from design.common import get_client_ip
from design.models import Project


def home(request):
    ip = get_client_ip(request)
    project = Project.objects.create(ip=ip)
    return redirect(reverse('design:home', kwargs={'code': project.code}))


class DesignView(TemplateView):
    template_name = 'design/design.html'
