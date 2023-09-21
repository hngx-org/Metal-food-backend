"""
test_models.py - Unit tests for the models in the Django application.

This module contains a suite of unit tests that verify the behavior of the models
defined in the Django application. Each test case is designed to check specific aspects
of the model's functionality, such as field validation, methods, and relationships.

Test cases in this module include:
    - TestOrganization: Tests for the Organization Model class.
    - TestLunchWallet: Tests for the LunchWallet Model class.
    - TestWithdrawals: Tests for the Withdrawals Model class.

Dependencies:
    - Django: This module assumes that Django is properly installed and configured in
      the project environment.

Usage:
    - Run the tests using a Django test runner. For example, using the command:
      `python manage.py pytest`

Author: Brian Obot
Copyright 2023 Brian Obot
"""

import pytest

from transaction.models import (
    Lunch,
    LunchWallet,
    LunchTransaction,
    Transaction,
    BankAccount,
    Wallet,
    Organization,
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
def lunch() -> Lunch:
    sender = User.objects.create()
    receiver = User.objects.create()
    return Lunch.objects.create(
        sender=sender,
        receiver=receiver,
        quantity=10,
        note="Visit https://brianobot.github.io for your code works",

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


class TestLunch:
    def test_str_method(self, lunch: Lunch):
        assert str(lunch) == "" # TODO: Replace with the expected result


    def test_fields(self, lunch: Lunch):
        assert isinstance(lunch.sender, User)
        assert isinstance(lunch.receiver, User)
        assert lunch.quantity == 10
        assert lunch.note == "Visit https://brianobot.github.io for your code works"


class TestLunchWallet:
    def test_str_method(self, launch_wallet: LunchWallet):
        assert str(launch_wallet) == "" # TODO: Replace with the expected result
    
    def test_fields(self, launch_wallet: LunchWallet, staff: Staff, organization: Organization):
        assert launch_wallet.staff == staff
        assert launch_wallet.organization == organization
        assert launch_wallet.type == "some test type"

    
class TestTransaction:
    def test_str_method(self, transaction: Transaction):
        assert str(transaction) == "" 

    def test_fields(self, transaction: Transaction):
        assert isinstance(transaction.sender, User)
        assert isinstance(transaction.receiver, User)
        assert transaction.currency == "NGN"
        assert transaction.status == "PENDING"


class TestLunchTransaction:
    def test_str_method(self, lunch_transaction: LunchTransaction):
        assert str(lunch_transaction) == "" # TODO: replace with actual expected value

    def test_fields(self, lunch_transaction: LunchTransaction, staff: Staff, organization: Organization):
        assert lunch_transaction.type == "some test type"
        assert isinstance(lunch_transaction.staff, Staff)
        assert isinstance(lunch_transaction.organization, Organization)


class TestBankAccount:
    def test_str_method(self, bank_account: BankAccount):
        assert str(bank_account) == "" # TODO: replace with actual expected value

    def test_fields(self, bank_account: BankAccount):
        assert bank_account.number == "8073487154"
        assert bank_account.name == "Brian David Obot"
        assert bank_account.bank_name == "Opay"
        assert bank_account.bank_code == "87618798198"
        assert isinstance(bank_account.user, User)

    
class TestWallet:
    def test_str_methods(self, wallet: Wallet):
        assert str(bank_account) == "" # TODO: replace with actual expected value

    def test_fields(self, wallet: Wallet):
        assert wallet.balance == 1000
        assert isinstance(wallet.organization, Organization)

    
class TestWithdrawals:
    def test_str_method(self, withdrawals: Withdrawals):
        return str(withdrawals) == "" # TODO: Replace with the expected result
    
    def test_fields(self, withdrawals: Withdrawals, user: User):
        assert withdrawals.user == user
        assert withdrawals.amount == 1000
        assert withdrawals.status == "SUCCESSFUL"
        assert getattr(withdrawals, "created_at") is not None
