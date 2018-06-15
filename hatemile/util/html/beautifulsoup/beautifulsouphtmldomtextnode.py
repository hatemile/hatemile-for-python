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
Module of BeautifulSoupHTMLDOMTextNode class.
"""

from bs4.element import NavigableString
from hatemile.util.html.htmldomtextnode import HTMLDOMTextNode
from .beautifulsouphtmldomelement import BeautifulSoupHTMLDOMElement
from .beautifulsouphtmldomnode import BeautifulSoupHTMLDOMNode


class BeautifulSoupHTMLDOMTextNode(BeautifulSoupHTMLDOMNode, HTMLDOMTextNode):
    """
    The VanillaHTMLDOMTextNode class is official implementation of
    :py:class:`hatemile.util.html.htmldomtextnode.HTMLDOMTextNode` for the
    :py:class:`bs4.element.NavigableString`.
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
