.PHONY: help

help:  ## This help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort

update-wsdl:  ## Update wsdl files
	@curl -o 'correios/wsdls/AtendeCliente-production.wsdl' 'https://apps.correios.com.br/SigepMasterJPA/AtendeClienteService/AtendeCliente?wsdl'
	@curl -o 'correios/wsdls/AtendeCliente-test.wsdl' 'https://apphom.correios.com.br/SigepMasterJPA/AtendeClienteService/AtendeCliente?wsdl'
	@curl -o 'correios/wsdls/Rastro.wsdl' 'https://webservice.correios.com.br/service/rastro/Rastro.wsdl'
	@curl -o 'correios/wsdls/CalcPrecoPrazo.asmx' 'http://ws.correios.com.br/calculador/CalcPrecoPrazo.asmx?WSDL'
	@curl -o 'correios/wsdls/Rastro_schema1.xsd' 'https://webservice.correios.com.br/service/rastro/Rastro_schema1.xsd'
