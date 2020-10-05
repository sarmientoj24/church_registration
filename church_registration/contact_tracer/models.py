from django.db import models
from django.utils.timezone import now


class Person(models.Model):
    name = models.CharField(max_length=100, null=False)
    temp = models.FloatField(null=False)
    contact = models.CharField(max_length=11, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateTimeField(default=now, editable=True, blank=True)
    # Blank is different than null. null is purely database-related, 
    # whereas blank is validation-related(required in form). If null=True , 
    # Django will store empty values as NULL in the database . 
    # If a field has blank=True , form validation will allow entry of an empty value .

    def __str__(self):
        return self.name
