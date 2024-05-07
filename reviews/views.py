from rest_framework import viewsets, status
from .models import Recruiter, Company, RecruiterReview
from .serializers import RecruiterSerializer, CompanySerializer, RecruiterReviewSerializer
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


class RecruiterViewSet(viewsets.ModelViewSet):
    queryset = Recruiter.objects.all().order_by(
        '-claimed')  # by default ordering by `claimed` field
    serializer_class = RecruiterSerializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    # Filtering by `claimed`, `name`, `email` and `company` fields
    filterset_fields = ['claimed', 'name', 'email', 'company']
    # Searching by `name`, `email` and `company` fields
    search_fields = ['name', 'email', 'company__name']
    # Ordering by `name`, `email`, `company` and `claimed` fields
    ordering_fields = ['name', 'email', 'company', 'claimed']
    ordering = ['name']  # Default ordering by `name` field


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all().order_by('name')
    serializer_class = CompanySerializer


class RecruiterReviewViewSet(viewsets.ModelViewSet):
    queryset = RecruiterReview.objects.all().order_by('-created_at')
    serializer_class = RecruiterReviewSerializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['recruiter', 'company', 'user', 'status']
    search_fields = ['recruiter__name', 'company__name',
                     'review_text', 'user__username']
    ordering_fields = ['recruiter', 'company', 'user', 'status', 'created_at']
    ordering = ['-created_at']
