from django.shortcuts import render
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets,filters,pagination
from .serializers import DoctorSerializer,DesignationSerializer,SpecializationSerializer,AvailableTimeSerializer,ReviewSerializer
from .models import Doctor,Specialization,Designation,AvailableTime,Review
# Create your views here.
class DoctorPagination(pagination.PageNumberPagination):
    page_size = 1
    page_size_query_params = page_size
    max_page_size = 100
class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['designation','specialization',]
    # def get_queryset(self):
    #     queryset = Doctor.objects.all()

    #     search = self.request.query_params.get('search')
    #     designation = self.request.query_params.get('designation')
    #     specialization = self.request.query_params.get('specialization')

    #     if search:
    #         queryset = queryset.filter(
    #             Q(user__first_name__icontains=search) |
    #             Q(user__last_name__icontains=search) |
    #             Q(designation__name__icontains=search) |
    #             Q(specialization__name__icontains=search)
    #         ).distinct()

    #     if designation:
    #         queryset = queryset.filter(designation__name=designation)

    #     if specialization:
    #         queryset = queryset.filter(specialization__name=specialization)

    #     return queryset
    # filter_backends = [filters.SearchFilter]
    # # pagination_class = DoctorPagination
    # search_fields = [
    #     'user__first_name',
    #     'user__last_name',
    #     'specialization__name',
    #     'desigantion__name'
    # ]
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

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
