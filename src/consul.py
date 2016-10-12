import requests
import logging
import json
import base64

logger = logging.getLogger('consul')

class Consul:
    def __init__(self, address, port, secure, token):
        self._address = "https://{}".format(address) if secure is True else "http://{}".format(address)
        self._port = port
        self._token = token

    def backup_kv(self):
        logger.info('Fetching KV')
        self._fetch_kv()
        logger.info('Parsing KV')
        self._parse_kv()
        logger.info('Outputting KV')
        self._output_kv()

    def restore_kv(self, restore_file):
        restore_file = open('/restore/{}'.format(restore_file), 'r')
        transaction_data = []

        for line in restore_file:
            kv = line.split(':')
            logger.debug('Key: {}, Value: {}'.format(kv[0], base64.standard_b64decode(kv[1]).decode('utf-8')))

            transaction_data.append({ 'KV' : { 'Verb': 'set', 'Key': kv[0], 'Value': kv[1] } })

        self._upload_kv(transaction_data)

    def _upload_kv(self, transaction_data):
        headers = { 'X-Consul-Token': self._token } if self._token is not None else {}
        request_url = '{address}/v1/txn'.format(address=self._address)

        try:
            r = requests.put(request_url, headers=headers, json=transaction_data)
            r.raise_for_status()            
        except requests.HTTPError:  
            logging.critical('Unable upload kv to %s', request_url, exc_info=True)
        except requests.ConnectionError:
            logging.critical('Unable to connect to Consul at address %s', request_url, exc_info=True)

       
    def _fetch_kv(self):
        headers = { 'X-Consul-Token': self._token } if self._token is not None else {}
        request_url = '{address}/v1/kv/?recurse'.format(address=self._address)

        try:
            r = requests.get(request_url, headers=headers)
            r.raise_for_status()
            self._kv_raw = json.loads(r.text)
            
        except requests.HTTPError:  
            logging.critical('Unable to fetch KV pairs from %s', request_url, exc_info=True)
        except requests.ConnectionError:
            logging.critical('Unable to connect to Consul at address %s', request_url, exc_info=True)

    def _parse_kv(self):
        self._kv = map(lambda kv: { 'Key': kv['Key'], 'Value': kv['Value'] }, self._kv_raw)

    def _output_kv(self):
        for kv in self._kv:
            print('{}:{}'.format(kv['Key'], kv['Value']))

    