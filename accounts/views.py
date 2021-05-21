from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Account
from .serializers import AccountSerializer


@api_view(['GET', 'DELETE', 'PUT'])
def get_delete_update_account(request, pk):
    try:
        account = Account.objects.get(pk=pk)
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # get details of a single account
    if request.method == 'GET':
        serializer = AccountSerializer(account)
        return Response(serializer.data)
    # delete a single account
    elif request.method == 'DELETE':
        account.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        # update details of a single account
    elif request.method == 'PUT':
        serializer = AccountSerializer(account, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def get_post_accounts(request):
    # get all accounts
    if request.method == 'GET':
        accounts = Account.objects.all()
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data)
    # insert a new record for a account
    elif request.method == 'POST':
        data = {
            'name': request.data.get('name'),
            'balance': float(request.data.get('balance')),
        }
        serializer = AccountSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_transfer(request, from_account, to_account, amount):
    try:
        from_account = Account.objects.get(pk=from_account)
        to_account = Account.objects.get(pk=to_account)
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        from_account.balance = from_account.balance - int(amount)/100
        to_account.balance = to_account.balance + int(amount)/100

        data = {
            'name': from_account.name,
            'balance': from_account.balance,
        }
        serializer = AccountSerializer(from_account, data=data)
        if serializer.is_valid():
            serializer.save()

            data = {
                'name': to_account.name,
                'balance': to_account.balance,
            }
            serializer = AccountSerializer(to_account, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
