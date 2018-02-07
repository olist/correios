Busca de endereço
=================

A busca de endereço consite em passar como parâmetro um cep válido e o pacote
executar o serviço consultaCEP no webservice dos correios.

Começando
---------

Os pré requisitos para executar este serviço são.

- Ter um usuário e senha válidos

- Ter o pacote instalado.

- Um cep válido


Faça os imports do client, model ZipCode e exceptions

.. code-block:: python

    from correios.models.address import ZipCode
    from correios.exceptions import InvalidZipCodeError, InvalidAddressesError

    try:
        from correios import client as correios
    except ImportError:
        correios = None


Realize a autenticação no webservice setando o ambiente

.. code-block:: python

    client = correios.Correios(
        username='sigep-test', password='sigep-test',
        environment=correios.Correios.TEST
    )


Após autenticado execute o método para buscar o cep

.. code-block:: python

    zip_address = client.find_zipcode(ZipCode(zip_code))

Script completo
---------------

.. code-block:: python

    # -*- coding: utf-8 -*-

    """
    Busca informações de um endereço de acordo com o cep informado
    """

    from flask import current_app

    from correios.models.address import ZipCode
    from correios.exceptions import InvalidZipCodeError, InvalidAddressesError

    try:
        from correios import client as correios
    except ImportError:
        correios = None


    def correios_search_cep(zip_code, test=True):
        '''
        Find address by zip code in correios ws
        '''
        if correios is None:
            return True, {'error': True, 'message': 'An error occurred.'}

        username = os.getenv['CORREIOS_USERNAME'] or None
        password = os.getenv['CORREIOS_PASSWORD'] or None

        error = False

        if username is None or password is None:
            return True, {'error': True, 'message': 'An error occurred.'}

        if test:
            environment = correios.Correios.TEST
        else:
            environment = correios.Correios.PRODUCTION,

        try:
            client = correios.Correios(
                username=username, password=password, environment=environment
            )

        except Exception as e:
            error = True
            info = {'error': error, 'message': e.message, 'ws': True}
            return error, info

        try:
            zip_address = client.find_zipcode(ZipCode(zip_code))

        except (InvalidZipCodeError, InvalidAddressesError) as e:
            error = True
            info = {'error': error, 'message': e.message, 'ws': True}
            return error, info

        except Exception as e:
            error = True
            info = {'error': error, 'message': e.message, 'ws': False}
            return error, info

        data = translate_fields(zip_address)

        info = {'error': error, 'message': 'Success.', 'data': data}

        return error, info


    def translate_fields(zip_address):
        '''
        Serializer object data to dict
        '''
        return {
            'zip_code': zip_address.zip_code.code,
            'zip_code_display': zip_address.zip_code.display(),
            'address': zip_address.address,
            'region': zip_address.zip_code.region, 'number': '',
            'info': zip_address.complements,
            'neighborhood': zip_address.district, 'city': zip_address.city,
            'state': zip_address.state.code,
            'state_display': zip_address.state.display(), 'country': 'Brasil'
        }


    if __name__ == '__main__':

        data = correios_search_cep('70070-705')
        print(data)

