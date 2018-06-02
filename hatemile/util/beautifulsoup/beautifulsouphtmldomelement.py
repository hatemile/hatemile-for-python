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

import copy
import re
from bs4 import BeautifulSoup
from bs4 import PageElement
from hatemile.util.htmldomelement import HTMLDOMElement


class BeautifulSoupHTMLDOMElement(HTMLDOMElement):
    """
    The BeautifulSoupHTMLDOMElement class is official implementation of
    HTMLDOMElement interface for the BeautifulSoup library.
    """

    def __init__(self, element):
        """
        Initializes a new object that encapsulate the BeautifulSoup Tag.
        @param element: The BeautifulSoup Tag.
        @type element: bs4.element.Tag
        """

        self.data = element

    def get_tag_name(self):
        return self.data.name.upper()

    def get_attribute(self, name):
        if not self.has_attribute(name):
            return None
        if isinstance(self.data[name], list):
            values = self.data[name]
            value = ''
            for item in values:
                value += item + ' '
            return value.strip()
        else:
            return self.data[name]

    def set_attribute(self, name, value):
        self.data[name] = value
        if bool(re.findall('^data-', name)):
            self.data[re.sub('^data-', 'dataaaaaa', name)] = value

    def remove_attribute(self, name):
        if self.has_attribute(name):
            del self.data[name]
            if bool(re.findall('^data-', name)):
                del self.data[re.sub('^data-', 'dataaaaaa', name)]

    def has_attribute(self, name):
        return self.data.has_attr(name)

    def has_attributes(self):
        return bool(self.data.attrs)

    def get_text_content(self):
        return self.data.get_text()

    def insert_before(self, new_element):
        self.data.insert_before(new_element.get_data())
        return new_element

    def insert_after(self, new_element):
        self.data.insert_after(new_element.get_data())
        return new_element

    def remove_element(self):
        self.data.extract()
        return self

    def replace_element(self, new_element):
        self.data.replace_with(new_element.get_data())
        return new_element

    def append_element(self, element):
        self.data.append(element.get_data())
        return element

    def get_children(self):
        children = []
        for child in self.data.children:
            if isinstance(child, PageElement):
                children.append(BeautifulSoupHTMLDOMElement(child))
        return children

    def append_text(self, text):
        self.data.append(text)

    def has_children(self):
        return bool(self.get_children())

    def get_parent_element(self):
        return BeautifulSoupHTMLDOMElement(self.data.parent)

    def get_inner_html(self):
        string = ''
        for child in self.data.children:
            string += str(child)
        return string

    def set_inner_html(self, html):
        document_auxiliar = BeautifulSoup(html, 'html.parser')
        children = []
        for child in self.data.children:
            children.append(child)
        for child in children:
            child.extract()
        for child in document_auxiliar.children:
            self.data.append(child)

    def get_outer_html(self):
        return str(self.data)

    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = data

    def clone_element(self):
        return BeautifulSoupHTMLDOMElement(copy.copy(self.data))

    def get_first_element_child(self):
        if not self.has_children():
            return None
        for child in self.data.children:
            if isinstance(child, PageElement):
                return BeautifulSoupHTMLDOMElement(child)
        return None

    def get_last_element_child(self):
        if not self.has_children():
            return None
        last_value = None
        for child in self.data.children:
            if isinstance(child, PageElement):
                last_value = child
        if last_value is not None:
            return BeautifulSoupHTMLDOMElement(last_value)
        return None
