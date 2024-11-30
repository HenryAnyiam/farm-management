from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission
from users.choices import RoleChoices




class IsFarmOwner(BasePermission):
    """
    Custom permission class that allows only farm owners to perform an action.

    Raises:
    - `PermissionDenied`: If the user is not a farm owner.

    Usage:
        Add the permission class to the view or viewset that requires farm owners access:
        permission_classes = [IsFarmOwner]
    """

    message = {"message": "Only farm owners have permission to perform this action."}

    def has_permission(self, request, view):
        # Check if the current user is a farm owner
        if request.user.is_authenticated and request.user.role >= RoleChoices.OWNER:
            return True
        raise PermissionDenied(self.message)


class IsFarmManager(BasePermission):
    """
    Custom permission class that allows only farm owners and managers to perform an action.

    Raises:
    - `PermissionDenied`: If the user is not a farm owner or a farm manager.

    Usage:
        Add the permission class to the view or viewset that requires farm owners and managers access:
        permission_classes = [IsFarmManager]
    """
    message = {"message": "Only farm owners and managers have permission to perform this action."}

    def has_permission(self, request, view):
        # Check if the current user is a farm manager
        if request.user.is_authenticated and request.user.role >= RoleChoices.MANAGER:
            return True
        raise PermissionDenied(self.message)


class IsAssistantFarmManager(BasePermission):
    """
    Custom permission class that allows only farm owners, managers, and assistants to perform an action.

    Raises:
    - `PermissionDenied`: If the user is not a farm owner, a farm manager, or an assistant farm manager.

    Usage:
        Add the permission class to the view or viewset that requires farm owners, managers, and assistants access:
        permission_classes = [IsAssistantFarmManager]
    """
    message = {"message": "Only farm owners, managers, and assistants have permission to perform this action."}

    def has_permission(self, request, view):
        # Check if the current user is an assistant farm manager
        if request.user.is_authenticated and request.user.role >= RoleChoices.ASST_MANAGER:
            return True
        raise PermissionDenied(self.message)


class IsFarmWorker(BasePermission):
    """
    Custom permission class that allows only farm staff and workers to perform an action.

    Raises:
    - `PermissionDenied`: If the user is not a farm owner, a farm worker, a farm manager, or an assistant farm manager.

    Usage:
        Add the permission class to the view or viewset that requires farm workers access:
        permission_classes = [IsFarmWorker]
    """
    message = {"message": "Only farm staff and workers have permission to perform this action."}

    def has_permission(self, request, view):
        # Check if the current user is a farm worker
        if request.user.is_authenticated and request.user.role >= RoleChoices.WORKER:
            return True
        raise PermissionDenied(self.message)


class IsTeamLeader(BasePermission):
    """
    Custom permission class that allows only team leaders to perform an action.

    Raises:
    - `PermissionDenied`: If the user is not a team leader, an assistant farm manager, a farm manager, or a farm owner.

    Usage:
        Add the permission class to the view or viewset that requires team leaders access:
        permission_classes = [IsTeamLeader]
    """
    message = {"message": "Only team leaders have permission to perform this action."}

    def has_permission(self, request, view):
        # Check if the current user is a team leader
        if request.user.is_authenticated and request.user.role >= RoleChoices.TEAM_LEADER:
            return True
        raise PermissionDenied(self.message)
