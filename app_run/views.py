from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.conf import settings
# Create your views here.

@api_view(['GET'])
def task_one(request):
    return Response({
        "COMPANY_NAME": settings.COMPANY_NAME,
        "SLOGAN": settings.SLOGAN,
        "CONTACTS": settings.CONTACTS,
    })