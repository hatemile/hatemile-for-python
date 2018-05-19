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

class HTMLDOMElement:
    """
    The HTMLDOMElement interface contains the methods for access of the HTML
    element.
    """

    def getTagName(self):
        """
        Returns the tag name of element.
        @return: The tag name of element in uppercase letters.
        @rtype: str
        """

        pass

    def getAttribute(self, name):
        """
        Returns the value of a attribute.
        @param name: The name of attribute.
        @type name: str
        @return: The value of the attribute, if the element not contains the
        attribute returns None.
        @rtype: str
        """

        pass

    def setAttribute(self, name, value):
        """
        Create or modify a attribute.
        @param name: The name of attribute.
        @type name: str
        @param value: The value of attribute.
        @type value: str
        """

        pass

    def removeAttribute(self, name):
        """
        Remove a attribute of element.
        @param name: The name of attribute.
        @type name: str
        """

        pass

    def hasAttribute(self, name):
        """
        Returns if the element has an attribute.
        @param name: The name of attribute.
        @type name: str
        @return: True if the element has the attribute or False if the element not
        has the attribute.
        @rtype: bool
        """

        pass

    def hasAttributes(self):
        """
        Returns if the element has attributes.
        @return: True if the element has attributes or False if the element not
        has attributes.
        @rtype: bool
        """

        pass

    def getTextContent(self):
        """
        Returns the text of element.
        @return: The text of element.
        @rtype: str
        """

        pass

    def insertBefore(self, newElement):
        """
        Insert a element before this element.
        @param newElement: The element that be inserted.
        @type newElement: L{hatemile.util.HTMLDOMElement}
        @return: The element inserted.
        @rtype: L{hatemile.util.HTMLDOMElement}
        """

        pass

    def insertAfter(self, newElement):
        """
        Insert a element after this element.
        @param newElement: The element that be inserted.
        @type newElement: L{hatemile.util.HTMLDOMElement}
        @return: The element inserted.
        @rtype: L{hatemile.util.HTMLDOMElement}
        """

        pass

    def removeElement(self):
        """
        Remove this element of the parser.
        @return: The removed element.
        @rtype: L{hatemile.util.HTMLDOMElement}
        """

        pass

    def replaceElement(self, newElement):
        """
        Replace this element for other element.
        @param newElement: The element that replace this element.
        @type newElement: L{hatemile.util.HTMLDOMElement}
        @return: The element replaced.
        @rtype: L{hatemile.util.HTMLDOMElement}
        """

        pass

    def appendElement(self, element):
        """
        Append a element child.
        @param element: The element that be inserted.
        @type element: L{hatemile.util.HTMLDOMElement}
        @return: The element inserted.
        @rtype: L{hatemile.util.HTMLDOMElement}
        """

        pass

    def getChildren(self):
        """
        Returns the children of this element.
        @return: The children of this element.
        @rtype: array.L{hatemile.util.HTMLDOMElement}
        """

        pass

    def appendText(self, text):
        """
        Append a text child.
        @param text: The text.
        @type text: str
        """

        pass

    def hasChildren(self):
        """
        Returns if the element has children.
        @return: True if the element has children or False if the element not has
        children.
        @rtype: bool
        """

        pass

    def getParentElement(self):
        """
        Returns the parent element of this element.
        @return: The parent element of this element.
        @rtype: L{hatemile.util.HTMLDOMElement}
        """

        pass

    def getInnerHTML(self):
        """
        Returns the inner HTML code of this element.
        @return: The inner HTML code of this element.
        @rtype: str
        """

        pass

    def setInnerHTML(self, html):
        """
        Modify the inner HTML code of this element.
        @param html: The HTML code.
        @type html: str
        """

        pass

    def getOuterHTML(self):
        """
        Returns the HTML code of this element.
        @return: The HTML code of this element.
        @rtype: str
        """

        pass

    def getData(self):
        """
        Returns the native object of this element.
        @return: The native object of this element.
        @rtype: object
        """

        pass

    def setData(self, data):
        """
        Modify the native object of this element.
        @param data: Modify the native object of this element.
        @type data: object
        """

        pass

    def cloneElement(self):
        """
        Clone this element.
        @return: The clone.
        @rtype: L{hatemile.util.HTMLDOMElement}
        """

        pass

    def getFirstElementChild(self):
        """
        Returns the first element child of this element.
        @return: The first element child of this element.
        @rtype: L{hatemile.util.HTMLDOMElement}
        """

        pass

    def getLastElementChild(self):
        """
        Returns the last element child of this element.
        @return: The last element child of this element.
        @rtype: L{hatemile.util.HTMLDOMElement}
        """

        pass
