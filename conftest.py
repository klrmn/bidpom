#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import py


def pytest_runtest_setup(item):
    pytest_mozwebqa = py.test.config.pluginmanager.getplugin('mozwebqa')
    pytest_mozwebqa.TestSetup.email = item.config.option.email
    pytest_mozwebqa.TestSetup.password = item.config.option.password

    if item.config.option.serverurl:
        pytest_mozwebqa.TestSetup.serverurl = item.config.option.serverurl
    else:
        base_url = item.config.option.base_url # works
        print base_url
        if 'dev' in base_url:
            pytest_mozwebqa.TestSetup.serverurl =  'https://login.dev.anosrep.org'
        elif base_url.count('beta'):  # not tested
            pytest_mozwebqa.TestSetup.serverurl =  'https://login.anosrep.org'
        else:  # works
            pytest_mozwebqa.TestSetup.serverurl =  'https://login.persona.org'
        print pytest_mozwebqa.TestSetup.serverurl


def pytest_addoption(parser):
    group = parser.getgroup('persona', 'persona')
    group._addoption('--email',
                     action='store',
                     metavar='str',
                     help='email address for persona account')
    group._addoption('--password',
                     action='store',
                     metavar='str',
                     help='password for persona account')
    group._addoption('--serverurl',
                     action='store',
                     metavar='url',
                     help='url of secondary identity server')


def pytest_funcarg__mozwebqa(request):
    return request.getfuncargvalue('mozwebqa')
