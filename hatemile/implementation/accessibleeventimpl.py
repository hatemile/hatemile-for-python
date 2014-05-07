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
from hatemile import AccessibleEvent

class AccessibleEventImpl(AccessibleEvent):
	def __init__(self, parser, configure):
		self.parser = parser
		self.prefixId = configure.getParameter('prefix-generated-ids')
		self.idScriptEvent = configure.getParameter('id-script-event')
		self.idListIdsScriptOnClick = configure.getParameter('id-list-ids-script-onclick')
		self.idFunctionScriptFixOnClick = configure.getParameter('id-function-script-fix-onclick')
		self.dataFocused = configure.getParameter('data-focused')
		self.dataPressed = configure.getParameter('data-pressed')
		self.dataIgnore = configure.getParameter('data-ignore')
		self.mainScriptAdded = False
		self.otherScriptsAdded = False
		self.scriptList = None
	def generateMainScript(self):
		if self.parser.find('#' + self.idScriptEvent).firstResult() == None:
			script = self.parser.createElement('script')
			script.setAttribute('id', self.idScriptEvent)
			script.setAttribute('type', 'text/javascript')
			javascript = """\nfunction onFocusEvent(element) {
				element.setAttribute('""" + self.dataFocused + """', 'true');
				if (element.onmouseover != undefined) {
					element.onmouseover();
				}
			}
			function onBlurEvent(element) {
				if (element.hasAttribute('""" + self.dataFocused + """')) {
					if ((element.getAttribute('""" + self.dataFocused + """').toLowerCase() == 'true') && (element.onmouseout != undefined)) {
						element.onmouseout();
					}
					element.setAttribute('""" + self.dataFocused + """', 'false');
				}
			}
			function onKeyPressEvent(element, event) {
				element.setAttribute('""" + self.dataPressed + """', event.keyCode);
			}
			function onKeyPressUp(element, event) {
				var key = event.keyCode;
				var enter1 = \"\\n\".charCodeAt(0);
				var enter2 = \"\\r\".charCodeAt(0);
				if ((key == enter1) || (key == enter2)) {
					if (element.hasAttribute('""" + self.dataPressed + """')) {
						if (key == parseInt(element.getAttribute('""" + self.dataPressed + """'))) {
							if (element.onclick != undefined) {
								element.click();
							}
							element.removeAttribute('""" + self.dataPressed + """');
						}
					}
				}
			}"""
			script.appendText(javascript)
			local = self.parser.find('head').firstResult()
			if local == None:
				local = self.parser.find('body').firstResult()
			local.appendElement(script)
	def generateOtherScripts(self):
		self.scriptList = self.parser.find('#' + self.idListIdsScriptOnClick).firstResult()
		if self.scriptList == None:
			self.scriptList = self.parser.createElement('script')
			self.scriptList.setAttribute('id', self.idListIdsScriptOnClick)
			self.scriptList.setAttribute('type', 'text/javascript')
			self.scriptList.appendText("\nidsElementsWithOnClick = [];\n")
			self.parser.find('body').firstResult().appendElement(self.scriptList)
		if self.parser.find('#' + self.idFunctionScriptFixOnClick).firstResult() == None:
			scriptFunction = self.parser.createElement('script')
			scriptFunction.setAttribute('id', self.idFunctionScriptFixOnClick)
			scriptFunction.setAttribute('type', 'text/javascript')
			javascript = """\nfor (var i = 0, length = idsElementsWithOnClick.length; i < length; i++) {
				var element = document.getElementById(idsElementsWithOnClick[i]);
				element.onkeypress = function(event) {
					onKeyPressEvent(element, event);
				};
				element.onkeyup = function(event) {
					onKeyPressUp(element, event);
				};
			}""";
			scriptFunction.appendText(javascript)
			self.parser.find('body').firstResult().appendElement(scriptFunction)
		self.otherScriptsAdded = True
	def addElementIdWithOnClick(self, idElement):
		self.scriptList.appendText("idsElementsWithOnClick.push('" + idElement + "');\n")
	def fixOnHover(self, element):
		if not self.mainScriptAdded:
			self.generateMainScript()
		tag = element.getTagName()
		if not (tag == 'INPUT' or tag == 'BUTTON' or tag == 'A' or tag == 'SELECT' or tag == 'TEXTAREA' or element.hasAttribute('tabindex')):
			element.setAttribute('tabindex', '0')
		if not element.hasAttribute('onfocus'):
			element.setAttribute('onfocus', 'onFocusEvent(this);')
		if not element.hasAttribute('onblur'):
			element.setAttribute('onblur', 'onBlurEvent(this);')
	def fixOnHovers(self):
		elements = self.parser.find('[onmouseover],[onmouseout]').listResults()
		for element in elements:
			if not element.hasAttribute(self.dataIgnore):
				self.fixOnHover(element)
	def fixOnClick(self, element):
		tag = element.getTagName()
		if not (tag == 'INPUT' or tag == 'BUTTON' or tag == 'A'):
			if not self.mainScriptAdded:
				self.generateMainScript()
			if not self.otherScriptsAdded:
				self.generateOtherScripts()
			if not (element.hasAttribute('tabindex') or tag == 'SELECT' or tag == 'TEXTAREA'):
				element.setAttribute('tabindex', '0')
			CommonFunctions.generateId(element, self.prefixId)
			if (not element.hasAttribute('onkeypress')) and (not element.hasAttribute('onkeyup')) and (not element.hasAttribute('onkeydown')):
				self.addElementIdWithOnClick(element.getAttribute('id'))
	def fixOnClicks(self):
		elements = self.parser.find('[onclick]').listResults()
		for element in elements:
			if not element.hasAttribute(self.dataIgnore):
				self.fixOnClick(element)