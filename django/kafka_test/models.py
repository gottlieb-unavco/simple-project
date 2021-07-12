from django.db import models
import uuid


def random_value():
    """
    Return some random value for a message
    """
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
    created_date = models.DateTimeField(auto_now_add=True)

    def delay(self):
        """
        Calculate the delay from when the message was sent to when
        it was saved to the db
        """
        if self.timestamp and self.created_date:
            return self.created_date - self.timestamp
