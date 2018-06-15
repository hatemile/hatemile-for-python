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
Module of AccessibleAssociation interface.
"""


class AccessibleAssociation:
    """
    The AccessibleAssociation interface improve accessibility, associating
    elements.
    """

    def fix_association_cells_table(self, table):
        """
        Associate all data cells with header cells of table.

        :param table: The table.
        :type table: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        pass

    def fix_association_cells_tables(self):
        """
        Associate all data cells with header cells of all tables of page.
        """

        pass

    def fix_label(self, label):
        """
        Associate label with field.

        :param label: The label.
        :type label: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        pass

    def fix_labels(self):
        """
        Associate all labels of page with fields.
        """

        pass
