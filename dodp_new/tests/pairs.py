# -*- coding: utf-8 -*-
from dodp_new.general import TagInfo
from dodp_new.tests.texts import text_1, text_2

tag_info_test_pairs = [
    (
        'Tests',
        text_1,
        'Tests',
        {},
        """
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
"""
    ),
    (
        'Name',
        text_1,
        'Name',
        {},
        'Convert number to string'
    ),
    (
        'Test',
        text_1,
        'Test',
        {'TestId': '0001', 'TestType': 'CMD'},
        """
    <Name>Convert number to string</Name>
    <CommandLine>Examp1.EXE</CommandLine>
    <Input>1</Input>
    <Output>One</Output>
  """
    ),
    (
        'questions',
        text_2,
        'ns1:questions',
        {},
        """
                <ns1:inputQuestion id="searchrequest">
                        <ns1:inputTypes>
                                <ns1:input type="TEXT_ALPHANUMERIC"/>
                                <ns1:input type="AUDIO"/>
                        </ns1:inputTypes>
                        <ns1:label>
                                <ns1:text>Введите строку для поиска. Поиск производится по автору, наименованию и диктору.</ns1:text>
                        </ns1:label>
                </ns1:inputQuestion>
        """
    )
]

full_tag_name_valid_test_pairs = [
    (
        'Test',
        text_1,
        'Test'
    ),
    (
        'CommandLine',
        text_1,
        'CommandLine'
    ),
    (
        'getQuestionsResponse',
        text_2,
        'ns1:getQuestionsResponse'
    ),
    (
        'label',
        text_2,
        'ns1:label'
    )
]

full_tag_name_invalid_test_pairs = [
    (
        'commandLine',
        text_1,
        None
    ),
    (
        'test',
        text_1,
        None
    ),
    (
        'GetQuestionsResponse',
        text_2,
        None
    ),
    (
        'inputquestion',
        text_2,
        None
    )
]

multiple_tag_info_test_pairs = [
    (
        'Tests',
        text_1,
        [
            TagInfo(
                name='Tests',
                params={},
                content="""
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
            """
            )
        ]
    ),
    (
        'Test',
        text_1,
        [
            TagInfo(
                name='Test',
                params={'TestId': '0001', 'TestType': 'CMD'},
                content="""
                <Name>Convert number to string</Name>
                <CommandLine>Examp1.EXE</CommandLine>
                <Input>1</Input>
                <Output>One</Output>
                """
            ),
            TagInfo(
                name='Test',
                params={'TestId': '0002', 'TestType': 'CMD'},
                content="""
                <Name>Find succeeding characters</Name>
                <CommandLine>Examp2.EXE</CommandLine>
                <Input>abc</Input>
                <Output>def</Output>
                """
            ),
            TagInfo(
                name='Test',
                params={'TestId': '0003', 'TestType': 'GUI'},
                content="""
                <Name>Convert multiple numbers to strings</Name>
                <CommandLine>Examp2.EXE /Verbose</CommandLine>
                <Input>123</Input>
                <Output>One Two Three</Output>
                """
            ),
            TagInfo(
                name='Test',
                params={'TestId': '0004', 'TestType': 'GUI'},
                content="""
                <Name>Find correlated key</Name>
                <CommandLine>Examp3.EXE</CommandLine>
                <Input>a1</Input>
                <Output>b1</Output>
                """
            ),
            TagInfo(
                name='Test',
                params={'TestId': '0005', 'TestType': 'GUI'},
                content="""
                <Name>Count characters</Name>
                <CommandLine>FinalExamp.EXE</CommandLine>
                <Input>This is a test</Input>
                <Output>14</Output>
                """
            ),
            TagInfo(
                name='Test',
                params={'TestId': '0006', 'TestType': 'GUI'},
                content="""
                <Name>Another Test</Name>
                <CommandLine>Examp2.EXE</CommandLine>
                <Input>Test Input</Input>
                <Output>10</Output>
                """
            ),
        ]
    ),
    (
        'Name',
        text_1,
        [
            TagInfo(name='Name', params={}, content='Convert number to string'),
            TagInfo(name='Name', params={}, content='Find succeeding characters'),
            TagInfo(name='Name', params={}, content='Convert multiple numbers to strings'),
            TagInfo(name='Name', params={}, content='Find correlated key'),
            TagInfo(name='Name', params={}, content='Count characters'),
            TagInfo(name='Name', params={}, content='Another Test')
        ]
    ),
    (
        'questions',
        text_2,
        [
            TagInfo(
                name='ns1:questions',
                params={},
                content="""
                <ns1:inputQuestion id="searchrequest">
                        <ns1:inputTypes>
                                <ns1:input type="TEXT_ALPHANUMERIC"/>
                                <ns1:input type="AUDIO"/>
                        </ns1:inputTypes>
                        <ns1:label>
                                <ns1:text>Введите строку для поиска. Поиск производится по автору, наименованию и диктору.</ns1:text>
                        </ns1:label>
                </ns1:inputQuestion>
                """
            )
        ]
    ),
    (
        'InputTypes',
        text_2,
        []
    ),
    (
        'input',
        text_2,
        [
            TagInfo(name='ns1:input', params={'type': 'TEXT_ALPHANUMERIC'}),
            TagInfo(name='ns1:input', params={'type': 'AUDIO'})
        ]
    )
]

"""
Используемые сокращения:
F_TN - false tag name (тег отсутствует в body)
F_WC - with_content = False (не подтягивать контент, только заголовок)
F_PK - false param key (ключ отсутствует в параметрах тега)
F_PV - false param value (значение параметра тега не равно значению, указанному в kwargs)

T_TN - true tag name
T_WC - with_content = True
T_PK - true param key
T_PV - true param value
"""

