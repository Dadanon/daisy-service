from .general import LOGIN_DICT


def LOGON_v2(username: str, password: str):
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
    <SOAP-ENV:Body xmlns="http://www.daisy.org/ns/daisy-online/">
        <logOn>
            <username>{username}</username>
            <password>{password}</password>
            <readingSystemAttributes>
                <manufacturer>{LOGIN_DICT['manufacturer']}</manufacturer>
                <model>{LOGIN_DICT['model_py']}</model>
                <serialNumber>{LOGIN_DICT['serial']}</serialNumber>
                <version>{LOGIN_DICT['version']}</version>
                <config>
                    <accessConfig>STREAM_ONLY</accessConfig>
                    <supportsMultipleSelections>true</supportsMultipleSelections>
                    <supportsAdvancedDynamicMenus>false</supportsAdvancedDynamicMenus>
                    <preferredUILanguage>ru</preferredUILanguage>
                    <supportedContentFormats></supportedContentFormats>
                    <supportedContentProtectionFormats></supportedContentProtectionFormats>
                    <supportedMimeTypes>
                        <mimeType type="audio/x-lkf"></mimeType>
                        <mimeType type="application/lgk"></mimeType>
                        <mimeType type="audio/mpeg"></mimeType>
                        <mimeType type="audio/x-wav"></mimeType>
                        <mimeType type="text/plain"></mimeType>
                        <mimeType type="text/xml"></mimeType>
                        <mimeType type="text/html"></mimeType>
                        <mimeType type="application/msword"></mimeType>
                    </supportedMimeTypes>
                    <supportedInputTypes>
                        <input type="TEXT_ALPHANUMERIC"></input>
                        <input type="AUDIO"></input>
                    </supportedInputTypes>
                    <requiresAudioLabels>true</requiresAudioLabels>
                </config>
            </readingSystemAttributes>
        </logOn>
    </SOAP-ENV:Body>
</SOAP-ENV:Envelope>
"""


GETCR_V2 = """<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
    <SOAP-ENV:Body xmlns="http://www.daisy.org/ns/daisy-online/">
        <getContentResources>
            <contentID>%s</contentID>
            <accessType>%s</accessType>
        </getContentResources>
    </SOAP-ENV:Body>`
</SOAP-ENV:Envelope>
"""
