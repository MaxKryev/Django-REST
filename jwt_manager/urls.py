from django.urls import path
from .views import CustomTokenObtainPairView, CustomTokenRefreshView, AuthView, UserRegistrationView, \
    UploadDocumentView, DeleteDocumentView, AnalyseDocumentView, GetTextDocumentView

urlpatterns = [
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path("auth_check/", AuthView.as_view(), name="auth_check"),
    path("register/", UserRegistrationView.as_view(), name="user_register"),
    path("upload/", UploadDocumentView.as_view(), name="upload"),
    path("delete/<int:doc_id>", DeleteDocumentView.as_view(), name="delete"),
    path("analyse/<int:doc_id>", AnalyseDocumentView.as_view(), name="analyse"),
    path("get_text/<int:doc_id>", GetTextDocumentView.as_view(), name="get_text"),
]