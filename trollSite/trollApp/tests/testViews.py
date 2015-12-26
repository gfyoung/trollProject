from django.test import TestCase
from trollApp.models import ConfigOption, Synonym
from trollApp.views import getBestSynonym, \
    getMissingImports, getSynonym, moduleExists

import unittest


class BasicUrlAccessTestCase(TestCase):
    missingDataMsg = "Expected data not found"

    def setUp(self):
        trollRedirectProb = ConfigOption.objects.filter(
            name="trollRedirectProb")[0]
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
        data = "Greetings, Fellow Troll!"

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data in response.content.decode('utf-8'),
                        msg=self.missingDataMsg)

    def testGetBackSlashTrollAppAbout(self):
        response = self.client.get("/trollApp/about")
        data = "May the troll be with you!"

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data in response.content.decode('utf-8'),
                        msg=self.missingDataMsg)

    def testGetBackSlashTrollAppDisplayDownloads(self):
        response = self.client.get("/trollApp/downloads")
        data = "Example Troll Files"

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data in response.content.decode('utf-8'),
                        msg=self.missingDataMsg)

    def testGetBackSlashTrollAppDownloadFile(self):
        # Could also create a temporary file, but
        # test runs into issues when that method
        # of testing is executed
        #
        # The downside of writing the test this
        # way is that it creates a dependency on
        # 'displaySuccessCall.exe' being in the
        # codebase. If it is ever removed, or if
        # the name is modified, this test will
        # also have to be modified to account
        # for the file change
        response = self.client.get(
            "/trollApp/downloads/Windows/displaySuccessCall.exe")
        self.assertEqual(response.status_code, 200)

    def testGetBackSlashTrollAppCustomCreation(self):
        response = self.client.get("/trollApp/customCreation")
        data = "Create Your Own Troll File!"

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data in response.content.decode('utf-8'),
                        msg=self.missingDataMsg)

    @unittest.skip("annoying to run")
    def testPostBackSlashTrollAppCustomCreationDownload(self):
        response = self.client.post("/trollApp/customCreation/download",
                                    {"code": "print 'Hello World!'",
                                     "OS": "Windows"})
        self.assertEqual(response.status_code, 302)

    def testGetBackSlashTrollAppSuggestions(self):
        response = self.client.get("/trollApp/suggestions")
        data = ("Send us your suggestions for new trolls "
                "and improvements to the website!")

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data in response.content.decode('utf-8'),
                        msg=self.missingDataMsg)

    def testGetBackSlashTrollAppSendSuggestions(self):
        response = self.client.post("/trollApp/sendSuggestion",
                                    {"suggestion": "This is awesome!"})
        self.assertEqual(response.status_code, 302)

    def testGetBackSlashTrollAppTrollifyEmail(self):
        response = self.client.get("/trollApp/trollifyEmail")
        data = ("Classic Troll: Make your messages "
                "deliberately confusing!")

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data in response.content.decode('utf-8'),
                        msg=self.missingDataMsg)

    def testPostBackSlashTrollAppTrollifyEmailCreate(self):
        response = self.client.post("/trollApp/trollifyEmail/create",
                                    {"origEmail": "This is awesome!"})
        self.assertEqual(response.status_code, 302)

    def testPostBackSlashTrollAppSendSuggestions(self):
        response = self.client.post("/trollApp/trollifyEmail/send",
                                    {"subject": "Awesomeness",
                                     "sender": "somebody@nowhere.com",
                                     "receiver": "nobody@somewhere.com",
                                     "trollEmail": "This is awesome!"})
        self.assertEqual(response.status_code, 302)

    @unittest.skip("annoying to run")
    def testGetBackSlashTrollAppPlayTrollSong(self):
        response = self.client.get("/trollApp/playTrollSong")
        self.assertEqual(response.status_code, 200)

    def testGetBackSlashTrollAppTrollGames(self):
        response = self.client.get("/trollApp/trollGames")
        data = "Welcome to the Troll Games!"

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data in response.content.decode('utf-8'),
                        msg=self.missingDataMsg)

    def testGetBackSlashTrollAppTrollSpeedTyping(self):
        response = self.client.get("/trollApp/trollGames/trollSpeedTyping")
        self.assertEqual(response.status_code, 200)

    def testGetBackSlashTrollAppTrollAlienInvasion(self):
        response = self.client.get("/trollApp/trollGames/trollAlienInvasion")
        self.assertEqual(response.status_code, 200)

    def testGetBackSlashTrollAppTrollSimulate(self):
        response = self.client.get("/trollApp/trollGames/trollSimulate")
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
        updateFrequency = ConfigOption.objects.filter(
            name="updateFrequency")[0]
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


