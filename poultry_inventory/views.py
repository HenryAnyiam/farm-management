from rest_framework import viewsets

from .serializers import *


class FlockInventoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for retrieving FlockInventory instances.

    Provides the following actions:
    - `list`: Retrieves a list of all flock inventories.
    - `retrieve`: Retrieves a specific flock inventory by its ID.

    """
    queryset = FlockInventory.objects.all()
    serializer_class = FlockInventorySerializer


class FlockInventoryHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for retrieving FlockInventoryHistory instances.

    Provides the following actions:
    - `list`: Retrieves a list of all flock inventory histories.
    - `retrieve`: Retrieves a specific flock inventory history by its ID.

    """
    queryset = FlockInventoryHistory.objects.all()
    serializer_class = FlockInventoryHistorySerializer



from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import FarmData
from .serializers import FarmDataSerializer

# Farm Data Entry View
class FarmDataCreateView(generics.CreateAPIView):
    queryset = FarmData.objects.all()
    serializer_class = FarmDataSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(CustomUser=self.request.user)
        self.request.user.last_activity = "Added new farm data"
        self.request.user.save()

# List Farm Data for reports
class FarmDataListView(generics.ListAPIView):
    queryset = FarmData.objects.all()
    serializer_class = FarmDataSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter the farm data based on the authenticated user
        user = self.request.user
        return FarmData.objects.filter(CustomUser = user)
       
