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

from hatemile.util.commonfunctions import CommonFunctions
from hatemile.accessibleevent import AccessibleEvent
import os

class AccessibleEventImplementation(AccessibleEvent):
    """
    The AccessibleEventImplementation class is official implementation of
    AccessibleEvent interface.
    """

    eventListenerScriptContent = None

    includeScriptContent = None

    def __init__(self, parser, configure, storeScriptsContent):
        """
        Initializes a new object that manipulate the accessibility of the
        Javascript events of elements of parser.
        @param parser: The HTML parser.
        @type parser: L{hatemile.util.HTMLDOMParser}
        @param configure: The configuration of HaTeMiLe.
        @type configure: L{hatemile.util.Configure}
        @param storeScriptsContent: The state that indicates if the scripts
        used are stored or deleted, after use.
        @type storeScriptsContent: bool
        """

        self.parser = parser
        self.storeScriptsContent = storeScriptsContent
        self.prefixId = configure.getParameter('prefix-generated-ids')
        self.idScriptEventListener = 'script-eventlistener'
        self.idListIdsScript = 'list-ids-script'
        self.idFunctionScriptFix = 'id-function-script-fix'
        self.dataIgnore = 'data-ignoreaccessibilityfix'
        self.mainScriptAdded = False
        self.scriptList = None

    def _keyboardAccess(self, element):
        """
        Provide keyboard access for element, if it not has.
        @param element: The element.
        @type element: L{hatemile.util.HTMLDOMElement}
        """

        if not element.hasAttribute('tabindex'):
            tag = element.getTagName()
            if (tag == 'A') and (not element.hasAttribute('href')):
                element.setAttribute('tabindex', '0')
            elif (tag != 'A') and (tag != 'INPUT') and (tag != 'BUTTON') and (tag != 'SELECT') and (tag != 'TEXTAREA'):
                element.setAttribute('tabindex', '0')

    def _generateMainScripts(self):
        """
        Include the scripts used by solutions.
        """

        head = self.parser.find('head').firstResult()
        if (head != None) and (self.parser.find('#' + self.idScriptEventListener).firstResult() == None):
            eventListenerFile = open(os.path.dirname(os.path.realpath(__file__)) + '/../../js/eventlistener.js', 'r') 
            if self.storeScriptsContent:
                if AccessibleEventImplementation.eventListenerScriptContent == None:
                    AccessibleEventImplementation.eventListenerScriptContent = eventListenerFile.read()
                localEventListenerScriptContent = AccessibleEventImplementation.eventListenerScriptContent
            else:
                localEventListenerScriptContent = eventListenerFile.read()
            eventListenerFile.close()

            script = self.parser.createElement('script')
            script.setAttribute('id', self.idScriptEventListener)
            script.setAttribute('type', 'text/javascript')
            script.appendText(localEventListenerScriptContent)
            if head.hasChildren():
                head.getFirstElementChild().insertBefore(script)
            else:
                head.appendElement(script)
        local = self.parser.find('body').firstResult()
        if local != None:
            self.scriptList = self.parser.find('#' + self.idListIdsScript).firstResult()
            if self.scriptList == None:
                self.scriptList = self.parser.createElement('script')
                self.scriptList.setAttribute('id', self.idListIdsScript)
                self.scriptList.setAttribute('type', 'text/javascript')
                self.scriptList.appendText('var activeElements = [];')
                self.scriptList.appendText('var hoverElements = [];')
                self.scriptList.appendText('var dragElements = [];')
                self.scriptList.appendText('var dropElements = [];')
                local.appendElement(self.scriptList)
            if self.parser.find('#' + self.idFunctionScriptFix).firstResult() == None:
                includeFile = open(os.path.dirname(os.path.realpath(__file__)) + '/../../js/include.js', 'r')
                if self.storeScriptsContent:
                    if AccessibleEventImplementation.includeScriptContent == None:
                        AccessibleEventImplementation.includeScriptContent = includeFile.read()
                    localIncludeScriptContent = AccessibleEventImplementation.includeScriptContent
                else:
                    localIncludeScriptContent = includeFile.read()
                includeFile.close()

                scriptFunction = self.parser.createElement('script')
                scriptFunction.setAttribute('id', self.idFunctionScriptFix)
                scriptFunction.setAttribute('type', 'text/javascript')
                scriptFunction.appendText(localIncludeScriptContent)
                local.appendElement(scriptFunction)
        self.mainScriptAdded = True

    def _addEventInElement(self, element, event):
        """
        Add a type of event in element.
        @param element: The element.
        @type element: L{hatemile.util.HTMLDOMElement}
        @param event: The type of event.
        @type event: str
        """

        if not self.mainScriptAdded:
            self._generateMainScripts()

        if self.scriptList != None:
            CommonFunctions.generateId(element, self.prefixId)
            self.scriptList.appendText(event + "Elements.push('" + element.getAttribute('id') + "');")

    def fixDrop(self, element):
        element.setAttribute('aria-dropeffect', 'none')

        self._addEventInElement(element, 'drop')

    def fixDrag(self, element):
        self._keyboardAccess(element)

        element.setAttribute('aria-grabbed', 'false')

        self._addEventInElement(element, 'drag')

    def fixDragsandDrops(self):
        draggableElements = self.parser.find('[ondrag],[ondragstart],[ondragend]').listResults()
        for draggableElement in draggableElements:
            if not draggableElement.hasAttribute(self.dataIgnore):
                self.fixDrag(draggableElement)
        droppableElements = self.parser.find('[ondrop],[ondragenter],[ondragleave],[ondragover]').listResults()
        for droppableElement in droppableElements:
            if not droppableElement.hasAttribute(self.dataIgnore):
                self.fixDrop(droppableElement)

    def fixHover(self, element):
        self._keyboardAccess(element)

        self._addEventInElement(element, 'hover')

    def fixHovers(self):
        elements = self.parser.find('[onmouseover],[onmouseout]').listResults()
        for element in elements:
            if not element.hasAttribute(self.dataIgnore):
                self.fixHover(element)

    def fixActive(self, element):
        self._keyboardAccess(element)

        self._addEventInElement(element, 'active')

    def fixActives(self):
        elements = self.parser.find('[onclick],[onmousedown],[onmouseup],[ondblclick]').listResults()
        for element in elements:
            if not element.hasAttribute(self.dataIgnore):
                self.fixActive(element)
