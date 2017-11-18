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


from decimal import Decimal
from unittest import mock

import pytest

from correios.utils import RangeSet, capitalize_phrase, get_resource_path, rreplace, to_decimal, to_integer

phrase = 'FOo bAr BAZ qux'


@pytest.fixture
def rangeset():
    """ returns the sequence 1, 2, 4, 5, 7, 8 """
    return RangeSet((1, 3), (4, 6), (7, 9))


def test_rangeset():
    assert list(RangeSet(range(3))) == [0, 1, 2]
    assert list(RangeSet((0, 3))) == [0, 1, 2]
    assert list(RangeSet((1, 3), (4, 6), (7, 9))) == [1, 2, 4, 5, 7, 8]
    assert list(RangeSet((1, 3), RangeSet((4, 6)), range(7, 9))) == [1, 2, 4, 5, 7, 8]

    with pytest.raises(ValueError):
        RangeSet(1)


@pytest.mark.parametrize('ranges_len, elements_len, ranges', (
    (1, 3, (range(3),)),
    (3, 6, ((1, 3), (4, 6), (7, 9))),
))
def test_rangeset_len(ranges_len, elements_len, ranges):
    rangeset = RangeSet(*ranges)
    assert len(rangeset) == elements_len
    assert len(rangeset.ranges) == ranges_len


@pytest.mark.parametrize('element', (1, 2, 4, 5, 7, 8))
def test_rangeset_contain(element, rangeset):
    assert element in rangeset


@pytest.mark.parametrize('element', (-1, 3, 6, 9, 10000, 12))
def test_rangeset_does_not_contain(element, rangeset):
    assert element not in rangeset


def test_rangeset_iter(rangeset):
    assert list(rangeset) == [1, 2, 4, 5, 7, 8]


@pytest.mark.parametrize('phrase', (phrase, phrase.upper(), phrase.lower()))
def test_capitalize_phrase(phrase):
    assert capitalize_phrase(phrase) == 'Foo Bar Baz Qux'


def test_rreplace():
    phrase = 'foo bar baz qux'
    assert rreplace(phrase, ' ', '-', 1) == 'foo bar baz-qux'
    assert rreplace(phrase, ' ', '-', 2) == 'foo bar-baz-qux'
    assert rreplace(phrase, ' ', '-', 3) == 'foo-bar-baz-qux'
    assert rreplace(phrase, ' ', '-') == 'foo-bar-baz-qux'


@pytest.mark.parametrize('s, d', (
    ("", Decimal("0.00")),
    ("3", Decimal("3.00")),
    ("3.57", Decimal("3.57")),
    ("3.468", Decimal("3.47")),
    ("3.4", Decimal("3.40")),
    ("3,57", Decimal("3.57")),
    ("3,468", Decimal("3.47")),
    ("3,4", Decimal("3.40")),
    ("1,357.93", Decimal("1357.93")),
    ("1.357,93", Decimal("1357.93")),
    ("1_357.93", Decimal("1357.93")),
    ("1_357,93", Decimal("1357.93")),
))
def test_to_decimal(s, d):
    assert to_decimal(s) == d


@pytest.mark.parametrize('v, p, r', (
    ("3.4", 1, Decimal("3.4")),
    ("3.4", 4, Decimal("3.4000")),
    ("3.4", 0, Decimal("3")),
    ("3.6", 0, Decimal("4")),
    ("3.46876", 2, Decimal("3.47")),
))
def test_to_decimal_precision(v, p, r):
    assert to_decimal(v, p) == r


@pytest.mark.parametrize('v, r', (
    (3, 3),
    ("3", 3),
    ("  \t3  \n", 3),
))
def test_to_integer(v, r):
    assert to_integer(v) == r


def test_get_wsdl_file_path():
    path = get_resource_path('fake')
    assert str(path).endswith('correios/data/fake')


@mock.patch("pkg_resources.resource_filename", return_value="/")
def test_should_use_pkg_resources_to_get_wsdl_files(mock_resource):
    path = get_resource_path('fake')

    mock_resource.assert_called_with('correios', 'data/fake')
    assert str(path) == "/"
