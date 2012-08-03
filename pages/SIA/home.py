#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from .. base import Base
from sign_in import SignIn

class HomePage(Base):

    _page_title = 'Mozilla Persona: A Better Way to Sign In'
    _page_url = '/'
    _sign_in_locator = (By.CSS_SELECTOR, 'a.signIn')
    _sign_up_locator = (By.CSS_SELECTOR, 'a.button.create')
    _manage_section_locator = (By.ID, 'manage')
    _sign_out_locator = (By.CSS_SELECTOR, 'a.signOut')

    def __init__(self, selenium, timeout, serverurl=None):
        Base.__init__(self, selenium, timeout)
        if serverurl:
            self.selenium.get(serverurl + self._page_url)

    def wait_for_page_load(self, logged_in=False):
        if logged_in:
            # page load takes longer when logged in
            WebDriverWait(self.selenium, self.timeout * 2).until(
                lambda s: s.find_element(*self._sign_out_locator) and \
                s.find_element(*self._sign_out_locator).is_displayed(),
                "the sign out button has not appeared within %s" % self.timeout)
        else:
            WebDriverWait(self.selenium, self.timeout).until(
                lambda s: s.find_element(*self._sign_in_locator) and \
                s.find_element(*self._sign_in_locator).is_displayed(),
                "the sign in button has not appeared within %s" % self.timeout)


    def click_sign_up(self):
        self.selenium.find_element(*self._sign_up_locator).click()
        return SignIn(self.selenium, self.timeout)

    def click_sign_in(self):
        self.selenium.find_element(*self._sign_in_locator).click()
        return SignIn(self.selenium, self.timeout)

    @property
    def is_manage_section_visible(self):
        return self.selenium.find_element(*self._manage_section_locator).is_displayed()

    @property
    def is_logged_in(self):
        return self.selenium.find_element(*self._sign_out_locator).is_displayed()

    @property
    def is_logged_out(self):
        return self.selenium.find_element(*self._sign_in_locator).is_displayed()

    def sign_out(self):
        self.selenium.find_element(*self._sign_out_locator).click()
        self.wait_for_page_load(logged_in=False)
