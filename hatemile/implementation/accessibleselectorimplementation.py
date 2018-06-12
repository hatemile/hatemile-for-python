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
Module of AccessibleSelectorImplementation class.
"""

from hatemile.accessibleselector import AccessibleSelector


class AccessibleSelectorImplementation(AccessibleSelector):
    """
    The AccessibleSelectorImpl class is official implementation of
    AccessibleSelector interface.
    """

    def __init__(self, parser, configure):
        """
        Initializes a new object that manipulate the accessibility through of
        the selectors of the configuration file.

        :param parser: The HTML parser.
        :type parser: hatemile.util.htmldomparser.HTMLDOMParser
        :param configure: The configuration of HaTeMiLe.
        :type configure: hatemile.util.configure.Configure
        """

        self.parser = parser
        self.changes = configure.get_selector_changes()
        self.data_ignore = 'data-ignoreaccessibilityfix'

    def fix_selectors(self):
        for change in self.changes:
            elements = self.parser.find(change.get_selector()).list_results()
            for element in elements:
                if not element.has_attribute(self.data_ignore):
                    element.set_attribute(
                        change.get_attribute(),
                        change.get_value_for_attribute()
                    )
