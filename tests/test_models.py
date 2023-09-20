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

from transaction.models import LaunchWallet, LaunchTransaction, Transaction, BankAccount, Wallet, Organization, Launch
from users.models import Staff


@pytest.fixture 
def launch_wallet(staff):
    return LaunchWallet.objects.create(
        staff=staff,
        balance=100.0,
    )


@pytest.fixture
def lanuch_transaction(staff, org):
    return LaunchTransaction.objects.create(
        staff=staff,
        organization=org,
        type="some test type",
    )


@pytest.fixture
def transaction():
    sender = Staff.objects.create()
    receiver = Staff.objects.create()
    return Transaction.objects.create(
        sender=sender,
        receiver=receiver,
        currency="NGN",
        status="PENDING",
    )