tag_info_by_params_test_pairs_invalid = [
    # INFO: проверяем варианты с None
    # Все варианты ниже с ложным tag_name должны возвращать None (проверяем F_TN)
    (
        'Baka',
        text_1,
        False,
        {'TestId': '0001'}
    ),
    (
        'Baka',
        text_1,
        True,
        {'TestId': '0001'}
    ),
    (
        'Baka',
        text_1,
        False,
        {}
    ),
    (
        'Baka',
        text_1,
        True,
        {}
    ),
    (
        'Baka',
        text_1,
        False,
        {'Tes': '0001'}
    ),
    (
        'Baka',
        text_1,
        True,
        {'Tes': '0001'}
    ),
    (
        'Baka',
        text_1,
        False,
        {'TestId': '1'}
    ),
    (
        'Baka',
        text_1,
        True,
        {'TestId': '1'}
    ),
    # Все варианты с ложным param key должны возвращать None, проверяем F_PK
    (
        'Test',
        text_1,
        False,
        {'TestI': '0001'}
    ),
    (
        'Test',
        text_1,
        True,
        {'TestI': '0001'}
    ),
    (
        'Test',
        text_1,
        False,
        {'TestI': '03'}
    ),
    (
        'Test',
        text_1,
        True,
        {'TestI': '03'}
    ),
    (
        'Test',
        text_1,
        True,
        {'TestI': '0001', 'TestType': 'CMD'}
    ),
    (
        'Test',
        text_1,
        True,
        {'TestId': '0001', 'TestTy': 'CMD'}
    ),
    # Все варианты с ложным param value должны возвращать None
    (
        'Test',
        text_1,
        True,
        {'TestId': '0010'}
    ),
    (
        'Test',
        text_1,
        False,
        {'TestId': '0010'}
    ),
    (
        'Test',
        text_1,
        True,
        {'TestId': '0002', 'TestType': 'CM'}
    ),
    (
        'Test',
        text_1,
        False,
        {'TestId': '0002', 'TestType': 'CM'}
    )
]


tag_info_by_params_test_pairs_valid = [
    # INFO: проверяем варианты не с None
    # Варианты, возвращающие НЕ None:
    # - T_TN, F_WC, T_PK, T_PV
    # - T_TN, T_WC, T_PK, T_PV
    # - T_TN, F_WC (без указания параметров)
    # - T_TN, T_WC
    (
        'Test',
        text_1,
        False,
        {'TestId': '0002'},
        TagInfo(name='Test', params={'TestId': '0002', 'TestType': 'CMD'})
    ),
    (
        'Test',
        text_1,
        False,
        {'TestId': '0004', 'TestType': 'GUI'},
        TagInfo(name='Test', params={'TestId': '0004', 'TestType': 'GUI'})
    ),
    (
        'Test',
        text_1,
        True,
        {'TestId': '0002'},
        TagInfo(
            name='Test',
            params={'TestId': '0002', 'TestType': 'CMD'},
            content="""
            <Name>Find succeeding characters</Name>
            <CommandLine>Examp2.EXE</CommandLine>
            <Input>abc</Input>
            <Output>def</Output>
            """
        )
    ),
    (
        'Test',
        text_1,
        True,
        {'TestId': '0004', 'TestType': 'GUI'},
        TagInfo(
            name='Test',
            params={'TestId': '0004', 'TestType': 'GUI'},
            content="""
            <Name>Find correlated key</Name>
            <CommandLine>Examp3.EXE</CommandLine>
            <Input>a1</Input>
            <Output>b1</Output>
            """
        )
    ),
    (
        'Test',
        text_1,
        False,
        {},
        TagInfo(name='Test', params={'TestId': '0001', 'TestType': 'CMD'})
    ),
    (
        'Test',
        text_1,
        True,
        {},
        TagInfo(
            name='Test',
            params={'TestId': '0001', 'TestType': 'CMD'},
            content="""
            <Name>Convert number to string</Name>
            <CommandLine>Examp1.EXE</CommandLine>
            <Input>1</Input>
            <Output>One</Output>
            """
        )
    ),
    # INFO: добавим валидных тестов для второго текста
    (
        'getQuestionsResponse',
        text_2,
        False,
        {},
        TagInfo(name='ns1:getQuestionsResponse')
    ),
    (
        'getQuestionsResponse',
        text_2,
        True,
        {},
        TagInfo(
            name='ns1:getQuestionsResponse',
            params={},
            content="""
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
            """
        )
    ),
    (
        'inputQuestion',
        text_2,
        False,
        {},
        TagInfo(name='ns1:inputQuestion', params={'id': 'searchrequest'})
    ),
    (
        'inputQuestion',
        text_2,
        True,
        {},
        TagInfo(
            name='ns1:inputQuestion',
            params={'id': 'searchrequest'},
            content="""
            <ns1:inputTypes>
                    <ns1:input type="TEXT_ALPHANUMERIC"/>
                    <ns1:input type="AUDIO"/>
            </ns1:inputTypes>
            <ns1:label>
                    <ns1:text>Введите строку для поиска. Поиск производится по автору, наименованию и диктору.</ns1:text>
            </ns1:label>
            """
        )
    ),
    (
        'input',
        text_2,
        True,
        {},
        TagInfo(name='ns1:input', params={'type': 'TEXT_ALPHANUMERIC'})
    )
]
