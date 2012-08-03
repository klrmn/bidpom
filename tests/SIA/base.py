#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re

import requests
from selenium.webdriver.support.ui import WebDriverWait

from ... mocks.user import MockUser
from .. base import BaseTest


class SIABaseTest(BaseTest):

    def create_verified_user(self, selenium, timeout, serverurl):
        user = MockUser()
        from ... pages.SIA.home import HomePage
        home = HomePage(selenium, timeout, serverurl)
        home.wait_for_page_load(logged_in=False)
        signup = home.click_sign_up()
        signup.sign_up(user.primary_email, user.password)

        # do email verification
        from ... pages.SIA.complete_registration import CompleteRegistration
        comp_reg = CompleteRegistration(selenium, timeout, 
            self.get_confirm_url_from_email(user.primary_email, timeout), 
            expect='success')
        assert 'Thank you' in comp_reg.thank_you
        # test precondition assumes signed out
        home = HomePage(selenium, timeout, serverurl)
        home.wait_for_page_load(logged_in=True)
        home.sign_out()
        return user
