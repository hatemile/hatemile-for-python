# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Module of TinyCSSParser interface.
"""

from urllib.parse import urljoin
import requests
import tinycss
from tinycss.css21 import RuleSet
from hatemile import helper
from hatemile.util.css.stylesheetparser import StyleSheetParser
from hatemile.util.html.htmldomparser import HTMLDOMParser
from .tinycssrule import TinyCSSRule


class TinyCSSParser(StyleSheetParser):
    """
    The TinyCSSParser class is official implementation of
    :py:class:`hatemile.util.css.stylesheetparser.StyleSheetParser` for
    tinycss.
    """

    def __init__(self, css_or_hp, current_url=None):
        """
        Initializes a new object that encapsulate the tinycss.

        :param css_or_hp: The HTML parser or CSS code of page.
        :type css_or_hp: str or hatemile.util.html.htmldomparser.HTMLDOMParser
        :param current_url: The current URL of page.
        :type current_url: str
        """

        helper.require_not_none(css_or_hp)
        helper.require_valid_type(css_or_hp, str, HTMLDOMParser)
        helper.require_valid_type(current_url, str)

        if isinstance(css_or_hp, str):
            self.stylesheet = tinycss.make_parser().parse_stylesheet(css_or_hp)
        else:
            self._create_parser(css_or_hp, current_url)

    def _create_parser(self, html_parser, current_url):
        """
        Create the tinycss stylesheet.

        :param html_parser: The HTML parser.
        :type html_parser: hatemile.util.html.htmldomparser.HTMLDOMParser
        :param current_url: The current URL of page.
        :type current_url: str
        """

        css_code = ''

        elements = html_parser.find(
            'style,link[rel="stylesheet"]'
        ).list_results()
        for element in elements:
            if element.get_tag_name() == 'STYLE':
                css_code = css_code + element.get_text_content()
            else:
                css_code = css_code + requests.get(
                    urljoin(current_url, element.get_attribute('href'))
                ).text

        self.stylesheet = tinycss.make_parser().parse_stylesheet(css_code)

    def get_rules(self, properties):
        rules = list()
        for rule in self.stylesheet.rules:
            if isinstance(rule, RuleSet):
                auxiliar_rule = TinyCSSRule(rule)
                for property_name in properties:
                    if auxiliar_rule.has_property(property_name):
                        rules.append(auxiliar_rule)
                        break
        return rules
