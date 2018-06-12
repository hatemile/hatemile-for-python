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
Module of AccessibleTableImplementation class.
"""

from hatemile.accessibletable import AccessibleTable
from hatemile.util.commonfunctions import CommonFunctions


class AccessibleTableImplementation(AccessibleTable):
    """
    The AccessibleTableImpl class is official implementation of AccessibleTable
    interface.
    """

    def __init__(self, parser, configure):
        """
        Initializes a new object that manipulate the accessibility of the
        tables of parser.

        :param parser: The HTML parser.
        :type parser: hatemile.util.htmldomparser.HTMLDOMParser
        :param configure: The configuration of HaTeMiLe.
        :type configure: hatemile.util.configure.Configure
        """

        self.parser = parser
        self.prefix_id = configure.get_parameter('prefix-generated-ids')
        self.data_ignore = 'data-ignoreaccessibilityfix'

    def _generate_part(self, part):
        """
        Returns a list that represents the table.

        :param part: The table header, table footer or table body.
        :type part: hatemile.util.htmldomelement.HTMLDOMElement
        :return: The list that represents the table.
        :rtype: list(list(hatemile.util.htmldomelement.HTMLDOMElement))
        """

        rows = self.parser.find(part).find_children('tr').list_results()
        table = []
        for row in rows:
            table.append(self._generate_colspan(self.parser.find(
                row
            ).find_children('td,th').list_results()))
        return self._generate_rowspan(table)

    def _generate_rowspan(self, rows):
        """
        Returns a list that represents the table with the rowspans.

        :param rows: The list that represents the table without the rowspans.
        :type rows: list(list(hatemile.util.htmldomelement.HTMLDOMElement))
        :return The list that represents the table with the rowspans.
        :rtype: list(list(hatemile.util.htmldomelement.HTMLDOMElement))
        """

        copy = [] + rows
        table = []
        if bool(rows):
            length_rows = len(rows)
            for i in range(0, length_rows):
                column_index = 0
                cells = [] + copy[i]
                if len(table) <= i:
                    table.append([])
                length_cells = len(cells)
                for j in range(0, length_cells):
                    cell = cells[j]
                    new_column_index = j + column_index
                    row = table[i]
                    while True:
                        if len(row) <= new_column_index:
                            row.append(None)
                            break
                        elif row[new_column_index] is None:
                            break
                        else:
                            column_index += 1
                            new_column_index = j + column_index
                    row[new_column_index] = cell
                    if cell.has_attribute('rowspan'):
                        rowspan = int(cell.get_attribute('rowspan'))
                        if rowspan > 1:
                            for k in range(1, rowspan):
                                new_row_index = i + k
                                if len(table) <= new_row_index:
                                    table.append([])
                                while (
                                    len(table[new_row_index])
                                    < new_column_index
                                ):
                                    table[new_row_index].append(None)
                                table[new_row_index].append(cell)
        return table

    def _generate_colspan(self, row):
        """
        Returns a list that represents the line of table with the colspans.

        :param row: The list that represents the line of table without the
                    colspans.
        :type row: list(hatemile.util.htmldomelement.HTMLDOMElement)
        :return: The list that represents the line of table with the colspans.
        :rtype: list(hatemile.util.htmldomelement.HTMLDOMElement)
        """

        copy = [] + row
        cells = [] + row
        size = len(row)
        for i in range(0, size):
            cell = cells[i]
            if cell.has_attribute('colspan'):
                colspan = int(cell.get_attribute('colspan'))
                if colspan > 1:
                    for j in range(1, colspan):
                        copy.insert(i + j, cell)
        return copy

    def _validate_header(self, header):
        """
        Validate the list that represents the table header.

        :param header: The list that represents the table header.
        :type header: list(list(hatemile.util.htmldomelement.HTMLDOMElement))
        :return: True if the table header is valid or False if the table header
                 is not valid.
        :rtype: bool
        """

        if not bool(header):
            return False
        length = -1
        for row in header:
            if not bool(row):
                return False
            elif length == -1:
                length = len(row)
            elif len(row) != length:
                return False
        return True

    def _return_list_ids_columns(self, header, index):
        """
        Returns a list with ids of rows of same column.

        :param header: The list that represents the table header.
        :type header: list(list(hatemile.util.htmldomelement.HTMLDOMElement))
        :param index: The index of columns.
        :type index: int
        :return: The list with ids of rows of same column.
        :rtype: list(str)
        """

        ids = []
        for row in header:
            if row[index].get_tag_name() == 'TH':
                ids.append(row[index].get_attribute('id'))
        return ids

    def _fix_body_or_footer(self, element):
        """
        Fix the table body or table footer.

        :param element: The table body or table footer.
        :type element: hatemile.util.htmldomelement.HTMLDOMElement
        """

        table = self._generate_part(element)
        for cells in table:
            headers_ids = []
            for cell in cells:
                if cell.get_tag_name() == 'TH':
                    CommonFunctions.generate_id(cell, self.prefix_id)
                    headers_ids.append(cell.get_attribute('id'))

                    cell.set_attribute('scope', 'row')
            if bool(headers_ids):
                for cell in cells:
                    if cell.get_tag_name() == 'TD':
                        headers = cell.get_attribute('headers')
                        for header_id in headers_ids:
                            headers = CommonFunctions.increase_in_list(
                                headers,
                                header_id
                            )
                        cell.set_attribute('headers', headers)

    def _fix_header(self, table_header):
        """
        Fix the table header.

        :param table_header: The table header.
        :type table_header: hatemile.util.htmldomelement.HTMLDOMElement
        """

        cells = self.parser.find(table_header).find_children(
            'tr'
        ).find_children('th').list_results()
        for cell in cells:
            CommonFunctions.generate_id(cell, self.prefix_id)

            cell.set_attribute('scope', 'col')

    def fix_association_cells_table(self, table):
        header = self.parser.find(table).find_children('thead').first_result()
        body = self.parser.find(table).find_children('tbody').first_result()
        footer = self.parser.find(table).find_children('tfoot').first_result()
        if header is not None:
            self._fix_header(header)

            header_cells = self._generate_part(header)
            if (body is not None) and (self._validate_header(header_cells)):
                length_header = len(header_cells[0])
                fake_table = self._generate_part(body)
                if footer is not None:
                    fake_table = fake_table + self._generate_part(footer)
                for cells in fake_table:
                    if len(cells) == length_header:
                        i = 0
                        for cell in cells:
                            headers_ids = self._return_list_ids_columns(
                                header_cells,
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
            self._fix_body_or_footer(body)
        if footer is not None:
            self._fix_body_or_footer(footer)

    def fix_association_cells_tables(self):
        tables = self.parser.find('table').list_results()
        for table in tables:
            if not table.has_attribute(self.data_ignore):
                self.fix_association_cells_table(table)
