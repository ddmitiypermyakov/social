from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *


urlpatterns = [
    # path('register/',register,name='register'),
    path('profile/<int:pk>/', get_profile, name='profile'),
    path('login/',user_login,name='login'),
    path('logout/',user_logout,name='logout'),
    path('accounts/register/done', UserRegisterDoneView.as_view(), name='register_done'),
    path('accounts/register/', UserRegisterView.as_view(), name='register_user'),
    path('accounts/profile/change/<int:pk>/', ChangeUserInfoView.as_view(), name='profile_user'),
    path('<int:pk>/',by_person,name='by_person'),
    # path('search/',Search.as_view(),name='search'),
    path('', mane_page,name='home'),
    path('gender/<int:gender_id>/', get_gender, name='gender'),

    path('sort_profile/', sort_profile, name='sort1'),
    path('sort_bith/', sort_profile_bith, name='sort2'),
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)