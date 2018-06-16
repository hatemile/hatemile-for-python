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
    The AccessibleNavigation interface improve the accessibility of navigation.
    """

    def provide_navigation_by_skipper(self, element):
        """
        Provide a content skipper for element.

        :param element: The element.
        :type element: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        pass

    def provide_navigation_by_all_skippers(self):
        """
        Provide navigation by content skippers.
        """

        pass

    def provide_navigation_by_heading(self, heading):
        """
        Provide navigation by heading.

        :param heading: The heading element.
        :type heading: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        pass

    def provide_navigation_by_all_headings(self):
        """
        Provide navigation by headings of page.
        """

        pass

    def provide_navigation_to_long_description(self, image):
        """
        Provide an alternative way to access the long description of element.

        :param image: The image with long description.
        :type image: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        pass

    def provide_navigation_to_all_long_descriptions(self):
        """
        Provide an alternative way to access the longs descriptions of all
        elements of page.
        """

        pass
