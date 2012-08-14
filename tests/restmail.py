#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json
import time
import re
import requests


def get_mail(username, message_count=1, timeout=60):
    username = username.partition('@restmail.net')[0]
    end_time = time.time() + timeout
    while(True):
        response = requests.get(
            'https://restmail.net/mail/%s' % username,
            verify=False)
        restmail = json.loads(response.content)
        if len(restmail) == message_count:
            return restmail
        time.sleep(0.5)
        if(time.time() > end_time):
            break
    raise Exception('Timeout after %(TIMEOUT)s seconds getting restmail for '
                    '%(USERNAME)s. Expected %(EXPECTED_MESSAGE_COUNT)s '
                    'messages but there were %(ACTUAL_MESSAGE_COUNT)s.' % {
                        'TIMEOUT': timeout,
                        'USERNAME': username,
                        'EXPECTED_MESSAGE_COUNT': message_count,
                        'ACTUAL_MESSAGE_COUNT': len(restmail)})

def get_confirm_url_from_email(email, message_count=1, regex='(https?:.*?token=.{48})'):
    '''
    Checks the restmail inbox for the specified address
    and returns the confirm url.
    Specify message_count if you expect there to be more than one message for the user.
    Specify regex if you wish to use a specific regex. By default searches for a url with a 48 char token."
    '''
    mail = get_mail(email, message_count=message_count, timeout=60)
    message_text = mail[message_count - 1]['text']
    return re.search(regex, message_text).group(0)
