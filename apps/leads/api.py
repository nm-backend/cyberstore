from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny

from .serializers import LeadCreateSerializer


class LeadViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Создание заявки через API."""

    serializer_class = LeadCreateSerializer
    permission_classes = [AllowAny]
