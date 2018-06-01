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
        self.prefixId = configure.get_parameter('prefix-generated-ids')
        self.idScriptEventListener = 'script-eventlistener'
        self.idListIdsScript = 'list-ids-script'
        self.idFunctionScriptFix = 'id-function-script-fix'
        self.dataIgnore = 'data-ignoreaccessibilityfix'
        self.mainScriptAdded = False
        self.scriptList = None

    def _keyboard_access(self, element):
        """
        Provide keyboard access for element, if it not has.
        @param element: The element.
        @type element: L{hatemile.util.HTMLDOMElement}
        """

        if not element.has_attribute('tabindex'):
            tag = element.get_tag_name()
            if (tag == 'A') and (not element.has_attribute('href')):
                element.set_attribute('tabindex', '0')
            elif (
                (tag != 'A')
                and (tag != 'INPUT')
                and (tag != 'BUTTON')
                and (tag != 'SELECT')
                and (tag != 'TEXTAREA')
            ):
                element.set_attribute('tabindex', '0')

    def _generate_main_scripts(self):
        """
        Include the scripts used by solutions.
        """

        head = self.parser.find('head').first_result()
        if (
            (head is not None)
            and (self.parser.find(
                '#' + self.idScriptEventListener
            ).first_result() is None)
        ):
            eventListenerFile = open(os.path.dirname(os.path.dirname(
                os.path.dirname(os.path.realpath(__file__))
            )) + '/js/eventlistener.js', 'r')
            if self.storeScriptsContent:
                if AccessibleEventImplementation.eventListenerScriptContent \
                        is None:
                    AccessibleEventImplementation.eventListenerScriptContent \
                            = eventListenerFile.read()
                localEventListenerScriptContent = (
                    AccessibleEventImplementation
                    .eventListenerScriptContent
                )
            else:
                localEventListenerScriptContent = eventListenerFile.read()
            eventListenerFile.close()

            script = self.parser.create_element('script')
            script.set_attribute('id', self.idScriptEventListener)
            script.set_attribute('type', 'text/javascript')
            script.append_text(localEventListenerScriptContent)
            if head.has_children():
                head.get_first_element_child().insert_before(script)
            else:
                head.append_element(script)
        local = self.parser.find('body').first_result()
        if local is not None:
            self.scriptList = self.parser.find(
                '#' + self.idListIdsScript
            ).first_result()
            if self.scriptList is None:
                self.scriptList = self.parser.create_element('script')
                self.scriptList.set_attribute('id', self.idListIdsScript)
                self.scriptList.set_attribute('type', 'text/javascript')
                self.scriptList.append_text('var activeElements = [];')
                self.scriptList.append_text('var hoverElements = [];')
                self.scriptList.append_text('var dragElements = [];')
                self.scriptList.append_text('var dropElements = [];')
                local.append_element(self.scriptList)
            if self.parser.find(
                    '#' + self.idFunctionScriptFix
            ).first_result() is None:
                includeFile = open(os.path.dirname(os.path.dirname(
                    os.path.dirname(os.path.realpath(__file__))
                )) + '/js/include.js', 'r')
                if self.storeScriptsContent:
                    if AccessibleEventImplementation.includeScriptContent \
                            is None:
                        AccessibleEventImplementation.includeScriptContent = (
                            includeFile.read()
                        )
                    localIncludeScriptContent = (
                        AccessibleEventImplementation
                        .includeScriptContent
                    )
                else:
                    localIncludeScriptContent = includeFile.read()
                includeFile.close()

                scriptFunction = self.parser.create_element('script')
                scriptFunction.set_attribute('id', self.idFunctionScriptFix)
                scriptFunction.set_attribute('type', 'text/javascript')
                scriptFunction.append_text(localIncludeScriptContent)
                local.append_element(scriptFunction)
        self.mainScriptAdded = True

    def _add_event_in_element(self, element, event):
        """
        Add a type of event in element.
        @param element: The element.
        @type element: L{hatemile.util.HTMLDOMElement}
        @param event: The type of event.
        @type event: str
        """

        if not self.mainScriptAdded:
            self._generate_main_scripts()

        if self.scriptList is not None:
            CommonFunctions.generate_id(element, self.prefixId)
            self.scriptList.append_text(
                event
                + "Elements.push('"
                + element.get_attribute('id')
                + "');"
            )

    def fix_drop(self, element):
        element.set_attribute('aria-dropeffect', 'none')

        self._add_event_in_element(element, 'drop')

    def fix_drag(self, element):
        self._keyboard_access(element)

        element.set_attribute('aria-grabbed', 'false')

        self._add_event_in_element(element, 'drag')

    def fix_drags_and_drops(self):
        draggableElements = self.parser.find(
            '[ondrag],[ondragstart],[ondragend]'
        ).list_results()
        for draggableElement in draggableElements:
            if not draggableElement.has_attribute(self.dataIgnore):
                self.fix_drag(draggableElement)

        droppableElements = self.parser.find(
            '[ondrop],[ondragenter],[ondragleave],[ondragover]'
        ).list_results()
        for droppableElement in droppableElements:
            if not droppableElement.has_attribute(self.dataIgnore):
                self.fix_drop(droppableElement)

    def fix_hover(self, element):
        self._keyboard_access(element)

        self._add_event_in_element(element, 'hover')

    def fix_hovers(self):
        elements = self.parser.find(
            '[onmouseover],[onmouseout]'
        ).list_results()
        for element in elements:
            if not element.has_attribute(self.dataIgnore):
                self.fix_hover(element)

    def fix_active(self, element):
        self._keyboard_access(element)

        self._add_event_in_element(element, 'active')

    def fix_actives(self):
        elements = self.parser.find(
            '[onclick],[onmousedown],[onmouseup],[ondblclick]'
        ).list_results()
        for element in elements:
            if not element.has_attribute(self.dataIgnore):
                self.fix_active(element)
