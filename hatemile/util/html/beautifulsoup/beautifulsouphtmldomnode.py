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
Module of BeautifulSoupHTMLDOMNode class.
"""

from hatemile.util.html.htmldomnode import HTMLDOMNode


class BeautifulSoupHTMLDOMNode(HTMLDOMNode):
    """
    The VanillaHTMLDOMNode class is official implementation of HTMLDOMNode
    interface for the HTMLDOMNode.
    """

    def __init__(self, node):
        """
        Initializes a new object that encapsulate the BeautifulSoup node.

        :param node: The BeautifulSoup node.
        :type node: bs4.element.PageElement
        """

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
        self.node = data
