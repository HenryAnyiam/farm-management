from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.filters import OrderingFilter
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError as DRFValidationError

from poultry.filters import *
from poultry.permissions import *
from poultry.serializers import *
import logging

logger = logging.getLogger(__name__)


class FlockSourceViewSet(viewsets.ModelViewSet):
    queryset = FlockSource.objects.all()
    serializer_class = FlockSourceSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = FlockSourceFilterSet
    ordering_fields = ["name"]

    def get_permissions(self):
        if self.action in ["create"]:
            # Only farm owner and farm manager should be allowed to create flock sources
            permission_classes = [CanAddFlockSource]
        elif self.action in ["destroy"]:
            # Only farm owner and farm manager should be allowed to delete flock sources
            permission_classes = [CanDeleteFlockSource]
        else:
            # For viewing flock sources, allow farm owner, farm manager, assistant farm manager, team leader,
            # and farm worker
            permission_classes = [CanViewFlockSource]
        return [permission() for permission in permission_classes]


    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed("PUT")

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            return Response([], status=status.HTTP_200_OK)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.request.user.last_activity = "Added new flock source"
            self.request.user.save()
            return Response({'detail': 'Data saved successfully'}, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'detail': e.message}, status=status.HTTP_400_BAD_REQUEST)
        except DRFValidationError as e:
            return Response({'detail': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f'Exception, {str(e)}')
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class FlockBreedViewSet(viewsets.ModelViewSet):
    queryset = FlockBreed.objects.all()
    serializer_class = FlockBreedSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = FlockBreedFilterSet
    ordering_fields = ["name"]

    def get_permissions(self):
        if self.action in ["create"]:
            # Only farm owner and farm manager should be allowed to create flock breeds

            permission_classes = [CanAddFlockBreed]
        elif self.action in ["destroy"]:
            # Only farm owner and farm manager should be allowed to delete flock breeds
            permission_classes = [CanDeleteFlockBreed]
        else:
            # For viewing flock breeds, allow farm owner, farm manager, assistant farm manager, team leader,
            # and farm worker
            permission_classes = [CanViewFlockBreeds]
        return [permission() for permission in permission_classes]

    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed("PUT")

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            return Response([], status=status.HTTP_200_OK)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            self.request.user.last_activity = "Added new flock breed"
            self.request.user.save()
            return Response({'detail': 'Data saved successfully'}, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'detail': e.message}, status=status.HTTP_400_BAD_REQUEST)
        except DRFValidationError as e:
            return Response({'detail': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f'Exception, {str(e)}')
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class HousingStructureViewSet(viewsets.ModelViewSet):
    queryset = HousingStructure.objects.all()
    serializer_class = HousingStructureSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = HousingStructureFilterSet
    ordering_fields = ["house_type", "category"]
    permission_classes = [CanActOnHousingStructure]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            return Response([], status=status.HTTP_200_OK)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            self.request.user.last_activity = "Added new housing structure"
            self.request.user.save()
            return Response({'detail': 'Data saved successfully'}, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'detail': e.message}, status=status.HTTP_400_BAD_REQUEST)
        except DRFValidationError as e:
            return Response({'detail': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f'Exception, {str(e)}')
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class FlockViewSet(viewsets.ModelViewSet):
    queryset = Flock.objects.all()
    serializer_class = FlockSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = FlockFilterSet
    ordering_fields = ["-date_established", "source"]

    def get_permissions(self):
        if self.action in ["create"]:
            permission_classes = [CanAddFlock]
        elif self.action in ["update", "partial_update"]:
            permission_classes = [CanUpdateFlock]
        elif self.action in ["destroy"]:
            permission_classes = [CanDeleteFlock]
        else:
            permission_classes = [CanViewFlock]
        return [permission() for permission in permission_classes]

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed("PUT")

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            return Response([], status=status.HTTP_200_OK)
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            self.request.user.last_activity = "Added new flock"
            self.request.user.save()
            return Response({'detail': 'Data saved successfully'}, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'detail': e.message}, status=status.HTTP_400_BAD_REQUEST)
        except DRFValidationError as e:
            return Response({'detail': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f'Exception, {str(e)}')
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)



class FlockHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FlockHistory.objects.all()
    serializer_class = FlockHistorySerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = FlockHistoryFilterSet
    ordering_fields = ["-date_changed", "flock", "rearing_method"]
    permission_classes = [CanActOnFlockHistory]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            return Response([], status=status.HTTP_200_OK)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            self.request.user.last_activity = "Added new flock history"
            self.request.user.save()
            return Response({'detail': 'Data saved successfully'}, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'detail': e.message}, status=status.HTTP_400_BAD_REQUEST)
        except DRFValidationError as e:
            return Response({'detail': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f'Exception, {str(e)}')
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class FlockMovementViewSet(viewsets.ModelViewSet):
    queryset = FlockMovement.objects.all()
    serializer_class = FlockMovementSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = FlockMovementFilterSet
    ordering_fields = ["-movement_date", "flock"]
    permission_classes = [CanActOnFlockMovement]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            return Response([], status=status.HTTP_200_OK)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            self.request.user.last_activity = "Recorded new flock movement"
            self.request.user.save()
            return Response({'detail': 'Data saved successfully'}, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'detail': e.message}, status=status.HTTP_400_BAD_REQUEST)
        except DRFValidationError as e:
            return Response({'detail': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f'Exception, {str(e)}')
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class FlockInspectionRecordViewSet(viewsets.ModelViewSet):
    queryset = FlockInspectionRecord.objects.all()
    serializer_class = FlockInspectionRecordSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = FlockInspectionRecordFilterSet
    ordering_fields = ["-date_of_inspection", "flock"]

    def get_permissions(self):
        if self.action in ["destroy"]:
            permission_classes = [CanDeleteFlockInspection]
        else:
            permission_classes = [CanAddViewUpdateFlockInspection]
        return [permission() for permission in permission_classes]

    def update(self, request, *args, **kwargs):
        # Disallowed updated for flock inspection records for sake of brevity—Temporary
        return Response(
            {"detail": "Updates are rejected!"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def destroy(self, request, *args, **kwargs):
        # Disallowed deletion for flock inspection records for sake of brevity—Temporary
        return Response(
            {"detail": "Deletion not allowed!"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            return Response([], status=status.HTTP_200_OK)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        try:
            print(request.data)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            self.request.user.last_activity = "Record new flock inspection"
            self.request.user.save()
            return Response({'detail': 'Data saved successfully'}, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'detail': e.message}, status=status.HTTP_400_BAD_REQUEST)
        except DRFValidationError as e:
            return Response({'detail': str(e.detail)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f'Exception, {str(e)}')
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class FlockBreedInformationViewSet(viewsets.ModelViewSet):
    queryset = FlockBreedInformation.objects.all()
    serializer_class = FlockBreedInformationSerializer
    permission_classes = [CanActOnFlockBreedInformation]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            self.request.user.last_activity = "Added new flock breed information"
            self.request.user.save()
            return Response({'detail': 'Data saved successfully'}, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'detail': e.message}, status=status.HTTP_400_BAD_REQUEST)
        except DRFValidationError as e:
            return Response({'detail': str(e.detail)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f'Exception, {str(e)}')
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class EggCollectionViewSet(viewsets.ModelViewSet):
    queryset = EggCollection.objects.all()
    serializer_class = EggCollectionSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = EggCollectionFilterSet
    ordering_fields = ["-date_of_collection", "-time_of_collection", "flock"]

    def get_permissions(self):
        if self.action in ["create"]:
            permission_classes = [CanAddEggCollection]
        elif self.action in ["destroy"]:
            permission_classes = [CanDeleteEggCollection]
        else:
            permission_classes = [CanViewEggCollection]
        return [permission() for permission in permission_classes]

    def update(self, request, *args, **kwargs):
        # Disallowed update for egg collection records— Temporary.
        return Response(
            {"detail": "Updates are not allowed!."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            return Response([], status=status.HTTP_200_OK)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            self.request.user.last_activity = "Added new egg collection"
            self.request.user.save()
            return Response({'detail': 'Data saved successfully'}, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'detail': e.message}, status=status.HTTP_400_BAD_REQUEST)
        except DRFValidationError as e:
            return Response({'detail': str(e.detail)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f'Exception, {str(e)}')
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

