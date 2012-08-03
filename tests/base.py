#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re

import requests
from selenium.webdriver.support.ui import WebDriverWait

import restmail
from .. browser_id import BrowserID


class BaseTest(object):

    def get_confirm_url_from_email(self, email_address, timeout):
        mail = restmail.get_mail(email_address, timeout=timeout)
        mail_text = mail[0]['text']
        return re.search(BrowserID.EMAILED_URL_REGEX, mail_text).group(0)
