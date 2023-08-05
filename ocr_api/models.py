import uuid
from django.db import models


class OcrModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lab_report = models.CharField(max_length=255, unique=True)
    patient_id = models.IntegerField(null=False,blank=False,unique=True)
    status = models.BooleanField(default=True,null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "ocr"
        ordering = ['-createdAt']

        def __str__(self) -> str:
            return self.patient_id
