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

    def associate_data_cells_with_header_cells(self, table):
        """
        Associate all data cells with header cells of table.

        :param table: The table.
        :type table: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        pass

    def associate_all_data_cells_with_header_cells(self):
        """
        Associate all data cells with header cells of all tables of page.
        """

        pass

    def associate_label_with_field(self, label):
        """
        Associate label with field.

        :param label: The label.
        :type label: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        pass

    def associate_all_labels_with_fields(self):
        """
        Associate all labels of page with fields.
        """

        pass
