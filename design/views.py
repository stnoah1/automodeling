from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView
from rest_framework.decorators import api_view
from rest_framework.response import Response

from design.common import get_client_ip
from design.models import Project


def home(request):
    ip = get_client_ip(request)
    project = Project.objects.create(ip=ip)
    return redirect(reverse('design:home', kwargs={'code': project.code}))


@api_view(['POST'])
def convert_view(request, code):
    # TODO : CONVERT
    # - Function Execute Sample
    #    stl_data = request.data
    #    get_model_info(stl_data)
    # - Return Sample
    context = {
        'class_info': [
            {'class': "chair", 'confidence_rate': 0.93},
            {'class': "desk", 'confidence_rate': 0.07}
        ],
        'related_models': ['chair_0001', 'chair_0002']
    }
    return Response(context)


class DesignView(TemplateView):
    template_name = 'design/design.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
