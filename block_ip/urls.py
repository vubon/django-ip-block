from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^test/', views.WhiteListAPI.as_view()),
    url(r'^block-ip-create-list/', views.BlockIPList.as_view()),
    url(r'^check/', views.TestView.as_view()),
]
