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

class AccessibleNavigation:
    """
    The AccessibleNavigation interface fixes accessibility problems associated
    with navigation.
    """

    def fixShortcut(self, element):
        """
        Display the shortcuts of element.
        @param element: The element with shortcuts.
        @type element: L{hatemile.util.HTMLDOMElement}
        """

        pass

    def fixShortcuts(self):
        """
        Display the shortcuts of elements.
        """

        pass

    def fixSkipper(self, element, skipper):
        """
        Provide content skipper for element.
        @param element: The element.
        @type element: L{hatemile.util.HTMLDOMElement}
        @param skipper: The skipper.
        @type skipper: L{hatemile.util.Skipper}
        """

        pass

    def fixSkippers(self):
        """
        Provide content skippers.
        """

        pass

    def fixHeading(self, element):
        """
        Provide a navigation by heading.
        @param element: The heading element.
        @type element: L{hatemile.util.HTMLDOMElement}
        """

        pass

    def fixHeadings(self):
        """
        Provide a navigation by headings.
        """

        pass
