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
Module of BeautifulSoupHTMLDOMParser class.
"""

import re
from bs4 import BeautifulSoup
from hatemile import helper
from hatemile.util.html.htmldomparser import HTMLDOMParser
from .bshtmldomnode import BeautifulSoupHTMLDOMElement


class BeautifulSoupHTMLDOMParser(HTMLDOMParser):
    """
    The class BeautifulSoupHTMLDOMParser is official implementation of
    :py:class:`hatemile.util.html.htmldomparser.HTMLDOMParser` for the
    BeautifulSoup library.
    """

    def __init__(self, code_or_parser):
        """
        Initializes a new object that encapsulate the parser of BeautifulSoup.

        :param code_or_parser: The root element of the parser or the HTML code.
        :type code_or_parser: str or bs4.BeautifulSoup
        """

        helper.require_not_none(code_or_parser)
        helper.require_valid_type(code_or_parser, str, BeautifulSoup)

        if isinstance(code_or_parser, BeautifulSoup):
            self.document = code_or_parser
        else:
            self.document = BeautifulSoup(code_or_parser, 'html.parser')
            self._fix_data_select()
        self.results = []

    def _in_list(self, original_list, item):
        """
        Check that an item as contained in a list.

        :param original_list: The list.
        :type original_list: list(object)
        :param item: The item.
        :type item: hatemile.util.html.htmldomelement.HTMLDOMElement
        :return: True if the item contained in the list or False if not.
        :rtype: bool
        """
        # pylint: disable=no-self-use

        for item_list in original_list:
            if item is item_list:
                return True
        return False

    def _sort_results(self, results):
        """
        Order the results.

        :param results: The disordened results.
        :type results: array.bs4.element.Tag
        :return: The ordened results.
        :rtype: array.bs4.element.Tag
        """

        parents = []
        groups = []
        for result in results:
            if not self._in_list(parents, result.parent):
                parents.append(result.parent)
                groups.append([])
                groups[len(groups) - 1].append(result)
            else:
                groups[parents.index(result.parent)].append(result)
        array = []
        for group in groups:
            array += sorted(
                group,
                key=lambda element: element.parent.contents.index(element)
            )
        return array

    def _fix_data_select(self):
        """
        Replace all hyphens of data attributes for 'aaaaa', to avoid error in
        search.
        """

        elements = self.document.select('*')
        for element in elements:
            attributes = element.attrs.keys()
            data_attributes = list()
            for attribute in attributes:
                if bool(re.findall('^data-', attribute)):
                    data_attributes.append({
                        'original': attribute,
                        'modified': re.sub('data-', 'dataaaaaa', attribute),
                        'value': element[attribute]
                    })
            if data_attributes:
                auxiliar_element = BeautifulSoupHTMLDOMElement(element)
                for data_attribute in data_attributes:
                    auxiliar_element.remove_attribute(
                        data_attribute['original']
                    )
                    auxiliar_element.set_attribute(
                        data_attribute['modified'],
                        data_attribute['value']
                    )

    def _remove_data_select(self):
        """
        Remove all data attributes with 'aaaaa', to display the correct HTML
        code of page.
        """

        elements = self.document.select('*')
        for element in elements:
            attributes = element.attrs.keys()
            data_attributes = list()
            for attribute in attributes:
                if bool(re.findall('^dataaaaaa', attribute)):
                    data_attributes.append(attribute)
            if data_attributes:
                auxiliar_element = BeautifulSoupHTMLDOMElement(element)
                for data_attribute in data_attributes:
                    auxiliar_element.remove_attribute(data_attribute)

    def find(self, selector):
        if isinstance(selector, BeautifulSoupHTMLDOMElement):
            self.results = [selector.get_data()]
        else:
            selector = re.sub('data-', 'dataaaaaa', selector)
            selectors = re.split(',', selector)
            self.results = []
            for sel in selectors:
                results = self.document.select(sel)
                for result in results:
                    if not self._in_list(self.results, result):
                        self.results.append(result)
        return self

    def find_children(self, selector):
        last_results = self.results
        self.results = []
        if isinstance(selector, BeautifulSoupHTMLDOMElement):
            for result in last_results:
                if self._in_list(result.children, selector):
                    self.results.append(selector.get_data())
                    break
        else:
            selector = re.sub('data-', 'dataaaaaa', selector)
            selectors = re.split(',', selector)
            for sel in selectors:
                for last_result in last_results:
                    results = last_result.select(sel)
                    for result in results:
                        if (
                            (self._in_list(last_result.children, result))
                            and (not self._in_list(self.results, result))
                        ):
                            self.results.append(result)
        return self

    def find_descendants(self, selector):
        last_results = self.results
        if isinstance(selector, BeautifulSoupHTMLDOMElement):
            for result in last_results:
                if self._in_list(selector.parents, result):
                    self.results = [selector.get_data()]
                    break
        else:
            selector = re.sub('data-', 'dataaaaaa', selector)
            selectors = re.split(',', selector)
            self.results = []
            for sel in selectors:
                for last_result in last_results:
                    results = last_result.select(sel)
                    for result in results:
                        if not self._in_list(self.results, result):
                            self.results.append(result)
        return self

    def find_ancestors(self, selector):
        last_results = self.results
        if isinstance(selector, BeautifulSoupHTMLDOMElement):
            for result in last_results:
                if self._in_list(result.parents, selector):
                    self.results = [selector.get_data()]
                    break
        else:
            parents = []
            self.results = []
            selector = re.sub('data-', 'dataaaaaa', selector)
            selectors = re.split(',', selector)
            for sel in selectors:
                results = self.document.select(sel)
                for result in results:
                    if not self._in_list(parents, result):
                        parents.append(result)
            for result in last_results:
                for parent in parents:
                    if (
                        (self._in_list(result.parents, parent))
                        and (not self._in_list(self.results, parent))
                    ):
                        self.results.append(parent)
        return self

    def first_result(self):
        if not bool(self.results):
            return None
        return BeautifulSoupHTMLDOMElement(self.results[0])

    def last_result(self):
        if not bool(self.results):
            return None
        return BeautifulSoupHTMLDOMElement(self.results[len(self.results) - 1])

    def list_results(self):
        array = []
        ordened_results = self._sort_results(self.results)
        for result in ordened_results:
            array.append(BeautifulSoupHTMLDOMElement(result))
        return array

    def create_element(self, tag):
        return BeautifulSoupHTMLDOMElement(self.document.new_tag(tag))

    def get_html(self):
        self._remove_data_select()
        content = str(self.document)
        self._fix_data_select()
        return content

    def get_parser(self):
        return self.document

    def clear_parser(self):
        del self.results[:]
        self.results = None
        self.document = None
