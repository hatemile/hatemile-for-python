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

from hatemile.util.commonfunctions import CommonFunctions
from hatemile.accessibletable import AccessibleTable


class AccessibleTableImplementation(AccessibleTable):
    """
    The AccessibleTableImpl class is official implementation of AccessibleTable
    interface.
    """

    def __init__(self, parser, configure):
        """
        Initializes a new object that manipulate the accessibility of the
        tables of parser.
        @param parser: The HTML parser.
        @type parser: L{hatemile.util.HTMLDOMParser}
        @param configure: The configuration of HaTeMiLe.
        @type configure: L{hatemile.util.Configure}
        """

        self.parser = parser
        self.prefixId = configure.getParameter('prefix-generated-ids')
        self.dataIgnore = 'data-ignoreaccessibilityfix'

    def _generatePart(self, part):
        """
        Returns a list that represents the table.
        @param part: The table header, table footer or table body.
        @type part: L{hatemile.util.HTMLDOMElement}
        @return: The list that represents the table.
        @rtype: array.array.L{hatemile.util.HTMLDOMElement}
        """

        rows = self.parser.find(part).findChildren('tr').listResults()
        table = []
        for row in rows:
            table.append(self._generateColspan(self.parser.find(
                row
            ).findChildren('td,th').listResults()))
        return self._generateRowspan(table)

    def _generateRowspan(self, rows):
        """
        Returns a list that represents the table with the rowspans.
        @param rows: The list that represents the table without the rowspans.
        @type rows: array.array.L{hatemile.util.HTMLDOMElement}
        @return The list that represents the table with the rowspans.
        @rtype: array.array.L{hatemile.util.HTMLDOMElement}
        """

        copy = [] + rows
        table = []
        if bool(rows):
            lengthRows = len(rows)
            for i in range(0, lengthRows):
                columnIndex = 0
                cells = [] + copy[i]
                if len(table) <= i:
                    table.append([])
                lengthCells = len(cells)
                for j in range(0, lengthCells):
                    cell = cells[j]
                    m = j + columnIndex
                    row = table[i]
                    while True:
                        if len(row) <= m:
                            row.append(None)
                            break
                        elif row[m] is None:
                            break
                        else:
                            columnIndex += 1
                            m = j + columnIndex
                    row[m] = cell
                    if cell.hasAttribute('rowspan'):
                        rowspan = int(cell.getAttribute('rowspan'))
                        if (rowspan > 1):
                            for k in range(1, rowspan):
                                n = i + k
                                if len(table) <= n:
                                    table.append([])
                                while len(table[n]) < m:
                                    table[n].append(None)
                                table[n].append(cell)
        return table

    def _generateColspan(self, row):
        """
        Returns a list that represents the line of table with the colspans.
        @param row: The list that represents the line of table without the
        colspans.
        @type row: array.L{hatemile.util.HTMLDOMElement}
        @return: The list that represents the line of table with the colspans.
        @rtype: array.L{hatemile.util.HTMLDOMElement}
        """

        copy = [] + row
        cells = [] + row
        size = len(row)
        for i in range(0, size):
            cell = cells[i]
            if cell.hasAttribute('colspan'):
                colspan = int(cell.getAttribute('colspan'))
                if colspan > 1:
                    for j in range(1, colspan):
                        copy.insert(i + j, cell)
        return copy

    def _validateHeader(self, header):
        """
        Validate the list that represents the table header.
        @param header: The list that represents the table header.
        @type header: array.array.L{hatemile.util.HTMLDOMElement}
        @return: True if the table header is valid or False if the table header
        is not valid.
        @rtype: bool
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

    def _returnListIdsColumns(self, header, index):
        """
        Returns a list with ids of rows of same column.
        @param header: The list that represents the table header.
        @type header: array.array.L{hatemile.util.HTMLDOMElement}
        @param index: The index of columns.
        @type index: int
        @return: The list with ids of rows of same column.
        @rtype: array.str
        """

        ids = []
        for row in header:
            if row[index].getTagName() == 'TH':
                ids.append(row[index].getAttribute('id'))
        return ids

    def _fixBodyOrFooter(self, element):
        """
        Fix the table body or table footer.
        @param element: The table body or table footer.
        @type element: L{hatemile.util.HTMLDOMElement}
        """

        table = self._generatePart(element)
        for cells in table:
            headersIds = []
            for cell in cells:
                if cell.getTagName() == 'TH':
                    CommonFunctions.generateId(cell, self.prefixId)
                    headersIds.append(cell.getAttribute('id'))

                    cell.setAttribute('scope', 'row')
            if bool(headersIds):
                for cell in cells:
                    if cell.getTagName() == 'TD':
                        headers = cell.getAttribute('headers')
                        for headerId in headersIds:
                            headers = CommonFunctions.increaseInList(
                                headers,
                                headerId
                            )
                        cell.setAttribute('headers', headers)

    def _fixHeader(self, tableHeader):
        """
        Fix the table header.
        @param tableHeader: The table header.
        @type tableHeader: L{hatemile.util.HTMLDOMElement}
        """

        cells = self.parser.find(tableHeader).findChildren('tr').findChildren(
            'th'
        ).listResults()
        for cell in cells:
            CommonFunctions.generateId(cell, self.prefixId)

            cell.setAttribute('scope', 'col')

    def fixAssociationCellsTable(self, table):
        header = self.parser.find(table).findChildren('thead').firstResult()
        body = self.parser.find(table).findChildren('tbody').firstResult()
        footer = self.parser.find(table).findChildren('tfoot').firstResult()
        if header is not None:
            self._fixHeader(header)

            headerCells = self._generatePart(header)
            if (body is not None) and (self._validateHeader(headerCells)):
                lengthHeader = len(headerCells[0])
                fakeTable = self._generatePart(body)
                if footer is not None:
                    fakeTable = fakeTable + self._generatePart(footer)
                for cells in fakeTable:
                    if len(cells) == lengthHeader:
                        i = 0
                        for cell in cells:
                            headersIds = self._returnListIdsColumns(
                                headerCells,
                                i
                            )
                            headers = cell.getAttribute('headers')
                            for headersId in headersIds:
                                headers = CommonFunctions.increaseInList(
                                    headers,
                                    headersId
                                )
                            cell.setAttribute('headers', headers)
                            i += 1
        if body is not None:
            self._fixBodyOrFooter(body)
        if footer is not None:
            self._fixBodyOrFooter(footer)

    def fixAssociationCellsTables(self):
        tables = self.parser.find('table').listResults()
        for table in tables:
            if not table.hasAttribute(self.dataIgnore):
                self.fixAssociationCellsTable(table)
