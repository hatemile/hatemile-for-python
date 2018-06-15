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
Module of HTMLDOMNode interface.
"""


class HTMLDOMNode:
    """
    The HTMLDOMNode interface contains the methods for access the Node.
    """

    def get_text_content(self):
        """
        Returns the text content of node.

        :return: The text content of node.
        :rtype: str
        """

        pass

    def insert_before(self, new_node):
        """
        Insert a node before this node.

        :param new_node: The node that be inserted.
        :type new_node: hatemile.util.html.htmldomnode.HTMLDOMNode
        :return: This node.
        :rtype: hatemile.util.html.htmldomnode.HTMLDOMNode
        """

        pass

    def insert_after(self, new_node):
        """
        Insert a node after this node.

        :param new_node: The node that be inserted.
        :type new_node: hatemile.util.html.htmldomnode.HTMLDOMNode
        :return: This node.
        :rtype: hatemile.util.html.htmldomnode.HTMLDOMNode
        """

        pass

    def remove_node(self):
        """
        Remove this node of the parser.

        :return: This node.
        :rtype: hatemile.util.html.htmldomnode.HTMLDOMNode
        """

        pass

    def replace_node(self, new_node):
        """
        Replace this node for other node.

        :param new_node: The node that replace this node.
        :type new_node: hatemile.util.html.htmldomnode.HTMLDOMNode
        :return: This node.
        :rtype: hatemile.util.html.htmldomnode.HTMLDOMNode
        """

        pass

    def append_text(self, text):
        """
        Append a text content in node.

        :param text: The text content.
        :type text: str
        :return: This node.
        :rtype: hatemile.util.html.htmldomnode.HTMLDOMNode
        """

        pass

    def prepend_text(self, text):
        """
        Prepend a text content in node.

        :param text: The text content.
        :type text: str
        :return: This node.
        :rtype: hatemile.util.html.htmldomnode.HTMLDOMNode
        """

        pass

    def get_parent_element(self):
        """
        Returns the parent element of this node.

        :return: The parent element of this node.
        :rtype: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        pass

    def get_data(self):
        """
        Returns the native object of this node.

        :return: The native object of this node.
        :rtype: object
        """

        pass

    def set_data(self, data):
        """
        Modify the native object of this node.

        :param data: The native object of this node.
        :type data: object
        """

        pass
