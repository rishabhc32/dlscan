import lxml.etree
import lxml.html
import requests
from PIL import Image

BASE_URL = 'https://parivahan.gov.in'
URL = 'https://parivahan.gov.in/rcdlstatus/?pur_cd=101'
DL_NO = 'DL-0420110149646'
DOB = '09-02-1976'
CAPTCH_IMG_ID = 'form_rcdl:j_idt34:j_idt39'

with requests.Session() as session:
    first_response = session.get(URL)
    res_html = first_response.text

    html = lxml.html.document_fromstring(res_html.encode('utf-8'))
    element = html.get_element_by_id(CAPTCH_IMG_ID)
    image_url = element.xpath("@src")[0]
    print(image_url)

    hidden_inputs = html.xpath("//form//input[@type='hidden']")
    payload = {x.attrib["name"]: x.attrib["value"] for x in hidden_inputs}

    captcha_image = session.get(
        "{}{}".format(BASE_URL, image_url), stream=True)
    img = Image.open(captcha_image.raw)
    img.show()

    captcha_text = input('Enter captcha: ')

    payload['form_rcdl:tf_dlNO'] = DL_NO
    payload['form_rcdl:tf_dob_input'] = DOB
    payload['form_rcdl:j_idt34:CaptchaID'] = captcha_text
    payload['javax.faces.partial.ajax'] = 'true'
    payload['javax.faces.source'] = 'form_rcdl:j_idt44'
    payload['javax.faces.partial.execute'] = '@all'
    payload['javax.faces.partial.render'] = 'form_rcdl:pnl_show form_rcdl:pg_show form_rcdl:rcdl_pnl'
    payload['form_rcdl:j_idt44'] = 'form_rcdl:j_idt44'

    res = session.post(
        'https://parivahan.gov.in/rcdlstatus/vahan/rcDlHome.xhtml', data=payload)
    print(res.text)

    with open("output.html", "w") as text_file:
        text_file.write(res.text)
