CONS_QuadientAPIMURL = 'https://sit.emea.studiogateway.chubb.com/enterprise.operations.authorization?Identity=AAD'
QuadientService = 'https://uat.emea.studiogateway.chubb.com/enterprise.system.chubbio-document-gen-connector/generate'

#http headers
Content_Type = 'application/json'
App_ID = '80e88a56-28ca-45ab-a6ea-7fc56ec8ca8d'
App_key = 'ALt8Q~Oq5QCkh9o7ZRCgwUNV5jiRP4dIU_rD~a4u'
Resource = 'ada821e9-fcbd-45c9-8edf-cf80e1a75876'
apiVersion = '1'

TEST_XML = 'C:\\Users\\MAMICCO\\Desktop\\test.xml'

#User_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0'
#http_user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36"

import requests
import json
import datetime
import xml.etree.ElementTree as ET

#unused, use if needing to debug a response
def _debug_print_response(response):
    req = response.request
    if req is not None:
        print(f"  Method: {req.method}")
        print(f"  URL: {req.url}")
        print("  Request headers:")
        for k, v in req.headers.items():
            print(f"    {k}: {v}")
        if req.body:
            body = req.body
            try:
                body = body.decode() if isinstance(body, (bytes, bytearray)) else str(body)
            except Exception:
                body = repr(body)           
    print("\nresponse cookies:")
    try:
        print(response.cookies.get_dict())
    except Exception:
        print("(cannot read cookies)")

    # Try JSON first, fall back to text
    print("\nresponse body:")
    try:
        j = response.json()
        print(json.dumps(j, indent=2))
    except Exception:
        txt = response.text or ""
        print(txt)

#Returns the requests.response on success. Raises requests.RequestException on error.
def get_quadient_token(timeout=10):
    headers = {
        'Content-Type': Content_Type,
        'App_ID': App_ID,
        'App_Key': App_key,
        'Resource': Resource,
        'apiVersion': apiVersion,
    }

    response = requests.post(CONS_QuadientAPIMURL, headers=headers, data=b'', timeout=timeout)
    response.raise_for_status()
    if response:
        request = response.request
        token = response.json()['access_token']
        return token
    return 'Response not found'

#print(get_quadient_token())

'''
def get_quadient_document(timeout=10):

    authorization = 'Bearer' + str(get_quadient_token())
    date_today = datetime.today().strftime("%d%m%Y")
    headers = {
        'Content-Type': Content_Type,
        'apiVersion': apiVersion,
        'Authorization': authorization,
        'Tenant': 'Chubb COG',
        'Region': 'EMEA',
        'LOB': Products.ProductFamily,
        'SubLOB': 'Indigenous',
        'SourceSystem': '2370418',
        'SourceSystemID': 'Ignite1',
        'Department': products.producttype,
        'Language': 'English',
        'DocType': documenttemplate.QuotePolicy,
        'CountryCode': risk_product_country.countrycode,
        'SourceSystemTransasctionID': Risk/UniqueId + '' + DocumentTemplate/UniqueId,
        'CorrelationID': Risk/UniqueId + '' + DocumentTemplate/UniqueId,
        'RequestType': 'Direct',
        'EventType': Risk.Status + '_' + Risk.RiskType,
        'DocOutputFormat': DocumentTemplate.OutputType,
        'SourceSystemCallbackURL':,
        'DestinationURL': 'https://scaler.emea-test.chubb.quadient.cloud/rest/api/submit-job/DocumentGenerationAPI1',
        'InsuredName': Risk/Risks.Risk_Customer/Parties.Customer/Name,
        'PolicyQuoteNumber': Quotenumber or policynumber,
        'TemplatePath': xpressionteamplatename,
        'UserID': 'IgniteUAT',
        'TransasctionDate': date_today
    }
    
    doc_response = requests.post(QuadientService, headers=headers, data=b'', timeout=timeout)
    '''
    #serve logica per selezionare il quadientINputList corretto (legato al doc)

def get_xml_data(attribute, xml):
    """Return the XML string (or text) for the element specified by attribute.

    xml must be a filename (string). The function parses the file and looks for the
    requested element. If the element has children the serialized element is
    returned; otherwise the element's text is returned. If not found an empty
    string is returned.
    """
    import os
    import xml.etree.ElementTree as ET

    if not isinstance(xml, str):
        raise TypeError('xml parameter must be a filename (string)')
    if not os.path.exists(xml):
        raise FileNotFoundError(f'XML file not found: {xml}')

    try:
        tree = ET.parse(xml)
        root = tree.getroot()
    except ET.ParseError as e:
        raise

    # Try direct find first (supports simple ElementTree paths)
    node = None
    try:
        node = root.find(attribute)
    except Exception:
        node = None

    if node is None:
        try:
            node = root.find('.//' + attribute)
        except Exception:
            node = None

    if node is None:
        # fallback: interpret attribute as slash-separated path and search ignoring namespaces
        parts = [p for p in attribute.split('/') if p]
        node = root
        matched = True
        for part in parts:
            found_child = None
            for child in node:
                tag = child.tag
                short = tag.split('}', 1)[1] if '}' in tag else tag
                if short == part or short.endswith(part):
                    found_child = child
                    break
            if found_child is None:
                matched = False
                break
            node = found_child
        if not matched:
            return ''

    # Return serialized element if it has children, otherwise return text
    if len(list(node)) > 0:
        return ET.tostring(node, encoding='unicode')
    return (node.text or '').strip()





