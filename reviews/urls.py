from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RecruiterViewSet, CompanyViewSet, RecruiterReviewViewSet

router = DefaultRouter()
router.register(r'recruiters', RecruiterViewSet)
router.register(r'companies', CompanyViewSet)
router.register(r'reviews', RecruiterReviewViewSet)

urlpatterns = [
    path('/', include(router.urls)),
]
