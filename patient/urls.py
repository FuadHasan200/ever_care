from rest_framework.routers import DefaultRouter
from django.urls import path,include
from .views import PatientViewset,PatientRegistrationViewset,UserloginApiView,UserLogOutView,GoogleLogin
from . import views
router = DefaultRouter()
router.register('list',PatientViewset)

urlpatterns = [
    path("", include(router.urls)),
    path('register/',PatientRegistrationViewset.as_view(),name='register'),
    path('login/',UserloginApiView.as_view(),name='login'),
    path('logout/',UserLogOutView.as_view(),name='logout'),
    path('active/<uid64>/<token>/',views.activate, name='activate'),
    path('googleLogin/',GoogleLogin.as_view(),name='google_login')
]
