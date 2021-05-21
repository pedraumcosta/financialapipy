from django.conf.urls import url
from . import views


urlpatterns = [
    url(
        r'^api/v1/accounts/(?P<pk>[0-9]+)$',
        views.get_delete_update_account,
        name='get_delete_update_account'
    ),
    url(
        r'^api/v1/accounts/$',
        views.get_post_accounts,
        name='get_post_accounts'
    ),
    url(
        r'^api/v1/transfer/(?P<from_account>[0-9]+)/(?P<to_account>[0-9]+)/(?P<amount>[0-9]+)$',
        views.get_transfer,
        name='get_transfer'
    )
]