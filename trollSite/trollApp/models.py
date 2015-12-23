from django.db import models


class Download(models.Model):
    target_os = models.CharField(max_length=200, verbose_name="Target OS")
    filename = models.CharField(max_length=200, verbose_name="Filename")
    description = models.CharField(max_length=200, verbose_name="Description")

    def getFullName(self):
        return self.filename if self.target_os != "Windows" \
            else self.filename + ".exe"

    def __unicode__(self):
        return "{filename}: {descr}".format(
                filename=self.filename, descr=self.description)


class Synonym(models.Model):
    word = models.CharField(max_length=200)
    synonym = models.CharField(max_length=200)

    def __unicode__(self):
        return "Word: {word}, Synonym: {syn}".format(
                word=self.word, syn=self.synonym)


class ConfigOption(models.Model):
    name = models.CharField(max_length=200)
    value = models.CharField(max_length=200)

    def __unicode__(self):
        return "Name: {name}, Value: {val}".format(
                name=self.name, val=self.value)
