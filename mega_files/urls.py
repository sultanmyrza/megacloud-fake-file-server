from django.urls.conf import path

from . import views

urlpatterns = [
    path(
        "resource/dir/users/<str:user_external_id>",
        views.create_file_or_directory,
        name="create_file_or_directory",
    ),
    path(
        "resource/files/<str:file_id>/users/<str:user_external_id>",
        views.specific_file_related_actions,
        name="specific_file_related_actions",
    ),
    path(
        "resource/files/users/<str:user_external_id>",
        views.get_files_from_root_directory,
        name="get_files_from_root_directory",
    ),
    path(
        "resource/dir/<str:dir_id>/users/<str:user_external_id>",
        views.specific_directory_related_actions,
        name="specific_directory_related_actions",
    ),
    path(
        "api/v1/resource/files/file_id/users/user_external_id/action/rename",
        views.rename_file,
        name="rename_file",
    ),
    path(
        "api/v1/resource/dir/dir_id/users/user_external_id/action/rename",
        views.directory_file,
        name="rename_file",
    ),
    path(
        "api/v1/resource/files/file_id/users/user_external_id/action/move",
        views.move_file,
        name="move_file",
    ),
]
