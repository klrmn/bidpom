#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re

import requests
from selenium.webdriver.support.ui import WebDriverWait

import restmail


class BaseTest(object):

    def get_confirm_url_from_email(email_address):
        mail = restmail.get_mail(user.additional_emails[0],
                                 timeout=mozwebqa.timeout)
        return re.search(BrowserID.CONFIRM_URL_REGEX, mail[0]['text']).group(0)
