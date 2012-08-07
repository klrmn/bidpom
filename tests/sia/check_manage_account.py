#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from unittestzero import Assert

from ... browser_id import BrowserID
from ... pages.sia.home import HomePage
from ... pages.sia.complete_registration import CompleteRegistration
from ... mocks.user import MockUser

from base import SIABaseTest


class TestManageAccount(SIABaseTest):

    @pytest.mark.moztrap(272)
    def test_can_create_new_user_account(self, mozwebqa):
        user = MockUser()
        home = HomePage(mozwebqa.selenium, mozwebqa.timeout)

        # sign up
        signup = home.click_sign_up()
        signup.sign_up(user.primary_email, user.password)
        Assert.equal(signup.result_notification_title, 'Confirm your email address')

        # do email verification
        comp_reg = CompleteRegistration(mozwebqa.selenium, mozwebqa.timeout, 
            BrowserID(None, None).get_confirm_url_from_email(user.primary_email), 
            expect='success')

        # verify now logged in
        account_manager = home.reload_original_url()
        Assert.true(account_manager.signed_in)

    @pytest.mark.moztrap(273)
    @pytest.mark.nondestructive
    def test_that_user_can_sign_in_and_out(self, mozwebqa):
        # the dev server is being continually wiped, verified user must be fresh
        user = self.create_verified_user(mozwebqa.selenium, mozwebqa.timeout)
        home = HomePage(mozwebqa.selenium, mozwebqa.timeout)

        # sign in
        signin = home.click_sign_in()
        account_manager = signin.sign_in(user.primary_email, user.password)
        Assert.true(account_manager.signed_in)

        # sign out
        home = account_manager.sign_out()
        Assert.false(home.signed_in)

    @pytest.mark.moztrap(274)
    @pytest.mark.destructive
    def test_that_user_can_change_password(self, mozwebqa):
        user = self.create_verified_user(mozwebqa.selenium, mozwebqa.timeout)

        # sign in with old password
        home = HomePage(mozwebqa.selenium, mozwebqa.timeout)
        signin = home.click_sign_in()
        account_manager = signin.sign_in(user.primary_email, user.password)
        assert user.primary_email in account_manager.emails

        # change password
        old_password = user.password
        user.password += '_new'
        account_manager.change_password(old_password, user.password)

        # sign out
        home = account_manager.sign_out()

        # sign in with new password
        signin = home.click_sign_in()
        account_manager = signin.sign_in(user.primary_email, user.password)
        Assert.true(account_manager.signed_in)
        assert user.primary_email in account_manager.emails

    @pytest.mark.moztrap(275)
    @pytest.mark.destructive
    def test_that_user_can_cancel_account_with_one_email(self, mozwebqa):
        user = self.create_verified_user(mozwebqa.selenium, mozwebqa.timeout)

        # sign in
        home = HomePage(mozwebqa.selenium, mozwebqa.timeout)
        signin = home.click_sign_in()
        account_manager = signin.sign_in(user.primary_email, user.password)

        # cancel account
        home = account_manager.cancel_account()

        # verify email not recognized
        signin = home.click_sign_in()
        signin.email = user.primary_email
        signin.click_next()
        Assert.equal(signin.current_ux_location, 'signing-up')


    @pytest.mark.destructive
    def test_that_user_can_reset_password(self, mozwebqa):
        pytest.skip("not implemented yet")
