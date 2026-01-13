from django.shortcuts import render
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets,filters,pagination
from .serializers import DoctorSerializer,DesignationSerializer,SpecializationSerializer,AvailableTimeSerializer,ReviewSerializer
from .models import Doctor,Specialization,Designation,AvailableTime,Review
# Create your views here.
class DoctorPagination(pagination.PageNumberPagination):
    page_size = 3
    page_size_query_params = 'page_size'
    max_page_size = 100


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['designation','specialization',]
    # pagination_class = DoctorPagination
    search_fields = [
        'user__first_name',
        'user__last_name',
        'designation__name',
        'specialization__name'
    ]
    
class SpecializationViewSet(viewsets.ModelViewSet):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer

class DesignationViewSet(viewsets.ModelViewSet):
    queryset = Designation.objects.all()
    serializer_class = DesignationSerializer

class AvailableTimeForSpecificDoctor(filters.BaseFilterBackend):
    def filter_queryset(self, request, query_set, view):
        doctor_id = request.query_params.get('doctor_id')

        if doctor_id:
            return query_set.filter(doctor=doctor_id)
        return query_set

class AvailabletimeViewSet(viewsets.ModelViewSet):
    queryset = AvailableTime.objects.all()
    serializer_class = AvailableTimeSerializer
    filter_backends = [AvailableTimeForSpecificDoctor]

class ReviewPagination(pagination.PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 100

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all().order_by('-created')
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['doctor']
    pagination_class = ReviewPagination
    # permission_classes = [IsAuthenticated]
    
    # GET hole amney dibe post hole authenticated labe
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(
        reviewer=self.request.user.patient
    )

        # 🔒 patient check
        if not hasattr(user, "patient"):
            raise ValidationError("Only patients can submit reviews")

        serializer.save(reviewer=user.patient)
   
