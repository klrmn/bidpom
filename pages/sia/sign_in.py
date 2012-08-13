#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from base import Base
from account_manager import AccountManager


class SignIn(Base):

    _email_locator = (By.ID, 'email')
    # https://github.com/mozilla/browserid/issues/2211
    _next_locator = (By.CSS_SELECTOR, 'div.submit.start > button')
    _sign_in_locator = (By.CSS_SELECTOR, 'div.submit.password_entry > button')
    _verify_email_locator =(By.ID, 'verifyEmail')
    _password_locator = (By.ID, 'password')
    _password_verify_locator = (By.ID, 'vpassword')
    _forgot_password_locator = (By.CSS_SELECTOR, 'a.forgot')
    _reset_password_locator = (By.CSS_SELECTOR, '#signUpForm button')
    # it's an li for sign-up or  a div for reset password, so don't specify node type
    _result_notification_title_locator = (By.CSS_SELECTOR, '.notification.emailsent > h2')

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

    def click_forgot_password(self):
        """Clicks the forgot password link."""
        self.selenium.find_element(*self._forgot_password_locator).click()
        WebDriverWait(self.selenium, self.timeout).until(
            lambda s: s.find_element(*self._password_verify_locator).is_displayed(),
            "verify password field did not appear within %s" % self.timeout)

    def click_reset_password(self):
        """Clicks the reset password button."""
        self.selenium.find_element(*self._reset_password_locator).click()
        WebDriverWait(self.selenium, self.timeout).until(
            lambda s: s.find_element(*self._result_notification_title_locator).is_displayed(),
            "verify email action did not produce result")

    @property
    def result_notification_title(self):
        """Get the text of the result notification title."""
        return self.selenium.find_element(*self._result_notification_title_locator).text

    @property 
    def current_ux_location(self):
        '''
        tells you which of the following stages you are in:
        - email (email field and next button visible)
        - signing-up (two password fields and verify email button visible)
        - signing-in (one password field and sign-in button visible)
        - verifying (email has been sent message visible)
        '''
        s = self.selenium
        if s.find_element(*self._email_locator).is_displayed():
            if s.find_element(*self._password_locator).is_displayed():
                if s.find_element(*self._password_verify_locator).is_displayed() and \
                   s.find_element(*self._verify_email_locator).is_displayed():
                    return 'signing-up'
                elif s.find_element(*self._sign_in_locator).is_displayed() and not \
                     s.find_element(*self._password_verify_locator).is_displayed():
                    return 'signing-in'
            elif s.find_element(*self._next_locator).is_displayed():
                return 'email'
        elif s.find_element(*self._result_notification_title_locator).is_displayed():
            return 'verifying'
        raise Exception("current ux location not known")

    def sign_in(self, email, password):
        """
        Helper method sign_in(email, password) signs in with the provided email 
        address and password.
        """
        self.email = email
        self.click_next()
        self.password = password
        self.click_sign_in()
        # should redirect to Account Manager (home, logged in) page
        actmgr = AccountManager(self.selenium, self.timeout)
        return actmgr

    def sign_up(self, email, password):
        """
        Helper method sign_up(email, password) signs up with the provided email 
        address and password.
        """
        self.email = email
        self.click_next()
        self.password = password
        self.verify_password = password
        self.click_verify_email()
        # does not redirect to anywhere

    def forgot_password(self, email, new_password):
        """
        Helper method forgot_password(email, new_password) performs the series of
        actions required to reset the user's password.
        """
        self.click_forgot_password()
        self.password = new_password
        self.verify_password = new_password
        self.click_reset_password()
        # does not redirect to anywhere

