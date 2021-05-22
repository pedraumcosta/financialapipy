from accounts.models import Account
from accounts.serializers import AccountSerializer
from django.db import transaction


class AccountNotFoundError(Exception):
    pass


class BusinessException(Exception):
    pass


class SerializationFailed(Exception):
    pass


class TransferBalance:
    def __init__(self, from_account_id, to_account_id, amount):
        self.from_account_id = from_account_id
        self.to_account_id = to_account_id
        self.amount = amount

    def execute(self):
        try:
            from_account = Account.objects.find(self.from_account_id)
            to_account = Account.objects.find(self.to_account_id)
        except Account.DoesNotExist:
            raise AccountNotFoundError('Account not found')

        if from_account.get_balance() - int(self.amount)/100 > 0:
            with transaction.atomic():
                from_account.set_balance(
                    from_account.get_balance() - int(self.amount)/100
                )

                to_account.set_balance(
                    to_account.get_balance() + int(self.amount)/100
                )

                self.persist(from_account)

                self.persist(to_account)

                return True
        else:
            raise BusinessException("Not enough funds on source account")
        return False

    def persist(self, account):
        data = {
            'name': account.get_name(),
            'balance': account.get_balance()
        }
        serializer = AccountSerializer(account, data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            raise SerializationFailed(serializer.errors)