from django.db import models


class RecipIngredient(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Fridge(models.Model):
    room_number = models.IntegerField(unique=True)

    def __str__(self):
        return f'Холодильник в комнате: {self.room_number}'


class FridgeIngredient(models.Model):
    name = models.CharField(max_length=50)
    expiration_date = models.DateField()
    recip_ingredient = models.OneToOneField(RecipIngredient, on_delete=models.DO_NOTHING)
    fridge = models.ForeignKey(Fridge, on_delete=models.CASCADE, related_name='products')
    quantity = models.DecimalField(max_digits=6, decimal_places=2)
    unit = models.CharField(max_length=50, choices=(('pcs', 'штуки'), ('grams', 'граммы'), ('ml', 'миллилитры')))

    def __str__(self):
        return self.name


class Recip(models.Model):
    name = models.CharField(max_length=64)
    ingredients = models.ManyToManyField(RecipIngredient, related_name='ingredients', blank=True)
    description = models.TextField()

    def __str__(self):
        return self.name


# Create your models here.
