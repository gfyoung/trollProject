from django.test import TestCase
from tempfile import NamedTemporaryFile
from trollApp.models import ConfigOption, Synonym
from trollApp.views import getBestSynonym, getSynonym

class BasicUrlAccessTestCase(TestCase):
    def setUp(self):
        trollRedirectProb = ConfigOption.objects.filter(name="trollRedirectProb")[0]
        trollRedirectProb.value = 0
        trollRedirectProb.save()

    def testGetBackSlash(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)

    def testGetBackSlashTrollApp(self):
        response = self.client.get("/trollApp/")
        self.assertEqual(response.status_code, 302)

    def testGetBackSlashTrollAppHome(self):
        response = self.client.get("/trollApp/home")
        self.assertEqual(response.status_code, 200)

    def testGetBackSlashTrollAppAbout(self):
        response = self.client.get("/trollApp/about")
        self.assertEqual(response.status_code, 200)

    def testGetBackSlashTrollAppDisplayDownloads(self):
        response = self.client.get("/trollApp/downloads")
        self.assertEqual(response.status_code, 200)

    def testGetBackSlashTrollAppDownloadFile(self):
        with NamedTemporaryFile(prefix="testFile", suffix=".exe",
                                dir="trollApp/trollCode/downloads/Windows") as testDownload:
            shortName = testDownload.name.split("/")[-1]

            response = self.client.get("/trollApp/downloads/Windows/" + shortName)
            self.assertEqual(response.status_code, 200)

    def testGetBackSlashTrollAppCustomCreation(self):
        response = self.client.get("/trollApp/customCreation")
        self.assertEqual(response.status_code, 200)

    def testPostBackSlashTrollAppCustomCreationDownload(self):
        response = self.client.post("/trollApp/customCreation/download",
                                    {"code": "print 'Hello World!'", "OS": "Windows"})
        self.assertEqual(response.status_code, 302)

    def testGetBackSlashTrollAppSuggestions(self):
        response = self.client.get("/trollApp/suggestions")
        self.assertEqual(response.status_code, 200)

    def testGetBackSlashTrollAppSendSuggestions(self):
        response = self.client.post("/trollApp/sendSuggestion", {"suggestion": "This is awesome!"})
        self.assertEqual(response.status_code, 302)

    def testGetBackSlashTrollAppTrollifyEmail(self):
        response = self.client.get("/trollApp/trollifyEmail")
        self.assertEqual(response.status_code, 200)

    def testPostBackSlashTrollAppTrollifyEmailCreate(self):
        response = self.client.post("/trollApp/trollifyEmail/create", {"origEmail": "This is awesome!"})
        self.assertEqual(response.status_code, 302)

    def testPostBackSlashTrollAppSendSuggestions(self):
        response = self.client.post("/trollApp/trollifyEmail/send",
                                    {"subject": "Awesomeness", "sender": "somebody@nowhere.com",
                                     "receiver": "nobody@somewhere.com", "trollEmail": "This is awesome!"})
        self.assertEqual(response.status_code, 302)

    def testgetBackSlashTrollAppPlayTrollSong(self):
        response = self.client.get("/trollApp/playTrollSong")
        self.assertEqual(response.status_code, 200)

class GetBestSynonymTestCase(TestCase):
    def testGetBestSynonymNoWord(self):
        bestSynonym = getBestSynonym("")
        self.assertEqual(bestSynonym, "")

    def testGetBestSynonymWithWord(self):
        bestSynonym = getBestSynonym("dog")
        self.assertEqual(bestSynonym, "Canis_familiaris")

    def testGetBestSynonymWithShorterCur(self):
        bestSynonym = getBestSynonym("dog", curSyn="andiron")
        self.assertEqual(bestSynonym, "Canis_familiaris")

    def testGetBestSynonymWithLongerCur(self):
        bestSynonym = getBestSynonym("dog", curSyn="Canis_familiaris_maximus")
        self.assertEqual(bestSynonym, "Canis_familiaris_maximus")

    def testGetBestSynonymNoSynonymsNoCur(self):
        bestSynonym = getBestSynonym("trollify")
        self.assertEqual(bestSynonym, "trollify")

    def testGetBestSynonymNoSynonymsWithCur(self):
        bestSynonym = getBestSynonym("trollify", curSyn="screwify")
        self.assertEqual(bestSynonym, "screwify")

class GetSynonymTestCase(TestCase):
    def setUp(self):
        updateFrequency = ConfigOption.objects.filter(name="updateFrequency")[0]
        updateFrequency.value = 0
        updateFrequency.save()

    def testGetSynonymNoWord(self):
        synonym = getSynonym("")
        self.assertEqual(synonym, "")

    def testGetSynonymWithWordNoCur(self):
        synonym = getSynonym("dog")
        self.assertEqual(synonym, "Canis_familiaris")

    def testGetSynonymWithWordWithCur(self):
        Synonym.objects.create(word="dog", synonym="andiron")
        synonym = getSynonym("dog")
        self.assertEqual(synonym, "andiron")
