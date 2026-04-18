from rest_framework.permissions import BasePermission


class IsProjectTeamOwner(BasePermission):
    """
    Only the project/team owner can alter or delete the project
    and add/remove members to the team.
    """
    def has_object_permission(self, request, view, obj):
        return obj.project_owner == request.user


class IsTeamMember(BasePermission):
    """
    Only a team member can access the project (inluding a project's
    associated tasks and milestones).
    """
    def has_object_permission(self, request, view, obj):
        return obj.project.team.members.filter(id=request.user.id).exists()