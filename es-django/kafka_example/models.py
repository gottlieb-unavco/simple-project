from django.db import models
import uuid
from datetime import timedelta


def random_value():
    """
    Return some random value for a message
    """
    return "example:py/%s" % str(uuid.uuid1())


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

    def delay_ms(self):
        """
        Calculate the delay from when the message was sent to when
        it was saved to the db
        """
        return self.delay() / timedelta(milliseconds=1)
