from django.db import models

class Download(models.Model):
    target_os = models.CharField(max_length=200)
    filename = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    
    def getShortName(self):
        return self.filename.replace(".exe", "")

    def __unicode__(self):
        return "{}: {}".format(self.filename, self.description)
