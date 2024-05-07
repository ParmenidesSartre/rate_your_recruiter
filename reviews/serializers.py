from rest_framework import serializers
from .models import Recruiter, Company, RecruiterReview


class RecruiterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recruiter
        fields = ['id', 'name', 'email', 'company', 'claimed']


class CompanySerializer(serializers.ModelSerializer):
    recruiters = RecruiterSerializer(
        many=True, read_only=True)

    class Meta:
        model = Company
        fields = ['id', 'name', 'recruiters', 'industry', 'consultancy']


class RecruiterReviewSerializer(serializers.ModelSerializer):
    recruiter_name = serializers.CharField(
        source='recruiter.name', read_only=True)
    company_name = serializers.CharField(
        source='recruiter.company.name', read_only=True)
    user = serializers.SerializerMethodField()

    class Meta:
        model = RecruiterReview
        fields = ['id', 'recruiter_name', 'company_name', 'user', 'status', 'contact_date',
                  'interaction_type', 'rating', 'review_text', 'proof', 'proof_link', 'anonymous', 'flagged']

    def get_user(self, obj):
        if obj.anonymous:
            return "Anonymous"
        return obj.user.username  # Show the username only if not anonymous
