#!/u/bin/env python

import os
import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from django.test import TestCase, LiveServerTestCase
#from testing import StaticLiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.management import call_command, CommandError

from django.contrib.auth.models import User

# from books.epub import Epub
from books.models import Author

#BASE = "http://localhost:8000"

class PathagarBook(StaticLiveServerTestCase): #LiveServerTestCase):
    ADMIN_USER = 'admin'
    ADMIN_PASS = 'pass'

    AUTHOR = "Anonymous"

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(2)

        self.adminuser = User.objects.create_user(self.ADMIN_USER, 'admin@test.com', self.ADMIN_PASS)
        self.adminuser.save()
        self.adminuser.is_staff = True
        self.adminuser.save()

        anonymous = Author(a_author=self.AUTHOR)
        anonymous.save()

    """
    def test_01_check_protected_url(self):

    def test_02_

    def test_03_

    def test_04_invalid_login(self):
    """

    def test_05_login(self):
        drv = self.driver
        drv.get(self.live_server_url)

        url = drv.current_url

        self.assertIn("Welcome to the Pathagar", drv.title)
        elem = drv.find_elements_by_xpath("//*[contains(text(), 'Log In')]")[0]
        elem.send_keys(Keys.RETURN)

        elem = drv.find_element_by_id("id_username")
        elem.send_keys(self.ADMIN_USER)
        elem = drv.find_element_by_id("id_password")
        elem.send_keys(self.ADMIN_PASS)
        elem.send_keys(Keys.RETURN)

        time.sleep(1)

        self.assertEqual(url, drv.current_url)

        # time.sleep(1)

        elem = drv.find_elements_by_xpath("//*[contains(text(), 'Add Book')]")[0]
        elem.send_keys(Keys.RETURN)

        # it assume that Author anonymous exist

        # time.sleep(1)

        fullpath = os.path.abspath("./examples/The Dunwich Horror.epub")
        self.assertTrue(os.path.isfile(fullpath))

        elem = drv.find_element_by_id("id_book_file")
        elem.send_keys(fullpath)

        elem = drv.find_element_by_id("id_a_title")
        elem.send_keys("The Dunwich Horror")

        elem = drv.find_element_by_id("id_a_author")
        elem.send_keys(self.AUTHOR)

        elem = drv.find_element_by_id("id_tags")
        elem.send_keys("selenium")

        elem = drv.find_element_by_id("id_a_summary")
        elem.send_keys("A little summary")

        elem = drv.find_element_by_xpath("//input[@value='Add']")
        elem.send_keys(Keys.RETURN)

        # XXX Check value

    def tearDown(self):
        self.driver.close()
