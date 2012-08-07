#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from base import Base


class SignIn(Base):

    _email_locator = (By.ID, 'email')
    # https://github.com/mozilla/browserid/issues/2211
    _next_locator = (By.CSS_SELECTOR, 'div.submit.start > button')
    _sign_in_locator = (By.CSS_SELECTOR, 'div.submit.password_entry > button')
    _verify_email_locator =(By.ID, 'verifyEmail')
    _password_locator = (By.ID, 'password')
    _password_verify_locator = (By.ID, 'vpassword')
    _result_notification_title_locator = (By.CSS_SELECTOR, 'li.notification.emailsent > h2')

    def __init__(self, selenium, timeout=60):
        Base.__init__(self, selenium, timeout)

        WebDriverWait(self.selenium, self.timeout).until(
            lambda s: s.find_element(*self._email_locator) and \
            s.find_element(*self._email_locator).is_displayed(),
            "email field did not appear within %s" % self.timeout)

    @property
    def email(self):
        """Get the value of the email field."""
        return self.selenium.find_element(*self._email_locator).text

    @email.setter
    def email(self, value):
        """Set the value of the email field."""
        field = self.selenium.find_element(*self._email_locator)
        field.clear()
        field.send_keys(value)

    def click_next(self):
        """This is the operative button after filling in email."""
        WebDriverWait(self.selenium, self.timeout).until(
            lambda s: s.find_element(*self._next_locator) and \
            s.find_element(*self._next_locator).is_displayed(),
            "next button is not found / not visible")
        self.selenium.find_element(*self._next_locator).click()
        WebDriverWait(self.selenium, self.timeout).until(
            lambda s: s.find_element(*self._password_locator).is_displayed(),
            "Password field did not appear within %s" % self.timeout
        )

    def click_sign_in(self):
        """This is the operative button after filling in password in sign-in."""
        WebDriverWait(self.selenium, self.timeout).until(
            lambda s: s.find_element(*self._sign_in_locator) and \
            s.find_element(*self._sign_in_locator).is_displayed(),
            "sign in button not found / not visible")
        self.selenium.find_element(*self._sign_in_locator).click()

    def click_verify_email(self):
        """This is the operative button after filling in password and verify in sign-up."""
        WebDriverWait(self.selenium, self.timeout).until(
            lambda s: s.find_element(*self._verify_email_locator) and \
            s.find_element(*self._verify_email_locator).is_displayed(),
            "verify email button not found / not visible")
        self.selenium.find_element(*self._verify_email_locator).click()
        WebDriverWait(self.selenium, self.timeout).until(
            lambda s: s.find_element(*self._result_notification_title_locator).is_displayed(),
            "verify email action did not produce result")

    @property 
    def password(self):
        """Get the value of the password field."""
        return self.selenium.find_element(*self._password_locator).text

    @password.setter
    def password(self, value):
        """Sets the value of the password field."""
        field = self.selenium.find_element(*self._password_locator)
        field.clear()
        field.send_keys(value)

    @property
    def verify_password(self):
        """Get the value of the verify password field."""
        return self.selenium.find_element(*self._password_verify_locator).text

    @verify_password.setter
    def verify_password(self, value):
        """Set the value of the verify password field."""
        field = self.selenium.find_element(*self._password_verify_locator)
        field.clear()
        field.send_keys(value)

    @property
    def result_notification_title(self):
        """Get the text of the result notification title."""
        return self.selenium.find_element(*self._result_notification_title_locator).text

    def sign_in(self, email, password):
        """Signs in with the provided email address and password."""
        self.email = email
        self.click_next()
        self.password = password
        self.click_sign_in()
        # should redirect to home page
        from home import HomePage  # circular reference
        home = HomePage(self.selenium, self.timeout)
        home.wait_for_page_load(logged_in=True)
        return home

    def sign_up(self, email, password):
        """Signs up with the provided email address and password."""
        self.email = email
        self.click_next()
        self.password = password
        self.verify_password = password
        self.click_verify_email()
        # does not redirect to anywhere
