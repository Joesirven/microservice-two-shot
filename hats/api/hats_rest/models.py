from django.db import models


class BinVO(models.Model):
    closet_name = models.CharField(max_length=100)
    bin_number = models.PositiveSmallIntegerField()
    bin_size = models.PositiveSmallIntegerField()
    import_href = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.closet_name} - {self.bin_number}/{self.bin_size}"

class Hat(models.Model):
    fabric = models.CharField(max_length=100)
    style = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    picture_url = models.URLField()
    wardrobe_location = models.CharField(max_length=100)
    bin = models.ForeignKey(BinVO, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.color} {self.fabric} {self.style}"
