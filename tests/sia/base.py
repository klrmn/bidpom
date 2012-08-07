#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re

import requests
from selenium.webdriver.support.ui import WebDriverWait

from ... mocks.user import MockUser
from ... browser_id import BrowserID

class SIABaseTest(object):

    # move this to BrowserID when personatestuser.org comes online
    def create_verified_user(self, selenium, timeout):
        user = MockUser()
        from ... pages.sia.home import HomePage
        home = HomePage(selenium, timeout)
        home.wait_for_page_load(logged_in=False)
        signup = home.click_sign_up()
        signup.sign_up(user.primary_email, user.password)

        # do email verification
        from ... pages.sia.complete_registration import CompleteRegistration
        comp_reg = CompleteRegistration(selenium, timeout, 
            BrowserID(None, None).get_confirm_url_from_email(user.primary_email), 
            expect='success')
        assert 'Thank you' in comp_reg.thank_you
        # go sign out (for some reason clearing the browser doesn't seem to work by itself)
        home.reload_home()
        home.wait_for_page_load(logged_in=True)
        home.sign_out()
        # clear browser and reload page for preconditions
        print "clearing browser"
        selenium.delete_all_cookies()
        selenium.execute_script('localStorage.clear()')
        home.reload_home()
        print selenium.title
        return user
