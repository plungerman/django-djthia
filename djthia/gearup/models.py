# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.safestring import mark_safe
from djtools.fields import BINARY_CHOICES
from djtools.fields.helpers import upload_to_path
from taggit.managers import TaggableManager


ALLOWED_EXTENSIONS = (
    'jpg',
    'JPG',
    'jpeg',
    'JPEG',
    'mp3',
    'MP3',
    'mov',
    'MOV',
    'pdf',
    'PDF',
    'png',
    'PNG',
    'wav',
    'WAV',
)
FILE_VALIDATORS = [
    FileExtensionValidator(allowed_extensions=ALLOWED_EXTENSIONS),
]
STATUS_CHOICES = (
    (
        "Have a job or accepted an offer (paid internship, part-time, full-time, own business, etc.)",
        "Have a job or accepted an offer (paid internship, part-time, full-time, own business, etc.)",
    ),
    (
        'Have a job, but am continuing to look for other options',
        "Have a job, but am continuing to look for other options",
    ),
    (
        "Participating in a volunteer, service program, or unpaid internship (e.g. Peace Corps, City Year, Americorps, etc.)",
        "Participating in a volunteer, service program, or unpaid internship (e.g. Peace Corps, City Year, Americorps, etc.)",
    ),
    ('Serving in the military', "Serving in the military"),
    (
        'Enrolled in a program of continuing education',
        "Enrolled in a program of continuing education",
    ),
    (
        'Planning to continue education, but not yet enrolled',
        "Planning to continue education, but not yet enrolled",
    ),
    ('Unemployed and seeking employment', "Unemployed and seeking employment"),
    (
        "Pursuing other options (travel, family, not seeking, etc.)",
        "Pursuing other options (travel, family, not seeking, etc.)",
    ),
    ('Uncertain what my plans are', "Uncertain what my plans are"),
)
DONATION_CHOICES = (
    (
        'Yes',
        """
        Yes, I would like to make a gift in support of the Class of 2020
        Endowed Scholarship.
        """,
    ),
    (
        'No',
        "No, I would not like to make a gift at this time.",
    ),
)
COLOUR_CHOICES = (
    ('Black', 'Black'),
    ('Blue', 'Blue'),
    ('Gold', 'Gold'),
    ('Gray', 'Gray'),
    ('Green', 'Green'),
    ('Orange', 'Orange'),
    ('Pink', 'Pink'),
    ('Purple', 'Purple'),
    ('Red', 'Red'),
    ('Silver', 'Silver'),
    ('Tan/Beige', 'Tan/Beige'),
    ('Teal/Turquoise', 'Teal/Turquoise'),
    ('White', 'White'),
    ('Yellow', 'Yellow'),
)
CAP_GOWN_SHIPPING = (
    ("address_mailing", "Mailing Address"),
    ("address_permanent", "Permanent Address"),
    ("address_cap_gown", "Cap and Gown Address"),
)


