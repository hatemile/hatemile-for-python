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
Module of StyleSheetParser interface.
"""


class StyleSheetParser:
    """
    The StyleSheetParser interface contains the methods for access the CSS
    parser.
    """

    def get_rules(self, properties):
        """
        Returns the rules of parser by properties.

        :param properties: The properties.
        :type properties: list(str)
        :return: The rules.
        :rtype: list(hatemile.util.css.stylesheetrule.StyleSheetRule)
        """

        pass
