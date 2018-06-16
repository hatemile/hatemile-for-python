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
Module of AccessibleEvent interface.
"""


class AccessibleEvent:
    """
    The AccessibleEvent interface improve the accessibility, making elements
    events available from a keyboard.
    """

    def make_accessible_drop_events(self, element):
        """
        Make the drop events of element available from a keyboard.

        :param element: The element with drop event.
        :type element: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        pass

    def make_accessible_drag_events(self, element):
        """
        Make the drag events of element available from a keyboard.

        :param element: The element with drag event.
        :type element: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        pass

    def make_accessible_all_drag_and_drop_events(self):
        """
        Make all Drag-and-Drop events of page available from a keyboard.
        """

        pass

    def make_accessible_hover_events(self, element):
        """
        Make the hover events of element available from a keyboard.

        :param element: The element with hover event.
        :type element: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        pass

    def make_accessible_all_hover_events(self):
        """
        Make all hover events of page available from a keyboard.
        """

        pass

    def make_accessible_click_events(self, element):
        """
        Make the click events of element available from a keyboard.

        :param element: The element with click events.
        :type element: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        pass

    def make_accessible_all_click_events(self):
        """
        Make all click events of page available from a keyboard.
        """

        pass
