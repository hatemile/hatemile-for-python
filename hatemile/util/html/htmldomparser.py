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
Module of HTMLDOMParser interface.
"""


class HTMLDOMParser:
    """
    The HTMLDOMParser interface contains the methods for access a native
    parser.
    """

    def find(self, selector):
        """
        Find all elements in the parser by selector.

        :param selector: The selector.
        :type selector: str or hatemile.util.html.htmldomelement.HTMLDOMElement
        :return: The parser with the elements found.
        :rtype: hatemile.util.html.htmldomparser.HTMLDOMParser
        """

        pass

    def find_children(self, selector):
        """
        Find all elements in the parser by selector, children of found
        elements.

        :param selector: The selector.
        :type selector: str or hatemile.util.html.htmldomelement.HTMLDOMElement
        :return: The parser with the elements found.
        :rtype: hatemile.util.html.htmldomparser.HTMLDOMParser
        """

        pass

    def find_descendants(self, selector):
        """
        Find all elements in the parser by selector, descendants of found
        elements.

        :param selector: The selector.
        :type selector: str or hatemile.util.html.htmldomelement.HTMLDOMElement
        :return: The parser with the elements found.
        :rtype: hatemile.util.html.htmldomparser.HTMLDOMParser
        """

        pass

    def find_ancestors(self, selector):
        """
        Find all elements in the parser by selector, ancestors of found
        elements.

        :param selector: The selector.
        :type selector: str or hatemile.util.html.htmldomelement.HTMLDOMElement
        :return: The parser with the elements found.
        :rtype: hatemile.util.html.htmldomparser.HTMLDOMParser
        """

        pass

    def first_result(self):
        """
        Returns the first element found.

        :return: The first element found or None if not have elements found.
        :rtype: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        pass

    def last_result(self):
        """
        Returns the last element found.

        :return: The last element found or None if not have elements found.
        :rtype: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        pass

    def list_results(self):
        """
        Returns a list with all elements found.

        :return: The list with all elements found.
        :rtype: list(hatemile.util.html.htmldomelement.HTMLDOMElement)
        """

        pass

    def create_element(self, tag):
        """
        Create a element.

        :param tag: The tag of element.
        :type tag: str
        :return: The element created.
        :rtype: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        pass

    def get_html(self):
        """
        Returns the HTML code of parser.

        :return: The HTML code of parser.
        :rtype: str
        """

        pass

    def get_parser(self):
        """
        Returns the parser.

        :return: The parser or root element of the parser.
        :rtype: object
        """

        pass

    def clear_parser(self):
        """
        Clear the memory of this object.
        """

        pass
