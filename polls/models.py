from django.db import models
from django.core.validators import FileExtensionValidator


class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    percent_number = models.IntegerField(default=0)
    document = models.FileField(
        upload_to="documents/", validators=[FileExtensionValidator(allowed_extensions=["xlsx"])]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
