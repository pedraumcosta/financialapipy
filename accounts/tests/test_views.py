import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import Account, create_account
from accounts.serializers import AccountSerializer


# initialize the APIClient app
client = Client()


class GetAllAccountsTest(TestCase):
    """ Test module for GET all accounts API """

    def setUp(self):
        create_account(name='Casper', balance=1000.0)
        create_account(name='Basil', balance=650.25)
        create_account(name='Watson', balance=700.0)
        create_account(name='James', balance=250.0)

    def test_get_all_accounts(self):
        # get API response
        response = client.get(reverse('get_post_accounts'))
        # get data from db
        accounts = Account.objects.all()
        serializer = AccountSerializer(accounts, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleAccountTest(TestCase):
    """ Test module for GET single Account API """

    def setUp(self):
        self.casper = create_account(name='Casper', balance=1000.0)
        create_account(name='Basil', balance=650.25)
        create_account(name='Watson', balance=700.0)
        create_account(name='James', balance=250.0)

    def test_get_valid_single_account(self):
        response = client.get(
            reverse('get_delete_update_account', kwargs={'pk': self.casper.pk}))
        account = Account.objects.get(pk=self.casper.pk)
        serializer = AccountSerializer(account)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_account(self):
        response = client.get(
            reverse('get_delete_update_account', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewAccountTest(TestCase):
    """ Test module for inserting a new Account """

    def setUp(self):
        self.valid_payload = {
            'name': 'Baptist',
            'balance': 400.0
        }
        self.invalid_payload = {
            'name': '',
            'balance': 600.0
        }
        self.invalid_balance = {
            'name': 'John',
            'balance': -600.0
        }

    def test_create_valid_account(self):
        response = client.post(
            reverse('get_post_accounts'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_Account(self):
        response = client.post(
            reverse('get_post_accounts'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_account_with_negative_balance(self):
        response = client.post(
            reverse('get_post_accounts'),
            data=json.dumps(self.invalid_balance),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleAccountTest(TestCase):
    """ Test module for updating an existing account record """

    def setUp(self):
        self.casper = create_account(name='Casper', balance=1000.0)
        self.basil = create_account(name='Basil', balance=650.25)
        self.valid_payload = {
            'name': 'Casper',
            'balance': 200.0
        }
        self.invalid_payload = {
            'name': '',
            'balance': 400.0,
        }

    def test_valid_update_account(self):
        response = client.put(
            reverse('get_delete_update_account', kwargs={'pk': self.casper.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_update_account(self):
        response = client.put(
            reverse('get_delete_update_account', kwargs={'pk': self.casper.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleAccountTest(TestCase):
    """ Test module for deleting an existing account record """

    def setUp(self):
        self.casper = create_account(name='Casper', balance=1000.0)
        self.basil = create_account(name='Basil', balance=650.25)

    def test_valid_delete_account(self):
        response = client.delete(
            reverse('get_delete_update_account', kwargs={'pk': self.casper.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_account(self):
        response = client.delete(
            reverse('get_delete_update_account', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TransferTest(TestCase):
    """ Test module for transfer balance between accounts"""

    def setUp(self):
        self.casper = create_account(name='Casper', balance=1000.0)
        self.basil = create_account(name='Basil', balance=650.25)

    def test_transfer(self):
        response = client.get(
            reverse('get_transfer', kwargs={'from_account': self.casper.pk, 'to_account': self.basil.pk, 'amount': '10000'}))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = client.get(
            reverse('get_delete_update_account', kwargs={'pk': self.casper.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(900.0, response.data['balance'])

        response = client.get(
            reverse('get_delete_update_account', kwargs={'pk': self.basil.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(750.25, response.data['balance'])
