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
Module of BeautifulSoupHTMLDOMNode, BeautifulSoupHTMLDOMElement and
BeautifulSoupHTMLDOMTextNode classes.
"""

import copy
import re
from bs4.element import NavigableString
from bs4.element import PageElement
from bs4.element import Tag
from hatemile import helper
from hatemile.util.html.htmldomelement import HTMLDOMElement
from hatemile.util.html.htmldomnode import HTMLDOMNode
from hatemile.util.html.htmldomtextnode import HTMLDOMTextNode


class BeautifulSoupHTMLDOMNode(HTMLDOMNode):
    """
    The VanillaHTMLDOMNode class is official implementation of
    :py:class:`hatemile.util.html.htmldomnode.HTMLDOMNode` for the
    BeautifulSoup library.
    """

    def __init__(self, node):
        """
        Initializes a new object that encapsulate the BeautifulSoup node.

        :param node: The BeautifulSoup node.
        :type node: bs4.element.PageElement
        """

        helper.require_not_none(node)
        helper.require_valid_type(node, PageElement)

        self.node = node

    def insert_before(self, new_node):
        self.node.insert_before(new_node.get_data())
        return self

    def insert_after(self, new_node):
        self.node.insert_after(new_node.get_data())
        return self

    def remove_node(self):
        self.node.extract()
        return self

    def replace_node(self, new_node):
        self.node.replace_with(new_node.get_data())
        return self

    def get_data(self):
        return self.node

    def set_data(self, data):
        helper.require_not_none(data)
        helper.require_valid_type(data, PageElement)

        self.node = data


class BeautifulSoupHTMLDOMElement(BeautifulSoupHTMLDOMNode, HTMLDOMElement):
    """
    The BeautifulSoupHTMLDOMElement class is official implementation of
    :py:class:`hatemile.util.html.htmldomelement.HTMLDOMElement` for the
    BeautifulSoup library.
    """

    def get_tag_name(self):
        return self.node.name.upper()

    def get_attribute(self, name):
        if not self.has_attribute(name):
            return None
        if isinstance(self.node[name], list):
            values = self.node[name]
            value = ''
            for item in values:
                value += item + ' '
            return value.strip()
        return self.node[name]

    def set_attribute(self, name, value):
        self.node[name] = value
        if bool(re.findall('^data-', name)):
            self.node[re.sub('^data-', 'dataaaaaa', name)] = value

    def remove_attribute(self, name):
        if self.has_attribute(name):
            del self.node[name]
            if bool(re.findall('^data-', name)):
                del self.node[re.sub('^data-', 'dataaaaaa', name)]

    def has_attribute(self, name):
        return self.node.has_attr(name)

    def has_attributes(self):
        return bool(self.node.attrs)

    def get_text_content(self):
        return self.node.get_text()

    def append_element(self, element):
        self.node.append(element.get_data())
        return self

    def prepend_element(self, element):
        if self.has_children():
            self.get_first_node_child().insert_before(element)
        else:
            self.append_element(element)
        return self

    def get_children_elements(self):
        children = []
        for child in self.node.children:
            if isinstance(child, Tag):
                children.append(BeautifulSoupHTMLDOMElement(child))
        return children

    def get_children(self):
        children = []
        for child in self.node.children:
            if isinstance(child, Tag):
                children.append(BeautifulSoupHTMLDOMElement(child))
            elif isinstance(child, NavigableString):
                children.append(BeautifulSoupHTMLDOMTextNode(child))
        return children

    def normalize(self):
        if self.has_children():
            last = None
            for child in self.get_children():
                if isinstance(child, BeautifulSoupHTMLDOMElement):
                    child.normalize()
                elif (
                    isinstance(child, BeautifulSoupHTMLDOMTextNode)
                    and isinstance(last, BeautifulSoupHTMLDOMTextNode)
                ):
                    child.prepend_text(last.get_text_content())
                    last.remove_node()
                last = child

    def append_text(self, text):
        self.node.append(text)
        return self

    def prepend_text(self, text):
        if self.has_children():
            self.get_first_node_child().get_data().insert_before(
                NavigableString(text)
            )
        else:
            self.append_text(text)
        return self

    def has_children_elements(self):
        for child in self.node.children:
            if isinstance(child, Tag):
                return True
        return False

    def has_children(self):
        for child in self.node.children:
            if isinstance(child, (NavigableString, Tag)):
                return True
        return False

    def get_parent_element(self):
        if self.node.parent is None:
            return None
        return BeautifulSoupHTMLDOMElement(self.node.parent)

    def get_inner_html(self):
        string = ''
        for child in self.node.children:
            string += str(child)
        return string

    def get_outer_html(self):
        return str(self.node)

    def clone_element(self):
        return BeautifulSoupHTMLDOMElement(copy.copy(self.node))

    def get_first_element_child(self):
        if not self.has_children_elements():
            return None
        for child in self.node.children:
            if isinstance(child, Tag):
                return BeautifulSoupHTMLDOMElement(child)
        return None

    def get_last_element_child(self):
        if not self.has_children_elements():
            return None
        last_value = None
        for child in self.node.children:
            if isinstance(child, Tag):
                last_value = child
        if last_value is not None:
            return BeautifulSoupHTMLDOMElement(last_value)
        return None

    def get_first_node_child(self):
        if not self.has_children():
            return None
        for child in self.node.children:
            if isinstance(child, Tag):
                return BeautifulSoupHTMLDOMElement(child)
            elif isinstance(child, NavigableString):
                return BeautifulSoupHTMLDOMTextNode(child)
        return None

    def get_last_node_child(self):
        if not self.has_children():
            return None
        last_value = None
        for child in self.node.children:
            if isinstance(child, (NavigableString, Tag)):
                last_value = child
        if last_value is not None:
            if isinstance(last_value, Tag):
                return BeautifulSoupHTMLDOMElement(last_value)
            elif isinstance(last_value, NavigableString):
                return BeautifulSoupHTMLDOMTextNode(last_value)
        return None

    def __eq__(self, obj):
        if isinstance(obj, BeautifulSoupHTMLDOMElement):
            return self.get_data() == obj.get_data()
        return False


class BeautifulSoupHTMLDOMTextNode(BeautifulSoupHTMLDOMNode, HTMLDOMTextNode):
    """
    The VanillaHTMLDOMTextNode class is official implementation of
    :py:class:`hatemile.util.html.htmldomtextnode.HTMLDOMTextNode` for the
    BeautifulSoup library.
    """

    def get_text_content(self):
        return str(self.node)

    def set_text_content(self, text):
        new_text_node = BeautifulSoupHTMLDOMTextNode(NavigableString(text))
        self.replace_node(new_text_node)

    def append_text(self, text):
        self.set_text_content(self.get_text_content() + text)
        return self

    def prepend_text(self, text):
        self.set_text_content(text + self.get_text_content())
        return self

    def get_parent_element(self):
        return BeautifulSoupHTMLDOMElement(self.node.parent)
