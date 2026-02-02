from rest_framework import viewsets
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.filters import SearchFilter

from django.conf import settings
from django.contrib.auth.models import User

from django.db import connection

from .models import Run
from .serializers import (RunSerializer,
                          UserSerializer
                          )

# Create your views here.

@api_view(['GET'])
def task_one(request):
    return Response({
        "company_name": settings.COMPANY_NAME,
        "slogan": settings.SLOGAN,
        "contacts": settings.CONTACTS,
    })

class RunViewSet(viewsets.ModelViewSet):
    queryset = Run.objects.select_related('athlete').all()
    serializer_class = RunSerializer

class ReadOnlyRunnerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.filter(is_superuser=False)
    serializer_class = UserSerializer
    filter_backends = [SearchFilter]
    search_fields = [
        'first_name',
        'last_name'
    ]

    def get_queryset(self):
        qs = self.queryset
        type = self.request.query_params.get('type', None)
        if type == 'coach':
            qs = qs.filter(is_staff=True)
        elif type == 'athlete':
            qs = qs.filter(is_staff=False)
        return qs