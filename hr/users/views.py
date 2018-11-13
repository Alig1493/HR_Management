from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView

from hr.users.config import Status
from hr.users.permissions import IsHRPermitted, IsManagerPermitted
from hr.users.serializers import HRApproveSerializer, UserPublicSerializer, ManagerApproveSerializer

User = get_user_model()


class RequestView(ListAPIView):

    permission_classes = [IsHRPermitted]
    queryset = User.objects.filter(status=Status.OPEN)
    serializer_class = UserPublicSerializer


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
    queryset = User.objects.filter(status=Status.HR_REVIEWED)


class ManagerApproveView(RetrieveUpdateAPIView):

    permission_classes = [IsManagerPermitted]
    serializer_class = ManagerApproveSerializer
    queryset = User.objects.all()
    lookup_field = "id"
    lookup_url_kwarg = "id"

    def perform_update(self, serializer):
        serializer.save(manager_approved_by=self.request.user)
