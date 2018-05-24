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


class HTMLDOMParser:
    """
    The HTMLDOMParser interface contains the methods for access a native
    parser.
    """

    def find(self, selector):
        """
        Find all elements in the parser by selector.
        @param selector: The selector.
        @type selector: str or L{hatemile.util.HTMLDOMElement}
        @return: The parser with the elements found.
        @rtype: L{hatemile.util.HTMLDOMParser}
        """

        pass

    def findChildren(self, selector):
        """
        Find all elements in the parser by selector, children of found
        elements.
        @param selector: The selector.
        @type selector: str or L{hatemile.util.HTMLDOMElement}
        @return: The parser with the elements found.
        @rtype: L{hatemile.util.HTMLDOMParser}
        """

        pass

    def findDescendants(self, selector):
        """
        Find all elements in the parser by selector, descendants of found
        elements.
        @param selector: The selector.
        @type selector: str or L{hatemile.util.HTMLDOMElement}
        @return: The parser with the elements found.
        @rtype: L{hatemile.util.HTMLDOMParser}
        """

        pass

    def findAncestors(self, selector):
        """
        Find all elements in the parser by selector, ancestors of found
        elements.
        @param selector: The selector.
        @type selector: str or L{hatemile.util.HTMLDOMElement}
        @return: The parser with the elements found.
        @rtype: L{hatemile.util.HTMLDOMParser}
        """

        pass

    def firstResult(self):
        """
        Returns the first element found.
        @return: The first element found or None if not have elements found.
        @rtype: L{hatemile.util.HTMLDOMElement}
        """

        pass

    def lastResult(self):
        """
        Returns the last element found.
        @return: The last element found or None if not have elements found.
        @rtype: L{hatemile.util.HTMLDOMElement}
        """

        pass

    def listResults(self):
        """
        Returns a list with all elements found.
        @return: The list with all elements found.
        @rtype: array.L{hatemile.util.HTMLDOMElement}
        """

        pass

    def createElement(self, tag):
        """
        Create a element.
        @param tag: The tag of element.
        @type tag: str
        @return: The element created.
        @rtype: L{hatemile.util.HTMLDOMElement}
        """

        pass

    def getHTML(self):
        """
        Returns the HTML code of parser.
        @return: The HTML code of parser.
        @rtype: str
        """

        pass

    def getParser(self):
        """
        Returns the parser.
        @return: The parser or root element of the parser.
        @rtype: object
        """

        pass

    def clearParser(self):
        """
        Clear the memory of this object.
        """

        pass
