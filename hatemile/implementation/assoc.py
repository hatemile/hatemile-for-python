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
Module of AccessibleAssociationImplementation class.
"""

import re
from hatemile import helper
from hatemile.accessibleassociation import AccessibleAssociation
from hatemile.util.commonfunctions import CommonFunctions
from hatemile.util.idgenerator import IDGenerator
from hatemile.util.html.htmldomparser import HTMLDOMParser


class AccessibleAssociationImplementation(AccessibleAssociation):
    """
    The AccessibleAssociationImplementation class is official implementation of
    :py:class:`hatemile.accessibleassociation.AccessibleAssociation`.
    """

    def __init__(self, parser):
        """
        Initializes a new object that improve the accessibility of associations
        of parser.

        :param parser: The HTML parser.
        :type parser: hatemile.util.html.htmldomparser.HTMLDOMParser
        """

        helper.require_not_none(parser)
        helper.require_valid_type(parser, HTMLDOMParser)

        self.parser = parser
        self.id_generator = IDGenerator('association')

    def _get_model_table(self, part):
        """
        Returns a list that represents the table.

        :param part: The table header, table footer or table body.
        :type part: hatemile.util.html.htmldomelement.HTMLDOMElement
        :return: The list that represents the table.
        :rtype: list(list(hatemile.util.html.htmldomelement.HTMLDOMElement))
        """

        rows = self.parser.find(part).find_children('tr').list_results()
        table = []
        for row in rows:
            table.append(self._get_model_row(self.parser.find(
                row
            ).find_children('td,th').list_results()))
        return self._get_valid_model_table(table)

    def _get_valid_model_table(self, ros):
        """
        Returns a list that represents the table with the rowspans.

        :param ros: The list that represents the table without the rowspans.
        :type ros: list(list(hatemile.util.html.htmldomelement.HTMLDOMElement))
        :return The list that represents the table with the rowspans.
        :rtype: list(list(hatemile.util.html.htmldomelement.HTMLDOMElement))
        """
        # pylint: disable=no-self-use

        new_table = []
        if bool(ros):
            length_table = len(ros)
            for row_index in range(0, length_table):
                cells_added = 0
                original_row = [] + ros[row_index]
                if len(new_table) <= row_index:
                    new_table.append([])
                length_row = len(original_row)
                for cell_index in range(0, length_row):
                    cell = original_row[cell_index]
                    new_cell_index = cell_index + cells_added
                    new_row = new_table[row_index]
                    while True:
                        if len(new_row) <= new_cell_index:
                            new_row.append(None)
                            break
                        elif new_row[new_cell_index] is None:
                            break
                        else:
                            cells_added += 1
                            new_cell_index = cell_index + cells_added
                    new_row[new_cell_index] = cell
                    if cell.has_attribute('rowspan'):
                        rowspan = int(cell.get_attribute('rowspan'))
                        if rowspan > 1:
                            for rowspan_index in range(1, rowspan):
                                new_row_index = row_index + rowspan_index
                                if len(new_table) <= new_row_index:
                                    new_table.append([])
                                while (
                                    len(new_table[new_row_index])
                                    < new_cell_index
                                ):
                                    new_table[new_row_index].append(None)
                                new_table[new_row_index].append(cell)
        return new_table

    def _get_model_row(self, row):
        """
        Returns a list that represents the line of table with the colspans.

        :param row: The list that represents the line of table without the
                    colspans.
        :type row: list(hatemile.util.html.htmldomelement.HTMLDOMElement)
        :return: The list that represents the line of table with the colspans.
        :rtype: list(hatemile.util.html.htmldomelement.HTMLDOMElement)
        """
        # pylint: disable=no-self-use

        new_row = [] + row
        size = len(row)
        for i in range(0, size):
            cell = row[i]
            if cell.has_attribute('colspan'):
                colspan = int(cell.get_attribute('colspan'))
                if colspan > 1:
                    for j in range(1, colspan):
                        new_row.insert(i + j, cell)
        return new_row

    def _validate_header(self, hed):
        """
        Validate the list that represents the table header.

        :param hed: The list that represents the table header.
        :type hed: list(list(hatemile.util.html.htmldomelement.HTMLDOMElement))
        :return: True if the table header is valid or False if the table header
                 is not valid.
        :rtype: bool
        """
        # pylint: disable=no-self-use

        if not bool(hed):
            return False
        length = -1
        for row in hed:
            if not bool(row):
                return False
            elif length == -1:
                length = len(row)
            elif len(row) != length:
                return False
        return True

    def _get_cells_headers_ids(self, hed, index):
        """
        Returns a list with ids of rows of same column.

        :param hed: The list that represents the table header.
        :type hed: list(list(hatemile.util.html.htmldomelement.HTMLDOMElement))
        :param index: The index of columns.
        :type index: int
        :return: The list with ids of rows of same column.
        :rtype: list(str)
        """
        # pylint: disable=no-self-use

        ids = []
        for row in hed:
            if row[index].get_tag_name() == 'TH':
                ids.append(row[index].get_attribute('id'))
        return ids

    def _associate_data_cells_with_header_cells_of_row(self, element):
        """
        Associate the data cell with header cell of row.

        :param element: The table body or table footer.
        :type element: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        table = self._get_model_table(element)
        for row in table:
            headers_ids = []
            for cell in row:
                if cell.get_tag_name() == 'TH':
                    self.id_generator.generate_id(cell)
                    headers_ids.append(cell.get_attribute('id'))

                    cell.set_attribute('scope', 'row')
            if bool(headers_ids):
                for cell in row:
                    if cell.get_tag_name() == 'TD':
                        headers = cell.get_attribute('headers')
                        for header_id in headers_ids:
                            headers = CommonFunctions.increase_in_list(
                                headers,
                                header_id
                            )
                        cell.set_attribute('headers', headers)

    def _prepare_header_cells(self, table_header):
        """
        Set the scope of header cells of table header.

        :param table_header: The table header.
        :type table_header: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        cells = self.parser.find(table_header).find_children(
            'tr'
        ).find_children('th').list_results()
        for cell in cells:
            self.id_generator.generate_id(cell)

            cell.set_attribute('scope', 'col')

    def associate_data_cells_with_header_cells(self, table):
        header = self.parser.find(table).find_children('thead').first_result()
        body = self.parser.find(table).find_children('tbody').first_result()
        footer = self.parser.find(table).find_children('tfoot').first_result()
        if header is not None:
            self._prepare_header_cells(header)

            header_rows = self._get_model_table(header)
            if (body is not None) and (self._validate_header(header_rows)):
                length_header = len(header_rows[0])
                fake_table = self._get_model_table(body)
                if footer is not None:
                    fake_table = fake_table + self._get_model_table(footer)
                for row in fake_table:
                    if len(row) == length_header:
                        i = 0
                        for cell in row:
                            headers_ids = self._get_cells_headers_ids(
                                header_rows,
                                i
                            )
                            headers = cell.get_attribute('headers')
                            for headers_id in headers_ids:
                                headers = CommonFunctions.increase_in_list(
                                    headers,
                                    headers_id
                                )
                            cell.set_attribute('headers', headers)
                            i += 1
        if body is not None:
            self._associate_data_cells_with_header_cells_of_row(body)
        if footer is not None:
            self._associate_data_cells_with_header_cells_of_row(footer)

    def associate_all_data_cells_with_header_cells(self):
        tables = self.parser.find('table').list_results()
        for table in tables:
            if CommonFunctions.is_valid_element(table):
                self.associate_data_cells_with_header_cells(table)

    def associate_label_with_field(self, label):
        if label.get_tag_name() == 'LABEL':
            if label.has_attribute('for'):
                field = self.parser.find(
                    '#'
                    + label.get_attribute('for')
                ).first_result()
            else:
                field = self.parser.find(label).find_descendants(
                    'input,select,textarea'
                ).first_result()

                if field is not None:
                    self.id_generator.generate_id(field)
                    label.set_attribute('for', field.get_attribute('id'))
            if field is not None:
                if not field.has_attribute('aria-label'):
                    field.set_attribute(
                        'aria-label',
                        re.sub(
                            '[ \n\r\t]+',
                            ' ',
                            label.get_text_content().strip()
                        )
                    )

                self.id_generator.generate_id(label)
                field.set_attribute(
                    'aria-labelledby',
                    CommonFunctions.increase_in_list(
                        field.get_attribute('aria-labelledby'),
                        label.get_attribute('id')
                    )
                )

    def associate_all_labels_with_fields(self):
        labels = self.parser.find('label').list_results()
        for label in labels:
            if CommonFunctions.is_valid_element(label):
                self.associate_label_with_field(label)
