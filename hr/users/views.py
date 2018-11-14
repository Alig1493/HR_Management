from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView

from hr.users.config import Status
from hr.users.models import Log
from hr.users.pagination import StandardResultsSetPagination
from hr.users.permissions import IsHRPermitted, IsManagerPermitted
from hr.users.serializers import HRApproveSerializer, UserPublicSerializer, ManagerApproveSerializer, LogSerializer

User = get_user_model()


class RequestView(ListAPIView):

    permission_classes = [IsHRPermitted]
    queryset = User.objects.filter(status=Status.OPEN).order_by("date_joined")
    serializer_class = UserPublicSerializer
    pagination_class = StandardResultsSetPagination


class HRApproveView(RetrieveUpdateAPIView):

    permission_classes = [IsHRPermitted]
    serializer_class = HRApproveSerializer
    queryset = User.objects.all()
    lookup_field = "id"
    lookup_url_kwarg = "id"

    def perform_update(self, serializer):
        serializer.save(hr_reviewed_by=self.request.user)


class ManagerRequestView(RequestView):

    permission_classes = [IsManagerPermitted]
    queryset = User.objects.filter(status=Status.HR_REVIEWED).order_by("date_joined")


class ManagerApproveView(RetrieveUpdateAPIView):

    permission_classes = [IsManagerPermitted]
    serializer_class = ManagerApproveSerializer
    queryset = User.objects.all().order_by("date_joined")
    lookup_field = "id"
    lookup_url_kwarg = "id"

    def perform_update(self, serializer):
        serializer.save(manager_approved_by=self.request.user)


class LogView(ListAPIView):

    serializer_class = LogSerializer
    queryset = Log.objects.all().order_by("created_at")
    pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        return [IsHRPermitted()] or [IsManagerPermitted()]
