# Copyright 2017 Adler Medrado
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from ..correios.client import Correios
from ..correios.models.user import Service, User


def get_tracking_codes(service, quantity):
    olist_user = User("Your Company's Name", "Your Company's CNPJ")
    client = Correios("Your Correio's username", "Your correio's password")
    tracking_codes = client.request_tracking_codes(olist_user, Service.get(service), quantity=quantity)
    print(tracking_codes)


get_tracking_codes('41068', 1)  # Request 1 PAC Tracking Code
get_tracking_codes('40068', 1)  # Request 1 SEDEX Tracking Code
