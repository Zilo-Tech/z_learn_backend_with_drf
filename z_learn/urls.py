from django.urls import path, include
from django.contrib import admin
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.conf import settings
from django.conf.urls.static import static

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from django.contrib.staticfiles.urls import staticfiles_urlpatterns


schema_view = get_schema_view(
   openapi.Info(
      title="Z-Learn",
      default_version='v1',
      description="This is the API documentation for ",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@myapi.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
   #  path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   #  path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # Your other URLs...
    
   path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
   path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    
   path('admin/', admin.site.urls),
   path('authentication/', include('authentication.urls')),
   path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),


   path('account/', include('authentication.api.urls')),
   path('notification/', include('annoucement_news.api.urls')),
   path('chat_section/', include('chat_section.api.urls')),
   path('concourse/', include('concourse.api.urls')),
   path('ai/', include('AI.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    
urlpatterns += staticfiles_urlpatterns()