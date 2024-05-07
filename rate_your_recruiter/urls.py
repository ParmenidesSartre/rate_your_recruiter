# urls.py

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from reviews.views import RecruiterViewSet, CompanyViewSet, RecruiterReviewViewSet
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

# Setup DRF router
router = DefaultRouter()
router.register(r'recruiters', RecruiterViewSet)
router.register(r'companies', CompanyViewSet)
router.register(r'reviews', RecruiterReviewViewSet)

# URL patterns combining both regular and API routes
urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'),
         name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('admin/', admin.site.urls),  # Admin URL
    path('api/', include(router.urls)),  # API URLs
]
