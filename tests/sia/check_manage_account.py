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
        home.wait_for_page_load(logged_in=False)

        # sign up
        signup = home.click_sign_up()
        signup.sign_up(user.primary_email, user.password)
        Assert.equal(signup.result_notification_title, 'Confirm your email address')

        # do email verification
        comp_reg = CompleteRegistration(mozwebqa.selenium, mozwebqa.timeout, 
            BrowserID(None, None).get_confirm_url_from_email(user.primary_email), 
            expect='success')

        # verify now logged in
        mozwebqa.selenium.get(BrowserID(None, None).persona_server_url(mozwebqa.base_url))
        home_pg = HomePage(mozwebqa.selenium, mozwebqa.timeout)
        home_pg.wait_for_page_load(logged_in=True)
        Assert.true(home_pg.is_logged_in)
        Assert.true(home_pg.is_manage_section_visible)

    @pytest.mark.moztrap(273)
    @pytest.mark.nondestructive
    def test_that_user_can_sign_in_and_out(self, mozwebqa):
        # the dev server is being continually wiped, verified user must be fresh
        user = self.create_verified_user(mozwebqa.selenium, mozwebqa.timeout)
        home = HomePage(mozwebqa.selenium, mozwebqa.timeout)
        home.wait_for_page_load(logged_in=False)

        # sign in
        signin = home.click_sign_in()
        home = signin.sign_in(user.primary_email, user.password)
        Assert.true(home.is_logged_in)

        # sign out
        home.sign_out()
        Assert.true(home.is_logged_out)

    @pytest.mark.moztrap(274)
    @pytest.mark.destructive
    def test_that_user_can_change_password(self, mozwebqa):
        pytest.skip("not implemented yet")

    @pytest.mark.moztrap(275)
    @pytest.mark.destructive
    def test_that_user_can_cancel_account(self, mozwebqa):
        pytest.skip("not implemented yet")
