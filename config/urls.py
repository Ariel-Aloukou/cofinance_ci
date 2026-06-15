from django.views.generic import TemplateView
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


 
urlpatterns = [
    path("admin/", admin.site.urls),
    # ===== DOCUMENTATION API =====
    
    path("api/auth/", include("apps.authentication.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    # ===== MODULES DE L'API =====
    path("api/credits/", include("apps.credits.urls")),
    path("api/remboursements/", include("apps.remboursements.urls")),
    path("api/assurance/", include("apps.assurance.urls")),
    path("api/dashboard/", include("apps.dashboard.urls")),
    path("api/notifications/", include("apps.notifications.urls")),
    path("api/chat/", include("apps.chat.urls")),
    # Interface HTML chat
    path("chat/", TemplateView.as_view(template_name="chat/chat.html"), name="chat"),
     path("login/",          TemplateView.as_view(template_name="login.html"),    name="login"),
    path("register/",       TemplateView.as_view(template_name="register.html"), name="register"),
    path("dashboard/",      TemplateView.as_view(template_name="app.html"),      name="dashboard"),
    path("dashboard-admin/",TemplateView.as_view(template_name="app.html"),      name="dashboard-admin"),
]


# Permet d'accéder aux fichiers uploadés en mode DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
