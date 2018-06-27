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
Module of HTMLDOMElement interface.
"""

from .htmldomnode import HTMLDOMNode


class HTMLDOMElement(HTMLDOMNode):
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
        :return: The value of the attribute or None if the element not contains
                 the attribute.
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
        Check that the element has an attribute.

        :param name: The name of attribute.
        :type name: str
        :return: True if the element has the attribute or False if the element
                 not has the attribute.
        :rtype: bool
        """

        pass

    def has_attributes(self):
        """
        Check that the element has attributes.

        :return: True if the element has attributes or False if the element not
                 has attributes.
        :rtype: bool
        """

        pass

    def append_element(self, element):
        """
        Append a element child.

        :param element: The element that be inserted.
        :type element: hatemile.util.html.htmldomelement.HTMLDOMElement
        :return: This element.
        :rtype: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        pass

    def prepend_element(self, element):
        """
        Prepend a element child.

        :param element: The element that be inserted.
        :type element: hatemile.util.html.htmldomelement.HTMLDOMElement
        :return: This element.
        :rtype: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        pass

    def get_children_elements(self):
        """
        Returns the elements children of this element.

        :return: The elements children of this element.
        :rtype: list(hatemile.util.html.htmldomelement.HTMLDOMElement)
        """

        pass

    def get_children(self):
        """
        Returns the children of this element.

        :return: The children of this element.
        :rtype: list(hatemile.util.html.htmldomnode.HTMLDOMNode)
        """

        pass

    def normalize(self):
        """
        Joins adjacent Text nodes.

        :return: This element.
        :rtype: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        pass

    def has_children_elements(self):
        """
        Check that the element has elements children.

        :return: True if the element has elements children or False if the
                 element not has elements children.
        :rtype: bool
        """

        pass

    def has_children(self):
        """
        Check that the element has children.

        :return: True if the element has children or False if the element not
                 has children.
        :rtype: bool
        """

        pass

    def get_inner_html(self):
        """
        Returns the inner HTML code of this element.

        :return: The inner HTML code of this element.
        :rtype: str
        """

        pass

    def get_outer_html(self):
        """
        Returns the HTML code of this element.

        :return: The HTML code of this element.
        :rtype: str
        """

        pass

    def clone_element(self):
        """
        Clone this element.

        :return: The clone.
        :rtype: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        pass

    def get_first_element_child(self):
        """
        Returns the first element child of this element.

        :return: The first element child of this element.
        :rtype: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        pass

    def get_last_element_child(self):
        """
        Returns the last element child of this element.

        :return: The last element child of this element.
        :rtype: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        pass

    def get_first_node_child(self):
        """
        Returns the first node child of this element.

        :return: The first node child of this element.
        :rtype: hatemile.util.html.htmldomnode.HTMLDOMNode
        """

        pass

    def get_last_node_child(self):
        """
        Returns the last node child of this element.

        :return: The last node child of this element.
        :rtype: hatemile.util.html.htmldomnode.HTMLDOMNode
        """

        pass
