from django.urls.conf import path

from . import views


urlpatterns = [
    path("resource/users/<str:external_id>", views.get_user_info, name="get_user_info"),
]
