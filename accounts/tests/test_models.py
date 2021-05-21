from django.test import TestCase
from django_mock_queries.query import MockSet
from accounts.models import Account


class AccountTest(TestCase):

    def setUp(self):
        Account.objects.create(name='Casper', balance=1000.0)
        Account.objects.create(name='Basil', balance=650.25)

    def test_account(self):
        casper = Account.objects.get(name='Casper')
        basil = Account.objects.get(name='Basil')
        self.assertEqual(casper.get_balance(), 1000.0)
        self.assertEqual(basil.get_balance(), 650.25)


class TestFindByAccountName:

    def test_when_username_exist_return_account(self, mocker):
        expected_result = [
            Account(
                name='john.smith',
                balance=2000
            )
        ]
        qs_mock = MockSet(expected_result[0])

        mocker.patch.object(
            Account.objects,
            'get_queryset',
            return_value=qs_mock
        )

        result = list(Account.objects.find_by_name('john.smith'))
        assert result == expected_result