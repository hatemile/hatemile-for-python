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

from bs4 import BeautifulSoup
from hatemile.util.htmldomparser import HTMLDOMParser
from .beautifulsouphtmldomelement import BeautifulSoupHTMLDOMElement
import re


class BeautifulSoupHTMLDOMParser(HTMLDOMParser):
    """
    The class BeautifulSoupHTMLDOMParser is official implementation of
    HTMLDOMParser interface for the BeautifulSoup library.
    """

    def __init__(self, codeOrParser):
        """
        Initializes a new object that encapsulate the parser of BeautifulSoup.
        @param codeOrParser: The root element of the parser or the HTML code.
        @type codeOrParser: str or bs4.element.Tag
        """

        if isinstance(codeOrParser, BeautifulSoup):
            self.document = codeOrParser
        else:
            self.document = BeautifulSoup(codeOrParser)
            self._fix_data_select()
        self.results = []

    def _in_list(self, originalList, item):
        for itemList in originalList:
            if item is itemList:
                return True
        return False

    def _sort_results(self, results):
        """
        Order the results.
        @param results: The disordened results.
        @type results: array.bs4.element.Tag
        @return: The ordened results.
        @rtype: array.bs4.element.Tag
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
        elements = self.document.select('*')
        for element in elements:
            attributes = element.attrs.keys()
            for attribute in attributes:
                if bool(re.findall('^data-', attribute)):
                    element[
                        re.sub('data-', 'dataaaaaa', attribute)
                    ] = element[attribute]

    def _remove_data_select(self):
        elements = self.document.select('*')
        for element in elements:
            attributes = element.attrs.keys()
            for attribute in attributes:
                if bool(re.findall('^dataaaaaa', attribute)):
                    del(element[attribute])

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
        lastResults = self.results
        if isinstance(selector, BeautifulSoupHTMLDOMElement):
            for result in lastResults:
                if self._in_list(result.children, selector):
                    self.results[selector.get_data()]
                    break
        else:
            selector = re.sub('data-', 'dataaaaaa', selector)
            selectors = re.split(',', selector)
            self.results = []
            for sel in selectors:
                for lastResult in lastResults:
                    results = lastResult.select(sel)
                    for result in results:
                        if (
                            (self._in_list(lastResult.children, result))
                            and (not self._in_list(self.results, result))
                        ):
                            self.results.append(result)
        return self

    def find_descendants(self, selector):
        lastResults = self.results
        if isinstance(selector, BeautifulSoupHTMLDOMElement):
            for result in lastResults:
                if self._in_list(selector.parents, result):
                    self.results = [selector.get_data()]
                    break
        else:
            selector = re.sub('data-', 'dataaaaaa', selector)
            selectors = re.split(',', selector)
            self.results = []
            for sel in selectors:
                for lastResult in lastResults:
                    results = lastResult.select(sel)
                    for result in results:
                        if not self._in_list(self.results, result):
                            self.results.append(result)
        return self

    def find_ancestors(self, selector):
        lastResults = self.results
        if isinstance(selector, BeautifulSoupHTMLDOMElement):
            for result in lastResults:
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
            for result in lastResults:
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
        ordenedResults = self._sort_results(self.results)
        for result in ordenedResults:
            array.append(BeautifulSoupHTMLDOMElement(result))
        return array

    def create_element(self, tag):
        return BeautifulSoupHTMLDOMElement(self.document.new_tag(tag))

    def get_html(self):
        self._remove_data_select()
        content = self.document.encode(formatter=None)
        self._fix_data_select()
        return content

    def get_parser(self):
        return self.document

    def clear_parser(self):
        del(self.results[:])
        self.results = None
        self.document = None
