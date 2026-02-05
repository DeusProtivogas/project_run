from rest_framework import serializers
from .models import Run
from django.contrib.auth.models import User

# from django.conf import settings

class UserSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    runs_finished = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'date_joined', 'username', 'last_name', 'first_name', 'type', 'runs_finished']

    def get_type(self, obj):
        return 'coach' if obj.is_staff else 'athlete'

    def get_runs_finished(self, obj):
        return Run.objects.filter(status='finished', athlete=obj).count()

class UserRunnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'last_name', 'first_name']

class RunSerializer(serializers.ModelSerializer):

    athlete_data = UserRunnerSerializer(
        source='athlete',
        read_only=True,
    )

    class Meta:
        model = Run
        fields = '__all__'