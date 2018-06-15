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
Module of BeautifulSoupHTMLDOMElement class.
"""

import copy
import re
from bs4.element import Tag
from hatemile.util.html.htmldomelement import HTMLDOMElement
from .beautifulsouphtmldomnode import BeautifulSoupHTMLDOMNode


class BeautifulSoupHTMLDOMElement(BeautifulSoupHTMLDOMNode, HTMLDOMElement):
    """
    The BeautifulSoupHTMLDOMElement class is official implementation of
    HTMLDOMElement interface for the BeautifulSoup library.
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

    def get_children(self):
        children = []
        for child in self.node.children:
            if isinstance(child, Tag):
                children.append(BeautifulSoupHTMLDOMElement(child))
        return children

    def append_text(self, text):
        self.node.append(text)
        return self

    def has_children(self):
        return bool(self.get_children())

    def get_parent_element(self):
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
        if not self.has_children():
            return None
        for child in self.node.children:
            if isinstance(child, Tag):
                return BeautifulSoupHTMLDOMElement(child)
        return None

    def get_last_element_child(self):
        if not self.has_children():
            return None
        last_value = None
        for child in self.node.children:
            if isinstance(child, Tag):
                last_value = child
        if last_value is not None:
            return BeautifulSoupHTMLDOMElement(last_value)
        return None

    def __eq__(self, obj):
        if isinstance(obj, BeautifulSoupHTMLDOMElement):
            return self.get_data() == obj.get_data()
        return False
