from accounts.models import Account
from accounts.usecases import (
    TransferBalance,
    AccountNotFoundError
)
from django.test import TestCase


class TransferBalanceExecuteTest(TestCase):
    # Test the execute method on TransferBalance use case

    def setUp(self):
        # setup method will be executed on each test
        self.casper = Account.objects.create(name='Casper', balance=1000.0)
        self.basil = Account.objects.create(name='Basil', balance=650.25)
        self.use_case = TransferBalance(from_account_id=self.casper.pk, to_account_id=self.basil.pk, amount=10000)

    def test_return_account_type(self):
        result = self.use_case.execute()
        assert result == True
        assert Account.objects.get(name='Casper').get_balance() == 900
        assert Account.objects.get(name='Basil').get_balance() == 750.25


# class TestValidData:
#     # Test the valid_data method on RegisterUserAccount use case
#
#     def test_when_username_already_exists_raise_username_already_exist_error(self, mocker):
#         qs_mock = MockSet(
#             UserAccount(
#                 username='john.smith',
#                 email='john.smith@example.com'
#             )
#         )
#
#         # We don't need to test this method again,
#         # since it has been tested by the
#         # test_user_account_manager.py file.
#         mocker.patch.object(
#             UserAccount.objects,
#             'find_by_username',
#             return_value=qs_mock
#         )
#
#         with pytest.raises(UsernameAlreadyExistError):
#             use_case = RegisterUserAccount(
#                 'john.smith',
#                 'john.smith@example.com',
#                 'P@ssword9'
#             )
#
#             use_case.valid_data()
#
#     def test_when_username_does_not_exists_returns_true(self, mocker):
#         expected_result = True
#         qs_mock = MockSet()
#
#         mocker.patch.object(
#             UserAccount.objects,
#             'find_by_username',
#             return_value=qs_mock
#         )
#
#         use_case = RegisterUserAccount(
#             'john.smith',
#             'john.smith@example.com',
#             'P@ssword9'
#         )
#
#         result = use_case.valid_data()
#         assert result == expected_result
