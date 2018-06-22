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
Module of AccessibleDisplay interface.
"""


class AccessibleDisplay:
    """
    The AccessibleDisplay interface improve accessibility, showing
    informations.
    """

    def display_shortcut(self, element):
        """
        Display the shortcuts of element.

        :param element: The element with shortcuts.
        :type element: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        pass

    def display_all_shortcuts(self):
        """
        Display all shortcuts of page.
        """

        pass

    def display_role(self, element):
        """
        Display the WAI-ARIA role of element.

        :param element: The element.
        :type element: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        pass

    def display_all_roles(self):
        """
        Display the WAI-ARIA roles of all elements of page.
        """

        pass

    def display_cell_header(self, table_cell):
        """
        Display the headers of each data cell of table.

        :param table_cell: The table cell.
        :type table_cell: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        pass

    def display_all_cell_headers(self):
        """
        Display the headers of each data cell of all tables of page.
        """

        pass

    def display_waiaria_states(self, element):
        """
        Display the WAI-ARIA attributes of element.

        :param element: The element with WAI-ARIA attributes.
        :type element: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        pass

    def display_all_waiaria_states(self):
        """
        Display the WAI-ARIA attributes of all elements of page.
        """

        pass

    def display_link_attributes(self, link):
        """
        Display the attributes of link.

        :param link: The link element.
        :type link: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        pass

    def display_all_links_attributes(self):
        """
        Display the attributes of all links of page.
        """

        pass

    def display_title(self, element):
        """
        Display the title of element.

        :param element: The element with title.
        :type element: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        pass

    def display_all_titles(self):
        """
        Display the titles of all elements of page.
        """

        pass

    def display_language(self, element):
        """
        Display the language of element.

        :param element: The element.
        :type element: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        pass

    def display_all_languages(self):
        """
        Display the language of all elements of page.
        """

        pass

    def display_alternative_text_image(self, image):
        """
        Display the alternative text of image.

        :param image: The image.
        :type image: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        pass

    def display_all_alternative_text_images(self):
        """
        Display the alternative text of all images of page.
        """

        pass
