from django.test import TestCase
from trollApp.models import Download, Synonym

class DownloadTestCase(TestCase):
    def setUp(self):
        Download.objects.create(target_os="Windows", filename="testFile.exe", description="Test Executable")
        Download.objects.create(target_os="Linux", filename="testFile", description="Test Executable")

    def testGetShortName(self):
        windowsDownload = Download.objects.get(target_os="Windows")
        linuxDownload = Download.objects.get(target_os="Linux")

        self.assertEqual(windowsDownload.getShortName(), "testFile")
        self.assertEqual(linuxDownload.getShortName(), "testFile")

    def testUnicode(self):
        windowsDownload = Download.objects.get(target_os="Windows")
        linuxDownload = Download.objects.get(target_os="Linux")

        self.assertEqual(unicode(windowsDownload), "testFile.exe: Test Executable")
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
