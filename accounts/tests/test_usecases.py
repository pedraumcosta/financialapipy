from accounts.models import Account
from accounts.usecases import (
    TransferBalance,
    AccountNotFoundError, BusinessException
)
from django.test import TestCase


class TransferBalanceExecuteTest(TestCase):
    # Test the execute method on TransferBalance use case

    def test_regular_transfer(self):
        self.casper = Account.objects.create(name='Casper', balance=1000.0)
        self.basil = Account.objects.create(name='Basil', balance=650.25)
        self.use_case = TransferBalance(from_account_id=self.casper.pk, to_account_id=self.basil.pk, amount=10000)

        result = self.use_case.execute()
        assert result == True
        assert Account.objects.get(name='Casper').get_balance() == 900
        assert Account.objects.get(name='Basil').get_balance() == 750.25

    def test_transfer_with_invalid_from_account(self):
        self.basil = Account.objects.create(name='Basil', balance=650.25)
        self.use_case = TransferBalance(from_account_id=66, to_account_id=self.basil.pk, amount=10000)
        with self.assertRaisesMessage(AccountNotFoundError, 'Account not found'):
            self.use_case.execute()

    def test_transfer_with_invalid_to_account(self):
        self.basil = Account.objects.create(name='Basil', balance=650.25)
        self.use_case = TransferBalance(from_account_id=self.basil.pk, to_account_id=66, amount=10000)
        with self.assertRaisesMessage(AccountNotFoundError, 'Account not found'):
            self.use_case.execute()

    def test_not_enough_fuunds_in_from_account(self):
        self.casper = Account.objects.create(name='Casper', balance=1000.0)
        self.basil = Account.objects.create(name='Basil', balance=650.25)
        self.use_case = TransferBalance(from_account_id=self.casper.pk, to_account_id=self.basil.pk, amount=200000)
        with self.assertRaisesMessage(BusinessException, 'Not enough funds on source account'):
            self.use_case.execute()
