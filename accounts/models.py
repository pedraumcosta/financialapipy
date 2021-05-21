from django.db import models


class Account(models.Model):
    """
    Account Model
    Defines the attributes of a account
    """
    name = models.CharField(max_length=255)
    balance = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_name(self):
        return self.name

    def get_balance(self):
        return self.balance

    def set_name(self, name):
        self.name = name

    def set_balance(self, balance):
        self.balance = balance
