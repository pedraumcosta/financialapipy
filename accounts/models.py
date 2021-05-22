from django.core.validators import MinValueValidator
from django.db import models


def create_account(name, balance):
    return Account.objects.create(name=name, balance=balance)


def create_account_dict(name, balance):
    return {
        'name': name,
        'balance': balance
    }


class AccountManager(models.Manager):

    def find(self, id):
        return self.get(pk=id)

    def find_by_name(self, name):
        return self.filter(models.Q(name=name))


class Account(models.Model):
    """
    Account Model
    Defines the attributes of an account
    """
    name = models.CharField(max_length=255)
    balance = models.FloatField(default=0, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AccountManager()

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_balance(self):
        return self.balance

    def set_balance(self, balance):
        self.balance = balance
