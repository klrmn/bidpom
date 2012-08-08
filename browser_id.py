#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import requests
import re

from tests import restmail


class BrowserID(object):

    VERIFY_URL_REGEX = 'https?:\/\/(\S+)\/verify_email_address\?token=(.{48})'
    CONFIRM_URL_REGEX = 'https?:\/\/(\S+)\/confirm\?token=(.{48})'
    RESET_URL_REGEX = 'https?:\/\/(\S+)\/reset_password\?token=(.{48})'
    INCLUDE_URL_REGEX = '(https?:\/\/(\S+))\/include\.js'
    TOKEN_URL_REGEX = '(https?:.*?token=.{48})'

    def __init__(self, selenium, timeout=60):
        self.selenium = selenium
        self.timeout = timeout

    def sign_in(self, email, password):
        """Signs in using the specified email address and password."""
        from pages.rp.sign_in import SignIn
        sign_in = SignIn(self.selenium, timeout=self.timeout, expect='new')
        sign_in.sign_in(email, password)

    # helper functions not requiring selenium

    def persona_server_url(self, base_url):
        '''
        Returns persona server url based on base_url
        May be called like "BrowserID(None, None).persona_server_url('http://123done.org')"
        '''
        response = requests.get('%s/' % base_url, verify=False)
        match = re.search(self.INCLUDE_URL_REGEX, response.content)
        if match:
            return match.group(1)
        else:
            raise Exception('Unable to determine BrowserID URL from %s.' % base_url)

    def get_confirm_url_from_email(self, email, message_count=1):
        '''
        Checks the restmail inbox for the specified address
        and returns the confirm url.
        Specify message_count if you expect there to be more than one message for the user.
        May be called like "BrowserID(None, None).get_confirm_url_from_email('george@restmail.com')"
        '''
        mail = restmail.get_mail(email, message_count=message_count, timeout=60)
        message_text = mail[message_count - 1]['text']
        return re.search(self.TOKEN_URL_REGEX, message_text).group(0)