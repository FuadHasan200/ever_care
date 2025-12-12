from rest_framework.routers import DefaultRouter
from django.urls import path,include
from .views import PatientViewset,PatientRegistrationViewset
from . import views
router = DefaultRouter()
router.register('list',PatientViewset)

urlpatterns = [
    path("", include(router.urls)),
    path('register/',PatientRegistrationViewset.as_view(),name='register'),
    path('active/<uid64>/<token>/',views.activate, name='activate'),
]
