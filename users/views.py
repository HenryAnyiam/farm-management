from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import *
from users.permissions import *
from users.serializers import *
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
import logging
from uuid import UUID

logger = logging.getLogger(__name__)


class LoginUserView(GenericAPIView):

    serializer_class=LoginSerializer
    def post(self, request):
        serializer= self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StaffView(APIView):

    parser_classes = [JSONParser, FormParser]
    permission_classes = [IsAuthenticated, IsFarmManager]

    def get(self, request):
        """get all staffs"""
        users = request.user.organization.users
        user_data = UserRegisterSerializer(users, many=True)
        return Response(user_data.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        """add a new staff"""
        user_data = { **request.data, 'organization': request.user.organization.id }
        serialized = UserRegisterSerializer(data=user_data)
        if serialized.is_valid():
            serialized.save()
            request.user.last_activity = f"Created new staff: {request.data.get('username')}"
            request.user.save()
            return Response({'message': 'Staff created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, staff_id=None):
        """edit staff details"""
        if not staff_id:
            return Response({'detail': 'Staff Id not included'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            UUID(staff_id)
            staff = User.objects.get(id=staff_id, organization=request.user.organization)
            serializer = UserRegisterSerializer(staff, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'User updated Successfully'}, status=status.HTTP_200_OK)
        except ValueError:
            return Response({'detail': 'Invalid Staff ID'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'detail': 'User Not Found'}, status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request, staff_id=None):
        """delete staff details"""

        if not staff_id:
            return Response({'detail': 'Staff Id not included'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            UUID(staff_id)
            staff = User.objects.get(id=staff_id, organization=request.user.organization)
            staff.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError:
            return Response({'detail': 'Invalid Staff ID'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'detail': 'User Not Found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@parser_classes([JSONParser, FormParser])
def create_admin(request):
    user_data = { "username": "Henry", 'is_admin': True, "is_superuser": True, "is_staff": True, "password": "Password12" }
    logger.info(user_data)
    logger.info(request.data)
    serialized = UserRegisterSerializer(data=user_data)
    if serialized.is_valid():
        serialized.save()
        return Response({'message': 'Staff created successfully'}, status=status.HTTP_201_CREATED)
    return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@parser_classes([JSONParser, FormParser])
def auth_user(request):
    """log in a user"""

    username = request.data.get('username')
    password = request.data.get('password')
    if username and password:
        if not User.objects.filter(username=username).exists():
            return Response({"message": f"User with username - {username} does not exist"},
                    status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)
        if user:
            token = UserAuthentication.encrypt_payload(payload={"id": str(user.id)})
            return Response({
                'token': token,
                'id': user.id,
                'username':user.username,
                'role': user.role,
                'users_role': user.users_role,
            }, status=status.HTTP_200_OK)

        return Response({"message": f"Incorrect Password"},
                status=status.HTTP_400_BAD_REQUEST)

    return Response({"message": "Invalid Login Credentials"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@parser_classes([MultiPartParser, FormParser])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    serializer = UserRegisterSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)


# class CustomUserViewSet(viewsets.ModelViewSet):
#     """
#     ViewSet to handle operations related to custom user accounts.

#     Provides CRUD functionality for custom user accounts.

#     - list: Get a list of all custom users.
#     - retrieve: Retrieve details of a specific custom user.
#     - create: Create a new custom user account.
#     - update: Update an existing custom user account.
#     - destroy: Delete an existing custom user account.

#     Serializer class used for request/response data depends on the action:
#     - CustomUserCreateSerializer for create action.
#     - CustomUserSerializer for other actions.

#     """
#     queryset = CustomUser.objects.all()

   

# class AssignFarmOwnerView(APIView):
#     """
#     API View to assign the farm owner role to selected users.

#     Only authenticated users with farm owner permission can access this view.

#     The view accepts a POST request with a list of user IDs in the request body
#     and assigns the farm owner role to the corresponding users.

#     If successful, it returns a response with a message indicating the users
#     who have been assigned the farm owner role. If any user ID is not found or
#     is invalid, appropriate error messages are returned in the response.

#     """
#     #permission_classes = [IsFarmOwner]

#     def post(self, request):
#         user_ids = request.data.getlist('user_ids', [])
#         current_user_id = request.user.id

#         assigned_users = []
#         not_found_ids = []
#         invalid_ids = []

#         for user_id in user_ids:
#             try:
#                 user_id_int = int(user_id)
#                 user = CustomUser.objects.get(id=user_id_int)

#                 if user.id == current_user_id:
#                     raise ValidationError("Cannot assign roles to yourself.")

#                 user.assign_farm_owner()
#                 assigned_users.append(user.username)

#             except (ValueError, CustomUser.DoesNotExist):
#                 if user_id.isdigit():
#                     not_found_ids.append(user_id)
#                 else:
#                     invalid_ids.append(user_id)

#         response_data = {}

#         if assigned_users:
#             if len(assigned_users) > 1:
#                 response_data['message'] = f"Users {', '.join(assigned_users)} have been assigned as farm owners."
#             else:
#                 response_data['message'] = f"User {assigned_users[0]} has been assigned as a farm owner."

#         if not_found_ids:
#             if len(not_found_ids) > 1:
#                 response_data['error'] = f"Users with the following IDs were not found: {', '.join(not_found_ids)}."
#             else:
#                 response_data['error'] = f"User with ID {not_found_ids[0]} was not found."

#         if invalid_ids:
#             if len(invalid_ids) > 1:
#                 response_data['invalid'] = f"The following IDs are invalid: {', '.join(invalid_ids)}."
#             else:
#                 response_data['invalid'] = f"The ID {invalid_ids[0]} is invalid."

#         return Response(response_data, status=status.HTTP_200_OK)


# class AssignFarmManagerView(APIView):
#     """
#     API View to assign the farm manager role to selected users.

#     Only authenticated users with farm owner permission can access this view.

#     The view accepts a POST request with a list of user IDs in the request body
#     and assigns the farm manager role to the corresponding users.

#     If successful, it returns a response with a message indicating the users
#     who have been assigned the farm manager role. If any user ID is not found
#     or is invalid, appropriate error messages are returned in the response.

#     """
#     #permission_classes = [IsFarmOwner]

#     def post(self, request):
#         user_ids = request.data.getlist('user_ids', [])
#         current_user_id = request.user.id

#         assigned_users = []
#         not_found_ids = []
#         invalid_ids = []

#         for user_id in user_ids:
#             try:
#                 user_id_int = int(user_id)
#                 user = CustomUser.objects.get(id=user_id_int)

#                 if user.id == current_user_id:
#                     raise ValidationError("Cannot assign roles to yourself.")

#                 user.assign_farm_manager()
#                 assigned_users.append(user.username)

#             except (ValueError, CustomUser.DoesNotExist):
#                 if user_id.isdigit():
#                     not_found_ids.append(user_id)
#                 else:
#                     invalid_ids.append(user_id)

#         response_data = {}

#         if assigned_users:
#             if len(assigned_users) > 1:
#                 response_data['message'] = f"Users {', '.join(assigned_users)} have been assigned as farm managers."
#             else:
#                 response_data['message'] = f"User {assigned_users[0]} has been assigned as a farm manager."

#         if not_found_ids:
#             if len(not_found_ids) > 1:
#                 response_data['error'] = f"Users with the following IDs were not found: {', '.join(not_found_ids)}."
#             else:
#                 response_data['error'] = f"User with ID '{not_found_ids[0]}' was not found."

#         if invalid_ids:
#             if len(invalid_ids) > 1:
#                 response_data['invalid'] = f"The following IDs are invalid: {', '.join(invalid_ids)}."
#             else:
#                 response_data['invalid'] = f"The ID '{invalid_ids[0]}' is invalid."

#         return Response(response_data, status=status.HTTP_200_OK)


# class AssignAssistantFarmManagerView(APIView):
#     """
#     API View to assign the assistant farm manager role to selected users.

#     Only authenticated users with farm owner permission can access this view.

#     The view accepts a POST request with a list of user IDs in the request body
#     and assigns the assistant farm manager role to the corresponding users.

#     If successful, it returns a response with a message indicating the users
#     who have been assigned the assistant farm manager role. If any user ID is not found
#     or is invalid, appropriate error messages are returned in the response.

#     """
#     #permission_classes = [IsFarmOwner]

#     def post(self, request):
#         user_ids = request.data.getlist('user_ids', [])
#         current_user_id = request.user.id

#         assigned_users = []
#         not_found_ids = []
#         invalid_ids = []

#         for user_id in user_ids:
#             try:
#                 user_id_int = int(user_id)
#                 user = CustomUser.objects.get(id=user_id_int)

#                 if user.id == current_user_id:
#                     raise ValidationError("Cannot assign roles to yourself.")

#                 user.assign_assistant_farm_manager()
#                 assigned_users.append(user.username)

#             except (ValueError, CustomUser.DoesNotExist):
#                 if user_id.isdigit():
#                     not_found_ids.append(user_id)
#                 else:
#                     invalid_ids.append(user_id)

#         response_data = {}

#         if assigned_users:
#             if len(assigned_users) > 1:
#                 response_data[
#                     'message'] = f"Users {', '.join(assigned_users)} have been assigned as assistant farm managers."
#             else:
#                 response_data['message'] = f"User {assigned_users[0]} has been assigned as an assistant farm manager."

#         if not_found_ids:
#             if len(not_found_ids) > 1:
#                 response_data['error'] = f"Users with the following IDs were not found: {', '.join(not_found_ids)}."
#             else:
#                 response_data['error'] = f"User with ID {not_found_ids[0]} was not found."

#         if invalid_ids:
#             if len(invalid_ids) > 1:
#                 response_data['invalid'] = f"The following IDs are invalid: {', '.join(invalid_ids)}."
#             else:
#                 response_data['invalid'] = f"The ID {invalid_ids[0]} is invalid."

#         return Response(response_data, status=status.HTTP_200_OK)


# class AssignTeamLeaderView(APIView):
#     """
#     API View to assign the team leader role to selected users.

#     Only authenticated users with assistant farm manager permission can access this view.

#     The view accepts a POST request with a list of user IDs in the request body
#     and assigns the team leader role to the corresponding users.

#     If successful, it returns a response with a message indicating the users
#     who have been assigned the team leader role. If any user ID is not found
#     or is invalid, appropriate error messages are returned in the response.

#     """
#     #permission_classes = [IsAssistantFarmManager]

#     def post(self, request):
#         user_ids = request.data.getlist('user_ids', [])
#         current_user_id = request.user.id

#         assigned_users = []
#         not_found_ids = []
#         invalid_ids = []

#         for user_id in user_ids:
#             try:
#                 user_id_int = int(user_id)
#                 user = CustomUser.objects.get(id=user_id_int)

#                 if user.id == current_user_id:
#                     raise ValidationError("Cannot assign roles to yourself.")

#                 user.assign_team_leader()
#                 assigned_users.append(user.username)

#             except (ValueError, CustomUser.DoesNotExist):
#                 if user_id.isdigit():
#                     not_found_ids.append(user_id)
#                 else:
#                     invalid_ids.append(user_id)

#         response_data = {}

#         if assigned_users:
#             if len(assigned_users) > 1:
#                 response_data['message'] = f"Users {', '.join(assigned_users)} have been assigned as team leaders."
#             else:
#                 response_data['message'] = f"User {assigned_users[0]} has been assigned as a team leader."

#         if not_found_ids:
#             if len(not_found_ids) > 1:
#                 response_data['error'] = f"Users with the following IDs were not found: {', '.join(not_found_ids)}."
#             else:
#                 response_data['error'] = f"User with ID '{not_found_ids[0]}' was not found."

#         if invalid_ids:
#             if len(invalid_ids) > 1:
#                 response_data['invalid'] = f"The following IDs are invalid: {', '.join(invalid_ids)}."
#             else:
#                 response_data['invalid'] = f"The ID '{invalid_ids[0]}' is invalid."

#         return Response(response_data, status=status.HTTP_200_OK)


# class AssignFarmWorkerView(APIView):
#     """
#     API View to assign the farm worker role to selected users.

#     Only authenticated users with farm manager permission can access this view.

#     The view accepts a POST request with a list of user IDs in the request body
#     and assigns the farm worker role to the corresponding users.

#     If successful, it returns a response with a message indicating the users
#     who have been assigned the farm worker role. If any user ID is not found
#     or is invalid, appropriate error messages are returned in the response.

#     """
#     #permission_classes = [IsFarmManager]

#     def post(self, request):
#         user_ids = request.data.getlist('user_ids', [])
#         current_user_id = request.user.id

#         assigned_users = []
#         not_found_ids = []
#         invalid_ids = []

#         for user_id in user_ids:
#             try:
#                 user_id_int = int(user_id)
#                 user = CustomUser.objects.get(id=user_id_int)

#                 if user.id == current_user_id:
#                     raise ValidationError("Cannot assign roles to yourself.")

#                 user.assign_farm_worker()
#                 assigned_users.append(user.username)

#             except (ValueError, CustomUser.DoesNotExist):
#                 if user_id.isdigit():
#                     not_found_ids.append(user_id)
#                 else:
#                     invalid_ids.append(user_id)

#         response_data = {}

#         if assigned_users:
#             if len(assigned_users) > 1:
#                 response_data['message'] = f"Users {', '.join(assigned_users)} have been assigned as farm workers."
#             else:
#                 response_data['message'] = f"User {assigned_users[0]} has been assigned as a farm worker."

#         if not_found_ids:
#             if len(not_found_ids) > 1:
#                 response_data['error'] = f"Users with the following IDs were not found: {', '.join(not_found_ids)}."
#             else:
#                 response_data['error'] = f"User with ID {not_found_ids[0]} was not found."

#         if invalid_ids:
#             if len(invalid_ids) > 1:
#                 response_data['invalid'] = f"The following IDs are invalid: {', '.join(invalid_ids)}."
#             else:
#                 response_data['invalid'] = f"The ID {invalid_ids[0]} is invalid."

#         return Response(response_data, status=status.HTTP_200_OK)


# class DismissFarmManagerView(APIView):
#     """
#     API View to dismiss the farm manager role from selected users.

#     Only authenticated users with farm owner permission can access this view.

#     The view accepts a POST request with a list of user IDs in the request body
#     and dismisses the farm manager role from the corresponding users.

#     If successful, it returns a response with a message indicating the users
#     who have been dismissed from the farm manager role. If any user ID is not found
#     or is invalid, appropriate error messages are returned in the response.

#     """
#     permission_classes = [IsFarmOwner]

#     def post(self, request):
#         user_ids = request.data.getlist('user_ids', [])
#         current_user_id = request.user.id

#         dismissed_users = []
#         not_found_ids = []
#         invalid_ids = []

#         for user_id in user_ids:
#             try:
#                 user_id_int = int(user_id)
#                 user = CustomUser.objects.get(id=user_id_int)

#                 if user.id == current_user_id:
#                     raise ValidationError("Cannot dismiss yourself.")

#                 user.dismiss_farm_manager()
#                 dismissed_users.append(user.username)

#             except (ValueError, CustomUser.DoesNotExist):
#                 if user_id.isdigit():
#                     not_found_ids.append(user_id)
#                 else:
#                     invalid_ids.append(user_id)

#         response_data = {}

#         if dismissed_users:
#             if len(dismissed_users) > 1:
#                 response_data['message'] = f"Users {', '.join(dismissed_users)} have been dismissed as farm managers."
#             else:
#                 response_data['message'] = f"User {dismissed_users[0]} has been dismissed as a farm manager."

#         if not_found_ids:
#             if len(not_found_ids) > 1:
#                 response_data['error'] = f"Users with the following IDs were not found: {', '.join(not_found_ids)}."
#             else:
#                 response_data['error'] = f"User with ID '{not_found_ids[0]}' was not found."

#         if invalid_ids:
#             if len(invalid_ids) > 1:
#                 response_data['invalid'] = f"The following IDs are invalid: {', '.join(invalid_ids)}."
#             else:
#                 response_data['invalid'] = f"The ID '{invalid_ids[0]}' is invalid."

#         return Response(response_data, status=status.HTTP_200_OK)


# class DismissAssistantFarmManagerView(APIView):
#     """
#     API View to dismiss the assistant farm manager role from selected users.

#     Only authenticated users with farm owner permission can access this view.

#     The view accepts a POST request with a list of user IDs in the request body
#     and dismisses the assistant farm manager role from the corresponding users.

#     If successful, it returns a response with a message indicating the users
#     who have been dismissed from the assistant farm manager role. If any user ID is not found
#     or is invalid, appropriate error messages are returned in the response.

#     """
#     #permission_classes = [IsFarmOwner]

#     def post(self, request):
#         user_ids = request.data.getlist('user_ids', [])
#         current_user_id = request.user.id

#         dismissed_users = []
#         not_found_ids = []
#         invalid_ids = []

#         for user_id in user_ids:
#             try:
#                 user_id_int = int(user_id)
#                 user = CustomUser.objects.get(id=user_id_int)

#                 if user.id == current_user_id:
#                     raise ValidationError("Cannot dismiss yourself.")

#                 user.dismiss_assistant_farm_manager()
#                 dismissed_users.append(user.username)

#             except (ValueError, CustomUser.DoesNotExist):
#                 if user_id.isdigit():
#                     not_found_ids.append(user_id)
#                 else:
#                     invalid_ids.append(user_id)

#         response_data = {}

#         if dismissed_users:
#             if len(dismissed_users) > 1:
#                 response_data[
#                     'message'] = f"Users {', '.join(dismissed_users)} have been dismissed as assistant farm managers."
#             else:
#                 response_data['message'] = f"User {dismissed_users[0]} has been dismissed as an assistant farm manager."

#         if not_found_ids:
#             if len(not_found_ids) > 1:
#                 response_data['error'] = f"Users with the following IDs were not found: {', '.join(not_found_ids)}."
#             else:
#                 response_data['error'] = f"User with ID {not_found_ids[0]} was not found."

#         if invalid_ids:
#             if len(invalid_ids) > 1:
#                 response_data['invalid'] = f"The following IDs are invalid: {', '.join(invalid_ids)}."
#             else:
#                 response_data['invalid'] = f"The ID {invalid_ids[0]} is invalid."

#         return Response(response_data, status=status.HTTP_200_OK)


# class DismissTeamLeaderView(APIView):
#     """
#     API View to dismiss the team leader role from selected users.

#     Only authenticated users with assistant farm manager permission can access this view.

#     The view accepts a POST request with a list of user IDs in the request body
#     and dismisses the team leader role from the corresponding users.

#     If successful, it returns a response with a message indicating the users
#     who have been dismissed from the team leader role. If any user ID is not found
#     or is invalid, appropriate error messages are returned in the response.

#     """
#     #permission_classes = [IsAssistantFarmManager]

#     def post(self, request):
#         user_ids = request.data.getlist('user_ids', [])
#         current_user_id = request.user.id

#         dismissed_users = []
#         not_found_ids = []
#         invalid_ids = []

#         for user_id in user_ids:
#             try:
#                 try:
#                     user_id_int = int(user_id)
#                 except ValueError:
#                     invalid_ids.append(user_id)
#                     continue

#                 user = CustomUser.objects.get(id=user_id_int)

#                 if user.id == current_user_id:
#                     raise ValidationError("Cannot dismiss yourself.")

#                 user.dismiss_team_leader()
#                 dismissed_users.append(user.username)

#             except (ValueError, CustomUser.DoesNotExist):
#                 if user_id.isdigit():
#                     not_found_ids.append(user_id)
#                 else:
#                     invalid_ids.append(user_id)

#         response_data = {}

#         if dismissed_users:
#             if len(dismissed_users) > 1:
#                 response_data['message'] = f"Users {', '.join(dismissed_users)} have been dismissed as team leaders."
#             else:
#                 response_data['message'] = f"User {dismissed_users[0]} has been dismissed as a team leader."

#         if not_found_ids:
#             if len(not_found_ids) > 1:
#                 response_data['error'] = f"Users with the following IDs were not found: {', '.join(not_found_ids)}."
#             else:
#                 response_data['error'] = f"User with ID '{not_found_ids[0]}' was not found."

#         if invalid_ids:
#             if len(invalid_ids) > 1:
#                 response_data['invalid'] = f"The following IDs are invalid: {', '.join(invalid_ids)}."
#             else:
#                 response_data['invalid'] = f"The ID '{invalid_ids[0]}' is invalid."

#         return Response(response_data, status=status.HTTP_200_OK)


# class DismissFarmWorkerView(APIView):
#     """
#     API View to dismiss the farm worker role from selected users.

#     Only authenticated users with farm manager permission can access this view.

#     The view accepts a POST request with a list of user IDs in the request body
#     and dismisses the farm worker role from the corresponding users.

#     If successful, it returns a response with a message indicating the users
#     who have been dismissed from the farm worker role. If any user ID is not found
#     or is invalid, appropriate error messages are returned in the response.

#     """
#     #permission_classes = [IsFarmManager]

#     def post(self, request):
#         user_ids = request.data.getlist('user_ids', [])
#         current_user_id = request.user.id

#         dismissed_users = []
#         not_found_ids = []
#         invalid_ids = []

#         for user_id in user_ids:
#             try:
#                 user_id_int = int(user_id)
#                 user = CustomUser.objects.get(id=user_id_int)

#                 if user.id == current_user_id:
#                     raise ValidationError("Cannot dismiss yourself.")

#                 user.dismiss_farm_worker()
#                 dismissed_users.append(user.username)

#             except (ValueError, CustomUser.DoesNotExist):
#                 if user_id.isdigit():
#                     not_found_ids.append(user_id)
#                 else:
#                     invalid_ids.append(user_id)

#         response_data = {}

#         if dismissed_users:
#             if len(dismissed_users) > 1:
#                 response_data['message'] = f"Users {', '.join(dismissed_users)} have been dismissed as farm workers."
#             else:
#                 response_data['message'] = f"User {dismissed_users[0]} has been dismissed as a farm worker."

#         if not_found_ids:
#             if len(not_found_ids) > 1:
#                 response_data['error'] = f"Users with the following IDs were not found: {', '.join(not_found_ids)}."
#             else:
#                 response_data['error'] = f"User with ID {not_found_ids[0]} was not found."

#         if invalid_ids:
#             if len(invalid_ids) > 1:
#                 response_data['invalid'] = f"The following IDs are invalid: {', '.join(invalid_ids)}."
#             else:
#                 response_data['invalid'] = f"The ID {invalid_ids[0]} is invalid."

#         return Response(response_data, status=status.HTTP_200_OK)


# class GenerateUsernameSlugAPIView(APIView):
#     """
#     API View to generate a unique username slug based on first name and last name.

#     This view accepts a POST request with the `first_name` and `last_name` fields in the request body.
#     It generates a username slug by concatenating the sanitized `first_name` and `last_name` strings
#     and returns it as a response.

#     The generated username slug is unique and can be used to create a new user with a username based
#     on their first name and last name. If the `first_name` or `last_name` is not provided in the request
#     body, it returns an error response with a message indicating that both fields are required.

#     Example usage:
#     POST: /users/generate-username/
#     Request Body:
#     {
#         "first_name": "Peter",
#         "last_name": "Evance"
#     }

#     Response:
#     {
#         "username": "peter-evance"
#     }
#     """

#     def post(self, request):
#         first_name = request.data.get('first_name')
#         last_name = request.data.get('last_name')

#         if not first_name:
#             return Response({'error': 'First name is required.'}, status=status.HTTP_400_BAD_REQUEST)

#         if not last_name:
#             return Response({'error': 'Last name is required.'}, status=status.HTTP_400_BAD_REQUEST)

#         username = CustomUser.generate_username(first_name, last_name)

#         return Response({'username': username})







# # Create your views here.
# logger = logging.getLogger('accounts')

# class RegisterView(GenericAPIView):
#     serializer_class = UserRegisterSerializer

#     def post(self, request):
#         user = request.data
#         serializer = self.serializer_class(data=user)
#         if serializer.is_valid(raise_exception=True):
#             new_user = serializer.save()
#             user_registration = UserRegistration.objects.create(user=new_user)
#             logger.info(f"User registration created: {user_registration}")
#             user_data = serializer.data
#             send_generated_otp_to_email(user_data['email'], request)
#             # Optionally send OTP to user's email
#             # send_generated_otp_to_email(user_data['email'], request)
#             return Response({
#                 'data': user_data,
#                 'message': 'Thanks for signing up! A passcode has been sent to verify your email.'
#             }, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





# class VerifyUserEmail(GenericAPIView):
#     def post(self, request):
#         try:
#             passcode = request.data.get('otp')
#             user_pass_obj=OneTimePassword.objects.get(otp=passcode)
#             user=user_pass_obj.user
#             if not user.is_verified:
#                 user.is_verified=True
#                 user.save()
#                 return Response({
#                     'message':'account email verified successfully'
#                 }, status=status.HTTP_200_OK)
#             return Response({'message':'passcode is invalid user is already verified'}, status=status.HTTP_204_NO_CONTENT)
#         except OneTimePassword.DoesNotExist as identifier:
#             return Response({'message':'passcode not provided'}, status=status.HTTP_400_BAD_REQUEST)

# '''
# class PasswordResetRequestView(GenericAPIView):
#     serializer_class=PasswordResetRequestSerializer

#     def post(self, request):
#         serializer=self.serializer_class(data=request.data, context={'request':request})
#         serializer.is_valid(raise_exception=True)
#         return Response({'message':'we have sent you a link to reset your password'}, status=status.HTTP_200_OK)
#         # return Response({'message':'user with that email does not exist'}, status=status.HTTP_400_BAD_REQUEST)
# '''  

# class PasswordResetRequestView(APIView):
#     def post(self, request):
#         serializer = PasswordResetRequestSerializer(data=request.data, context={'request': request})
#         if serializer.is_valid():
#             return Response({"detail": "Password reset link has been sent to your email"}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# class PasswordResetRequestView(APIView):
#     def post(self, request):
#         serializer = PasswordResetRequestSerializer(data=request.data, context={'request': request})
#         if serializer.is_valid():
#             return Response({"detail": "Password reset link has been sent to your email"}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class PasswordResetConfirm(GenericAPIView):

#     def get(self, request, uidb64, token):
#         try:
#             user_id=smart_str(urlsafe_base64_decode(uidb64))
#             user=CustomUser.objects.get(id=user_id)

#             if not PasswordResetTokenGenerator().check_token(user, token):
#                 return Response({'message':'token is invalid or has expired'}, status=status.HTTP_401_UNAUTHORIZED)
#             return Response({'success':True, 'message':'credentials is valid', 'uidb64':uidb64, 'token':token}, status=status.HTTP_200_OK)

#         except DjangoUnicodeDecodeError as identifier:
#             return Response({'message':'token is invalid or has expired'}, status=status.HTTP_401_UNAUTHORIZED)

# class SetNewPasswordView(GenericAPIView):
#     serializer_class=SetNewPasswordSerializer

#     def patch(self, request):
#         serializer=self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         return Response({'success':True, 'message':"password reset is succesful"}, status=status.HTTP_200_OK)


# class TestingAuthenticatedReq(GenericAPIView):
#     permission_classes=[IsAuthenticated]

#     def get(self, request):

#         data={
#             'msg':'its works'
#         }
#         return Response(data, status=status.HTTP_200_OK)

# class LogoutApiView(GenericAPIView):
#     serializer_class=LogoutUserSerializer
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         serializer=self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(status=status.HTTP_204_NO_CONTENT)
 

    

# from rest_framework import viewsets
# from .models import CustomUser


# class CustomUserViewSet(viewsets.ModelViewSet):
#     queryset = CustomUser.objects.all()
#     serializer_class = UserSerializer
