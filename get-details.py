import os
from io import StringIO

import lxml
from lxml import etree, html
from lxml.html.clean import Cleaner


def get_details(input_html):
    xml_tree = etree.fromstring(input_html.encode('utf-8'))
    r = xml_tree.xpath("/partial-response/changes/update")[1]

    html_tree = html.fragment_fromstring(r.text)

    cleaner = Cleaner(scripts=True, javascript=True, style=True,
                      inline_style=True, remove_unknown_tags=True)
    clean_html = cleaner.clean_html(html_tree)

    html_string = html.tostring(clean_html, pretty_print=True).decode()
    print(html_string)


if __name__ == '__main__':
    input_html = True

    with open('output.html', 'r') as input_file:
        input_html = input_file.read()

    get_details(input_html)
