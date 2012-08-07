#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import requests
import re

from selenium.webdriver.support.ui import WebDriverWait

from ... browser_id import BrowserID

def pytest_runtest_setup(item):
    item.config.option.api = 'webdriver'


def pytest_funcarg__mozwebqa(request):
    mozwebqa = request.getfuncargvalue('mozwebqa')
    mozwebqa.selenium.get('%s/' % 
        BrowserID(None, None).persona_server_url(mozwebqa.base_url))
    return mozwebqa
