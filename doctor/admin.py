from django.contrib import admin
from . models import Doctor,Specialization,Designation,AvailableTime,Review
# Register your models here.
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['first_name','fee']
    def first_name(self,obj):
        return obj.user.username
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ['name']
    prepopulated_fields = {'slug':('name',),}
admin.site.register(Specialization,SpecializationAdmin)
class DesignationAdmin(admin.ModelAdmin):
    list_display = ['name']
    prepopulated_fields = { 'slug':('name',),}
admin.site.register(Designation,DesignationAdmin)
admin.site.register(AvailableTime)
admin.site.register(Review)
admin.site.register(Doctor,DoctorAdmin)
