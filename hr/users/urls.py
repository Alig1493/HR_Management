
from django.conf.urls import url, include

from hr.users.views import HRApproveView, RequestView, ManagerRequestView, ManagerApproveView, LogView

urlpatterns = [
    url(r'^', include('rest_auth.urls')),
    url(r'^registration/', include('rest_auth.registration.urls'))
]

hr_urlpatterns = [
    url(r'^requests/$', RequestView.as_view(), name="user-requests"),
    url(r'^requests/(?P<id>[\d]+)/$', HRApproveView.as_view(), name="user-requests-approve")
]

manager_urlpatterns = [
    url(r'^requests/$', ManagerRequestView.as_view(), name="user-requests"),
    url(r'^requests/(?P<id>[\d]+)/$', ManagerApproveView.as_view(), name="user-requests-approve")
]

log_urlpatterns = [
    url(r'^$', LogView.as_view(), name="list"),
]
