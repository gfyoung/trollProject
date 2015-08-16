from django.db import models

class Download(models.Model):
    target_os = models.CharField(max_length=200)
    filename = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    
    def getShortName(self):
        return self.filename.replace(".exe", "")

    def __unicode__(self):
        return "{}: {}".format(self.filename, self.description)

class Synonym(models.Model):
    word = models.CharField(max_length=200)
    synonym = models.CharField(max_length=200)

    def __unicode__(self):
        return "Word: {}, Synonym: {}".format(self.word, self.synonym)

class ConfigOption(models.Model):
    name = models.CharField(max_length=200)
    value = models.CharField(max_length=200)

    def __unicode__(self):
        return "Name: {}, Value: {}".format(self.name, self.value)
