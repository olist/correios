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
      <s:element name="CalcPrazoObjeto">
        <s:complexType>
          <s:sequence>
            <s:element minOccurs="0" maxOccurs="1" name="codigoObjeto" type="s:string" />
          </s:sequence>
        </s:complexType>
      </s:element>
      <s:element name="CalcPrazoObjetoResponse">
        <s:complexType>
          <s:sequence>
            <s:element minOccurs="1" maxOccurs="1" name="CalcPrazoObjetoResult" type="tns:cResultadoObjeto" />
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
          <s:element minOccurs="0" maxOccurs="1" name="dataEntrega" type="s:string" />
          <s:element minOccurs="0" maxOccurs="1" name="dataMaxEntrega" type="s:string" />
          <s:element minOccurs="0" maxOccurs="1" name="erro" type="s:string" />
          <s:element minOccurs="0" maxOccurs="1" name="msgErro" type="s:string" />
        </s:sequence>
      </s:complexType>
      <s:element name="cResultado" type="tns:cResultado" />
      <s:element name="cResultadoObjeto" type="tns:cResultadoObjeto" />
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
  <wsdl:message name="CalcPrazoObjetoSoapIn">
    <wsdl:part name="parameters" element="tns:CalcPrazoObjeto" />
  </wsdl:message>
  <wsdl:message name="CalcPrazoObjetoSoapOut">
    <wsdl:part name="parameters" element="tns:CalcPrazoObjetoResponse" />
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
  <wsdl:message name="CalcPrazoObjetoHttpGetIn">
    <wsdl:part name="codigoObjeto" type="s:string" />
  </wsdl:message>
  <wsdl:message name="CalcPrazoObjetoHttpGetOut">
    <wsdl:part name="Body" element="tns:cResultadoObjeto" />
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
  <wsdl:message name="CalcPrazoObjetoHttpPostIn">
    <wsdl:part name="codigoObjeto" type="s:string" />
  </wsdl:message>
  <wsdl:message name="CalcPrazoObjetoHttpPostOut">
    <wsdl:part name="Body" element="tns:cResultadoObjeto" />
  </wsdl:message>
  <wsdl:portType name="CalcPrecoPrazoWSSoap">
    <wsdl:operation name="CalcPrecoPrazo">
      <wsdl:input message="tns:CalcPrecoPrazoSoapIn" />
      <wsdl:output message="tns:CalcPrecoPrazoSoapOut" />
    </wsdl:operation>
    <wsdl:operation name="CalcPrecoPrazoData">
      <wsdl:input message="tns:CalcPrecoPrazoDataSoapIn" />
      <wsdl:output message="tns:CalcPrecoPrazoDataSoapOut" />
    </wsdl:operation>
    <wsdl:operation name="CalcPrecoPrazoRestricao">
      <wsdl:input message="tns:CalcPrecoPrazoRestricaoSoapIn" />
      <wsdl:output message="tns:CalcPrecoPrazoRestricaoSoapOut" />
    </wsdl:operation>
    <wsdl:operation name="CalcPreco">
      <wsdl:input message="tns:CalcPrecoSoapIn" />
      <wsdl:output message="tns:CalcPrecoSoapOut" />
    </wsdl:operation>
    <wsdl:operation name="CalcPrecoData">
      <wsdl:input message="tns:CalcPrecoDataSoapIn" />
      <wsdl:output message="tns:CalcPrecoDataSoapOut" />
    </wsdl:operation>
    <wsdl:operation name="CalcPrazo">
      <wsdl:input message="tns:CalcPrazoSoapIn" />
      <wsdl:output message="tns:CalcPrazoSoapOut" />
    </wsdl:operation>
    <wsdl:operation name="CalcPrazoData">
      <wsdl:input message="tns:CalcPrazoDataSoapIn" />
      <wsdl:output message="tns:CalcPrazoDataSoapOut" />
    </wsdl:operation>
    <wsdl:operation name="CalcPrazoRestricao">
      <wsdl:input message="tns:CalcPrazoRestricaoSoapIn" />
      <wsdl:output message="tns:CalcPrazoRestricaoSoapOut" />
    </wsdl:operation>
    <wsdl:operation name="CalcPrecoFAC">
      <wsdl:input message="tns:CalcPrecoFACSoapIn" />
      <wsdl:output message="tns:CalcPrecoFACSoapOut" />
    </wsdl:operation>
    <wsdl:operation name="CalcPrazoObjeto">
      <wsdl:documentation xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/">Calcula a data máxima de entrega de determinado objeto</wsdl:documentation>
      <wsdl:input message="tns:CalcPrazoObjetoSoapIn" />
      <wsdl:output message="tns:CalcPrazoObjetoSoapOut" />
    </wsdl:operation>
  </wsdl:portType>
  <wsdl:portType name="CalcPrecoPrazoWSHttpGet">
    <wsdl:operation name="CalcPrecoPrazo">
      <wsdl:input message="tns:CalcPrecoPrazoHttpGetIn" />
      <wsdl:output message="tns:CalcPrecoPrazoHttpGetOut" />
    </wsdl:operation>
    <wsdl:operation name="CalcPrecoPrazoData">
      <wsdl:input message="tns:CalcPrecoPrazoDataHttpGetIn" />
      <wsdl:output message="tns:CalcPrecoPrazoDataHttpGetOut" />
    </wsdl:operation>
    <wsdl:operation name="CalcPrecoPrazoRestricao">
      <wsdl:input message="tns:CalcPrecoPrazoRestricaoHttpGetIn" />
      <wsdl:output message="tns:CalcPrecoPrazoRestricaoHttpGetOut" />
    </wsdl:operation>
    <wsdl:operation name="CalcPreco">
      <wsdl:input message="tns:CalcPrecoHttpGetIn" />
      <wsdl:output message="tns:CalcPrecoHttpGetOut" />
    </wsdl:operation>
    <wsdl:operation name="CalcPrecoData">
      <wsdl:input message="tns:CalcPrecoDataHttpGetIn" />
      <wsdl:output message="tns:CalcPrecoDataHttpGetOut" />
    </wsdl:operation>
    <wsdl:operation name="CalcPrazo">
      <wsdl:input message="tns:CalcPrazoHttpGetIn" />
      <wsdl:output message="tns:CalcPrazoHttpGetOut" />
    </wsdl:operation>
    <wsdl:operation name="CalcPrazoData">
      <wsdl:input message="tns:CalcPrazoDataHttpGetIn" />
      <wsdl:output message="tns:CalcPrazoDataHttpGetOut" />
    </wsdl:operation>
    <wsdl:operation name="CalcPrazoRestricao">
      <wsdl:input message="tns:CalcPrazoRestricaoHttpGetIn" />
      <wsdl:output message="tns:CalcPrazoRestricaoHttpGetOut" />
    </wsdl:operation>
    <wsdl:operation name="CalcPrecoFAC">
      <wsdl:input message="tns:CalcPrecoFACHttpGetIn" />
      <wsdl:output message="tns:CalcPrecoFACHttpGetOut" />
    </wsdl:operation>
    <wsdl:operation name="CalcPrazoObjeto">
      <wsdl:documentation xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/">Calcula a data máxima de entrega de determinado objeto</wsdl:documentation>
      <wsdl:input message="tns:CalcPrazoObjetoHttpGetIn" />
      <wsdl:output message="tns:CalcPrazoObjetoHttpGetOut" />
    </wsdl:operation>
  </wsdl:portType>
  <wsdl:portType name="CalcPrecoPrazoWSHttpPost">
    <wsdl:operation name="CalcPrecoPrazo">
      <wsdl:input message="tns:CalcPrecoPrazoHttpPostIn" />
      <wsdl:output message="tns:CalcPrecoPrazoHttpPostOut" />
    </wsdl:operation>
    <wsdl:operation name="CalcPrecoPrazoData">
      <wsdl:input message="tns:CalcPrecoPrazoDataHttpPostIn" />
      <wsdl:output message="tns:CalcPrecoPrazoDataHttpPostOut" />
    </wsdl:operation>
    <wsdl:operation name="CalcPrecoPrazoRestricao">
      <wsdl:input message="tns:CalcPrecoPrazoRestricaoHttpPostIn" />
      <wsdl:output message="tns:CalcPrecoPrazoRestricaoHttpPostOut" />
    </wsdl:operation>
    <wsdl:operation name="CalcPreco">
      <wsdl:input message="tns:CalcPrecoHttpPostIn" />
      <wsdl:output message="tns:CalcPrecoHttpPostOut" />
    </wsdl:operation>
    <wsdl:operation name="CalcPrecoData">
      <wsdl:input message="tns:CalcPrecoDataHttpPostIn" />
      <wsdl:output message="tns:CalcPrecoDataHttpPostOut" />
    </wsdl:operation>
    <wsdl:operation name="CalcPrazo">
      <wsdl:input message="tns:CalcPrazoHttpPostIn" />
      <wsdl:output message="tns:CalcPrazoHttpPostOut" />
    </wsdl:operation>
    <wsdl:operation name="CalcPrazoData">
      <wsdl:input message="tns:CalcPrazoDataHttpPostIn" />
      <wsdl:output message="tns:CalcPrazoDataHttpPostOut" />
    </wsdl:operation>
    <wsdl:operation name="CalcPrazoRestricao">
      <wsdl:input message="tns:CalcPrazoRestricaoHttpPostIn" />
      <wsdl:output message="tns:CalcPrazoRestricaoHttpPostOut" />
    </wsdl:operation>
    <wsdl:operation name="CalcPrecoFAC">
      <wsdl:input message="tns:CalcPrecoFACHttpPostIn" />
      <wsdl:output message="tns:CalcPrecoFACHttpPostOut" />
    </wsdl:operation>
    <wsdl:operation name="CalcPrazoObjeto">
      <wsdl:documentation xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/">Calcula a data máxima de entrega de determinado objeto</wsdl:documentation>
      <wsdl:input message="tns:CalcPrazoObjetoHttpPostIn" />
      <wsdl:output message="tns:CalcPrazoObjetoHttpPostOut" />
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
    <wsdl:operation name="CalcPrazoObjeto">
      <soap:operation soapAction="http://tempuri.org/CalcPrazoObjeto" style="document" />
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
    <wsdl:operation name="CalcPrazoObjeto">
      <soap12:operation soapAction="http://tempuri.org/CalcPrazoObjeto" style="document" />
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
    <wsdl:operation name="CalcPrazoObjeto">
      <http:operation location="/CalcPrazoObjeto" />
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
    <wsdl:operation name="CalcPrazoObjeto">
      <http:operation location="/CalcPrazoObjeto" />
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
      <http:address location="http://ws.correios.com.br/calculador/CalcPrecoPrazo.asmx" />
    </wsdl:port>
    <wsdl:port name="CalcPrecoPrazoWSHttpPost" binding="tns:CalcPrecoPrazoWSHttpPost">
      <http:address location="http://ws.correios.com.br/calculador/CalcPrecoPrazo.asmx" />
    </wsdl:port>
  </wsdl:service>
</wsdl:definitions>