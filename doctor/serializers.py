from rest_framework import serializers
from .models import Review, Doctor,Designation,Specialization,AvailableTime
from patient.serializers import PatientSerialzer
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

class ReviewSerializer(serializers.ModelSerializer):
    reviewer = PatientSerialzer(read_only=True)
    doctor = DoctorSerializer(read_only=True)
    doctor = serializers.PrimaryKeyRelatedField(
        queryset=Doctor.objects.all()
    )
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ["reviewer","created"]
    
#    
    def validate_doctor(self, doctor):
        user = self.context['request'].user

        # ❌ Doctor হলে review দিতে পারবে না
        if hasattr(user, 'doctor'):
            raise serializers.ValidationError(
                {
                   'err': ["Doctors are not allowed to give reviews"]
                }
            )


        # 🔒 Only patient can review
        if not hasattr(user, 'patient'):
            raise serializers.ValidationError(
                {
                   'err': ["Only patients can give reviews"]
                }
            )

        # 🔒 Same patient can't review same doctor twice
        if Review.objects.filter(
            reviewer=user.patient,
            doctor=doctor
        ).exists():
            raise serializers.ValidationError(
                {
                   'err':["You already reviewed this doctor"]
                }
            )
        

        return doctor