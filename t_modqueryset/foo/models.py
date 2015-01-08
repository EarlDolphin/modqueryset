from django.db import models

class Foo(models.Model):
  attr1 = models.TextField()
  attr2 = models.PositiveIntegerField()
  attr3 = models.FloatField()
