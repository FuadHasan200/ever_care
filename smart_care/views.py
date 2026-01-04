from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_framework.exceptions import ValidationError
from google.oauth2 import id_token
from google.auth.transport import requests

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    # client_class = OAuth2Client
    
    # def post(self, request, *args, **kwargs):
    #     id_token_str = request.data.get("id_token")

    #     if not id_token_str:
    #         raise ValidationError("id_token is required")

    #     try:
    #         info = id_token.verify_oauth2_token(
    #             id_token_str,
    #             requests.Request(),
    #             "666777518408-uf7s4h7u74aaoa8a0afhoa80oggjtcn4.apps.googleusercontent.com"
    #         )
    #     except Exception:
    #         raise ValidationError("Invalid Google token")

    #     # dj-rest-auth কে deceive করছি 😄
    #     request.data["access_token"] = id_token_str

    #     return super().post(request, *args, **kwargs)

class GithubLogin(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter