from django.test import TestCase
from trollApp.models import ConfigOption, Download, Synonym


class DownloadTestCase(TestCase):
    def setUp(self):
        Download.objects.all().delete()
        Download.objects.create(target_os="Windows",
                                filename="testFile",
                                description="Test Executable")
        Download.objects.create(target_os="Linux",
                                filename="testFile",
                                description="Test Executable")

    def testGetFullName(self):
        windowsDownload = Download.objects.get(target_os="Windows")
        linuxDownload = Download.objects.get(target_os="Linux")

        self.assertEqual(windowsDownload.getFullName(), "testFile.exe")
        self.assertEqual(linuxDownload.getFullName(), "testFile")

    def testUnicode(self):
        windowsDownload = Download.objects.get(target_os="Windows")
        linuxDownload = Download.objects.get(target_os="Linux")

        self.assertEqual(unicode(windowsDownload), "testFile: Test Executable")
        self.assertEqual(unicode(linuxDownload), "testFile: Test Executable")


class SynonymTestCase(TestCase):
    def setUp(self):
        Synonym.objects.create(word="cat", synonym="feline")
        Synonym.objects.create(word="dog", synonym="canine")

    def testUnicode(self):
        catSynonym = Synonym.objects.get(word="cat")
        dogSynonym = Synonym.objects.get(word="dog")

        self.assertEqual(unicode(catSynonym), "Word: cat, Synonym: feline")
        self.assertEqual(unicode(dogSynonym), "Word: dog, Synonym: canine")


class ConfigOptionTestCase(TestCase):
    def setUp(self):
        ConfigOption.objects.all().delete()
        ConfigOption.objects.create(name="maxWordLength", value=5)
        ConfigOption.objects.create(name="minWordLength", value=1)

    def testUnicode(self):
        maxWordLengthConfig = ConfigOption.objects.get(name="maxWordLength")
        minWordLengthConfig = ConfigOption.objects.get(name="minWordLength")

        self.assertEqual(unicode(maxWordLengthConfig),
                         "Name: maxWordLength, Value: 5")
        self.assertEqual(unicode(minWordLengthConfig),
                         "Name: minWordLength, Value: 1")
