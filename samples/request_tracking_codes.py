from ..correios.client import Correios
from ..correios.models.user import User, Service


def get_tracking_codes(service, quantity):
    olist_user = User('Your Company\'s Name', 'Your Company\'s CNPJ')
    client = Correios('Your Correio\'s username', 'Your correio\'s password')
    tracking_codes = client.request_tracking_codes(olist_user, Service.get(service), quantity=quantity)
    print(tracking_codes)

get_tracking_codes('41068', 1)  # Request 1 PAC Tracking Code
get_tracking_codes('40068', 1)  # Request 1 SEDEX Tracking Code
