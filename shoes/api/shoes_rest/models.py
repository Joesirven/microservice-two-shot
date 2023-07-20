from django.db import models


# Create your models here.

class BinVO(models.Model):
    closet_name = models.CharField(max_length=100)
    bin_number = models.PositiveSmallIntegerField()
    bin_size = models.PositiveSmallIntegerField()
    import_href = models.CharField(max_length=200, unique=True,)

    def __str__(self):
        return f"{self.closet_name} - {self.bin_number}/{self.bin_size}"


class Shoe(models.Model):
    manufacturer = models.CharField(max_length=200,)
    model_name = models.CharField(max_length=200,)
    color = models.CharField(max_length=50,)
    picture = models.URLField()
    bin = models.ForeignKey(BinVO, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.manufacturer} {self.model_name} - {self.color}"
