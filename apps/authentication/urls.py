# apps/authentication/urls.py

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import InscriptionView, LoginView, ProfilView
from .views import PresenceAgentListView, MettreAJourPresenceView

urlpatterns = [
    path('register/',          InscriptionView.as_view(),        name='inscription'),
    path('login/',             LoginView.as_view(),               name='login'),
    path('token/refresh/',     TokenRefreshView.as_view(),        name='token-refresh'),
    path('profil/',            ProfilView.as_view(),              name='profil'),
    path('agents/presence/',   PresenceAgentListView.as_view(),   name='presence-list'),
    path('agents/ma-presence/', MettreAJourPresenceView.as_view(), name='ma-presence'),
]