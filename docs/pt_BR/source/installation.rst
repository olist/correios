Instalação
----------

.. code-block:: shell

    $ pip install correios  # suporte básico à modelos
    $ pip install correios[pdf]  # suporte a geração de etiquetas e PLP
    $ pip install correios[api]  # suporte ao cliente das APIs SIGEP/SRO
    $ pip install correios[pdf,api]  # instalação completa


Atualize arquivos WSDL locais
-----------------------------

Arquivos WSDL locais são utilizados para melhorar a performance em requisições
SOAP. Eventualmente você vai precisar atualizar esses arquivos sem que seja
necessário atualizar essa biblioteca.

Se você deseja manter esses arquivos em um local personalizado você poderá
informar o parâmetro ``path`` com esse endereço alternativo ao instanciar
o cliente. Utilize apenas ``path`` absoluto.

Execute:

.. code-block:: shell

    $ update-correios-wsdl -p /path/to/your/custom/wsdl/folder

Parâmetros::

    * -p, --path: Diretório onde os arquivos WSDLs serão gravados. Essa opção
      tem precedência sobre a variável de ambiente ``CORREIOS_WSDL_PATH``.


Você também pode fazer essa atualização via código com método
``WSDLUpdater.update_all()``.

.. code-block:: python

    from correios.update_wsdl import WSDLUpdater

    updater = WSDLUpdater(wsdl_path="/tmp/wsdls")
    updater.update_all()
