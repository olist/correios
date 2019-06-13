import pytest

from correios.models.builders import ModelBuilder
from correios.models.posting import Package
from correios.xml_utils import fromstring


@pytest.fixture
def post_info_data():
    return """
      <objeto_postal>
        <numero_etiqueta></numero_etiqueta>
        <codigo_objeto_cliente></codigo_objeto_cliente>
        <codigo_servico_postagem></codigo_servico_postagem>
        <cubagem></cubagem>
        <peso>2250</peso>
        <rt1></rt1>
        <rt2></rt2>
        <destinatario></destinatario>
        <nacional></nacional>
        <servico_adicional>
            <codigo_servico_adicional></codigo_servico_adicional>
        </servico_adicional>
        <dimensao_objeto>
          <tipo_objeto>2</tipo_objeto>
          <dimensao_altura>8.0</dimensao_altura>
          <dimensao_largura>35.0</dimensao_largura>
          <dimensao_comprimento>20.0</dimensao_comprimento>
          <dimensao_diametro>5.0</dimensao_diametro>
        </dimensao_objeto>
        <data_postagem_sara></data_postagem_sara>
        <status_processamento></status_processamento>
        <numero_comprovante_postagem></numero_comprovante_postagem>
        <valor_cobrado></valor_cobrado>
      </objeto_postal>
    """


@pytest.fixture
def model_builder():
    return ModelBuilder()


@pytest.mark.parametrize(
    "expected_fields, package_type",
    (
        (("height", "length", "weight", "width", "package_type"), Package.TYPE_BOX),
        (("diameter", "length", "weight", "package_type"), Package.TYPE_CYLINDER),
        (("weight", "package_type"), Package.TYPE_ENVELOPE),
    ),
)
def test_load_package_fields(model_builder, post_info_data, expected_fields, package_type):
    post_info = fromstring(post_info_data)
    post_info.dimensao_objeto.tipo_objeto = package_type

    package_data = model_builder._build_package_data(post_info)

    assert set(package_data.keys()) == set(expected_fields)
