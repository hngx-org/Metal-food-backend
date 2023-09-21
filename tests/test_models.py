"""
test_models.py - Unit tests for the models in the Django application.

This module contains a suite of unit tests that verify the behavior of the models
defined in the Django application. Each test case is designed to check specific aspects
of the model's functionality, such as field validation, methods, and relationships.

Test cases in this module include:
    - TestModelTestCase: Tests for the TestModel class.
    - AnotherModelTestCase: Tests for the AnotherModel class.

Dependencies:
    - Django: This module assumes that Django is properly installed and configured in
      the project environment.

Usage:
    - Run the tests using a Django test runner. For example, using the command:
      `python manage.py test myapp.tests.test_model`

Author: Brian Obot
Copyright 2023 Brian Obot
"""

import pytest

from transaction.models import (
    LunchWallet,
    LunchTransaction,
    Transaction,
    BankAccount,
    Wallet,
    Organization,
    Lunch,
    Withdrawals
)
from users.models import User, Staff, Organization

"""
In order to avoid initial conflicts with my fellow teammate i have placed these fixtures
within the test_module script, when the merge is complete, this would be moved into a dedicated
conftest.py module
"""
@pytest.fixture
def user() -> User:
    return User.objects.create(email="brianobot9@gmail.com", password="testpassword")


@pytest.fixture
def organization() -> Organization:
    return Organization.objects.create(
        name="Test Organization",
        email="testorg@org.com",
        role="Humanitarian",
    )


@pytest.fixture
def lunch_wallet(staff) -> LunchWallet:
    return LunchWallet.objects.create(
        staff=staff,
        balance=100.0,
    )


@pytest.fixture
def lunch_transaction(staff, org) -> LunchTransaction:
    return LunchTransaction.objects.create(
        staff=staff,
        organization=org,
        type="some test type",
    )


@pytest.fixture
def transaction() -> Transaction:
    sender = Staff.objects.create()
    receiver = Staff.objects.create()
    return Transaction.objects.create(
        sender=sender,
        receiver=receiver,
        currency="NGN",
        status="PENDING",
    )


@pytest.fixture
def bank_account(user) -> BankAccount:
    return BankAccount.objects.create(
        number="8073487154",
        name="Brian David Obot",
        bank_name="Opay",
        bank_code="87618798198",
        user=user,
    )


@pytest.fixture
def wallet(org) -> Wallet:
    return Wallet.objects.create(
        balance=1000,
        organization=org,
    )


@pytest.fixture
def withdrawals(user: User) -> Withdrawals:
    return Withdrawals.objects.create(
        user=user,
        amount=1000,
        status="SUCCESSFUL",
    )


"""
Test Classes here
"""
class TestOrganization:
    def test_str_method(self, organization):
        assert str(organization) == "" # TODO: Replace with the expected result

    def test_fields(self, organization: Organization):
        assert organization.email == "testorg@org.com"
        assert organization.name == "Test Organization"
        assert organization.role == "Humanitarian"


class TestLunchWallet:
    def test_str_method(self, launch_wallet: LunchWallet):
        return str(launch_wallet) == "" # TODO: Replace with the expected result
    
    def test_fields(self, launch_wallet: LunchWallet, staff: Staff, organization: Organization):
        assert launch_wallet.staff == staff
        assert launch_wallet.organization == organization
        assert launch_wallet.type == "some test type"


class TestWithdrawals:
    def test_str_method(self, withdrawals: Withdrawals):
        return str(withdrawals) == "" # TODO: Replace with the expected result
    
    def test_fields(self, withdrawals: Withdrawals, user: User):
        assert withdrawals.user == user
        assert withdrawals.amount == 1000
        assert withdrawals.status == "SUCCESSFUL"
        assert getattr(withdrawals, "created_at") is not None

    