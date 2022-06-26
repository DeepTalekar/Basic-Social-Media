import pytest

from app.calculations import *


@pytest.fixture
def zero_bank_account():
    print("Creating an empty bank account")
    return BankAccount()


@pytest.fixture
def bank_account():
    return BankAccount(50)


@pytest.mark.parametrize("num1, num2, expected", [
    (2, 4, 6),
    (3, 5, 8),
    (15, 24, 39),
])
def test_add(num1, num2, expected):
    assert add(num1, num2) == expected


def test_subtract():
    assert subtract(9, 4) == 5


def test_multiply():
    assert multiply(2, 3) == 6


def test_divide():
    assert divide(4, 2) == 2


def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 50


def test_bank_default_amount(zero_bank_account):
    print("Testing my bank account")
    assert zero_bank_account.balance == 0


def test_withdraw(bank_account):
    bank_account.withdraw(20)
    assert bank_account.balance == 30


def test_deposit(bank_account):
    bank_account.deposit(20)
    assert bank_account.balance == 70


def test_collect_interest(bank_account):
    bank_account.collect_interest()
    assert bank_account.balance == 50 * 1.4


@pytest.mark.parametrize("deposited, withdraw, expected", [
    (200, 100, 100),
    (50, 10, 40),
    (4000, 720, 3280),
])
def test_bank_transaction(zero_bank_account, deposited, withdraw, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdraw)
    assert zero_bank_account.balance == expected


@pytest.mark.parametrize("deposited, withdraw", [
    (200, 1000),
])
def test_insufficient_funds(bank_account, deposited, withdraw):
    bank_account.deposit(deposited)
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(withdraw)
