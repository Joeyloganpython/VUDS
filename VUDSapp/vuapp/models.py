from unittest import expectedFailure
from django.db import models
from django.core.exceptions import ValidationError

yes_no_choices = [("Yes", "Yes"), ("No", "No")]

bladder_choices = [
    ("Smooth;Round", "Smooth;Round"),
    ("Smooth", "Smooth"),
    ("Smooth;Oblong", "Smooth;Oblong"),
    ("Trabeculated;Oblong", "Trabeculated;Oblong"),
    ("Unknown", "Unknown"),
    ("Trabeculated", "Trabeculated"),
    (
        "Oblong;Few diverticula, generally smooth",
        "Oblong;Few diverticula, generally smooth",
    ),
    ("Trabeculated;Round", "Trabeculated;Round"),
]

rating_choices = [("Good", "Good"), ("Bad", "Bad"), ("Ugly", "Ugly")]


def validate_file_extension(value):
    if not value.name.endswith(".txt"):
        raise ValidationError("Please upload .txt files only")


def validate_dicom_extension(value):
    if not value.name.endswith(".dcm"):
        raise ValidationError("Please upload .dcm files only")


class Flowsheet(models.Model):
    Leak_Present = models.CharField(max_length=5, choices=yes_no_choices)
    Reflux = models.CharField(max_length=5, choices=yes_no_choices)
    desd = models.CharField(max_length=5, choices=yes_no_choices)
    bladder_shape = models.CharField(max_length=50)
    age_time_of_study = models.FloatField()
    pvr = models.FloatField()
    percent_full = models.FloatField()
    bladder_shape = models.CharField(max_length=50, choices=bladder_choices)
    pressure_25 = models.FloatField()
    pressure_half_ebc = models.FloatField()
    press_three_four_ebc = models.FloatField()
    your_expert_rating = models.CharField(max_length=50, choices=rating_choices)

    class Meta:
        managed = True
        db_table = "flowsheet"


class TextfileUpload(models.Model):
    upload = models.FileField(
        upload_to="textfilesupload/", validators=[validate_file_extension]
    )
    expected_bladder_capacity = models.FloatField()


class DicomefileUpload(models.Model):
    dicom_upload = models.FileField(
        upload_to="textfilesupload/", validators=[validate_dicom_extension]
    )
