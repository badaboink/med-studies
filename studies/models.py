from django.db import models

class Referentiel(models.Model):
    title = models.CharField(max_length=255)
    short = models.CharField(max_length=20)

class Item(models.Model):
    title = models.TextField(max_length=500, null=True, blank=True)
    status = models.BooleanField(default=False)

class ItemReferentiel(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="item_referentiels")
    ref = models.ForeignKey(Referentiel, on_delete=models.CASCADE, related_name="item_referentiels")
    status = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["item", "ref"],
                name="unique_item_referentiel",
            )
        ]

class Margot(models.Model):
    text = models.TextField(max_length=500, null=True, blank=True)