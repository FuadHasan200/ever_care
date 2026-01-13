from django.shortcuts import render,redirect
import environ
from django.conf import settings
from rest_framework import viewsets
env = environ.Env()
environ.Env.read_env()
from .models import Patient
from .serializers import PatientSerialzer,RegistrationSerializer,loginSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from rest_framework.authtoken.models import Token
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from google.oauth2 import id_token
from rest_framework.exceptions import ValidationError
from google.auth.transport import requests
# for sending email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

# Create your views here.
class PatientViewset(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerialzer

class PatientRegistrationViewset(APIView):
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            print("user ", user)
            token = default_token_generator.make_token(user)
            print("token ",token)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            print("uid ",uid)
            confirm_link = f"http://127.0.0.1:8000/patient/active/{uid}/{token}"
            email_subject = 'Confirm Your Email'
            email_body = render_to_string('confirm_email.html',{'confirm_link':confirm_link})
            email = EmailMultiAlternatives(email_subject,'',to=[user.email])
            email.attach_alternative(email_body,'text/html')
            email.send()
            return Response({"message": "Check your email for confirmation"},status=201)
        return Response(serializer.errors)

def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except(User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect("https://ever-care-frontend.vercel.app")
    else:
        return redirect("https://ever-care-frontend.vercel.app/signup")
    
class UserloginApiView(APIView):
    def post(self,request):
        print(request.data)
        serializer = loginSerializer(data = self.request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            
            if user is None:
                return Response({'error':'Invalid username or password'}, status=401)
            if not user.is_active:
                return Response(
                    {'error': 'Please verify your email first'},
                    status=403
                )
            if user:
                token,_ = Token.objects.get_or_create(user=user)
                login(request,user)
                return Response({'token': token.key, 'user':username})
            else:
                return Response({'error':'invalid credentials'})
        else:
            return Response(serializer.errors, status=400)

class UserLogOutView(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            request.user.auth_token.delete()
            logout(request)
        return Response({"message":"logged out successfully"}, status=200)

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client

    def post(self, request):
        token = request.data.get("id_token")
        
        if not token:
            return Response({"error": "id_token required"}, status=400)

        try:
            info = id_token.verify_oauth2_token(
                token,
                requests.Request(),
                env("clientId"),
                
            )
        except Exception:
            return Response({"error": "Invalid Google token"}, status=400)

        email = info.get("email")
        name = info.get("name")

        user, created = User.objects.get_or_create(
            email=email,
            defaults={"username": email.split("@")[0]}
        )

        if created:
            user.set_unusable_password()
            user.is_active = True
            user.save()

        token_obj, _ = Token.objects.get_or_create(user=user)

        return Response({
            "key": token_obj.key,
            "user": {
                "username": user.username,
                "email": user.email
            }
        })
    # for debuging purpose
    # def post(self, request):
    #     token = request.data.get("id_token")

    #     print("TOKEN RECEIVED:", token[:40])
    #     print("ENV CLIENT_ID:", env("clientId"))

    #     try:
    #         info = id_token.verify_oauth2_token(
    #             token,
    #             requests.Request(),
    #             env("clientId"),
    #         )
    #         print("GOOGLE INFO:", info)
    #     except Exception as e:
    #         print("GOOGLE VERIFY ERROR:", e)
    #         return Response({"error": "Invalid Google token"}, status=400)

    #     return Response({"success": True})