import os
import pprint
from io import StringIO

import lxml
from lxml import etree, html
from lxml.html.clean import Cleaner


def get_license_details(details_html_table):
    details_html = details_html_table.xpath("./tr")
    ouput_json = {}

    holder_name_html = details_html[1].xpath("./td")[1]
    holder_name = holder_name_html.text_content().strip()
    ouput_json['holder_name'] = " ".join(holder_name.split())

    active_status_html = details_html[0].xpath("./td")[1]
    active_status = active_status_html.text_content().strip()
    ouput_json['license_status'] = active_status

    issue_date_html = details_html[2].xpath("./td")[1]
    issue_date = issue_date_html.text_content().strip()
    ouput_json['issue-date'] = issue_date

    return ouput_json


def get_validity_details(validity_html_table):
    details_html = validity_html_table.xpath("./tr")
    ouput_json = {'transport': {}, 'non-transport': {}}

    non_transport_html = details_html[0].xpath("./td")
    ouput_json['non-transport']['from'] = non_transport_html[1].text_content().strip()[6:]
    ouput_json['non-transport']['to'] = non_transport_html[2].text_content().strip()[4:]

    transport_html = details_html[1].xpath("./td")
    ouput_json['transport']['from'] = transport_html[1].text_content().strip()[6:]
    ouput_json['transport']['to'] = transport_html[2].text_content().strip()[4:]

    return ouput_json


def get_hazardous_detail(hazordous_detail_html):
    details_html = hazordous_detail_html.xpath("./tr/td")
    ouput_json = {}

    ouput_json['hazardous-valid-till'] = details_html[1].text_content().strip()
    ouput_json['hill-valid-till'] = details_html[3].text_content().strip()

    return ouput_json


def get_class_detail(class_detail_html):
    table_body = class_detail_html.xpath("./tbody/tr")
    output_json = []

    for detail_rows in table_body:
        details = detail_rows.xpath("./td")

        one_row_detail = {
            'COV-Category': details[0].text_content(),
            'Class-of-Vehicle': details[1].text_content(),
            'COV-issue-date': details[2].text_content()
        }

        output_json.append(one_row_detail)

    return output_json


def extract_details(input_html):
    ouput_json = {}

    html = input_html.xpath("/div/span/div/div/div/div/div")[0]

    license_num = html.xpath("./div")[0]
    license_text = license_num.text_content().strip()
    license_text_index = license_text.find('DL')
    license_no = license_text[license_text_index:]
    ouput_json['license_no'] = license_no

    details_html = html.xpath("./table")

    license_details_json = get_license_details(details_html[0])
    ouput_json.update(license_details_json)

    validity_detail_json = get_validity_details(details_html[1])
    ouput_json.update(validity_detail_json)

    hazard_detail_json = get_hazardous_detail(details_html[2])
    ouput_json.update(hazard_detail_json)

    class_detail_html = html.xpath("./div/div/table")[0]
    class_detail_list = get_class_detail(class_detail_html)
    class_detail_json = {
        'Class-of-vehicle-details': class_detail_list
    }
    ouput_json.update(class_detail_json)

    return ouput_json


def get_details(input_html):
    xml_tree = etree.fromstring(input_html.encode('utf-8'))
    r = xml_tree.xpath("/partial-response/changes/update")[1]

    html_tree = html.fragment_fromstring(r.text)

    cleaner = Cleaner(scripts=True, javascript=True, style=True,
                      inline_style=True, remove_unknown_tags=True)
    clean_html = cleaner.clean_html(html_tree)

    return extract_details(clean_html)


if __name__ == '__main__':
    input_html = True

    with open('output.html', 'r') as input_file:
        input_html = input_file.read()

    extracted_details = get_details(input_html)

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(extracted_details)
