from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.throttling import ScopedRateThrottle

from .serializers import LeadCreateSerializer


class LeadViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Создание заявки через API."""

    serializer_class = LeadCreateSerializer
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "leads"
