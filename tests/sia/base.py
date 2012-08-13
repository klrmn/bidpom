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

        # create the user
        from ... pages.sia.home import HomePage
        home = HomePage(selenium, timeout)
        signup = home.click_sign_up()
        signup.sign_up(user.primary_email, user.password)

        # do email verification
        from ... pages.sia.complete_registration import CompleteRegistration
        complete_registration = CompleteRegistration(selenium, timeout, 
            BrowserID(None, None).get_confirm_url_from_email(user.primary_email), 
            expect='success')
        assert 'Thank you' in complete_registration.thank_you

        # go sign out and reload page for preconditions
        account_manager = home.reload_original_url()
        account_manager.sign_out()
        home.reload_original_url()  # test will instantiate HomePage

        return user
