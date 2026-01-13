from .views import MeView
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('contact_us/',include('contactus.urls')),
    path('patient/',include('patient.urls')),
    path('service/',include('service.urls')),
    path('doctor/',include('doctor.urls')),
    path('appointment/',include('appointment.urls')),
    path('me/',MeView.as_view(),name='me'),
    path("auth/", include("dj_rest_auth.urls")),
    # path("auth/registration/", include("dj_rest_auth.registration.urls")),
    path('accounts/', include("allauth.urls")),
  
    
   
    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
