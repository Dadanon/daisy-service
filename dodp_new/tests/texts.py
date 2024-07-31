# -*- coding: utf-8 -*-


text_1 = """
<?xml version="1.0"?>
<Tests>
  <Test TestId="0001" TestType="CMD">
    <Name>Convert number to string</Name>
    <CommandLine>Examp1.EXE</CommandLine>
    <Input>1</Input>
    <Output>One</Output>
  </Test>
  <Test TestId="0002" TestType="CMD">
    <Name>Find succeeding characters</Name>
    <CommandLine>Examp2.EXE</CommandLine>
    <Input>abc</Input>
    <Output>def</Output>
  </Test>
  <Test TestId="0003" TestType="GUI">
    <Name>Convert multiple numbers to strings</Name>
    <CommandLine>Examp2.EXE /Verbose</CommandLine>
    <Input>123</Input>
    <Output>One Two Three</Output>
  </Test>
  <Test TestId="0004" TestType="GUI">
    <Name>Find correlated key</Name>
    <CommandLine>Examp3.EXE</CommandLine>
    <Input>a1</Input>
    <Output>b1</Output>
  </Test>
  <Test TestId="0005" TestType="GUI">
    <Name>Count characters</Name>
    <CommandLine>FinalExamp.EXE</CommandLine>
    <Input>This is a test</Input>
    <Output>14</Output>
  </Test>
  <Test TestId="0006" TestType="GUI">
    <Name>Another Test</Name>
    <CommandLine>Examp2.EXE</CommandLine>
    <Input>Test Input</Input>
    <Output>10</Output>
  </Test>
</Tests>
"""


text_2 = """
<?xml version="1.0" encoding="utf-8"?>
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns1="http://www.daisy.org/ns/daisy-online/">
<SOAP-ENV:Body>
<ns1:getQuestionsResponse>
        <ns1:questions>
                <ns1:inputQuestion id="searchrequest">
                        <ns1:inputTypes>
                                <ns1:input type="TEXT_ALPHANUMERIC"/>
                                <ns1:input type="AUDIO"/>
                        </ns1:inputTypes>
                        <ns1:label>
                                <ns1:text>Введите строку для поиска. Поиск производится по автору, наименованию и диктору.</ns1:text>
                        </ns1:label>
                </ns1:inputQuestion>
        </ns1:questions>
</ns1:getQuestionsResponse>
</SOAP-ENV:Body>
</SOAP-ENV:Envelope>
"""

# End block