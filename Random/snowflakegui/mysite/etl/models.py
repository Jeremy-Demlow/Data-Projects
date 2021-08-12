from django.db import models


class Functionality(models.Model):
    """Creates three objects which will be used by the website.

    * title: what the functionality is
    * description: short description of the functionality
    * form_path: which form path to grab in the view
    * image: catchy picture :)

    """
    title = models.CharField(max_length=100)
    description = models.TextField()
    form_path = models.CharField(max_length=100, null=True)
    image = models.FilePathField(path="/img")

    def __str__(self):
        return self.title
