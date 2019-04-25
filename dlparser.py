import lxml
from lxml import etree, html
from lxml.html.clean import Cleaner


class DetailsParser:
    def __init__(self, parsing_string):
        self.xml_tree = etree.fromstring(parsing_string.encode('utf-8'))
        self.html_tree = None
        self.output_json = {}

    def __get_licenseno(self):
        license_num_html = self.html_tree.xpath("./div")[0]

        license_text = license_num_html.text_content().strip()
        license_text_index = license_text.find('DL')
        license_no = license_text[license_text_index:]

        self.output_json['license_no'] = license_no

    def __get_hazard_details(self, hazordous_detail_html):
        details_html = hazordous_detail_html.xpath("./tr/td")

        self.output_json['hazardous-valid-till'] = details_html[1].text_content().strip()
        self.output_json['hill-valid-till'] = details_html[3].text_content().strip()

    def __get_validity_details(self, validity_html_table):
        details_html = validity_html_table.xpath("./tr")

        non_transport_html = details_html[0].xpath("./td")
        transport_html = details_html[1].xpath("./td")

        self.output_json['non-transport'] = {}
        self.output_json['transport'] = {}

        self.output_json['non-transport']['from'] = non_transport_html[1].text_content().strip()[6:]
        self.output_json['non-transport']['to'] = non_transport_html[2].text_content().strip()[4:]
        self.output_json['transport']['from'] = transport_html[1].text_content().strip()[6:]
        self.output_json['transport']['to'] = transport_html[2].text_content().strip()[4:]

    def __get_license_details(self, details_html_table):
        details_html = details_html_table.xpath("./tr")

        holder_name_html = details_html[1].xpath("./td")[1]
        holder_name = holder_name_html.text_content().strip()
        self.output_json['holder_name'] = " ".join(holder_name.split())

        active_status_html = details_html[0].xpath("./td")[1]
        active_status = active_status_html.text_content().strip()
        self.output_json['license_status'] = active_status

        issue_date_html = details_html[2].xpath("./td")[1]
        issue_date = issue_date_html.text_content().strip()
        self.output_json['issue-date'] = issue_date

    def __get_vehicle_class_details(self):
        class_detail_html = self.html_tree.xpath("./div/div/table")[0]
        table_body = class_detail_html.xpath("./tbody/tr")
        output_list = []

        for detail_rows in table_body:
            details = detail_rows.xpath("./td")

            one_row_detail = {
                'COV-Category': details[0].text_content(),
                'Class-of-Vehicle': details[1].text_content(),
                'COV-issue-date': details[2].text_content()
            }

            output_list.append(one_row_detail)

        self.output_json['Class-of-vehicle-details'] = output_list

    def __extractdetails(self):
        self.html_tree = self.html_tree.xpath(
            "/div/span/div/div/div/div/div")[0]
        details_html_table = self.html_tree.xpath("./table")

        self.__get_licenseno()
        self.__get_license_details(details_html_table[0])
        self.__get_validity_details(details_html_table[1])
        self.__get_hazard_details(details_html_table[2])
        self.__get_vehicle_class_details()

    def __cleanhtml(self):
        html_cleaner = Cleaner(scripts=True, javascript=True,
                               style=True, inline_style=True, remove_unknown_tags=True)
        self.html_tree = html_cleaner.clean_html(self.html_tree)

    def getdetails(self):
        try:
            root = self.xml_tree.xpath("/partial-response/changes/update")[1]
            self.html_tree = html.fragment_fromstring(root.text)

            self.__cleanhtml()
            self.__extractdetails()

            return self.output_json

        except IndexError:
            return False
