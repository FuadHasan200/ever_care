from rest_framework import serializers
from .models import Review, Doctor,Designation,Specialization,AvailableTime

class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = '__all__'

class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = '__all__'

class AvailableTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableTime
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class DoctorSerializer(serializers.ModelSerializer):
    # user = serializers.StringRelatedField(many=False)
    # desigantion = serializers.StringRelatedField(many=True)
    # specialization = serializers.StringRelatedField(many=True)
    # available_time = serializers.StringRelatedField(many=True)
    user = serializers.SerializerMethodField()
    designation = DesignationSerializer(many=True)
    specialization = SpecializationSerializer(many=True)
    available_time = AvailableTimeSerializer(many=True)

    class Meta:
        model = Doctor
        fields = [
            'id',
            'user',
            'designation',
            'specialization',
            'available_time',
            'fee',
            'meet_link',
            'image'
        ]
    def get_user(self, obj):
        return {
            "id": obj.user.id,
            "first_name": obj.user.first_name,
            "last_name": obj.user.last_name,
            "username": obj.user.username,
            "email": obj.user.email,
        }

