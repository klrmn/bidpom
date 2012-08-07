#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

class Base(object):

    _body_locator = (By.TAG_NAME, 'body')

    def __init__(self, selenium, timeout=60):
        self.selenium = selenium
        self.timeout = timeout

        self._original_page_url = self.selenium.current_url

    @property
    def signed_in(self):
        return 'not_authenticated' not in self.selenium.find_element(*self._body_locator).get_attribute('class')

    def reload_original_url(self):
        '''
        The original url for this page is saved upon instanciation of the page.
        This method loads the page, waits for ajax to finish, and determines which 
        page object to return, HomePage, AccountManager, or (rarely) SignIn.
        '''
        
        self.selenium.get(self._original_page_url)
        self.wait_for_ajax()
        WebDriverWait(self.selenium, self.timeout).until(
            lambda s: s.find_element(*self._body_locator))

        if 'signin' in self.selenium.current_url:
            # this shouldn't happen, but just in case
            # must be first because not signed in would be true
            from sign_in import SignIn
            return SignIn(self.selenium, self.timeout)
        elif self.signed_in:
            from account_manager import AccountManager
            return AccountManager(self.selenium, self.timeout)
        elif not self.signed_in:
            from home import HomePage
            return HomePage(self.selenium, self.timeout)
        else:
            raise Exception('unexpected situation encountered')

    def wait_for_ajax(self):
        WebDriverWait(self.selenium, self.timeout).until(
            lambda s: s.execute_script("return jQuery.active == 0"),
            "Wait for AJAX timed out after %s seconds" % self.timeout)
        
