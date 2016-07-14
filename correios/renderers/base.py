# Copyright 2016 Osvaldo Santana Neto
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
from typing import Tuple, Sequence

from reportlab.lib.pagesizes import A4

from correios.models.posting import ShippingLabel


class AbstractDocument(object):
    def __init__(self, paper_size: Tuple[float, float]=A4):
        self.paper_size = paper_size
        self.posting_list = []
        self.shipping_labels = []

    def add_posting_list(self, posting_list):  # TODO: add PostingList type annotation
        self.posting_list.append(posting_list)
        self.add_shipping_labels(posting_list.shipping_labels)

    def add_shipping_labels(self, shipping_labels: Sequence[ShippingLabel]):
        self.shipping_labels.extend(shipping_labels)

    def add_shipping_label(self, shipping_label: ShippingLabel):
        self.shipping_labels.append(shipping_label)

    def render(self):
        raise NotImplementedError()
