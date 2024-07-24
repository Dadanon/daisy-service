LOGOFF_BODY = """<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
    <SOAP-ENV:Body xmlns="http://www.daisy.org/ns/daisy-online/">
        <logOff></logOff>
    </SOAP-ENV:Body>
</SOAP-ENV:Envelope>
"""


SEARCH_BODY = """<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
    <SOAP-ENV:Body xmlns="http://www.daisy.org/ns/daisy-online/">
        <getQuestions xmlns="http://www.daisy.org/ns/daisy-online/">
            <userResponses>
                <userResponse questionID="search"></userResponse>
            </userResponses>
        </getQuestions>
    </SOAP-ENV:Body>
</SOAP-ENV:Envelope>
"""


GET_CONTENT_LIST_ID_BODY = """<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
    <SOAP-ENV:Body xmlns="http://www.daisy.org/ns/daisy-online/">
        <getQuestions xmlns="http://www.daisy.org/ns/daisy-online/">
            <userResponses>
                <userResponse questionID="%s" value="%s"></userResponse>
            </userResponses>
        </getQuestions>
    </SOAP-ENV:Body>
</SOAP-ENV:Envelope>
"""


GET_BOOKS_LIST_BODY = """<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
    <SOAP-ENV:Body xmlns="http://www.daisy.org/ns/daisy-online/">
        <getContentList>
            <id>%s</id>
            <firstItem>%d</firstItem>
            <lastItem>%d</lastItem>
        </getContentList>
    </SOAP-ENV:Body>
</SOAP-ENV:Envelope>
"""