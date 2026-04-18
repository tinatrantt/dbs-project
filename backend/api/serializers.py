from .models import User, Team, Project, Task, Milestone, Note
from rest_framework import serializers
from django.utils import timezone


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'date_joined']
        extra_kwargs = {
            'passoword': {'write_only': True},
            'date_joined': {'read_only': True}
        }

        def create(self, validated_data):
            return User.objects.create_user(**validated_data)
        

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'created_at', 'members']
        extra_kwargs = {'created_at': {'read_only': True}}


class ProjectSerializer(serializers.ModelSerializer):
    team_name = serializers.CharField(source='team.name', read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 
            'name', 
            'description', 
            'created_at', 
            'project_owner', 
            'team', 
            'team_name',
            'status'
        ]
        extra_kwargs = {
            'created_at': {'read_only': True},
            'project_owner': {'read_only': True}
        }


class TodoSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    project_name = serializers.CharField(source='project.name', read_only=True)

    class Meta:
        fields = [
            'id', 
            'title', 
            'description', 
            'created_at', 
            'project', 
            'project_name',
            'status',
            'status_display'
        ]
        extra_kwargs = {
            'created_at': {'read_only': True}}
        

class TaskSerializer(TodoSerializer):
    class Meta:
        model = Task
        fields = TodoSerializer.Meta.fields + ['assigned_to']


class MilestoneSerializer(TodoSerializer):
    class Meta:
        model = Milestone
        fields = TodoSerializer.Meta.fields + ['deadline']

    def is_overdue(self, obj):
        return obj.deadline < timezone.now() and\
        obj.status != Milestone.StatusChoices.COMPLETE


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = [
            'id', 
            'title', 
            'content', 
            'created_at', 
            'last_modified',
            'note_owner'
        ]
        extra_kwargs = {
            'created_at': {'read_only': True},
            'last_modified': {'read_only': True}}