from django.db import models


class LastUpdatedMixin(models.Model):
    class Meta:
        abstract = True

    last_updated = models.DateTimeField(
        auto_now=True,
    )