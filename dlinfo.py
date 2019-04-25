import lxml.html
import requests
import requests.exceptions as RequestsException
from dlparser import DetailsParser
from PIL import Image


class ExtractInfo:
    __BASE_URL = 'https://parivahan.gov.in'
    __URL = 'https://parivahan.gov.in/rcdlstatus/?pur_cd=101'
    __CAPTCH_IMG_ID = 'form_rcdl:j_idt34:j_idt39'

    def __init__(self, dl_no, dob):
        self.html = None
        self.dl_no = dl_no
        self.dob = dob
        self.session = requests.Session()

    def __preparepayload(self):
        captcha_text = self.__getcaptcha()

        hidden_inputs = self.html.xpath("//form//input[@type='hidden']")
        payload = {x.attrib["name"]: x.attrib["value"] for x in hidden_inputs}

        payload['form_rcdl:j_idt34:CaptchaID'] = captcha_text
        payload['form_rcdl:tf_dlNO'] = self.dl_no
        payload['form_rcdl:tf_dob_input'] = self.dob
        payload['javax.faces.partial.ajax'] = 'true'
        payload['javax.faces.source'] = 'form_rcdl:j_idt44'
        payload['javax.faces.partial.execute'] = '@all'
        payload['javax.faces.partial.render'] = 'form_rcdl:pnl_show form_rcdl:pg_show form_rcdl:rcdl_pnl'
        payload['form_rcdl:j_idt44'] = 'form_rcdl:j_idt44'

        return payload

    def __getcaptcha(self):
        captcha_el = self.html.get_element_by_id(self.__CAPTCH_IMG_ID)
        captcha_url = captcha_el.xpath("@src")[0]

        captcha_image = self.session.get(
            "{}{}".format(self.__BASE_URL, captcha_url), stream=True
        )
        captcha_image.raise_for_status()

        img = Image.open(captcha_image.raw)
        img.show()

        return input('Enter captcha: ')

    def __getpage(self):
        try:
            enter_info_page = self.session.get(self.__URL)
            enter_info_page.raise_for_status()

            res_html_string = enter_info_page.text

            self.html = lxml.html.document_fromstring(
                res_html_string.encode('utf-8')
            )

            payload = self.__preparepayload()
            res = self.session.post(
                'https://parivahan.gov.in/rcdlstatus/vahan/rcDlHome.xhtml', data=payload
            )
            res.raise_for_status()

            return res.text

        except RequestsException.ConnectionError:
            print("Error: Network Problem")

        except RequestsException.Timeout:
            print("Error: Connection timeout")

        except RequestsException.HTTPError as err:
            print("Error:", err)

       

    def extract(self):
        res_details_str = self.__getpage()

        if res_details_str == None:
            return

        detail_parser = DetailsParser(res_details_str)
        details = detail_parser.getdetails()

        if details == False:
            return "Details not found"

        return details
