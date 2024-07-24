from .general import LOGIN_DICT


LOGON = """<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
    <SOAP-ENV:Body xmlns="http://www.daisy.org/ns/daisy-online/">
        <logOn>
            <username>%s</username>
            <password>%s</password>
        </logOn>
    </SOAP-ENV:Body>
</SOAP-ENV:Envelope>
"""


# INFO: получить список возможностей сервера (get service attributes)
GETSA = """<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
    <SOAP-ENV:Body xmlns="http://www.daisy.org/ns/daisy-online/">
        <getServiceAttributes></getServiceAttributes>
    </SOAP-ENV:Body>
</SOAP-ENV:Envelope>
"""


# INFO: список возможностей плеера для отправки на сервер (set reading system attributes)
SETRSA = f"""<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
    <SOAP-ENV:Body xmlns="http://www.daisy.org/ns/daisy-online/">
        <setReadingSystemAttributes>
            <readingSystemAttributes>
                <manufacturer>{LOGIN_DICT['manufacturer']}</manufacturer>
                <model>{LOGIN_DICT['model_go']}</model>
                <version>{LOGIN_DICT['version']}</version>
                <config>
                    <supportsMultipleSelections>false</supportsMultipleSelections>
                    <preferredUILanguage>ru-RU</preferredUILanguage>
                    <supportedContentFormats></supportedContentFormats>
                    <supportedContentProtectionFormats></supportedContentProtectionFormats>
                    <supportedMimeTypes>
                        <mimeType type="audio/x-lkf"></mimeType>
                        <mimeType type="application/lgk"></mimeType>
                        <mimeType type="audio/mpeg"></mimeType>
                    </supportedMimeTypes>
                    <supportedInputTypes>
                        <input type="TEXT_ALPHANUMERIC"></input>
                        <input type="AUDIO"></input>
                    </supportedInputTypes>
                    <requiresAudioLabels>false</requiresAudioLabels>
                </config>
            </readingSystemAttributes>
        </setReadingSystemAttributes>
    </SOAP-ENV:Body>
</SOAP-ENV:Envelope>
"""


GETCR = """<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
    <SOAP-ENV:Body xmlns="http://www.daisy.org/ns/daisy-online/">
        <getContentResources>
            <contentID>%s</contentID>
        </getContentResources>
    </SOAP-ENV:Body>
</SOAP-ENV:Envelope>
"""