class ModuleExistsTest(TestCase):
    def testModuleExistsNonexistentModule(self):
        moduleName = "nonExistentModule"
        self.assertEqual(moduleExists(moduleName), False)

    def testModuleExistsExistentModule(self):
        moduleName = "django"
        self.assertEqual(moduleExists(moduleName), True)


class GetMissingModulesTest(TestCase):
    # Python 3 Compatibility
    try:
        TestCase.assertItemsEqual
    except AttributeError:
        assertItemsEqual = TestCase.assertCountEqual

    def testGetMissingModulesDirectExistingSingle(self):
        importStatement = "import math"
        self.assertEqual(len(getMissingImports(importStatement)), 0)

    def testGetMissingModulesDirectExistingMultiple(self):
        importStatement = "import math, os"
        self.assertEqual(len(getMissingImports(importStatement)), 0)

    def testGetMissingModulesDirectExistingFunnySpacing(self):
        importStatement = "import math,os,      sys"
        self.assertEqual(len(getMissingImports(importStatement)), 0)

    def testGetMissingModulesDirectExistingWithDot(self):
        importStatement = "import django.test"
        self.assertEqual(len(getMissingImports(importStatement)), 0)

    def testGetMissingModulesDirectNonExistent(self):
        importStatement = "import math, pilo"
        missingImports = getMissingImports(importStatement)
        self.assertEqual(len(missingImports), 1)
        self.assertItemsEqual(["pilo"], missingImports)

    def testGetMissingModulesDirectMulitpleNonExistent(self):
        importStatement = "import math, pilo, silo"
        missingImports = getMissingImports(importStatement)
        self.assertEqual(len(missingImports), 2)
        self.assertItemsEqual(["pilo", "silo"], missingImports)

    def testGetMissingModulesDirectNonExistentFunnySpacing(self):
        importStatement = "import math       ,pilo"
        missingImports = getMissingImports(importStatement)
        self.assertEqual(len(missingImports), 1)
        self.assertItemsEqual(["pilo"], missingImports)

    def testGetMissingModulesFromExisting(self):
        importStatement = "from math import pi"
        self.assertEqual(len(getMissingImports(importStatement)), 0)

    def testGetMissingModulesFromExistingFunnySpacing(self):
        importStatement = "from  math    import      pi"
        self.assertEqual(len(getMissingImports(importStatement)), 0)

    def testGetMissingModulesFromExistingWithDot(self):
        importStatement = "from django.test import testcases"
        self.assertEqual(len(getMissingImports(importStatement)), 0)

    def testGetMissingModulesFromNonExistent(self):
        importStatement = "from pilo import silo"
        missingImports = getMissingImports(importStatement)
        self.assertEqual(len(missingImports), 1)
        self.assertItemsEqual(["pilo"], missingImports)

    def testGetMissingModulesFromMultipleNonExistent(self):
        importStatement = "from pilo import silo, zilo\nfrom nilo import tilo"
        missingImports = getMissingImports(importStatement)
        self.assertEqual(len(missingImports), 2)
        self.assertItemsEqual(["pilo", "nilo"], missingImports)

    def testGetMissingModulesFromDirectCombo(self):
        importStatement = "from math import pi\nimport re"
        self.assertEqual(len(getMissingImports(importStatement)), 0)

    def testGetMissingModulesFromDirectComboFunnySpacing(self):
        importStatement = "from  math import  pi\n  import     re"
        self.assertEqual(len(getMissingImports(importStatement)), 0)

    def testGetMissingModulesFromDirectComboNonExistent(self):
        importStatement = "from pilo import zilo\nimport tilo"
        missingImports = getMissingImports(importStatement)
        self.assertEqual(len(missingImports), 2)
        self.assertItemsEqual(["pilo", "tilo"], missingImports)

    def testGetMissingModulesFromDirectComboNonExistentWithDot(self):
        importStatement = "from pilo.silo import zilo\nimport tilo"
        missingImports = getMissingImports(importStatement)
        self.assertEqual(len(missingImports), 2)
        self.assertItemsEqual(["pilo", "tilo"], missingImports)
