#Copyright 2014 Carlson Santana Cruz
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

from hatemile.util import CommonFunctions
from hatemile import AccessibleTable

class AccessibleTableImpl(AccessibleTable):
	def __init__(self, parser, configure):
		self.parser = parser
		self.prefixId = configure.getParameter('prefix-generated-ids')
		self.dataIgnore = configure.getParameter('data-ignore')
	def generatePart(self, part):
		rows = self.parser.find(part).findChildren('tr').listResults()
		table = []
		for row in rows:
			table.append(self.generateColspan(self.parser.find(row).findChildren('td,th').listResults()))
		return self.generateRowspan(table)
	def generateRowspan(self, rows):
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
						elif row[m] == None:
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
	def generateColspan(self, row):
		copy = []  + row
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
	def validateHeader(self, header):
		if not bool(header):
			return False
		length = -1
		for elements in header:
			if not bool(elements):
				return False
			elif length == -1:
				length = len(elements)
			elif len(elements) != length:
				return False
		return True
	def returnListIdsColumns(self, header, index):
		ids = []
		for row in header:
			if row[index].getTagName() == 'TH':
				ids.append(row[index].getAttribute('id'))
		return ids
	def fixBodyOrFooter(self, element):
		table = self.generatePart(element)
		for cells in table:
			headersIds = []
			for cell in cells:
				if cell.getTagName() == 'TH':
					CommonFunctions.generateId(cell, self.prefixId)
					cell.setAttribute('scope', 'row')
					headersIds.append(cell.getAttribute('id'))
			if bool(headersIds):
				for cell in cells:
					if cell.getTagName() == 'TD':
						headers = None
						if cell.hasAttribute('headers'):
							headers = cell.getAttribute('headers')
						for headerId in headersIds:
							headers = CommonFunctions.increaseInList(headers, headerId)
						cell.setAttribute('headers', headers)
	def fixHeader(self, element):
		if element.getTagName() == 'THEAD':
			cells = self.parser.find(element).findChildren('tr').findChildren('th').listResults()
			for cell in cells:
				CommonFunctions.generateId(cell, self.prefixId)
				cell.setAttribute('scope', 'col')
	def fixFooter(self, element):
		if element.getTagName() == 'TFOOT':
			self.fixBodyOrFooter(element)
	def fixBody(self, element):
		if element.getTagName() == 'TBODY':
			self.fixBodyOrFooter(element)
	def fixTable(self, element):
		header = self.parser.find(element).findChildren('thead').firstResult()
		body = self.parser.find(element).findChildren('tbody').firstResult()
		footer = self.parser.find(element).findChildren('tfoot').firstResult()
		if header != None:
			self.fixHeader(header)
			headerCells = self.generatePart(header)
			if (self.validateHeader(headerCells)) and (body != None):
				lengthHeader = len(headerCells[0])
				table = self.generatePart(body)
				if footer != None:
					table = table + self.generatePart(footer)
				for cells in table:
					i = 0
					if len(cells) == lengthHeader:
						for cell in cells:
							ids = self.returnListIdsColumns(headerCells, i)
							headers = None
							if cell.hasAttribute('headers'):
								headers = cell.getAttribute('headers')
							for idElement in ids:
								headers = CommonFunctions.increaseInList(headers, idElement)
							cell.setAttribute('headers', headers)
							i += 1
		if body != None:
			self.fixBody(body)
		if footer != None:
			self.fixFooter(footer)
	def fixTables(self):
		elements = self.parser.find('table').listResults()
		for element in elements:
			if not element.hasAttribute(self.dataIgnore):
				self.fixTable(element)