class Questionnaire(models.Model):
    """Graduate gear up questionnaire for graduation."""

    # meta
    created_by = models.OneToOneField(
        User,
        verbose_name="Created by",
        related_name='questionnaire',
        editable=False,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    updated_by = models.ForeignKey(
        User,
        verbose_name="Updated by",
        related_name='updated_by',
        editable=False,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField("Date Created", auto_now_add=True)
    updated_at = models.DateTimeField("Date Updated", auto_now=True)
    # core
    name_full = models.CharField(
        "Full Name (first middle last) for diploma",
        max_length=128,
    )
    name_phonetic = models.CharField(
        "Phonetic Pronunciation of Name",
        max_length=128,
    )
    major_minor = models.CharField(
        "Are your majors and minors correct?",
        max_length=4,
        choices=BINARY_CHOICES,
        help_text=mark_safe("""
        If your majors and/or minors are incorrect, please contact
        <a href="mailto:registrar@carthage.edu">the registrar.</a>.
        """),
    )
    address_mailing = models.TextField(
        "Current Mailing Address",
    )
    address_permanent = models.TextField(
        "Permanent Address",
        null=True,
        blank=True,
        help_text="(if different than mailing address)",
    )
    email = models.EmailField(
        "Email other than carthage.edu", null=True, blank=True,
    )
    phone = models.CharField(
        "Your Phone Number",
        max_length=12,
        help_text="Format: XXX-XXX-XXXX",
    )
    guardian1 = models.CharField(
        "Parent Guardian Name 1",
        max_length=128,
        null=True,
        blank=True,
    )
    guardian2 = models.CharField(
        "Parent Guardian Name 2",
        max_length=128,
        null=True,
        blank=True,
    )
    name_spouse = models.CharField(
        "Spouse's Name",
        max_length=128,
        null=True,
        blank=True,
    )
    year_spouse = models.CharField(
        "Spouse's Class Year",
        max_length=4,
        null=True,
        blank=True,
        help_text="(Carthage student only)",
    )
    marriage_anniversary = models.DateTimeField(
        "Wedding Anniversary",
        help_text="Format: YYYY-MM-DD",
        blank=True,
        null=True,
    )
    status_postgrad = models.CharField(
        "Which of the following BEST describes your PRIMARY current status?",
        max_length=128,
        choices=STATUS_CHOICES,
    )
    graduate_school_name = models.CharField(
        "Graduate School Institution Name",
        max_length=128,
        null=True,
        blank=True,
    )
    graduate_school_program = models.CharField(
        "Graduate School Program Name",
        max_length=128,
        null=True,
        blank=True,
    )
    graduate_school_address = models.TextField(
        "Graduate School Address",
        null=True,
        blank=True,
    )
    graduate_school_city = models.CharField(
        "Graduate School City",
        max_length=128,
        null=True,
        blank=True,
    )
    graduate_school_state = models.CharField(
        "Graduate School State/Territory",
        max_length=128,
        null=True,
        blank=True,
    )
    graduate_school_postal_code = models.CharField(
        "Graduate School Postal Code",
        max_length=10,
        null=True,
        blank=True,
    )
    graduate_school_country = models.CharField(
        "Graduate School Country",
        max_length=128,
        null=True,
        blank=True,
    )
    graduate_school_email = models.EmailField(
        "Graduate School email", null=True, blank=True,
    )
    employer_name = models.CharField(
        "Post-Graduation Employer Name",
        max_length=128,
        null=True,
        blank=True,
    )
    employer_address = models.TextField(
        "Post-Graduation Employer Address",
        null=True,
        blank=True,
    )
    employer_city = models.CharField(
        "Post-Graduation Employer City",
        max_length=128,
        null=True,
        blank=True,
    )
    employer_state = models.CharField(
        "Post-Graduation Employer State/Territory",
        max_length=128,
        null=True,
        blank=True,
    )
    employer_postal_code = models.CharField(
        "Post-Graduation Employer Postal Code",
        max_length=10,
        null=True,
        blank=True,
    )
    employer_country = models.CharField(
        "Post-Graduation Employer Country",
        max_length=128,
        null=True,
        blank=True,
    )
    employer_email = models.EmailField(
        "Post-Graduation Employer email", null=True, blank=True,
    )
    employer_job_title = models.CharField(
        "Post-Graduation Employer Job Title",
        max_length=128,
        null=True,
        blank=True,
    )
    clubs_orgs = models.CharField(
        "Clubs and Orgs",
        max_length=255,
        help_text="""
            Please list all clubs, organizations, greek life, honor societies,
            and athletics you have been involved with during your time at Carthage
        """,
    )
    donation = models.CharField(
        "Class of 2020 Gift",
        max_length=4,
        choices=DONATION_CHOICES,
        help_text="""
            The recommended gift is $5, and every $5 gift is an entry into
            a drawing to receive a pair of Apple Airpods!
        """,
    )
    color = models.CharField(
        verbose_name="""
            Cast your vote for the Ribbon Color to represent 2020
            on the Key of Knowledge
        """,
        max_length=32,
        choices=COLOUR_CHOICES,
    )
    speaker = models.CharField(
        verbose_name="""
            Cast your vote for the faculty member you would like to speak
            as part of your celebration
        """,
        max_length=128,
        null=True,
        blank=True,
    )
    # thank you notes are FK from Comments data model
    # counseling file is FK from Documents data model
    cap_gown = models.CharField(
        "Have you ordered your Cap and Gown?",
        max_length=4,
        choices=BINARY_CHOICES,
        help_text=mark_safe("""
            If 'No', you can do so
            <a href='http://colleges.herffjones.com/college/carthage/' target='_blank'>here</a>.
            All orders will be shipped beginning May 4.
            Make sure to wear your regalia during the virtual ceremony,
            as graduates will perform the symbolic tradition of moving your
            tassels signaling you've obtained your degree.
        """),
        null=True,
        blank=True,
    )
    cap_gown_shipping = models.CharField(
        "Cap and Gown Shipping",
        max_length=32,
        choices=CAP_GOWN_SHIPPING,
        null=True,
        blank=True,
    )
    address_cap_gown = models.TextField(
        "Cap and Gown Shipping Address", null=True, blank=True,
    )

    class Meta:
        """Information about the data model class."""

        ordering = ['-created_at']
        get_latest_by = 'created_at'

    def __unicode__(self):
        """Default data for display."""
        return self.created_by.username

    def exit_counseling(self):
        """Check if the exit counseling form has been uploaded."""
        status = False
        for phile in self.files.all():
            for tag in phile.tags.all():
                if tag.name == 'Finaid':
                    status = phile.phile.name
                    break
        return status

    def photos(self):
        """Check if they have uploaded commencement photos."""
        fotos = []
        for phile in self.files.all():
            for tag in phile.tags.all():
                if tag.name == 'Commencement Photos':
                    fotos.append(phile)
                    break
        return fotos

    def get_absolute_url(self):
        """Absoluate URL for UI level."""
        return ('gearup_detail', [str(self.id)])


class Annotation(models.Model):
    """Notes, comments, etc."""

    questionnaire = models.ForeignKey(
        Questionnaire,
        related_name='notes',
        on_delete=models.CASCADE,
    )
    created_by = models.ForeignKey(
        User,
        verbose_name="Created by",
        related_name='note_creator',
        on_delete=models.PROTECT,
    )
    updated_by = models.ForeignKey(
        User,
        verbose_name="Updated by",
        related_name='note_updated',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField("Date Created", auto_now_add=True)
    updated_at = models.DateTimeField("Date Updated", auto_now=True)
    recipients = models.ManyToManyField(User, blank=True)
    body = models.TextField(verbose_name="Content")
    status = models.BooleanField(default=True, verbose_name="Active?")
    tags = TaggableManager(blank=True)

    class Meta:
        """Information about the data model class."""

        ordering = ('-created_at',)

    def __str__(self):
        """Default data for display."""
        return "{0}, {1}".format(
            self.created_by.last_name, self.created_by.first_name,
        )


class Document(models.Model):
    """Supporting documents."""

    created_by = models.ForeignKey(
        User,
        verbose_name="Created by",
        related_name='doc_creator',
        on_delete=models.CASCADE,
    )
    updated_by = models.ForeignKey(
        User,
        verbose_name="Updated by",
        related_name='doc_updated',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField("Date Created", auto_now_add=True)
    updated_at = models.DateTimeField("Date Updated", auto_now=True)
    questionnaire = models.ForeignKey(
        Questionnaire,
        related_name='files',
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        "Short description of file",
        max_length=128,
        null=True,
        blank=True,
    )
    phile = models.FileField(
        "Dependent files",
        upload_to=upload_to_path,
        validators=FILE_VALIDATORS,
        max_length=768,
        null=True,
        blank=True,
    )
    tags = TaggableManager(blank=True)

    class Meta:
        """Information about the data model class."""

        ordering = ['-created_at']
        get_latest_by = 'created_at'

    def get_slug(self):
        """Slug for file uploads."""
        return 'gearup-document'

    def __str__(self):
        """Default data for display."""
        return str(self.questionnaire)
