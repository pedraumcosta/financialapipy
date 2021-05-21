from accounts.models import Account, create_account_dict
from accounts.serializers import AccountSerializer
from django.db import transaction


class AccountNotFoundError(Exception):
    pass


class SerializationFailed(Exception):
    pass


class TransferBalance:
    def __init__(self, from_account_id, to_account_id, amount):
        self.from_account_id = from_account_id
        self.to_account_id = to_account_id
        self.amount = amount

    def execute(self):
        # validations
        try:
            from_account = Account.objects.find(self.from_account_id)
            to_account = Account.objects.find(self.to_account_id)
        except Account.DoesNotExist:
            raise AccountNotFoundError('Account not found')

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
        return False

    def persist(self, account):
        data = create_account_dict(account.get_name(), account.get_balance())
        serializer = AccountSerializer(account, data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            raise SerializationFailed(serializer.errors)