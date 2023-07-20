from django.db import models


class LocationVO(models.Model):
    closet_name = models.CharField(max_length=100)
    section_number = models.PositiveSmallIntegerField()
    shelf_number = models.PositiveSmallIntegerField()
    import_href = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.closet_name} - {self.section_number}/{self.shelf_number}"

class Hat(models.Model):
    fabric = models.CharField(max_length=100)
    style = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    picture_url = models.URLField()
    wardrobe_location = models.ForeignKey(
        LocationVO,
        related_name="hat",
        on_delete=models.CASCADE
        )

    def __str__(self):
        return f"{self.color} {self.fabric} {self.style}"
