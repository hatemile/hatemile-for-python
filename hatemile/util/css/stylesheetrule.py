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
Module of StyleSheetRule interface.
"""


class StyleSheetRule:
    """
    The StyleSheetRule interface contains the methods for access the CSS rule.
    """

    def has_property(self, property_name):
        """
        Returns that the rule has a declaration with the property.

        :param property_name: The name of property.
        :type property_name: str
        :return: True if the rule has a declaration with the property or False
                 if the rule not has a declaration with the property.
        :rtype: bool
        """

        pass

    def has_declarations(self):
        """
        Returns that the rule has declarations.

        :return: True if the rule has the property or False if the rule not has
                 declarations.
        :rtype: bool
        """

        pass

    def get_declarations(self, property_name):
        """
        Returns the declarations with the property.

        :param property_name: The property.
        :type property_name: str
        :return: The declarations with the property.
        :rtype: hatemile.util.css.stylesheetdeclaration.StyleSheetDeclaration
        """

        pass

    def get_selector(self):
        """
        Returns the selector of rule.

        :return: The selector of rule.
        :rtype: str
        """

        pass
