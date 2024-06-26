from .models import RecruiterReview
from django.contrib import admin
from django import forms
from .models import (
    RecruiterReview, Recruiter, Company, RecruiterClaim, RecruiterResponse, ReviewFeedback
)


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'industry', 'consultancy')
    search_fields = ['name', 'industry', 'consultancy']
    list_filter = ('industry', 'consultancy')


class RecruiterReviewForm(forms.ModelForm):
    class Meta:
        model = RecruiterReview
        fields = '__all__'

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating < 1:
            raise forms.ValidationError("Rating must be at least 1.")
        return rating


class RecruiterReviewAdmin(admin.ModelAdmin):
    form = RecruiterReviewForm
    list_display = (
        'recruiter', 'company', 'user', 'contact_date',
        'responsiveness_rating', 'professionalism_rating',
        'transparency_rating', 'rating', 'created_at'
    )
    list_filter = (
        'created_at', 'company__name', 'responsiveness_rating',
        'professionalism_rating', 'transparency_rating', 'rating'
    )
    search_fields = (
        'recruiter__name', 'company__name', 'review_text', 'user__username'
    )
    autocomplete_fields = ('recruiter', 'user', 'company')
    readonly_fields = ('points_awarded_for_update',)

    class Meta:
        model = RecruiterReview


class RecruiterAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'company')
    search_fields = ('name', 'email', 'company__name')
    list_filter = ('company__name',)
    readonly_fields = ('claimed',)
    autocomplete_fields = ['company', 'claimed_by']


class RecruiterClaimAdmin(admin.ModelAdmin):
    list_display = ('recruiter', 'claimant', 'approved',
                    'created_at', 'reviewed_by')
    list_filter = ('approved', 'created_at')
    search_fields = ('recruiter__name', 'claimant__username')
    raw_id_fields = ('recruiter', 'claimant', 'reviewed_by')

# Custom ModelAdmin for RecruiterResponse


class RecruiterResponseAdmin(admin.ModelAdmin):
    list_display = ('review', 'recruiter', 'created_at')
    search_fields = ('review__review_text', 'recruiter__name')

# Custom ModelAdmin for ReviewFeedback


class ReviewFeedbackAdmin(admin.ModelAdmin):
    list_display = ('review', 'user', 'resolved', 'created_at')
    list_filter = ('resolved', 'created_at')
    search_fields = ('review__review_text', 'user__username')


# Registering models with their respective custom admin configurations
admin.site.register(Company, CompanyAdmin)
admin.site.register(RecruiterReview, RecruiterReviewAdmin)
admin.site.register(Recruiter, RecruiterAdmin)
admin.site.register(RecruiterClaim, RecruiterClaimAdmin)
admin.site.register(RecruiterResponse, RecruiterResponseAdmin)
admin.site.register(ReviewFeedback, ReviewFeedbackAdmin)

# Customizing the admin site headers and titles
admin.site.site_header = "Recruitment Reviews Administration"
admin.site.site_title = "Recruiter Review Portal"
admin.site.index_title = "Welcome to the Recruitment Review Admin"
