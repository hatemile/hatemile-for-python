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

    def get_tag_name(self):
        """
        Returns the tag name of element.

        :return: The tag name of element in uppercase letters.
        :rtype: str
        """

        pass

    def get_attribute(self, name):
        """
        Returns the value of a attribute.

        :param name: The name of attribute.
        :type name: str
        :return: The value of the attribute, if the element not contains the
        attribute returns None.
        :rtype: str
        """

        pass

    def set_attribute(self, name, value):
        """
        Create or modify a attribute.

        :param name: The name of attribute.
        :type name: str
        :param value: The value of attribute.
        :type value: str
        """

        pass

    def remove_attribute(self, name):
        """
        Remove a attribute of element.

        :param name: The name of attribute.
        :type name: str
        """

        pass

    def has_attribute(self, name):
        """
        Returns if the element has an attribute.

        :param name: The name of attribute.
        :type name: str
        :return: True if the element has the attribute or False if the element
        not has the attribute.
        :rtype: bool
        """

        pass

    def has_attributes(self):
        """
        Returns if the element has attributes.

        :return: True if the element has attributes or False if the element not
        has attributes.
        :rtype: bool
        """

        pass

    def get_text_content(self):
        """
        Returns the text of element.

        :return: The text of element.
        :rtype: str
        """

        pass

    def insert_before(self, new_element):
        """
        Insert a element before this element.

        :param new_element: The element that be inserted.
        :type new_element: hatemile.util.htmldomelement.HTMLDOMElement
        :return: The element inserted.
        :rtype: hatemile.util.htmldomelement.HTMLDOMElement
        """

        pass

    def insert_after(self, new_element):
        """
        Insert a element after this element.

        :param new_element: The element that be inserted.
        :type new_element: hatemile.util.htmldomelement.HTMLDOMElement
        :return: The element inserted.
        :rtype: hatemile.util.htmldomelement.HTMLDOMElement
        """

        pass

    def remove_element(self):
        """
        Remove this element of the parser.

        :return: The removed element.
        :rtype: hatemile.util.htmldomelement.HTMLDOMElement
        """

        pass

    def replace_element(self, new_element):
        """
        Replace this element for other element.

        :param new_element: The element that replace this element.
        :type new_element: hatemile.util.htmldomelement.HTMLDOMElement
        :return: The element replaced.
        :rtype: hatemile.util.htmldomelement.HTMLDOMElement
        """

        pass

    def append_element(self, element):
        """
        Append a element child.

        :param element: The element that be inserted.
        :type element: hatemile.util.htmldomelement.HTMLDOMElement
        :return: The element inserted.
        :rtype: hatemile.util.htmldomelement.HTMLDOMElement
        """

        pass

    def get_children(self):
        """
        Returns the children of this element.

        :return: The children of this element.
        :rtype: list(hatemile.util.htmldomelement.HTMLDOMElement)
        """

        pass

    def append_text(self, text):
        """
        Append a text child.

        :param text: The text.
        :type text: str
        """

        pass

    def has_children(self):
        """
        Returns if the element has children.

        :return: True if the element has children or False if the element not
        has children.
        :rtype: bool
        """

        pass

    def get_parent_element(self):
        """
        Returns the parent element of this element.

        :return: The parent element of this element.
        :rtype: hatemile.util.htmldomelement.HTMLDOMElement
        """

        pass

    def get_inner_html(self):
        """
        Returns the inner HTML code of this element.

        :return: The inner HTML code of this element.
        :rtype: str
        """

        pass

    def set_inner_html(self, html):
        """
        Modify the inner HTML code of this element.

        :param html: The HTML code.
        :type html: str
        """

        pass

    def get_outer_html(self):
        """
        Returns the HTML code of this element.

        :return: The HTML code of this element.
        :rtype: str
        """

        pass

    def get_data(self):
        """
        Returns the native object of this element.

        :return: The native object of this element.
        :rtype: object
        """

        pass

    def set_data(self, data):
        """
        Modify the native object of this element.

        :param data: Modify the native object of this element.
        :type data: object
        """

        pass

    def clone_element(self):
        """
        Clone this element.

        :return: The clone.
        :rtype: hatemile.util.htmldomelement.HTMLDOMElement
        """

        pass

    def get_first_element_child(self):
        """
        Returns the first element child of this element.

        :return: The first element child of this element.
        :rtype: hatemile.util.htmldomelement.HTMLDOMElement
        """

        pass

    def get_last_element_child(self):
        """
        Returns the last element child of this element.

        :return: The last element child of this element.
        :rtype: hatemile.util.htmldomelement.HTMLDOMElement
        """

        pass
