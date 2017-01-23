import pytest

from correios.utils import capitalize_phrase, RangeSet, rreplace

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
