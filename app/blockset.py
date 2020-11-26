import uuid
from django.conf import settings
import requests


def fetch(method, resource, **params):
    headers = {'authorization': 'Bearer ' + settings.BLOCKSET_TOKEN}
    if 'headers' in params:
        params['headers'].update(headers)
    else:
        params['headers'] = headers
    resp = requests.request(method, 'https://api.blockset.com/' + resource, **params)
    resp.raise_for_status()
    if len(resp.content) > 0:
        return resp.json()
    return None


def get_blockchains():
    mainnets = fetch('get', 'blockchains')['_embedded']['blockchains']
    testnets = fetch('get', 'blockchains', params={'testnet': 'true'})['_embedded']['blockchains']
    blockchains = mainnets + testnets
    blockchains.sort(key=lambda b: b['name'])
    return blockchains


def create_subscription(to_url, addresses):
    currencies = {}
    for addr in addresses:
        blockchain_id, *blockchain_addr = addr.split(':')
        currencies.setdefault(blockchain_id, [])
        currencies[blockchain_id].append(':'.join(blockchain_addr))

    spec = {
        'device_id': str(uuid.uuid4()),
        'endpoint': {
            'environment': 'production',
            'kind': 'webhook',
            'value': to_url
        },
        'currencies': [{
                'currency_id': blockchain_id + ':__native__',
                'addresses': addrs,
                'events': [{
                        'name': 'submitted',
                        'confirmations': [],
                    }, {
                        'name': 'confirmed',
                        'confirmations': _get_confirmations(blockchain_id)
                    }
                ]
            } for blockchain_id, addrs in currencies.items()
        ]
    }

    return fetch('post', 'subscriptions', json=spec)


def delete_subscription(subscription_id):
    fetch('delete', f'subscriptions/{subscription_id}')


def _get_confirmations(blockchain_id):
    confirmations = {
        'bitcoin': [1, 6],
        'ethereum': [1, 10],
    }
    for k in confirmations.keys():
        if k in blockchain_id:
            return confirmations[k]
    return [1]
