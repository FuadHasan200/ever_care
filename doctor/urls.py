from rest_framework.routers import DefaultRouter
from django.urls import path,include
from .views import DoctorViewSet,DesignationViewSet,SpecializationViewSet,AvailabletimeViewSet,ReviewViewSet

router = DefaultRouter()
router.register('list',DoctorViewSet)
router.register('designation',DesignationViewSet)
router.register('specialization',SpecializationViewSet)
router.register('available_time',AvailabletimeViewSet)
router.register('reviews',ReviewViewSet)

urlpatterns = [
    path('',include(router.urls)),
    
]
