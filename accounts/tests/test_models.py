from django.test import TestCase
from ..models import Account


class AccountTest(TestCase):
    """ Test module for Account model """

    def setUp(self):
        Account.objects.create(name='Casper', balance=1000.0)
        Account.objects.create(name='Basil', balance=650.25)

    def test_account(self):
        casper = Account.objects.get(name='Casper')
        basil = Account.objects.get(name='Basil')
        self.assertEqual(casper.get_balance(), 1000.0)
        self.assertEqual(basil.get_balance(), 650.25)
