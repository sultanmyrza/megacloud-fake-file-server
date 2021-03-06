"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from mega_files import urls as mega_files_urls
from mega_files.views import DownloadUploadApiView
from mega_users import urls as mega_users_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("<str:id>/<str:file_name>", view=DownloadUploadApiView.as_view()),
    # path("<uuid:user_external_id>/<str:server_file_name>", view=download_file),
    # path("<uuid:mega_file_id>/<str:file_name>", view=upload_mega_binary_file),
    path("api/v1/", include(mega_files_urls)),
    path("api/v1/", include(mega_users_urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
