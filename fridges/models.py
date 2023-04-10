from django.db import models

from users.models import CustomUser


class RecipIngredient(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class FridgeIngredient(models.Model):
    name = models.CharField(max_length=50)
    expiration_date = models.DateField()
    recip_ingredient = models.ForeignKey(RecipIngredient, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='products')
    quantity = models.DecimalField(max_digits=6, decimal_places=2)
    unit = models.CharField(max_length=50, choices=(('штук', 'штук'), ('грамм', 'грамм'), ('миллилитров', 'миллилитров')))

    def __str__(self):
        return self.name


class Recip(models.Model):
    name = models.CharField(max_length=64)
    ingredients = models.ManyToManyField(RecipIngredient, related_name='ingredients', blank=True)
    description = models.TextField()

    def __str__(self):
        return self.name

    def get_name_of_ingredients(self):
        res = []
        for i in self.ingredients.all():
            res.append(i.name)
        return res
