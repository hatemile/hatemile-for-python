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
Module of AccessibleNavigation interface.
"""


class AccessibleNavigation:
    """
    The AccessibleNavigation interface fixes accessibility problems associated
    with navigation.
    """

    def fix_shortcut(self, element):
        """
        Display the shortcuts of element.

        :param element: The element with shortcuts.
        :type element: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        pass

    def fix_shortcuts(self):
        """
        Display the shortcuts of elements.
        """

        pass

    def fix_skipper(self, element, skipper):
        """
        Provide content skipper for element.

        :param element: The element.
        :type element: hatemile.util.html.htmldomelement.HTMLDOMElement
        :param skipper: The skipper.
        :type skipper: list(dict(str, str))
        """

        pass

    def fix_skippers(self):
        """
        Provide content skippers.
        """

        pass

    def fix_heading(self, element):
        """
        Provide a navigation by heading.

        :param element: The heading element.
        :type element: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        pass

    def fix_headings(self):
        """
        Provide a navigation by headings.
        """

        pass

    def fix_long_description(self, element):
        """
        Provide an alternative way to access the long description of element.

        :param element: The element with long description.
        :type element: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        pass

    def fix_long_descriptions(self):
        """
        Provide an alternative way to access the longs descriptions of
        elements.
        """

        pass
