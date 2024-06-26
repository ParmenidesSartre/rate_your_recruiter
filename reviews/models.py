from django.db import models
from django.db.models import Avg
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from simple_history.models import HistoricalRecords
from django.utils.translation import gettext_lazy as _


class InteractionType(models.TextChoices):
    EMAIL = 'Email', _('Email')
    PHONE = 'Phone', _('Phone Call')
    WHATSAPP = 'WhatsApp', _('WhatsApp')
    IN_PERSON = 'InPerson', _('In-Person Meeting')


class RecruitmentStatus(models.TextChoices):
    APPLIED = 'Applied', _('Applied')
    INTERVIEWED = 'Interviewed', _('Interviewed')
    REJECTED = 'Rejected', _('Rejected')
    OFFERED = 'Offered', _('Offered')
    ACCEPTED = 'Accepted', _('Accepted')
    DECLINED = 'Declined', _('Declined')
    WITHDRAWN = 'Withdrawn', _('Withdrawn')
    GHOSTED = 'Ghosted', _('Ghosted')
    OTHER = 'Other', _('Other')


class Industry(models.TextChoices):
    TECH = 'Tech', _('Technology')
    FINANCE = 'Finance', _('Finance')
    HEALTHCARE = 'Healthcare', _('Healthcare')
    CONSULTING = 'Consulting', _('Consulting')
    EDUCATION = 'Education', _('Education')
    GOVERNMENT = 'Government', _('Government')
    RETAIL = 'Retail', _('Retail')
    MANUFACTURING = 'Manufacturing', _('Manufacturing')
    OTHER = 'Other', _('Other')


class Company(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    industry = models.CharField(
        max_length=255, blank=True, choices=Industry.choices, default=Industry.OTHER)
    consultancy = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"


class Recruiter(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='recruiters', db_index=True)
    history = HistoricalRecords()
    claimed = models.BooleanField(default=False)
    claimed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    impact_score = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0.00), MaxValueValidator(5.00)],
        help_text="Calculated based on responsiveness, accuracy of job descriptions, and candidate experience."
    )

    def update_impact_score(self):
        reviews = RecruiterReview.objects.filter(recruiter=self)
        if reviews.exists():  # Check if there are any reviews
            average_ratings = reviews.aggregate(
                avg_responsiveness=Avg('responsiveness_rating'),
                avg_professionalism=Avg('professionalism_rating'),
                avg_transparency=Avg('transparency_rating')
            )

            response_score = average_ratings['avg_responsiveness'] or 0
            professionalism_score = average_ratings['avg_professionalism'] or 0
            transparency_score = average_ratings['avg_transparency'] or 0

            self.impact_score = (
                response_score + professionalism_score + transparency_score) / 3
        else:
            self.impact_score = 0
        self.save()

    def __str__(self):
        return f"{self.name} - {self.company.name}"


class RecruiterClaim(models.Model):
    recruiter = models.OneToOneField(
        Recruiter, on_delete=models.CASCADE, db_index=True)
    claimant = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    proof = models.FileField(upload_to='claim_proofs/')
    approved = models.BooleanField(default=False)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='claims_reviewed', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Claim by {self.claimant.username} for {self.recruiter.name}"


class RecruiterReview(models.Model):
    recruiter = models.ForeignKey(
        Recruiter, null=True, on_delete=models.CASCADE)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    points_awarded_for_update = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20,
        choices=RecruitmentStatus.choices,
        default=RecruitmentStatus.APPLIED,
        help_text="Current status of the recruitment process."
    )
    contact_date = models.DateField()
    interaction_type = models.CharField(
        max_length=20,
        choices=InteractionType.choices,
        default=InteractionType.EMAIL,
        help_text="Method of interaction with the recruiter."
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="General rating should be between 1 and 5.",
    )
    responsiveness_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating of recruiter's responsiveness, from 1 (poor) to 5 (excellent)."
    )
    professionalism_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating of recruiter's professionalism, from 1 (poor) to 5 (excellent)."
    )
    transparency_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating of recruiter's transparency in the recruitment process, from 1 (poor) to 5 (excellent)."
    )
    review_text = models.TextField()
    proof = models.FileField(upload_to='proofs/', null=True, blank=True)
    proof_link = models.URLField(blank=True, null=True)
    anonymous = models.BooleanField(default=False)
    flagged = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        interaction = self.get_interaction_type_display()
        return f"{self.user.username} - {self.recruiter.name} at {self.recruiter.company.name} via {interaction}"

    class Meta:
        verbose_name = "Recruiter Review"
        verbose_name_plural = "Recruiter Reviews"
        ordering = ['-created_at']


class RecruiterResponse(models.Model):
    review = models.ForeignKey(RecruiterReview, on_delete=models.CASCADE)
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE)
    response_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response by {self.recruiter.name} on {self.review}"

    class Meta:
        verbose_name = "Recruiter Response"
        verbose_name_plural = "Recruiter Responses"


class ReviewFeedback(models.Model):
    review = models.ForeignKey(RecruiterReview, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    feedback = models.TextField()
    resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.user.username} on {self.review}"

    class Meta:
        verbose_name = "Review Feedback"
        verbose_name_plural = "Review Feedbacks"
