import uuid
from django.db import models
from django.utils.timezone import now


def today():
    return now().date()


class ModelBase(models.Model):
    class Meta:
        abstract = True

    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        instance.save()
        return instance

    @classmethod
    def get_or_create(cls, **kwargs):
        existing = cls.objects.filter(**kwargs)
        if existing.exists():
            instance = existing.first()
        else:
            instance = cls(**kwargs)
            instance.save()
        return instance
