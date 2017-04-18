import pytest

try:
    from correios import xml_utils
except ImportError:
    xml_utils = None


@pytest.mark.skipif(not xml_utils, reason="API Client support disabled")
def test_cdata_special_chars_handling():
    document = xml_utils.Element("test", cdata="áéíóú")
    xml = xml_utils.tostring(document, encoding="unicode").encode("iso-8859-1")
    assert xml == "<test><![CDATA[áéíóú]]></test>".encode("iso-8859-1")
