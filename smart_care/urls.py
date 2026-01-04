
from dj_rest_auth.registration.views import SocialLoginView

from .views import GoogleLogin,GithubLogin
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

     path("auth/", include("dj_rest_auth.urls")),
    # path("auth/registration/", include("dj_rest_auth.registration.urls")),
    path('accounts/', include("allauth.urls")),
   path("google/", GoogleLogin.as_view(), name="google_login"),
    path(
        "github/",
        GithubLogin.as_view(), name='github_login'),
   
    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
