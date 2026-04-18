from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from django.contrib.auth.models import User
from .models import Project, Team, Task, Milestone, Note
from .serializers import (
    UserSerializer,
    ProjectSerializer, 
    TeamSerializer, 
    TaskSerializer, 
    MilestoneSerializer,
    NoteSerializer
)

from rest_framework.exceptions import PermissionDenied
from .permissions import IsProjectTeamOwner, IsTeamMember


class RegisterView(APIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not username or not email or not password:
            return Response(
                {'error': 'Username, Email, and Password required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if User.objects.filter(username=username).exists():
            return Response(
                {'error': 'Username already taken.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            validate_password(password)
        except ValidationError as e:
            return Response(
                {'error': e.messages},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = User.objects.create_user(
            username=username, email=email, password=password)
        return Response({
            'user': {'id': user.id, 'username': user.username, 'email': user.email}},
            status=status.HTTP_201_CREATED)


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(team__members=self.request.user)
    
    def get_permissions(self):
        if self.action in ['destroy', 'update', 'partial_update']:
            return [IsAuthenticated(), IsProjectTeamOwner()]
        return [IsAuthenticated()]
    
    def perform_create(self, serializer):
        team = Team.objects.create(name='Unamed Team')
        team.members.add(self.request.user)
        serializer.save(project_owner=self.request.user, team=team)

    @action(detail=True, methods=['get'], url_path='dashboard')
    def dashboard(self, request, pk=None):
        project = self.get_object()
        return Response({
            'members': [
                {'id': member.id, 'username': member.username}
                for member in project.team.members.all()],

            'tasks': TaskSerializer(
                project.task_set.all(),many=True).data,

            'milestones': MilestoneSerializer(
                project.milestone_set.all(), many=True).data,
        })
    

class TeamViewSet(ModelViewSet):
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Team.objects.filter(
            members=self.request.user).prefetch_related('members')
    
    def get_permissions(self):
        if self.action in ['destroy', 'add_member', 'remove_member']:
            return [IsAuthenticated(), IsProjectTeamOwner()]
        return [IsAuthenticated()]
        
    @action(detail=True, methods=['post'], url_path='add-member')
    def add_member(self, request, pk=None):
        team = self.get_object()
        username = request.data.get('username')

        if username:
            user = get_object_or_404(User, username=username)
        else:
            return Response(
                {'error': 'Provide a username'},
                status=status.HTTP_400_BAD_REQUEST)
        
        if team.members.filter(id=user.id).exists():
            return Response(
                {'error': 'This user is already in the team.'},
                status=status.HTTP_400_BAD_REQUEST)
        
        team.members.add(user)
        return Response({'detail': f'{user.username} has been added to the team.'})
    

    @action(detail=True, methods=['delete'], url_path='remove-member')
    def remove_member(self, request, pk=None):
        team = self.get_object()
        user_id = request.data.get('user_id')
        user = get_object_or_404(User, id=user_id)
        if not user_id:
            return Response(
                {'error': 'User ID required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        team.members.remove(user)
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsTeamMember]
        
    def get_queryset(self):
        qs = Task.objects.filter(
            project__team__members=self.request.user)\
            .select_related('project', 'assigned_to')
        project_id = self.request.query_params.get('project')
        if project_id:
            qs = qs.filter(project_id=project_id)
        return qs
    
    def get_permissions(self):
        if self.action in ['destroy', 'partial_update', 'update']:
            return [IsAuthenticated(), IsTeamMember()]
        return [IsAuthenticated(), IsTeamMember()]
    
    def perform_update(self, serializer):
        task = self.get_object()
        data = serializer.validated_data

        if 'status' in data and task.assigned_to != self.request.user:
            raise PermissionDenied('Only the assigned user can update the status.')
        
        serializer.save()

        
class MilestoneViewSet(ModelViewSet):
    serializer_class = MilestoneSerializer
    permission_classes = [IsAuthenticated, IsTeamMember]

    def get_queryset(self):
        qs = Milestone.objects.filter(
            project__team__members=self.request.user)\
            .select_related('project')
        project_id = self.request.query_params.get('project')
        if project_id:
            qs = qs.filter(project_id=project_id)
        return qs
    
    def get_permissions(self):
        if self.action == 'destroy':
            return [IsAuthenticated(), IsProjectTeamOwner()]
        return [IsAuthenticated(), IsTeamMember()]


class NoteViewSet(ModelViewSet):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Note.objects.filter(note_owner=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(note_owner=self.request.user)