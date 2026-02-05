from http.client import HTTPResponse

from django.core.serializers import serialize
from django.http import JsonResponse
from rest_framework import viewsets
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.conf import settings
from django.contrib.auth.models import User

from django.db import connection

from .models import Run, AthleteInfo
from .serializers import (RunSerializer,
                          UserSerializer,
                          AthleteInfoAPIViewSerializer
                          )

class RunPagination(PageNumberPagination):
    # page_size = 5
    page_size_query_param = 'size'
    max_page_size = 20

class RunnerPagination(PageNumberPagination):
    # page_size = 5
    page_size_query_param = 'size'
    max_page_size = 20


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
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = [
        'athlete',
        'status'
    ]
    ordering_fields = [
        'created_at',
    ]
    pagination_class = RunPagination


class ReadOnlyRunnerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.filter(is_superuser=False)
    serializer_class = UserSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = [
        'first_name',
        'last_name'
    ]
    ordering_fields = [
        'date_joined',
    ]
    pagination_class = RunnerPagination

    def get_queryset(self):
        qs = self.queryset
        type = self.request.query_params.get('type', None)
        if type == 'coach':
            qs = qs.filter(is_staff=True)
        elif type == 'athlete':
            qs = qs.filter(is_staff=False)
        return qs

class RunStartAPIView(APIView):
    def post(self, request, id):
        run = get_object_or_404(Run, pk=id)

        if run.status == 'in_progress' or run.status == 'finished':
            return JsonResponse({
                'content': 'Забег не может быть начат!',
            },
            status=400
            )

        run.status = 'in_progress'
        run.save()
        return JsonResponse({
            'id': run.id,
            'status': run.status,
        })

class RunStopAPIView(APIView):
    def post(self, request, id):
        run = get_object_or_404(Run, pk=id)

        if run.status == 'init' or run.status == 'finished':
            return JsonResponse({
                'content': 'Забег не может быть закончен!',
            },
            status=400
            )

        run.status = 'finished'
        run.save()
        return JsonResponse({
            'id': run.id,
            'status': run.status,
        })

class AthleteInfoAPIView(APIView):
    def get(self, request, id):
        user = User.objects.filter(pk=id).first()
        print('TEST ', user)
        if not user:
            return JsonResponse({
                'content': 'Пользователя нет!',
            },
                status=404
            )
        athlete_info, created = AthleteInfo.objects.get_or_create(pk=id)
        # print(created, user.id)
        if created:
            athlete_info.user = user
            athlete_info.save()
        return JsonResponse({
            'user_id': athlete_info.user.id,
            'weight': athlete_info.weight,
            'goals': athlete_info.goals,
        })

    def put(self, request, id):
        serializer = AthleteInfoAPIViewSerializer(data=request.data)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)

        weight = request.data.get('weight', None)
        goals = request.data.get('goals', None)

        print(weight, goals)

        defaults = {}

        if weight:
            if int(weight) <= 0 or int(weight) >= 900:
                return JsonResponse({
                    'message': 'Wrong weight!'
                }, status=400)
            defaults['weight'] = int(weight)
        if goals:
            defaults['goals'] = goals

        athlete_info, created = AthleteInfo.objects.update_or_create(
            pk=id,
            defaults=defaults,
        )
        return JsonResponse({
            'user_id': athlete_info.user.id,
            'weight': athlete_info.weight,
            'goals': athlete_info.goals,
        },
        status=201)

