
from django.conf.urls import url, include

from hr.users.views import (HRApproveView, OpenRequestView, ManagerRequestView,
                            ManagerApproveView, LogView,
                            ProcessedRequestView, ReviewedRequestView)

urlpatterns = [
    url(r'^', include('rest_auth.urls')),
    url(r'^registration/', include('rest_auth.registration.urls'))
]

hr_urlpatterns = [
    url(r'^requests/$', OpenRequestView.as_view(), name="user-requests"),
    url(r'^requests/(?P<id>[\d]+)/$', HRApproveView.as_view(), name="user-requests-approve")
]

manager_urlpatterns = [
    url(r'^requests/$', ManagerRequestView.as_view(), name="user-requests"),
    url(r'^requests/(?P<id>[\d]+)/$', ManagerApproveView.as_view(), name="user-requests-approve")
]

log_urlpatterns = [
    url(r'^$', LogView.as_view(), name="list"),
]

requests_urlpatterns = [
    url(r'^open/$', OpenRequestView.as_view(), name="open"),
    url(r'^processed/$', ProcessedRequestView.as_view(), name="processed"),
    url(r'^reviewed/$', ReviewedRequestView.as_view(), name="hr-reviewed"),
]
