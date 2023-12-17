from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("admin/blogger", admin.site.urls),
    # This is my default URL pattern
    #
    path("", include("myblogAppV3.urls")),
    path("api/", include("myblogAppV3.urls_api")),
    path("froala_editor/", include("froala_editor.urls")),
    path("api-auth/", include("rest_framework.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
