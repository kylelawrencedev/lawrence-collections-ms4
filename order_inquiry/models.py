from django.db import models

# Create your models here.


class OrderInquiry(models.Model):
    """ Allow users to contact store for general
    enquiries or about an order
    """
    name = models.CharField(max_length=64, null=False, blank=False)
    contact_email = models.EmailField(null=False, blank=False)
    order_number = models.CharField(max_length=64, null=False, blank=False)
    message = models.TextField(null=False, blank=False)

    def __str__(self):
        return self.name
