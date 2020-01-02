<?xml version="1.0" encoding="utf-8"?>
<wsdl:definitions xmlns:s="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://schemas.xmlsoap.org/wsdl/soap12/" xmlns:http="http://schemas.xmlsoap.org/wsdl/http/" xmlns:mime="http://schemas.xmlsoap.org/wsdl/mime/" xmlns:tns="http://tempuri.org/" xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/" xmlns:tm="http://microsoft.com/wsdl/mime/textMatching/" xmlns:soapenc="http://schemas.xmlsoap.org/soap/encoding/" targetNamespace="http://tempuri.org/" xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/">
  <wsdl:types>
    <s:schema elementFormDefault="qualified" targetNamespace="http://tempuri.org/">
      <s:element name="CalcPrecoPrazo">
        <s:complexType>
          <s:sequence>
            <s:element minOccurs="0" maxOccurs="1" name="nCdEmpresa" type="s:string" />
            <s:element minOccurs="0" maxOccurs="1" name="sDsSenha" type="s:string" />
            <s:element minOccurs="0" maxOccurs="1" name="nCdServico" type="s:string" />
            <s:element minOccurs="0" maxOccurs="1" name="sCepOrigem" type="s:string" />
            <s:element minOccurs="0" maxOccurs="1" name="sCepDestino" type="s:string" />
            <s:element minOccurs="0" maxOccurs="1" name="nVlPeso" type="s:string" />
            <s:element minOccurs="1" maxOccurs="1" name="nCdFormato" type="s:int" />
            <s:element minOccurs="1" maxOccurs="1" name="nVlComprimento" type="s:decimal" />
            <s:element minOccurs="1" maxOccurs="1" name="nVlAltura" type="s:decimal" />
            <s:element minOccurs="1" maxOccurs="1" name="nVlLargura" type="s:decimal" />
            <s:element minOccurs="1" maxOccurs="1" name="nVlDiametro" type="s:decimal" />
            <s:element minOccurs="0" maxOccurs="1" name="sCdMaoPropria" type="s:string" />
            <s:element minOccurs="1" maxOccurs="1" name="nVlValorDeclarado" type="s:decimal" />
            <s:element minOccurs="0" maxOccurs="1" name="sCdAvisoRecebimento" type="s:string" />
          </s:sequence>
        </s:complexType>
      </s:element>
      <s:element name="CalcPrecoPrazoResponse">
        <s:complexType>
          <s:sequence>
            <s:element minOccurs="1" maxOccurs="1" name="CalcPrecoPrazoResult" type="tns:cResultado" />
          </s:sequence>
        </s:complexType>
      </s:element>
      <s:complexType name="cResultado">
        <s:sequence>
          <s:element minOccurs="0" maxOccurs="1" name="Servicos" type="tns:ArrayOfCServico" />
        </s:sequence>
      </s:complexType>
      <s:complexType name="ArrayOfCServico">
        <s:sequence>
          <s:element minOccurs="0" maxOccurs="unbounded" name="cServico" type="tns:cServico" />
        </s:sequence>
      </s:complexType>
      <s:complexType name="cServico">
        <s:sequence>
          <s:element minOccurs="1" maxOccurs="1" name="Codigo" type="s:int" />
          <s:element minOccurs="0" maxOccurs="1" name="Valor" type="s:string" />
          <s:element minOccurs="0" maxOccurs="1" name="PrazoEntrega" type="s:string" />
          <s:element minOccurs="0" maxOccurs="1" name="ValorMaoPropria" type="s:string" />
          <s:element minOccurs="0" maxOccurs="1" name="ValorAvisoRecebimento" type="s:string" />
          <s:element minOccurs="0" maxOccurs="1" name="ValorValorDeclarado" type="s:string" />
          <s:element minOccurs="0" maxOccurs="1" name="EntregaDomiciliar" type="s:string" />
          <s:element minOccurs="0" maxOccurs="1" name="EntregaSabado" type="s:string" />
          <s:element minOccurs="0" maxOccurs="1" name="Erro" type="s:string" />
          <s:element minOccurs="0" maxOccurs="1" name="MsgErro" type="s:string" />
          <s:element minOccurs="0" maxOccurs="1" name="ValorSemAdicionais" type="s:string" />
          <s:element minOccurs="0" maxOccurs="1" name="obsFim" type="s:string" />
          <s:element minOccurs="0" maxOccurs="1" name="DataMaxEntrega" type="s:string" />
          <s:element minOccurs="0" maxOccurs="1" name="HoraMaxEntrega" type="s:string" />
        </s:sequence>
      </s:complexType>
      <s:element name="CalcPrecoPrazoData">
        <s:complexType>
          <s:sequence>
            <s:element minOccurs="0" maxOccurs="1" name="nCdEmpresa" type="s:string" />
            <s:element minOccurs="0" maxOccurs="1" name="sDsSenha" type="s:string" />
            <s:element minOccurs="0" maxOccurs="1" name="nCdServico" type="s:string" />
            <s:element minOccurs="0" maxOccurs="1" name="sCepOrigem" type="s:string" />
            <s:element minOccurs="0" maxOccurs="1" name="sCepDestino" type="s:string" />
            <s:element minOccurs="0" maxOccurs="1" name="nVlPeso" type="s:string" />
            <s:element minOccurs="1" maxOccurs="1" name="nCdFormato" type="s:int" />
            <s:element minOccurs="1" maxOccurs="1" name="nVlComprimento" type="s:decimal" />
            <s:element minOccurs="1" maxOccurs="1" name="nVlAltura" type="s:decimal" />
            <s:element minOccurs="1" maxOccurs="1" name="nVlLargura" type="s:decimal" />
            <s:element minOccurs="1" maxOccurs="1" name="nVlDiametro" type="s:decimal" />
            <s:element minOccurs="0" maxOccurs="1" name="sCdMaoPropria" type="s:string" />
            <s:element minOccurs="1" maxOccurs="1" name="nVlValorDeclarado" type="s:decimal" />
            <s:element minOccurs="0" maxOccurs="1" name="sCdAvisoRecebimento" type="s:string" />
            <s:element minOccurs="0" maxOccurs="1" name="sDtCalculo" type="s:string" />
          </s:sequence>
        </s:complexType>
      </s:element>
      <s:element name="CalcPrecoPrazoDataResponse">
        <s:complexType>
          <s:sequence>
            <s:element minOccurs="1" maxOccurs="1" name="CalcPrecoPrazoDataResult" type="tns:cResultado" />
          </s:sequence>
        </s:complexType>
      </s:element>
      <s:element name="CalcPrecoPrazoRestricao">
        <s:complexType>
          <s:sequence>
            <s:element minOccurs="0" maxOccurs="1" name="nCdEmpresa" type="s:string" />
            <s:element minOccurs="0" maxOccurs="1" name="sDsSenha" type="s:string" />
            <s:element minOccurs="0" maxOccurs="1" name="nCdServico" type="s:string" />
            <s:element minOccurs="0" maxOccurs="1" name="sCepOrigem" type="s:string" />
            <s:element minOccurs="0" maxOccurs="1" name="sCepDestino" type="s:string" />
            <s:element minOccurs="0" maxOccurs="1" name="nVlPeso" type="s:string" />
            <s:element minOccurs="1" maxOccurs="1" name="nCdFormato" type="s:int" />
            <s:element minOccurs="1" maxOccurs="1" name="nVlComprimento" type="s:decimal" />
            <s:element minOccurs="1" maxOccurs="1" name="nVlAltura" type="s:decimal" />
            <s:element minOccurs="1" maxOccurs="1" name="nVlLargura" type="s:decimal" />
            <s:element minOccurs="1" maxOccurs="1" name="nVlDiametro" type="s:decimal" />
            <s:element minOccurs="0" maxOccurs="1" name="sCdMaoPropria" type="s:string" />
            <s:element minOccurs="1" maxOccurs="1" name="nVlValorDeclarado" type="s:decimal" />
            <s:element minOccurs="0" maxOccurs="1" name="sCdAvisoRecebimento" type="s:string" />
            <s:element minOccurs="0" maxOccurs="1" name="sDtCalculo" type="s:string" />
          </s:sequence>
        </s:complexType>
      </s:element>
      <s:element name="CalcPrecoPrazoRestricaoResponse">
        <s:complexType>
          <s:sequence>
            <s:element minOccurs="1" maxOccurs="1" name="CalcPrecoPrazoRestricaoResult" type="tns:cResultado" />
          </s:sequence>
        </s:complexType>
      </s:element>
      <s:element name="CalcPreco">
        <s:complexType>
          <s:sequence>
            <s:element minOccurs="0" maxOccurs="1" name="nCdEmpresa" type="s:string" />
            <s:element minOccurs="0" maxOccurs="1" name="sDsSenha" type="s:string" />
            <s:element minOccurs="0" maxOccurs="1" name="nCdServico" type="s:string" />
            <s:element minOccurs="0" maxOccurs="1" name="sCepOrigem" type="s:string" />
            <s:element minOccurs="0" maxOccurs="1" name="sCepDestino" type="s:string" />
            <s:element minOccurs="0" maxOccurs="1" name="nVlPeso" type="s:string" />
            <s:element minOccurs="1" maxOccurs="1" name="nCdFormato" type="s:int" />
            <s:element minOccurs="1" maxOccurs="1" name="nVlComprimento" type="s:decimal" />
            <s:element minOccurs="1" maxOccurs="1" name="nVlAltura" type="s:decimal" />
            <s:element minOccurs="1" maxOccurs="1" name="nVlLargura" type="s:decimal" />
            <s:element minOccurs="1" maxOccurs="1" name="nVlDiametro" type="s:decimal" />
            <s:element minOccurs="0" maxOccurs="1" name="sCdMaoPropria" type="s:string" />
            <s:element minOccurs="1" maxOccurs="1" name="nVlValorDeclarado" type="s:decimal" />
            <s:element minOccurs="0" maxOccurs="1" name="sCdAvisoRecebimento" type="s:string" />
          </s:sequence>
        </s:complexType>
      </s:element>
      <s:element name="CalcPrecoResponse">
        <s:complexType>
          <s:sequence>
            <s:element minOccurs="1" maxOccurs="1" name="CalcPrecoResult" type="tns:cResultado" />
          </s:sequence>
        </s:complexType>
      </s:element>
      <s:element name="CalcPrecoData">
        <s:complexType>
          <s:sequence>
            <s:element minOccurs="0" maxOccurs="1" name="nCdEmpresa" type="s:string" />
            <s:element minOccurs="0" maxOccurs="1" name="sDsSenha" type="s:string" />
            <s:element minOccurs="0" maxOccurs="1" name="nCdServico" type="s:string" />
            <s:element minOccurs="0" maxOccurs="1" name="sCepOrigem" type="s:string" />
            <s:element minOccurs="0" maxOccurs="1" name="sCepDestino" type="s:string" />
            <s:element minOccurs="0" maxOccurs="1" name="nVlPeso" type="s:string" />
            <s:element minOccurs="1" maxOccurs="1" name="nCdFormato" type="s:int" />
            <s:element minOccurs="1" maxOccurs="1" name="nVlComprimento" type="s:decimal" />
            <s:element minOccurs="1" maxOccurs="1" name="nVlAltura" type="s:decimal" />
            <s:element minOccurs="1" maxOccurs="1" name="nVlLargura" type="s:decimal" />
            <s:element minOccurs="1" maxOccurs="1" name="nVlDiametro" type="s:decimal" />
            <s:element minOccurs="0" maxOccurs="1" name="sCdMaoPropria" type="s:string" />
            <s:element minOccurs="1" maxOccurs="1" name="nVlValorDeclarado" type="s:decimal" />
            <s:element minOccurs="0" maxOccurs="1" name="sCdAvisoRecebimento" type="s:string" />
            <s:element minOccurs="0" maxOccurs="1" name="sDtCalculo" type="s:string" />
          </s:sequence>
        </s:complexType>
      </s:element>
      <s:element name="CalcPrecoDataResponse">
        <s:complexType>
          <s:sequence>
            <s:element minOccurs="1" maxOccurs="1" name="CalcPrecoDataResult" type="tns:cResultado" />
          </s:sequence>
        </s:complexType>
      </s:element>
      <s:element name="CalcPrazo">
        <s:complexType>
          <s:sequence>
            <s:element minOccurs="0" maxOccurs="1" name="nCdServico" type="s:string" />
            <s:element minOccurs="0" maxOccurs="1" name="sCepOrigem" type="s:string" />
            <s:element minOccurs="0" maxOccurs="1" name="sCepDestino" type="s:string" />
          </s:sequence>
        </s:complexType>
      </s:element>
      <s:element name="CalcPrazoResponse">
        <s:complexType>
          <s:sequence>
            <s:element minOccurs="1" maxOccurs="1" name="CalcPrazoResult" type="tns:cResultado" />
          </s:sequence>
        </s:complexType>
      </s:element>
      <s:element name="CalcPrazoData">
        <s:complexType>
          <s:sequence>
            <s:element minOccurs="0" maxOccurs="1" name="nCdServico" type="s:string" />
            <s:element minOccurs="0" maxOccurs="1" name="sCepOrigem" type="s:string" />
            <s:element minOccurs="0" maxOccurs="1" name="sCepDestino" type="s:string" />
            <s:element minOccurs="0" maxOccurs="1" name="sDtCalculo" type="s:string" />
          </s:sequence>
        </s:complexType>
      </s:element>
      <s:element name="CalcPrazoDataResponse">
        <s:complexType>
          <s:sequence>
            <s:element minOccurs="1" maxOccurs="1" name="CalcPrazoDataResult" type="tns:cResultado" />
          </s:sequence>
        </s:complexType>
      </s:element>
      <s:element name="CalcPrazoRestricao">
        <s:complexType>
          <s:sequence>
            <s:element minOccurs="0" maxOccurs="1" name="nCdServico" type="s:string" />
            <s:element minOccurs="0" maxOccurs="1" name="sCepOrigem" type="s:string" />
            <s:element minOccurs="0" maxOccurs="1" name="sCepDestino" type="s:string" />
            <s:element minOccurs="0" maxOccurs="1" name="sDtCalculo" type="s:string" />
          </s:sequence>
        </s:complexType>
      </s:element>
      <s:element name="CalcPrazoRestricaoResponse">
        <s:complexType>
          <s:sequence>
            <s:element minOccurs="1" maxOccurs="1" name="CalcPrazoRestricaoResult" type="tns:cResultado" />
          </s:sequence>
        </s:complexType>
      </s:element>
      <s:element name="CalcPrecoFAC">
        <s:complexType>
          <s:sequence>
            <s:element minOccurs="0" maxOccurs="1" name="nCdServico" type="s:string" />
            <s:element minOccurs="0" maxOccurs="1" name="nVlPeso" type="s:string" />
            <s:element minOccurs="0" maxOccurs="1" name="strDataCalculo" type="s:string" />
          </s:sequence>
        </s:complexType>
      </s:element>
      <s:element name="CalcPrecoFACResponse">
        <s:complexType>
          <s:sequence>
            <s:element minOccurs="1" maxOccurs="1" name="CalcPrecoFACResult" type="tns:cResultado" />
          </s:sequence>
        </s:complexType>
      </s:element>
      <s:element name="CalcDataMaxima">
        <s:complexType>
          <s:sequence>
            <s:element minOccurs="0" maxOccurs="1" name="codigoObjeto" type="s:string" />
          </s:sequence>
        </s:complexType>
      </s:element>
      <s:element name="CalcDataMaximaResponse">
        <s:complexType>
          <s:sequence>
            <s:element minOccurs="1" maxOccurs="1" name="CalcDataMaximaResult" type="tns:cResultadoObjeto" />
          </s:sequence>
        </s:complexType>
      </s:element>
      <s:complexType name="cResultadoObjeto">
        <s:sequence>
          <s:element minOccurs="0" maxOccurs="1" name="Objetos" type="tns:ArrayOfCObjeto" />
        </s:sequence>
      </s:complexType>
      <s:complexType name="ArrayOfCObjeto">
        <s:sequence>
          <s:element minOccurs="0" maxOccurs="unbounded" name="cObjeto" type="tns:cObjeto" />
        </s:sequence>
      </s:complexType>
      <s:complexType name="cObjeto">
        <s:sequence>
          <s:element minOccurs="0" maxOccurs="1" name="codigo" type="s:string" />
          <s:element minOccurs="0" maxOccurs="1" name="servico" type="s:string" />
          <s:element minOccurs="0" maxOccurs="1" name="cepOrigem" type="s:string" />
          <s:element minOccurs="0" maxOccurs="1" name="cepDestino" type="s:string" />
          <s:element minOccurs="1" maxOccurs="1" name="prazoEntrega" type="s:int" />
          <s:element minOccurs="0" maxOccurs="1" name="dataPostagem" type="s:string" />
          <s:element minOccurs="0" maxOccurs="1" name="dataPostagemCalculo" type="s:string" />
          <s:element minOccurs="0" maxOccurs="1" name="dataMaxEntrega" type="s:string" />
          <s:element minOccurs="0" maxOccurs="1" name="postagemDH" type="s:string" />
          <s:element minOccurs="0" maxOccurs="1" name="dataUltimoEvento" type="s:string" />
          <s:element minOccurs="0" maxOccurs="1" name="codigoUltimoEvento" type="s:string" />
          <s:element minOccurs="0" maxOccurs="1" name="tipoUltimoEvento" type="s:string" />
          <s:element minOccurs="0" maxOccurs="1" name="descricaoUltimoEvento" type="s:string" />
          <s:element minOccurs="0" maxOccurs="1" name="erro" type="s:string" />
          <s:element minOccurs="0" maxOccurs="1" name="msgErro" type="s:string" />
          <s:element minOccurs="0" maxOccurs="1" name="nuTicket" type="s:string" />
          <s:element minOccurs="0" maxOccurs="1" name="formaPagamento" type="s:string" />
          <s:element minOccurs="0" maxOccurs="1" name="valorPagamento" type="s:string" />
          <s:element minOccurs="0" maxOccurs="1" name="nuContrato" type="s:string" />
          <s:element minOccurs="0" maxOccurs="1" name="nuCartaoPostagem" type="s:string" />
        </s:sequence>
      </s:complexType>
      <s:element name="ListaServicos">
        <s:complexType />
      </s:element>
      <s:element name="ListaServicosResponse">
        <s:complexType>
          <s:sequence>
            <s:element minOccurs="1" maxOccurs="1" name="ListaServicosResult" type="tns:cResultadoServicos" />
          </s:sequence>
        </s:complexType>
      </s:element>
      <s:complexType name="cResultadoServicos">
        <s:sequence>
          <s:element minOccurs="0" maxOccurs="1" name="ServicosCalculo" type="tns:ArrayOfCServicosCalculo" />
        </s:sequence>
      </s:complexType>
      <s:complexType name="ArrayOfCServicosCalculo">
        <s:sequence>
          <s:element minOccurs="0" maxOccurs="unbounded" name="cServicosCalculo" type="tns:cServicosCalculo" />
        </s:sequence>
      </s:complexType>
      <s:complexType name="cServicosCalculo">
        <s:sequence>
          <s:element minOccurs="0" maxOccurs="1" name="codigo" type="s:string" />
          <s:element minOccurs="0" maxOccurs="1" name="descricao" type="s:string" />
          <s:element minOccurs="0" maxOccurs="1" name="calcula_preco" type="s:string" />
          <s:element minOccurs="0" maxOccurs="1" name="calcula_prazo" type="s:string" />
          <s:element minOccurs="0" maxOccurs="1" name="erro" type="s:string" />
          <s:element minOccurs="0" maxOccurs="1" name="msgErro" type="s:string" />
        </s:sequence>
      </s:complexType>
      <s:element name="ListaServicosSTAR">
        <s:complexType />
      </s:element>
      <s:element name="ListaServicosSTARResponse">
        <s:complexType>
          <s:sequence>
            <s:element minOccurs="1" maxOccurs="1" name="ListaServicosSTARResult" type="tns:cResultadoServicos" />
          </s:sequence>
        </s:complexType>
      </s:element>
      <s:element name="VerificaModal">
        <s:complexType>
          <s:sequence>
            <s:element minOccurs="0" maxOccurs="1" name="nCdServico" type="s:string" />
            <s:element minOccurs="0" maxOccurs="1" name="sCepOrigem" type="s:string" />
            <s:element minOccurs="0" maxOccurs="1" name="sCepDestino" type="s:string" />
          </s:sequence>
        </s:complexType>
      </s:element>
      <s:element name="VerificaModalResponse">
        <s:complexType>
          <s:sequence>
            <s:element minOccurs="1" maxOccurs="1" name="VerificaModalResult" type="tns:cResultadoModal" />
          </s:sequence>
        </s:complexType>
      </s:element>
      <s:complexType name="cResultadoModal">
        <s:sequence>
          <s:element minOccurs="0" maxOccurs="1" name="ServicosModal" type="tns:ArrayOfCModal" />
        </s:sequence>
      </s:complexType>
      <s:complexType name="ArrayOfCModal">
        <s:sequence>
          <s:element minOccurs="0" maxOccurs="unbounded" name="cModal" type="tns:cModal" />
        </s:sequence>
      </s:complexType>
      <s:complexType name="cModal">
        <s:sequence>
          <s:element minOccurs="0" maxOccurs="1" name="codigo" type="s:string" />
          <s:element minOccurs="0" maxOccurs="1" name="modal" type="s:string" />
          <s:element minOccurs="0" maxOccurs="1" name="obs" type="s:string" />
        </s:sequence>
      </s:complexType>
      <s:element name="getVersao">
        <s:complexType />
      </s:element>
      <s:element name="getVersaoResponse">
        <s:complexType>
          <s:sequence>
            <s:element minOccurs="1" maxOccurs="1" name="getVersaoResult" type="tns:versao" />
          </s:sequence>
        </s:complexType>
      </s:element>
      <s:complexType name="versao">
        <s:sequence>
          <s:element minOccurs="0" maxOccurs="1" name="versaoAtual" type="s:string" />
        </s:sequence>
      </s:complexType>
      <s:element name="cResultado" type="tns:cResultado" />
      <s:element name="cResultadoObjeto" type="tns:cResultadoObjeto" />
      <s:element name="cResultadoServicos" type="tns:cResultadoServicos" />
      <s:element name="cResultadoModal" type="tns:cResultadoModal" />
      <s:element name="versao" type="tns:versao" />
    </s:schema>
  </wsdl:types>
  <wsdl:message name="CalcPrecoPrazoSoapIn">
    <wsdl:part name="parameters" element="tns:CalcPrecoPrazo" />
  </wsdl:message>
  <wsdl:message name="CalcPrecoPrazoSoapOut">
    <wsdl:part name="parameters" element="tns:CalcPrecoPrazoResponse" />
  </wsdl:message>
  <wsdl:message name="CalcPrecoPrazoDataSoapIn">
    <wsdl:part name="parameters" element="tns:CalcPrecoPrazoData" />
  </wsdl:message>
  <wsdl:message name="CalcPrecoPrazoDataSoapOut">
    <wsdl:part name="parameters" element="tns:CalcPrecoPrazoDataResponse" />
  </wsdl:message>
  <wsdl:message name="CalcPrecoPrazoRestricaoSoapIn">
    <wsdl:part name="parameters" element="tns:CalcPrecoPrazoRestricao" />
  </wsdl:message>
  <wsdl:message name="CalcPrecoPrazoRestricaoSoapOut">
    <wsdl:part name="parameters" element="tns:CalcPrecoPrazoRestricaoResponse" />
  </wsdl:message>
  <wsdl:message name="CalcPrecoSoapIn">
    <wsdl:part name="parameters" element="tns:CalcPreco" />
  </wsdl:message>
  <wsdl:message name="CalcPrecoSoapOut">
    <wsdl:part name="parameters" element="tns:CalcPrecoResponse" />
  </wsdl:message>
  <wsdl:message name="CalcPrecoDataSoapIn">
    <wsdl:part name="parameters" element="tns:CalcPrecoData" />
  </wsdl:message>
  <wsdl:message name="CalcPrecoDataSoapOut">
    <wsdl:part name="parameters" element="tns:CalcPrecoDataResponse" />
  </wsdl:message>
  <wsdl:message name="CalcPrazoSoapIn">
    <wsdl:part name="parameters" element="tns:CalcPrazo" />
  </wsdl:message>
  <wsdl:message name="CalcPrazoSoapOut">
    <wsdl:part name="parameters" element="tns:CalcPrazoResponse" />
  </wsdl:message>
  <wsdl:message name="CalcPrazoDataSoapIn">
    <wsdl:part name="parameters" element="tns:CalcPrazoData" />
  </wsdl:message>
  <wsdl:message name="CalcPrazoDataSoapOut">
    <wsdl:part name="parameters" element="tns:CalcPrazoDataResponse" />
  </wsdl:message>
  <wsdl:message name="CalcPrazoRestricaoSoapIn">
    <wsdl:part name="parameters" element="tns:CalcPrazoRestricao" />
  </wsdl:message>
  <wsdl:message name="CalcPrazoRestricaoSoapOut">
    <wsdl:part name="parameters" element="tns:CalcPrazoRestricaoResponse" />
  </wsdl:message>
  <wsdl:message name="CalcPrecoFACSoapIn">
    <wsdl:part name="parameters" element="tns:CalcPrecoFAC" />
  </wsdl:message>
  <wsdl:message name="CalcPrecoFACSoapOut">
    <wsdl:part name="parameters" element="tns:CalcPrecoFACResponse" />
  </wsdl:message>
  <wsdl:message name="CalcDataMaximaSoapIn">
    <wsdl:part name="parameters" element="tns:CalcDataMaxima" />
  </wsdl:message>
  <wsdl:message name="CalcDataMaximaSoapOut">
    <wsdl:part name="parameters" element="tns:CalcDataMaximaResponse" />
  </wsdl:message>
  <wsdl:message name="ListaServicosSoapIn">
    <wsdl:part name="parameters" element="tns:ListaServicos" />
  </wsdl:message>
  <wsdl:message name="ListaServicosSoapOut">
    <wsdl:part name="parameters" element="tns:ListaServicosResponse" />
  </wsdl:message>
  <wsdl:message name="ListaServicosSTARSoapIn">
    <wsdl:part name="parameters" element="tns:ListaServicosSTAR" />
  </wsdl:message>
  <wsdl:message name="ListaServicosSTARSoapOut">
    <wsdl:part name="parameters" element="tns:ListaServicosSTARResponse" />
  </wsdl:message>
  <wsdl:message name="VerificaModalSoapIn">
    <wsdl:part name="parameters" element="tns:VerificaModal" />
  </wsdl:message>
  <wsdl:message name="VerificaModalSoapOut">
    <wsdl:part name="parameters" element="tns:VerificaModalResponse" />
  </wsdl:message>
  <wsdl:message name="getVersaoSoapIn">
    <wsdl:part name="parameters" element="tns:getVersao" />
  </wsdl:message>
  <wsdl:message name="getVersaoSoapOut">
    <wsdl:part name="parameters" element="tns:getVersaoResponse" />
  </wsdl:message>
  <wsdl:message name="CalcPrecoPrazoHttpGetIn">
    <wsdl:part name="nCdEmpresa" type="s:string" />
    <wsdl:part name="sDsSenha" type="s:string" />
    <wsdl:part name="nCdServico" type="s:string" />
    <wsdl:part name="sCepOrigem" type="s:string" />
    <wsdl:part name="sCepDestino" type="s:string" />
    <wsdl:part name="nVlPeso" type="s:string" />
    <wsdl:part name="nCdFormato" type="s:string" />
    <wsdl:part name="nVlComprimento" type="s:string" />
    <wsdl:part name="nVlAltura" type="s:string" />
    <wsdl:part name="nVlLargura" type="s:string" />
    <wsdl:part name="nVlDiametro" type="s:string" />
    <wsdl:part name="sCdMaoPropria" type="s:string" />
    <wsdl:part name="nVlValorDeclarado" type="s:string" />
    <wsdl:part name="sCdAvisoRecebimento" type="s:string" />
  </wsdl:message>
  <wsdl:message name="CalcPrecoPrazoHttpGetOut">
    <wsdl:part name="Body" element="tns:cResultado" />
  </wsdl:message>
  <wsdl:message name="CalcPrecoPrazoDataHttpGetIn">
    <wsdl:part name="nCdEmpresa" type="s:string" />
    <wsdl:part name="sDsSenha" type="s:string" />
    <wsdl:part name="nCdServico" type="s:string" />
    <wsdl:part name="sCepOrigem" type="s:string" />
    <wsdl:part name="sCepDestino" type="s:string" />
    <wsdl:part name="nVlPeso" type="s:string" />
    <wsdl:part name="nCdFormato" type="s:string" />
    <wsdl:part name="nVlComprimento" type="s:string" />
    <wsdl:part name="nVlAltura" type="s:string" />
    <wsdl:part name="nVlLargura" type="s:string" />
    <wsdl:part name="nVlDiametro" type="s:string" />
    <wsdl:part name="sCdMaoPropria" type="s:string" />
    <wsdl:part name="nVlValorDeclarado" type="s:string" />
    <wsdl:part name="sCdAvisoRecebimento" type="s:string" />
    <wsdl:part name="sDtCalculo" type="s:string" />
  </wsdl:message>
  <wsdl:message name="CalcPrecoPrazoDataHttpGetOut">
    <wsdl:part name="Body" element="tns:cResultado" />
  </wsdl:message>
  <wsdl:message name="CalcPrecoPrazoRestricaoHttpGetIn">
    <wsdl:part name="nCdEmpresa" type="s:string" />
    <wsdl:part name="sDsSenha" type="s:string" />
    <wsdl:part name="nCdServico" type="s:string" />
    <wsdl:part name="sCepOrigem" type="s:string" />
    <wsdl:part name="sCepDestino" type="s:string" />
    <wsdl:part name="nVlPeso" type="s:string" />
    <wsdl:part name="nCdFormato" type="s:string" />
    <wsdl:part name="nVlComprimento" type="s:string" />
    <wsdl:part name="nVlAltura" type="s:string" />
    <wsdl:part name="nVlLargura" type="s:string" />
    <wsdl:part name="nVlDiametro" type="s:string" />
    <wsdl:part name="sCdMaoPropria" type="s:string" />
    <wsdl:part name="nVlValorDeclarado" type="s:string" />
    <wsdl:part name="sCdAvisoRecebimento" type="s:string" />
    <wsdl:part name="sDtCalculo" type="s:string" />
  </wsdl:message>
  <wsdl:message name="CalcPrecoPrazoRestricaoHttpGetOut">
    <wsdl:part name="Body" element="tns:cResultado" />
  </wsdl:message>
  <wsdl:message name="CalcPrecoHttpGetIn">
    <wsdl:part name="nCdEmpresa" type="s:string" />
    <wsdl:part name="sDsSenha" type="s:string" />
    <wsdl:part name="nCdServico" type="s:string" />
    <wsdl:part name="sCepOrigem" type="s:string" />
    <wsdl:part name="sCepDestino" type="s:string" />
    <wsdl:part name="nVlPeso" type="s:string" />
    <wsdl:part name="nCdFormato" type="s:string" />
    <wsdl:part name="nVlComprimento" type="s:string" />
    <wsdl:part name="nVlAltura" type="s:string" />
    <wsdl:part name="nVlLargura" type="s:string" />
    <wsdl:part name="nVlDiametro" type="s:string" />
    <wsdl:part name="sCdMaoPropria" type="s:string" />
    <wsdl:part name="nVlValorDeclarado" type="s:string" />
    <wsdl:part name="sCdAvisoRecebimento" type="s:string" />
  </wsdl:message>
  <wsdl:message name="CalcPrecoHttpGetOut">
    <wsdl:part name="Body" element="tns:cResultado" />
  </wsdl:message>
  <wsdl:message name="CalcPrecoDataHttpGetIn">
    <wsdl:part name="nCdEmpresa" type="s:string" />
    <wsdl:part name="sDsSenha" type="s:string" />
    <wsdl:part name="nCdServico" type="s:string" />
    <wsdl:part name="sCepOrigem" type="s:string" />
    <wsdl:part name="sCepDestino" type="s:string" />
    <wsdl:part name="nVlPeso" type="s:string" />
    <wsdl:part name="nCdFormato" type="s:string" />
    <wsdl:part name="nVlComprimento" type="s:string" />
    <wsdl:part name="nVlAltura" type="s:string" />
    <wsdl:part name="nVlLargura" type="s:string" />
    <wsdl:part name="nVlDiametro" type="s:string" />
    <wsdl:part name="sCdMaoPropria" type="s:string" />
    <wsdl:part name="nVlValorDeclarado" type="s:string" />
    <wsdl:part name="sCdAvisoRecebimento" type="s:string" />
    <wsdl:part name="sDtCalculo" type="s:string" />
  </wsdl:message>
  <wsdl:message name="CalcPrecoDataHttpGetOut">
    <wsdl:part name="Body" element="tns:cResultado" />
  </wsdl:message>
  <wsdl:message name="CalcPrazoHttpGetIn">
    <wsdl:part name="nCdServico" type="s:string" />
    <wsdl:part name="sCepOrigem" type="s:string" />
    <wsdl:part name="sCepDestino" type="s:string" />
  </wsdl:message>
  <wsdl:message name="CalcPrazoHttpGetOut">
    <wsdl:part name="Body" element="tns:cResultado" />
  </wsdl:message>
  <wsdl:message name="CalcPrazoDataHttpGetIn">
    <wsdl:part name="nCdServico" type="s:string" />
    <wsdl:part name="sCepOrigem" type="s:string" />
    <wsdl:part name="sCepDestino" type="s:string" />
    <wsdl:part name="sDtCalculo" type="s:string" />
  </wsdl:message>
  <wsdl:message name="CalcPrazoDataHttpGetOut">
    <wsdl:part name="Body" element="tns:cResultado" />
  </wsdl:message>
  <wsdl:message name="CalcPrazoRestricaoHttpGetIn">
    <wsdl:part name="nCdServico" type="s:string" />
    <wsdl:part name="sCepOrigem" type="s:string" />
    <wsdl:part name="sCepDestino" type="s:string" />
    <wsdl:part name="sDtCalculo" type="s:string" />
  </wsdl:message>
  <wsdl:message name="CalcPrazoRestricaoHttpGetOut">
    <wsdl:part name="Body" element="tns:cResultado" />
  </wsdl:message>
  <wsdl:message name="CalcPrecoFACHttpGetIn">
    <wsdl:part name="nCdServico" type="s:string" />
    <wsdl:part name="nVlPeso" type="s:string" />
    <wsdl:part name="strDataCalculo" type="s:string" />
  </wsdl:message>
  <wsdl:message name="CalcPrecoFACHttpGetOut">
    <wsdl:part name="Body" element="tns:cResultado" />
  </wsdl:message>
  <wsdl:message name="CalcDataMaximaHttpGetIn">
    <wsdl:part name="codigoObjeto" type="s:string" />
  </wsdl:message>
  <wsdl:message name="CalcDataMaximaHttpGetOut">
    <wsdl:part name="Body" element="tns:cResultadoObjeto" />
  </wsdl:message>
  <wsdl:message name="ListaServicosHttpGetIn" />
  <wsdl:message name="ListaServicosHttpGetOut">
    <wsdl:part name="Body" element="tns:cResultadoServicos" />
  </wsdl:message>
  <wsdl:message name="ListaServicosSTARHttpGetIn" />
  <wsdl:message name="ListaServicosSTARHttpGetOut">
    <wsdl:part name="Body" element="tns:cResultadoServicos" />
  </wsdl:message>
  <wsdl:message name="VerificaModalHttpGetIn">
    <wsdl:part name="nCdServico" type="s:string" />
    <wsdl:part name="sCepOrigem" type="s:string" />
    <wsdl:part name="sCepDestino" type="s:string" />
  </wsdl:message>
  <wsdl:message name="VerificaModalHttpGetOut">
    <wsdl:part name="Body" element="tns:cResultadoModal" />
  </wsdl:message>
  <wsdl:message name="getVersaoHttpGetIn" />
  <wsdl:message name="getVersaoHttpGetOut">
    <wsdl:part name="Body" element="tns:versao" />
  </wsdl:message>
  <wsdl:message name="CalcPrecoPrazoHttpPostIn">
    <wsdl:part name="nCdEmpresa" type="s:string" />
    <wsdl:part name="sDsSenha" type="s:string" />
    <wsdl:part name="nCdServico" type="s:string" />
    <wsdl:part name="sCepOrigem" type="s:string" />
    <wsdl:part name="sCepDestino" type="s:string" />
    <wsdl:part name="nVlPeso" type="s:string" />
    <wsdl:part name="nCdFormato" type="s:string" />
    <wsdl:part name="nVlComprimento" type="s:string" />
    <wsdl:part name="nVlAltura" type="s:string" />
    <wsdl:part name="nVlLargura" type="s:string" />
    <wsdl:part name="nVlDiametro" type="s:string" />
    <wsdl:part name="sCdMaoPropria" type="s:string" />
    <wsdl:part name="nVlValorDeclarado" type="s:string" />
    <wsdl:part name="sCdAvisoRecebimento" type="s:string" />
  </wsdl:message>
  <wsdl:message name="CalcPrecoPrazoHttpPostOut">
    <wsdl:part name="Body" element="tns:cResultado" />
  </wsdl:message>
  <wsdl:message name="CalcPrecoPrazoDataHttpPostIn">
    <wsdl:part name="nCdEmpresa" type="s:string" />
    <wsdl:part name="sDsSenha" type="s:string" />
    <wsdl:part name="nCdServico" type="s:string" />
    <wsdl:part name="sCepOrigem" type="s:string" />
    <wsdl:part name="sCepDestino" type="s:string" />
    <wsdl:part name="nVlPeso" type="s:string" />
    <wsdl:part name="nCdFormato" type="s:string" />
    <wsdl:part name="nVlComprimento" type="s:string" />
    <wsdl:part name="nVlAltura" type="s:string" />
    <wsdl:part name="nVlLargura" type="s:string" />
    <wsdl:part name="nVlDiametro" type="s:string" />
    <wsdl:part name="sCdMaoPropria" type="s:string" />
    <wsdl:part name="nVlValorDeclarado" type="s:string" />
    <wsdl:part name="sCdAvisoRecebimento" type="s:string" />
    <wsdl:part name="sDtCalculo" type="s:string" />
  </wsdl:message>
  <wsdl:message name="CalcPrecoPrazoDataHttpPostOut">
    <wsdl:part name="Body" element="tns:cResultado" />
  </wsdl:message>
  <wsdl:message name="CalcPrecoPrazoRestricaoHttpPostIn">
    <wsdl:part name="nCdEmpresa" type="s:string" />
    <wsdl:part name="sDsSenha" type="s:string" />
    <wsdl:part name="nCdServico" type="s:string" />
    <wsdl:part name="sCepOrigem" type="s:string" />
    <wsdl:part name="sCepDestino" type="s:string" />
    <wsdl:part name="nVlPeso" type="s:string" />
    <wsdl:part name="nCdFormato" type="s:string" />
    <wsdl:part name="nVlComprimento" type="s:string" />
    <wsdl:part name="nVlAltura" type="s:string" />
    <wsdl:part name="nVlLargura" type="s:string" />
    <wsdl:part name="nVlDiametro" type="s:string" />
    <wsdl:part name="sCdMaoPropria" type="s:string" />
    <wsdl:part name="nVlValorDeclarado" type="s:string" />
    <wsdl:part name="sCdAvisoRecebimento" type="s:string" />
    <wsdl:part name="sDtCalculo" type="s:string" />
  </wsdl:message>
  <wsdl:message name="CalcPrecoPrazoRestricaoHttpPostOut">
    <wsdl:part name="Body" element="tns:cResultado" />
  </wsdl:message>
  <wsdl:message name="CalcPrecoHttpPostIn">
    <wsdl:part name="nCdEmpresa" type="s:string" />
    <wsdl:part name="sDsSenha" type="s:string" />
    <wsdl:part name="nCdServico" type="s:string" />
    <wsdl:part name="sCepOrigem" type="s:string" />
    <wsdl:part name="sCepDestino" type="s:string" />
    <wsdl:part name="nVlPeso" type="s:string" />
    <wsdl:part name="nCdFormato" type="s:string" />
    <wsdl:part name="nVlComprimento" type="s:string" />
    <wsdl:part name="nVlAltura" type="s:string" />
    <wsdl:part name="nVlLargura" type="s:string" />
    <wsdl:part name="nVlDiametro" type="s:string" />
    <wsdl:part name="sCdMaoPropria" type="s:string" />
    <wsdl:part name="nVlValorDeclarado" type="s:string" />
    <wsdl:part name="sCdAvisoRecebimento" type="s:string" />
  </wsdl:message>
  <wsdl:message name="CalcPrecoHttpPostOut">
    <wsdl:part name="Body" element="tns:cResultado" />
  </wsdl:message>
  <wsdl:message name="CalcPrecoDataHttpPostIn">
    <wsdl:part name="nCdEmpresa" type="s:string" />
    <wsdl:part name="sDsSenha" type="s:string" />
    <wsdl:part name="nCdServico" type="s:string" />
    <wsdl:part name="sCepOrigem" type="s:string" />
    <wsdl:part name="sCepDestino" type="s:string" />
    <wsdl:part name="nVlPeso" type="s:string" />
    <wsdl:part name="nCdFormato" type="s:string" />
    <wsdl:part name="nVlComprimento" type="s:string" />
    <wsdl:part name="nVlAltura" type="s:string" />
    <wsdl:part name="nVlLargura" type="s:string" />
    <wsdl:part name="nVlDiametro" type="s:string" />
    <wsdl:part name="sCdMaoPropria" type="s:string" />
    <wsdl:part name="nVlValorDeclarado" type="s:string" />
    <wsdl:part name="sCdAvisoRecebimento" type="s:string" />
    <wsdl:part name="sDtCalculo" type="s:string" />
  </wsdl:message>
  <wsdl:message name="CalcPrecoDataHttpPostOut">
    <wsdl:part name="Body" element="tns:cResultado" />
  </wsdl:message>
  <wsdl:message name="CalcPrazoHttpPostIn">
    <wsdl:part name="nCdServico" type="s:string" />
    <wsdl:part name="sCepOrigem" type="s:string" />
    <wsdl:part name="sCepDestino" type="s:string" />
  </wsdl:message>
  <wsdl:message name="CalcPrazoHttpPostOut">
    <wsdl:part name="Body" element="tns:cResultado" />
  </wsdl:message>
  <wsdl:message name="CalcPrazoDataHttpPostIn">
    <wsdl:part name="nCdServico" type="s:string" />
    <wsdl:part name="sCepOrigem" type="s:string" />
    <wsdl:part name="sCepDestino" type="s:string" />
    <wsdl:part name="sDtCalculo" type="s:string" />
  </wsdl:message>
  <wsdl:message name="CalcPrazoDataHttpPostOut">
    <wsdl:part name="Body" element="tns:cResultado" />
  </wsdl:message>
  <wsdl:message name="CalcPrazoRestricaoHttpPostIn">
    <wsdl:part name="nCdServico" type="s:string" />
    <wsdl:part name="sCepOrigem" type="s:string" />
    <wsdl:part name="sCepDestino" type="s:string" />
    <wsdl:part name="sDtCalculo" type="s:string" />
  </wsdl:message>
  <wsdl:message name="CalcPrazoRestricaoHttpPostOut">
    <wsdl:part name="Body" element="tns:cResultado" />
  </wsdl:message>
  <wsdl:message name="CalcPrecoFACHttpPostIn">
    <wsdl:part name="nCdServico" type="s:string" />
    <wsdl:part name="nVlPeso" type="s:string" />
    <wsdl:part name="strDataCalculo" type="s:string" />
  </wsdl:message>
  <wsdl:message name="CalcPrecoFACHttpPostOut">
    <wsdl:part name="Body" element="tns:cResultado" />
  </wsdl:message>
  <wsdl:message name="CalcDataMaximaHttpPostIn">
    <wsdl:part name="codigoObjeto" type="s:string" />
  </wsdl:message>
  <wsdl:message name="CalcDataMaximaHttpPostOut">
    <wsdl:part name="Body" element="tns:cResultadoObjeto" />
  </wsdl:message>
  <wsdl:message name="ListaServicosHttpPostIn" />
  <wsdl:message name="ListaServicosHttpPostOut">
    <wsdl:part name="Body" element="tns:cResultadoServicos" />
  </wsdl:message>
  <wsdl:message name="ListaServicosSTARHttpPostIn" />
  <wsdl:message name="ListaServicosSTARHttpPostOut">
    <wsdl:part name="Body" element="tns:cResultadoServicos" />
  </wsdl:message>
  <wsdl:message name="VerificaModalHttpPostIn">
    <wsdl:part name="nCdServico" type="s:string" />
    <wsdl:part name="sCepOrigem" type="s:string" />
    <wsdl:part name="sCepDestino" type="s:string" />
  </wsdl:message>
  <wsdl:message name="VerificaModalHttpPostOut">
    <wsdl:part name="Body" element="tns:cResultadoModal" />
  </wsdl:message>
  <wsdl:message name="getVersaoHttpPostIn" />
  <wsdl:message name="getVersaoHttpPostOut">
    <wsdl:part name="Body" element="tns:versao" />
  </wsdl:message>
  <wsdl:portType name="CalcPrecoPrazoWSSoap">
    <wsdl:operation name="CalcPrecoPrazo">
      <wsdl:documentation xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/">Calcula o preço e o prazo com a data atual</wsdl:documentation>
      <wsdl:input message="tns:CalcPrecoPrazoSoapIn" />
      <wsdl:output message="tns:CalcPrecoPrazoSoapOut" />
    </wsdl:operation>
    <wsdl:operation name="CalcPrecoPrazoData">
      <wsdl:documentation xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/">Calcula o preço e o prazo com uma data especificada</wsdl:documentation>
      <wsdl:input message="tns:CalcPrecoPrazoDataSoapIn" />
      <wsdl:output message="tns:CalcPrecoPrazoDataSoapOut" />
    </wsdl:operation>
    <wsdl:operation name="CalcPrecoPrazoRestricao">
      <wsdl:documentation xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/">Calcula o preço e o prazo considerando as restrições de entrega</wsdl:documentation>
      <wsdl:input message="tns:CalcPrecoPrazoRestricaoSoapIn" />
      <wsdl:output message="tns:CalcPrecoPrazoRestricaoSoapOut" />
    </wsdl:operation>
    <wsdl:operation name="CalcPreco">
      <wsdl:documentation xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/">Calcula somente o preço com a data atual</wsdl:documentation>
      <wsdl:input message="tns:CalcPrecoSoapIn" />
      <wsdl:output message="tns:CalcPrecoSoapOut" />
    </wsdl:operation>
    <wsdl:operation name="CalcPrecoData">
      <wsdl:documentation xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/">Calcula somente o preço com uma data especificada</wsdl:documentation>
      <wsdl:input message="tns:CalcPrecoDataSoapIn" />
      <wsdl:output message="tns:CalcPrecoDataSoapOut" />
    </wsdl:operation>
    <wsdl:operation name="CalcPrazo">
      <wsdl:documentation xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/">Calcula somente o prazo com a data atual</wsdl:documentation>
      <wsdl:input message="tns:CalcPrazoSoapIn" />
      <wsdl:output message="tns:CalcPrazoSoapOut" />
    </wsdl:operation>
    <wsdl:operation name="CalcPrazoData">
      <wsdl:documentation xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/">Calcula somente o prazo com uma data especificada</wsdl:documentation>
      <wsdl:input message="tns:CalcPrazoDataSoapIn" />
      <wsdl:output message="tns:CalcPrazoDataSoapOut" />
    </wsdl:operation>
    <wsdl:operation name="CalcPrazoRestricao">
      <wsdl:documentation xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/">Calcula o prazo considerando restrição de entrega</wsdl:documentation>
      <wsdl:input message="tns:CalcPrazoRestricaoSoapIn" />
      <wsdl:output message="tns:CalcPrazoRestricaoSoapOut" />
    </wsdl:operation>
    <wsdl:operation name="CalcPrecoFAC">
      <wsdl:documentation xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/">Calcula os preços dos serviços FAC</wsdl:documentation>
      <wsdl:input message="tns:CalcPrecoFACSoapIn" />
      <wsdl:output message="tns:CalcPrecoFACSoapOut" />
    </wsdl:operation>
    <wsdl:operation name="CalcDataMaxima">
      <wsdl:documentation xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/">Calcula a data máxima de entrega de determinado objeto</wsdl:documentation>
      <wsdl:input message="tns:CalcDataMaximaSoapIn" />
      <wsdl:output message="tns:CalcDataMaximaSoapOut" />
    </wsdl:operation>
    <wsdl:operation name="ListaServicos">
      <wsdl:documentation xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/">Lista os serviços que estão disponíveis para cálculo de preço e/ou prazo</wsdl:documentation>
      <wsdl:input message="tns:ListaServicosSoapIn" />
      <wsdl:output message="tns:ListaServicosSoapOut" />
    </wsdl:operation>
    <wsdl:operation name="ListaServicosSTAR">
      <wsdl:documentation xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/">Lista os serviços que são calculados pelo STAR</wsdl:documentation>
      <wsdl:input message="tns:ListaServicosSTARSoapIn" />
      <wsdl:output message="tns:ListaServicosSTARSoapOut" />
    </wsdl:operation>
    <wsdl:operation name="VerificaModal">
      <wsdl:documentation xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/">Método para mostrar se o trecho consultado utiliza modal aéreo ou terrestre</wsdl:documentation>
      <wsdl:input message="tns:VerificaModalSoapIn" />
      <wsdl:output message="tns:VerificaModalSoapOut" />
    </wsdl:operation>
    <wsdl:operation name="getVersao">
      <wsdl:documentation xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/">Retorna a versão atual do componente</wsdl:documentation>
      <wsdl:input message="tns:getVersaoSoapIn" />
      <wsdl:output message="tns:getVersaoSoapOut" />
    </wsdl:operation>
  </wsdl:portType>
  <wsdl:portType name="CalcPrecoPrazoWSHttpGet">
    <wsdl:operation name="CalcPrecoPrazo">
      <wsdl:documentation xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/">Calcula o preço e o prazo com a data atual</wsdl:documentation>
      <wsdl:input message="tns:CalcPrecoPrazoHttpGetIn" />
      <wsdl:output message="tns:CalcPrecoPrazoHttpGetOut" />
    </wsdl:operation>
    <wsdl:operation name="CalcPrecoPrazoData">
      <wsdl:documentation xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/">Calcula o preço e o prazo com uma data especificada</wsdl:documentation>
      <wsdl:input message="tns:CalcPrecoPrazoDataHttpGetIn" />
      <wsdl:output message="tns:CalcPrecoPrazoDataHttpGetOut" />
    </wsdl:operation>
    <wsdl:operation name="CalcPrecoPrazoRestricao">
      <wsdl:documentation xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/">Calcula o preço e o prazo considerando as restrições de entrega</wsdl:documentation>
      <wsdl:input message="tns:CalcPrecoPrazoRestricaoHttpGetIn" />
      <wsdl:output message="tns:CalcPrecoPrazoRestricaoHttpGetOut" />
    </wsdl:operation>
    <wsdl:operation name="CalcPreco">
      <wsdl:documentation xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/">Calcula somente o preço com a data atual</wsdl:documentation>
      <wsdl:input message="tns:CalcPrecoHttpGetIn" />
      <wsdl:output message="tns:CalcPrecoHttpGetOut" />
    </wsdl:operation>
    <wsdl:operation name="CalcPrecoData">
      <wsdl:documentation xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/">Calcula somente o preço com uma data especificada</wsdl:documentation>
      <wsdl:input message="tns:CalcPrecoDataHttpGetIn" />
      <wsdl:output message="tns:CalcPrecoDataHttpGetOut" />
    </wsdl:operation>
    <wsdl:operation name="CalcPrazo">
      <wsdl:documentation xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/">Calcula somente o prazo com a data atual</wsdl:documentation>
      <wsdl:input message="tns:CalcPrazoHttpGetIn" />
      <wsdl:output message="tns:CalcPrazoHttpGetOut" />
    </wsdl:operation>
    <wsdl:operation name="CalcPrazoData">
      <wsdl:documentation xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/">Calcula somente o prazo com uma data especificada</wsdl:documentation>
      <wsdl:input message="tns:CalcPrazoDataHttpGetIn" />
      <wsdl:output message="tns:CalcPrazoDataHttpGetOut" />
    </wsdl:operation>
    <wsdl:operation name="CalcPrazoRestricao">
      <wsdl:documentation xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/">Calcula o prazo considerando restrição de entrega</wsdl:documentation>
      <wsdl:input message="tns:CalcPrazoRestricaoHttpGetIn" />
      <wsdl:output message="tns:CalcPrazoRestricaoHttpGetOut" />
    </wsdl:operation>
    <wsdl:operation name="CalcPrecoFAC">
      <wsdl:documentation xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/">Calcula os preços dos serviços FAC</wsdl:documentation>
      <wsdl:input message="tns:CalcPrecoFACHttpGetIn" />
      <wsdl:output message="tns:CalcPrecoFACHttpGetOut" />
    </wsdl:operation>
    <wsdl:operation name="CalcDataMaxima">
      <wsdl:documentation xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/">Calcula a data máxima de entrega de determinado objeto</wsdl:documentation>
      <wsdl:input message="tns:CalcDataMaximaHttpGetIn" />
      <wsdl:output message="tns:CalcDataMaximaHttpGetOut" />
    </wsdl:operation>
    <wsdl:operation name="ListaServicos">
      <wsdl:documentation xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/">Lista os serviços que estão disponíveis para cálculo de preço e/ou prazo</wsdl:documentation>
      <wsdl:input message="tns:ListaServicosHttpGetIn" />
      <wsdl:output message="tns:ListaServicosHttpGetOut" />
    </wsdl:operation>
    <wsdl:operation name="ListaServicosSTAR">
      <wsdl:documentation xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/">Lista os serviços que são calculados pelo STAR</wsdl:documentation>
      <wsdl:input message="tns:ListaServicosSTARHttpGetIn" />
      <wsdl:output message="tns:ListaServicosSTARHttpGetOut" />
    </wsdl:operation>
    <wsdl:operation name="VerificaModal">
      <wsdl:documentation xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/">Método para mostrar se o trecho consultado utiliza modal aéreo ou terrestre</wsdl:documentation>
      <wsdl:input message="tns:VerificaModalHttpGetIn" />
      <wsdl:output message="tns:VerificaModalHttpGetOut" />
    </wsdl:operation>
    <wsdl:operation name="getVersao">
      <wsdl:documentation xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/">Retorna a versão atual do componente</wsdl:documentation>
      <wsdl:input message="tns:getVersaoHttpGetIn" />
      <wsdl:output message="tns:getVersaoHttpGetOut" />
    </wsdl:operation>
  </wsdl:portType>
  <wsdl:portType name="CalcPrecoPrazoWSHttpPost">
    <wsdl:operation name="CalcPrecoPrazo">
      <wsdl:documentation xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/">Calcula o preço e o prazo com a data atual</wsdl:documentation>
      <wsdl:input message="tns:CalcPrecoPrazoHttpPostIn" />
      <wsdl:output message="tns:CalcPrecoPrazoHttpPostOut" />
    </wsdl:operation>
    <wsdl:operation name="CalcPrecoPrazoData">
      <wsdl:documentation xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/">Calcula o preço e o prazo com uma data especificada</wsdl:documentation>
      <wsdl:input message="tns:CalcPrecoPrazoDataHttpPostIn" />
      <wsdl:output message="tns:CalcPrecoPrazoDataHttpPostOut" />
    </wsdl:operation>
    <wsdl:operation name="CalcPrecoPrazoRestricao">
      <wsdl:documentation xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/">Calcula o preço e o prazo considerando as restrições de entrega</wsdl:documentation>
      <wsdl:input message="tns:CalcPrecoPrazoRestricaoHttpPostIn" />
      <wsdl:output message="tns:CalcPrecoPrazoRestricaoHttpPostOut" />
    </wsdl:operation>
    <wsdl:operation name="CalcPreco">
      <wsdl:documentation xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/">Calcula somente o preço com a data atual</wsdl:documentation>
      <wsdl:input message="tns:CalcPrecoHttpPostIn" />
      <wsdl:output message="tns:CalcPrecoHttpPostOut" />
    </wsdl:operation>
    <wsdl:operation name="CalcPrecoData">
      <wsdl:documentation xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/">Calcula somente o preço com uma data especificada</wsdl:documentation>
      <wsdl:input message="tns:CalcPrecoDataHttpPostIn" />
      <wsdl:output message="tns:CalcPrecoDataHttpPostOut" />
    </wsdl:operation>
    <wsdl:operation name="CalcPrazo">
      <wsdl:documentation xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/">Calcula somente o prazo com a data atual</wsdl:documentation>
      <wsdl:input message="tns:CalcPrazoHttpPostIn" />
      <wsdl:output message="tns:CalcPrazoHttpPostOut" />
    </wsdl:operation>
    <wsdl:operation name="CalcPrazoData">
      <wsdl:documentation xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/">Calcula somente o prazo com uma data especificada</wsdl:documentation>
      <wsdl:input message="tns:CalcPrazoDataHttpPostIn" />
      <wsdl:output message="tns:CalcPrazoDataHttpPostOut" />
    </wsdl:operation>
    <wsdl:operation name="CalcPrazoRestricao">
      <wsdl:documentation xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/">Calcula o prazo considerando restrição de entrega</wsdl:documentation>
      <wsdl:input message="tns:CalcPrazoRestricaoHttpPostIn" />
      <wsdl:output message="tns:CalcPrazoRestricaoHttpPostOut" />
    </wsdl:operation>
    <wsdl:operation name="CalcPrecoFAC">
      <wsdl:documentation xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/">Calcula os preços dos serviços FAC</wsdl:documentation>
      <wsdl:input message="tns:CalcPrecoFACHttpPostIn" />
      <wsdl:output message="tns:CalcPrecoFACHttpPostOut" />
    </wsdl:operation>
    <wsdl:operation name="CalcDataMaxima">
      <wsdl:documentation xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/">Calcula a data máxima de entrega de determinado objeto</wsdl:documentation>
      <wsdl:input message="tns:CalcDataMaximaHttpPostIn" />
      <wsdl:output message="tns:CalcDataMaximaHttpPostOut" />
    </wsdl:operation>
    <wsdl:operation name="ListaServicos">
      <wsdl:documentation xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/">Lista os serviços que estão disponíveis para cálculo de preço e/ou prazo</wsdl:documentation>
      <wsdl:input message="tns:ListaServicosHttpPostIn" />
      <wsdl:output message="tns:ListaServicosHttpPostOut" />
    </wsdl:operation>
    <wsdl:operation name="ListaServicosSTAR">
      <wsdl:documentation xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/">Lista os serviços que são calculados pelo STAR</wsdl:documentation>
      <wsdl:input message="tns:ListaServicosSTARHttpPostIn" />
      <wsdl:output message="tns:ListaServicosSTARHttpPostOut" />
    </wsdl:operation>
    <wsdl:operation name="VerificaModal">
      <wsdl:documentation xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/">Método para mostrar se o trecho consultado utiliza modal aéreo ou terrestre</wsdl:documentation>
      <wsdl:input message="tns:VerificaModalHttpPostIn" />
      <wsdl:output message="tns:VerificaModalHttpPostOut" />
    </wsdl:operation>
    <wsdl:operation name="getVersao">
      <wsdl:documentation xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/">Retorna a versão atual do componente</wsdl:documentation>
      <wsdl:input message="tns:getVersaoHttpPostIn" />
      <wsdl:output message="tns:getVersaoHttpPostOut" />
    </wsdl:operation>
  </wsdl:portType>
  <wsdl:binding name="CalcPrecoPrazoWSSoap" type="tns:CalcPrecoPrazoWSSoap">
    <soap:binding transport="http://schemas.xmlsoap.org/soap/http" />
    <wsdl:operation name="CalcPrecoPrazo">
      <soap:operation soapAction="http://tempuri.org/CalcPrecoPrazo" style="document" />
      <wsdl:input>
        <soap:body use="literal" />
      </wsdl:input>
      <wsdl:output>
        <soap:body use="literal" />
      </wsdl:output>
    </wsdl:operation>
    <wsdl:operation name="CalcPrecoPrazoData">
      <soap:operation soapAction="http://tempuri.org/CalcPrecoPrazoData" style="document" />
      <wsdl:input>
        <soap:body use="literal" />
      </wsdl:input>
      <wsdl:output>
        <soap:body use="literal" />
      </wsdl:output>
    </wsdl:operation>
    <wsdl:operation name="CalcPrecoPrazoRestricao">
      <soap:operation soapAction="http://tempuri.org/CalcPrecoPrazoRestricao" style="document" />
      <wsdl:input>
        <soap:body use="literal" />
      </wsdl:input>
      <wsdl:output>
        <soap:body use="literal" />
      </wsdl:output>
    </wsdl:operation>
    <wsdl:operation name="CalcPreco">
      <soap:operation soapAction="http://tempuri.org/CalcPreco" style="document" />
      <wsdl:input>
        <soap:body use="literal" />
      </wsdl:input>
      <wsdl:output>
        <soap:body use="literal" />
      </wsdl:output>
    </wsdl:operation>
    <wsdl:operation name="CalcPrecoData">
      <soap:operation soapAction="http://tempuri.org/CalcPrecoData" style="document" />
      <wsdl:input>
        <soap:body use="literal" />
      </wsdl:input>
      <wsdl:output>
        <soap:body use="literal" />
      </wsdl:output>
    </wsdl:operation>
    <wsdl:operation name="CalcPrazo">
      <soap:operation soapAction="http://tempuri.org/CalcPrazo" style="document" />
      <wsdl:input>
        <soap:body use="literal" />
      </wsdl:input>
      <wsdl:output>
        <soap:body use="literal" />
      </wsdl:output>
    </wsdl:operation>
    <wsdl:operation name="CalcPrazoData">
      <soap:operation soapAction="http://tempuri.org/CalcPrazoData" style="document" />
      <wsdl:input>
        <soap:body use="literal" />
      </wsdl:input>
      <wsdl:output>
        <soap:body use="literal" />
      </wsdl:output>
    </wsdl:operation>
    <wsdl:operation name="CalcPrazoRestricao">
      <soap:operation soapAction="http://tempuri.org/CalcPrazoRestricao" style="document" />
      <wsdl:input>
        <soap:body use="literal" />
      </wsdl:input>
      <wsdl:output>
        <soap:body use="literal" />
      </wsdl:output>
    </wsdl:operation>
    <wsdl:operation name="CalcPrecoFAC">
      <soap:operation soapAction="http://tempuri.org/CalcPrecoFAC" style="document" />
      <wsdl:input>
        <soap:body use="literal" />
      </wsdl:input>
      <wsdl:output>
        <soap:body use="literal" />
      </wsdl:output>
    </wsdl:operation>
    <wsdl:operation name="CalcDataMaxima">
      <soap:operation soapAction="http://tempuri.org/CalcDataMaxima" style="document" />
      <wsdl:input>
        <soap:body use="literal" />
      </wsdl:input>
      <wsdl:output>
        <soap:body use="literal" />
      </wsdl:output>
    </wsdl:operation>
    <wsdl:operation name="ListaServicos">
      <soap:operation soapAction="http://tempuri.org/ListaServicos" style="document" />
      <wsdl:input>
        <soap:body use="literal" />
      </wsdl:input>
      <wsdl:output>
        <soap:body use="literal" />
      </wsdl:output>
    </wsdl:operation>
    <wsdl:operation name="ListaServicosSTAR">
      <soap:operation soapAction="http://tempuri.org/ListaServicosSTAR" style="document" />
      <wsdl:input>
        <soap:body use="literal" />
      </wsdl:input>
      <wsdl:output>
        <soap:body use="literal" />
      </wsdl:output>
    </wsdl:operation>
    <wsdl:operation name="VerificaModal">
      <soap:operation soapAction="http://tempuri.org/VerificaModal" style="document" />
      <wsdl:input>
        <soap:body use="literal" />
      </wsdl:input>
      <wsdl:output>
        <soap:body use="literal" />
      </wsdl:output>
    </wsdl:operation>
    <wsdl:operation name="getVersao">
      <soap:operation soapAction="http://tempuri.org/getVersao" style="document" />
      <wsdl:input>
        <soap:body use="literal" />
      </wsdl:input>
      <wsdl:output>
        <soap:body use="literal" />
      </wsdl:output>
    </wsdl:operation>
  </wsdl:binding>
  <wsdl:binding name="CalcPrecoPrazoWSSoap12" type="tns:CalcPrecoPrazoWSSoap">
    <soap12:binding transport="http://schemas.xmlsoap.org/soap/http" />
    <wsdl:operation name="CalcPrecoPrazo">
      <soap12:operation soapAction="http://tempuri.org/CalcPrecoPrazo" style="document" />
      <wsdl:input>
        <soap12:body use="literal" />
      </wsdl:input>
      <wsdl:output>
        <soap12:body use="literal" />
      </wsdl:output>
    </wsdl:operation>
    <wsdl:operation name="CalcPrecoPrazoData">
      <soap12:operation soapAction="http://tempuri.org/CalcPrecoPrazoData" style="document" />
      <wsdl:input>
        <soap12:body use="literal" />
      </wsdl:input>
      <wsdl:output>
        <soap12:body use="literal" />
      </wsdl:output>
    </wsdl:operation>
    <wsdl:operation name="CalcPrecoPrazoRestricao">
      <soap12:operation soapAction="http://tempuri.org/CalcPrecoPrazoRestricao" style="document" />
      <wsdl:input>
        <soap12:body use="literal" />
      </wsdl:input>
      <wsdl:output>
        <soap12:body use="literal" />
      </wsdl:output>
    </wsdl:operation>
    <wsdl:operation name="CalcPreco">
      <soap12:operation soapAction="http://tempuri.org/CalcPreco" style="document" />
      <wsdl:input>
        <soap12:body use="literal" />
      </wsdl:input>
      <wsdl:output>
        <soap12:body use="literal" />
      </wsdl:output>
    </wsdl:operation>
    <wsdl:operation name="CalcPrecoData">
      <soap12:operation soapAction="http://tempuri.org/CalcPrecoData" style="document" />
      <wsdl:input>
        <soap12:body use="literal" />
      </wsdl:input>
      <wsdl:output>
        <soap12:body use="literal" />
      </wsdl:output>
    </wsdl:operation>
    <wsdl:operation name="CalcPrazo">
      <soap12:operation soapAction="http://tempuri.org/CalcPrazo" style="document" />
      <wsdl:input>
        <soap12:body use="literal" />
      </wsdl:input>
      <wsdl:output>
        <soap12:body use="literal" />
      </wsdl:output>
    </wsdl:operation>
    <wsdl:operation name="CalcPrazoData">
      <soap12:operation soapAction="http://tempuri.org/CalcPrazoData" style="document" />
      <wsdl:input>
        <soap12:body use="literal" />
      </wsdl:input>
      <wsdl:output>
        <soap12:body use="literal" />
      </wsdl:output>
    </wsdl:operation>
    <wsdl:operation name="CalcPrazoRestricao">
      <soap12:operation soapAction="http://tempuri.org/CalcPrazoRestricao" style="document" />
      <wsdl:input>
        <soap12:body use="literal" />
      </wsdl:input>
      <wsdl:output>
        <soap12:body use="literal" />
      </wsdl:output>
    </wsdl:operation>
    <wsdl:operation name="CalcPrecoFAC">
      <soap12:operation soapAction="http://tempuri.org/CalcPrecoFAC" style="document" />
      <wsdl:input>
        <soap12:body use="literal" />
      </wsdl:input>
      <wsdl:output>
        <soap12:body use="literal" />
      </wsdl:output>
    </wsdl:operation>
    <wsdl:operation name="CalcDataMaxima">
      <soap12:operation soapAction="http://tempuri.org/CalcDataMaxima" style="document" />
      <wsdl:input>
        <soap12:body use="literal" />
      </wsdl:input>
      <wsdl:output>
        <soap12:body use="literal" />
      </wsdl:output>
    </wsdl:operation>
    <wsdl:operation name="ListaServicos">
      <soap12:operation soapAction="http://tempuri.org/ListaServicos" style="document" />
      <wsdl:input>
        <soap12:body use="literal" />
      </wsdl:input>
      <wsdl:output>
        <soap12:body use="literal" />
      </wsdl:output>
    </wsdl:operation>
    <wsdl:operation name="ListaServicosSTAR">
      <soap12:operation soapAction="http://tempuri.org/ListaServicosSTAR" style="document" />
      <wsdl:input>
        <soap12:body use="literal" />
      </wsdl:input>
      <wsdl:output>
        <soap12:body use="literal" />
      </wsdl:output>
    </wsdl:operation>
    <wsdl:operation name="VerificaModal">
      <soap12:operation soapAction="http://tempuri.org/VerificaModal" style="document" />
      <wsdl:input>
        <soap12:body use="literal" />
      </wsdl:input>
      <wsdl:output>
        <soap12:body use="literal" />
      </wsdl:output>
    </wsdl:operation>
    <wsdl:operation name="getVersao">
      <soap12:operation soapAction="http://tempuri.org/getVersao" style="document" />
      <wsdl:input>
        <soap12:body use="literal" />
      </wsdl:input>
      <wsdl:output>
        <soap12:body use="literal" />
      </wsdl:output>
    </wsdl:operation>
  </wsdl:binding>
  <wsdl:binding name="CalcPrecoPrazoWSHttpGet" type="tns:CalcPrecoPrazoWSHttpGet">
    <http:binding verb="GET" />
    <wsdl:operation name="CalcPrecoPrazo">
      <http:operation location="/CalcPrecoPrazo" />
      <wsdl:input>
        <http:urlEncoded />
      </wsdl:input>
      <wsdl:output>
        <mime:mimeXml part="Body" />
      </wsdl:output>
    </wsdl:operation>
    <wsdl:operation name="CalcPrecoPrazoData">
      <http:operation location="/CalcPrecoPrazoData" />
      <wsdl:input>
        <http:urlEncoded />
      </wsdl:input>
      <wsdl:output>
        <mime:mimeXml part="Body" />
      </wsdl:output>
    </wsdl:operation>
    <wsdl:operation name="CalcPrecoPrazoRestricao">
      <http:operation location="/CalcPrecoPrazoRestricao" />
      <wsdl:input>
        <http:urlEncoded />
      </wsdl:input>
      <wsdl:output>
        <mime:mimeXml part="Body" />
      </wsdl:output>
    </wsdl:operation>
    <wsdl:operation name="CalcPreco">
      <http:operation location="/CalcPreco" />
      <wsdl:input>
        <http:urlEncoded />
      </wsdl:input>
      <wsdl:output>
        <mime:mimeXml part="Body" />
      </wsdl:output>
    </wsdl:operation>
    <wsdl:operation name="CalcPrecoData">
      <http:operation location="/CalcPrecoData" />
      <wsdl:input>
        <http:urlEncoded />
      </wsdl:input>
      <wsdl:output>
        <mime:mimeXml part="Body" />
      </wsdl:output>
    </wsdl:operation>
    <wsdl:operation name="CalcPrazo">
      <http:operation location="/CalcPrazo" />
      <wsdl:input>
        <http:urlEncoded />
      </wsdl:input>
      <wsdl:output>
        <mime:mimeXml part="Body" />
      </wsdl:output>
    </wsdl:operation>
    <wsdl:operation name="CalcPrazoData">
      <http:operation location="/CalcPrazoData" />
      <wsdl:input>
        <http:urlEncoded />
      </wsdl:input>
      <wsdl:output>
        <mime:mimeXml part="Body" />
      </wsdl:output>
    </wsdl:operation>
    <wsdl:operation name="CalcPrazoRestricao">
      <http:operation location="/CalcPrazoRestricao" />
      <wsdl:input>
        <http:urlEncoded />
      </wsdl:input>
      <wsdl:output>
        <mime:mimeXml part="Body" />
      </wsdl:output>
    </wsdl:operation>
    <wsdl:operation name="CalcPrecoFAC">
      <http:operation location="/CalcPrecoFAC" />
      <wsdl:input>
        <http:urlEncoded />
      </wsdl:input>
      <wsdl:output>
        <mime:mimeXml part="Body" />
      </wsdl:output>
    </wsdl:operation>
    <wsdl:operation name="CalcDataMaxima">
      <http:operation location="/CalcDataMaxima" />
      <wsdl:input>
        <http:urlEncoded />
      </wsdl:input>
      <wsdl:output>
        <mime:mimeXml part="Body" />
      </wsdl:output>
    </wsdl:operation>
    <wsdl:operation name="ListaServicos">
      <http:operation location="/ListaServicos" />
      <wsdl:input>
        <http:urlEncoded />
      </wsdl:input>
      <wsdl:output>
        <mime:mimeXml part="Body" />
      </wsdl:output>
    </wsdl:operation>
    <wsdl:operation name="ListaServicosSTAR">
      <http:operation location="/ListaServicosSTAR" />
      <wsdl:input>
        <http:urlEncoded />
      </wsdl:input>
      <wsdl:output>
        <mime:mimeXml part="Body" />
      </wsdl:output>
    </wsdl:operation>
    <wsdl:operation name="VerificaModal">
      <http:operation location="/VerificaModal" />
      <wsdl:input>
        <http:urlEncoded />
      </wsdl:input>
      <wsdl:output>
        <mime:mimeXml part="Body" />
      </wsdl:output>
    </wsdl:operation>
    <wsdl:operation name="getVersao">
      <http:operation location="/getVersao" />
      <wsdl:input>
        <http:urlEncoded />
      </wsdl:input>
      <wsdl:output>
        <mime:mimeXml part="Body" />
      </wsdl:output>
    </wsdl:operation>
  </wsdl:binding>
  <wsdl:binding name="CalcPrecoPrazoWSHttpPost" type="tns:CalcPrecoPrazoWSHttpPost">
    <http:binding verb="POST" />
    <wsdl:operation name="CalcPrecoPrazo">
      <http:operation location="/CalcPrecoPrazo" />
      <wsdl:input>
        <mime:content type="application/x-www-form-urlencoded" />
      </wsdl:input>
      <wsdl:output>
        <mime:mimeXml part="Body" />
      </wsdl:output>
    </wsdl:operation>
    <wsdl:operation name="CalcPrecoPrazoData">
      <http:operation location="/CalcPrecoPrazoData" />
      <wsdl:input>
        <mime:content type="application/x-www-form-urlencoded" />
      </wsdl:input>
      <wsdl:output>
        <mime:mimeXml part="Body" />
      </wsdl:output>
    </wsdl:operation>
    <wsdl:operation name="CalcPrecoPrazoRestricao">
      <http:operation location="/CalcPrecoPrazoRestricao" />
      <wsdl:input>
        <mime:content type="application/x-www-form-urlencoded" />
      </wsdl:input>
      <wsdl:output>
        <mime:mimeXml part="Body" />
      </wsdl:output>
    </wsdl:operation>
    <wsdl:operation name="CalcPreco">
      <http:operation location="/CalcPreco" />
      <wsdl:input>
        <mime:content type="application/x-www-form-urlencoded" />
      </wsdl:input>
      <wsdl:output>
        <mime:mimeXml part="Body" />
      </wsdl:output>
    </wsdl:operation>
    <wsdl:operation name="CalcPrecoData">
      <http:operation location="/CalcPrecoData" />
      <wsdl:input>
        <mime:content type="application/x-www-form-urlencoded" />
      </wsdl:input>
      <wsdl:output>
        <mime:mimeXml part="Body" />
      </wsdl:output>
    </wsdl:operation>
    <wsdl:operation name="CalcPrazo">
      <http:operation location="/CalcPrazo" />
      <wsdl:input>
        <mime:content type="application/x-www-form-urlencoded" />
      </wsdl:input>
      <wsdl:output>
        <mime:mimeXml part="Body" />
      </wsdl:output>
    </wsdl:operation>
    <wsdl:operation name="CalcPrazoData">
      <http:operation location="/CalcPrazoData" />
      <wsdl:input>
        <mime:content type="application/x-www-form-urlencoded" />
      </wsdl:input>
      <wsdl:output>
        <mime:mimeXml part="Body" />
      </wsdl:output>
    </wsdl:operation>
    <wsdl:operation name="CalcPrazoRestricao">
      <http:operation location="/CalcPrazoRestricao" />
      <wsdl:input>
        <mime:content type="application/x-www-form-urlencoded" />
      </wsdl:input>
      <wsdl:output>
        <mime:mimeXml part="Body" />
      </wsdl:output>
    </wsdl:operation>
    <wsdl:operation name="CalcPrecoFAC">
      <http:operation location="/CalcPrecoFAC" />
      <wsdl:input>
        <mime:content type="application/x-www-form-urlencoded" />
      </wsdl:input>
      <wsdl:output>
        <mime:mimeXml part="Body" />
      </wsdl:output>
    </wsdl:operation>
    <wsdl:operation name="CalcDataMaxima">
      <http:operation location="/CalcDataMaxima" />
      <wsdl:input>
        <mime:content type="application/x-www-form-urlencoded" />
      </wsdl:input>
      <wsdl:output>
        <mime:mimeXml part="Body" />
      </wsdl:output>
    </wsdl:operation>
    <wsdl:operation name="ListaServicos">
      <http:operation location="/ListaServicos" />
      <wsdl:input>
        <mime:content type="application/x-www-form-urlencoded" />
      </wsdl:input>
      <wsdl:output>
        <mime:mimeXml part="Body" />
      </wsdl:output>
    </wsdl:operation>
    <wsdl:operation name="ListaServicosSTAR">
      <http:operation location="/ListaServicosSTAR" />
      <wsdl:input>
        <mime:content type="application/x-www-form-urlencoded" />
      </wsdl:input>
      <wsdl:output>
        <mime:mimeXml part="Body" />
      </wsdl:output>
    </wsdl:operation>
    <wsdl:operation name="VerificaModal">
      <http:operation location="/VerificaModal" />
      <wsdl:input>
        <mime:content type="application/x-www-form-urlencoded" />
      </wsdl:input>
      <wsdl:output>
        <mime:mimeXml part="Body" />
      </wsdl:output>
    </wsdl:operation>
    <wsdl:operation name="getVersao">
      <http:operation location="/getVersao" />
      <wsdl:input>
        <mime:content type="application/x-www-form-urlencoded" />
      </wsdl:input>
      <wsdl:output>
        <mime:mimeXml part="Body" />
      </wsdl:output>
    </wsdl:operation>
  </wsdl:binding>
  <wsdl:service name="CalcPrecoPrazoWS">
    <wsdl:port name="CalcPrecoPrazoWSSoap" binding="tns:CalcPrecoPrazoWSSoap">
      <soap:address location="http://ws.correios.com.br/calculador/CalcPrecoPrazo.asmx" />
    </wsdl:port>
    <wsdl:port name="CalcPrecoPrazoWSSoap12" binding="tns:CalcPrecoPrazoWSSoap12">
      <soap12:address location="http://ws.correios.com.br/calculador/CalcPrecoPrazo.asmx" />
    </wsdl:port>
    <wsdl:port name="CalcPrecoPrazoWSHttpGet" binding="tns:CalcPrecoPrazoWSHttpGet">
      <http:address location="http://ws.correios.com.br:8080/calculador/CalcPrecoPrazo.asmx" />
    </wsdl:port>
    <wsdl:port name="CalcPrecoPrazoWSHttpPost" binding="tns:CalcPrecoPrazoWSHttpPost">
      <http:address location="http://ws.correios.com.br:8080/calculador/CalcPrecoPrazo.asmx" />
    </wsdl:port>
  </wsdl:service>
</wsdl:definitions>