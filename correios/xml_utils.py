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

from functools import wraps

from lxml import etree, objectify


def add_text_argument(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        text = kwargs.pop("text", None)
        cdata = kwargs.pop("cdata", None)
        element = f(*args, **kwargs)
        if cdata:
            element.text = etree.CDATA(cdata)
        elif text:
            element.text = text
        else:
            element.text = None
        return element

    return wrapper


Element = add_text_argument(etree.Element)
SubElement = add_text_argument(etree.SubElement)
tostring = etree.tostring
parse = etree.parse
XMLSchema = etree.XMLSchema
fromstring = objectify.fromstring
