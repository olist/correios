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


import pytest

from correios.exceptions import InvalidZipCode
from correios.models import Zip


def test_basic_zip():
    zip_code = Zip("82940150")
    assert zip_code.code == "82940150"


def test_sanitize_zip():
    zip_code = Zip("82940-150")
    assert zip_code.code == "82940150"


def test_fail_invalid_zip():
    with pytest.raises(InvalidZipCode):
        Zip("12345")

    with pytest.raises(InvalidZipCode):
        Zip("123456789")


def test_convert_zip_to_str():
    assert str(Zip("82940-150")) == "82940150"


def test_zip_repr():
    assert repr(Zip("82940-150")) == "<Zip code: 82940150>"


def test_zip_display():
    assert Zip("82940150").display() == "82940-150"
