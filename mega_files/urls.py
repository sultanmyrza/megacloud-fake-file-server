from django.urls.conf import path

from . import views


urlpatterns = [
    path(
        "resource/dir/users/<str:user_external_id>",
        views.create_directory,
        name="create_directory",
    ),
]
