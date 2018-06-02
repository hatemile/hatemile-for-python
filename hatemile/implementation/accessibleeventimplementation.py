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

import os
from hatemile.accessibleevent import AccessibleEvent
from hatemile.util.commonfunctions import CommonFunctions


class AccessibleEventImplementation(AccessibleEvent):
    """
    The AccessibleEventImplementation class is official implementation of
    AccessibleEvent interface.
    """

    event_listener_script_content = None

    include_script_content = None

    def __init__(self, parser, configure, store_scripts_content):
        """
        Initializes a new object that manipulate the accessibility of the
        Javascript events of elements of parser.
        @param parser: The HTML parser.
        @type parser: L{hatemile.util.HTMLDOMParser}
        @param configure: The configuration of HaTeMiLe.
        @type configure: L{hatemile.util.Configure}
        @param store_scripts_content: The state that indicates if the scripts
        used are stored or deleted, after use.
        @type store_scripts_content: bool
        """

        self.parser = parser
        self.store_scripts_content = store_scripts_content
        self.prefix_id = configure.get_parameter('prefix-generated-ids')
        self.id_script_event_listener = 'script-eventlistener'
        self.id_list_ids_script = 'list-ids-script'
        self.id_function_script_fix = 'id-function-script-fix'
        self.data_ignore = 'data-ignoreaccessibilityfix'
        self.main_script_added = False
        self.script_list = None

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
                '#' + self.id_script_event_listener
            ).first_result() is None)
        ):
            event_listener_file = open(os.path.dirname(os.path.dirname(
                os.path.dirname(os.path.realpath(__file__))
            )) + '/js/eventlistener.js', 'r')
            if self.store_scripts_content:
                if (
                    AccessibleEventImplementation
                    .event_listener_script_content
                ) is None:
                    AccessibleEventImplementation\
                        .event_listener_script_content = (
                            event_listener_file.read()
                        )
                local_event_listener_script_content = (
                    AccessibleEventImplementation
                    .event_listener_script_content
                )
            else:
                local_event_listener_script_content = (
                    event_listener_file.read()
                )
            event_listener_file.close()

            script = self.parser.create_element('script')
            script.set_attribute('id', self.id_script_event_listener)
            script.set_attribute('type', 'text/javascript')
            script.append_text(local_event_listener_script_content)
            if head.has_children():
                head.get_first_element_child().insert_before(script)
            else:
                head.append_element(script)
        local = self.parser.find('body').first_result()
        if local is not None:
            self.script_list = self.parser.find(
                '#' + self.id_list_ids_script
            ).first_result()
            if self.script_list is None:
                self.script_list = self.parser.create_element('script')
                self.script_list.set_attribute('id', self.id_list_ids_script)
                self.script_list.set_attribute('type', 'text/javascript')
                self.script_list.append_text('var activeElements = [];')
                self.script_list.append_text('var hoverElements = [];')
                self.script_list.append_text('var dragElements = [];')
                self.script_list.append_text('var dropElements = [];')
                local.append_element(self.script_list)
            if self.parser.find(
                    '#' + self.id_function_script_fix
            ).first_result() is None:
                include_file = open(os.path.dirname(os.path.dirname(
                    os.path.dirname(os.path.realpath(__file__))
                )) + '/js/include.js', 'r')
                if self.store_scripts_content:
                    if AccessibleEventImplementation.include_script_content \
                            is None:
                        AccessibleEventImplementation \
                            .include_script_content = include_file.read()
                    local_include_script_content = (
                        AccessibleEventImplementation
                        .include_script_content
                    )
                else:
                    local_include_script_content = include_file.read()
                include_file.close()

                script_function = self.parser.create_element('script')
                script_function.set_attribute(
                    'id',
                    self.id_function_script_fix
                )
                script_function.set_attribute('type', 'text/javascript')
                script_function.append_text(local_include_script_content)
                local.append_element(script_function)
        self.main_script_added = True

    def _add_event_in_element(self, element, event):
        """
        Add a type of event in element.
        @param element: The element.
        @type element: L{hatemile.util.HTMLDOMElement}
        @param event: The type of event.
        @type event: str
        """

        if not self.main_script_added:
            self._generate_main_scripts()

        if self.script_list is not None:
            CommonFunctions.generate_id(element, self.prefix_id)
            self.script_list.append_text(
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
        draggable_elements = self.parser.find(
            '[ondrag],[ondragstart],[ondragend]'
        ).list_results()
        for draggable_element in draggable_elements:
            if not draggable_element.has_attribute(self.data_ignore):
                self.fix_drag(draggable_element)

        droppable_elements = self.parser.find(
            '[ondrop],[ondragenter],[ondragleave],[ondragover]'
        ).list_results()
        for droppable_element in droppable_elements:
            if not droppable_element.has_attribute(self.data_ignore):
                self.fix_drop(droppable_element)

    def fix_hover(self, element):
        self._keyboard_access(element)

        self._add_event_in_element(element, 'hover')

    def fix_hovers(self):
        elements = self.parser.find(
            '[onmouseover],[onmouseout]'
        ).list_results()
        for element in elements:
            if not element.has_attribute(self.data_ignore):
                self.fix_hover(element)

    def fix_active(self, element):
        self._keyboard_access(element)

        self._add_event_in_element(element, 'active')

    def fix_actives(self):
        elements = self.parser.find(
            '[onclick],[onmousedown],[onmouseup],[ondblclick]'
        ).list_results()
        for element in elements:
            if not element.has_attribute(self.data_ignore):
                self.fix_active(element)
