from django.db import models
import uuid


def random_value():
    return str(uuid.uuid1())


class ExampleValue(models.Model):
    """
    Simple model corresponding to the example avro value
    """
    timestamp = models.DateTimeField()
    value = models.CharField(
        max_length=64,
        default=random_value,
    )
