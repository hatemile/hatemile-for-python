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
Module of AccessibleEventImplementation class.
"""

import os
from hatemile import helper
from hatemile.accessibleevent import AccessibleEvent
from hatemile.util.commonfunctions import CommonFunctions
from hatemile.util.idgenerator import IDGenerator
from hatemile.util.html.htmldomparser import HTMLDOMParser


class AccessibleEventImplementation(AccessibleEvent):
    """
    The AccessibleEventImplementation class is official implementation of
    :py:class:`hatemile.accessibleevent.AccessibleEvent`.
    """

    #: The id of script element that replace the event listener methods.
    ID_SCRIPT_EVENT_LISTENER = 'script-eventlistener'

    #: The id of script element that contains the list of elements that has
    #: inaccessible events.
    ID_LIST_IDS_SCRIPT = 'list-ids-script'

    #: The id of script element that modify the events of elements.
    ID_FUNCTION_SCRIPT_FIX = 'id-function-script-fix'

    #: The ID of script element that contains the common functions of scripts.
    ID_SCRIPT_COMMON_FUNCTIONS = 'hatemile-common-functions'

    def __init__(self, parser):
        """
        Initializes a new object that manipulate the accessibility of the
        Javascript events of elements of parser.

        :param parser: The HTML parser.
        :type parser: hatemile.util.html.htmldomparser.HTMLDOMParser
        """

        helper.require_not_none(parser)
        helper.require_valid_type(parser, HTMLDOMParser)

        self.parser = parser
        self.id_generator = IDGenerator('event')
        self.main_script_added = False
        self.script_list = None

    def _keyboard_access(self, element):
        """
        Provide keyboard access for element, if it not has.

        :param element: The element.
        :type element: hatemile.util.html.htmldomelement.HTMLDOMElement
        """
        # pylint: disable=no-self-use

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
        if head is not None:
            common_functions_script = self.parser.find(
                '#'
                + AccessibleEventImplementation.ID_SCRIPT_COMMON_FUNCTIONS
            ).first_result()
            if common_functions_script is None:
                common_functions_file = open(
                    os.path.join(
                        os.path.dirname(os.path.dirname(os.path.dirname(
                            os.path.realpath(__file__)
                        ))),
                        'js',
                        'common.js'
                    ),
                    'r'
                )
                common_functions_content = common_functions_file.read()
                common_functions_file.close()

                common_functions_script = self.parser.create_element('script')
                common_functions_script.set_attribute(
                    'id',
                    AccessibleEventImplementation.ID_SCRIPT_COMMON_FUNCTIONS
                )
                common_functions_script.set_attribute(
                    'type',
                    'text/javascript'
                )
                common_functions_script.append_text(common_functions_content)
                head.prepend_element(common_functions_script)
            if (
                self.parser.find(
                    '#'
                    + AccessibleEventImplementation.ID_SCRIPT_EVENT_LISTENER
                ).first_result() is None
            ):
                event_listener_file = open(
                    os.path.join(
                        os.path.dirname(os.path.dirname(os.path.dirname(
                            os.path.realpath(__file__)
                        ))),
                        'js',
                        'eventlistener.js'
                    ),
                    'r'
                )
                event_listener_script_content = event_listener_file.read()
                event_listener_file.close()

                script = self.parser.create_element('script')
                script.set_attribute(
                    'id',
                    AccessibleEventImplementation.ID_SCRIPT_EVENT_LISTENER
                )
                script.set_attribute('type', 'text/javascript')
                script.append_text(event_listener_script_content)
                common_functions_script.insert_after(script)
        local = self.parser.find('body').first_result()
        if local is not None:
            self.script_list = self.parser.find(
                '#'
                + AccessibleEventImplementation.ID_LIST_IDS_SCRIPT
            ).first_result()
            if self.script_list is None:
                self.script_list = self.parser.create_element('script')
                self.script_list.set_attribute(
                    'id',
                    AccessibleEventImplementation.ID_LIST_IDS_SCRIPT
                )
                self.script_list.set_attribute('type', 'text/javascript')
                self.script_list.append_text('var activeElements = [];')
                self.script_list.append_text('var hoverElements = [];')
                self.script_list.append_text('var dragElements = [];')
                self.script_list.append_text('var dropElements = [];')
                local.append_element(self.script_list)
            if self.parser.find(
                    '#'
                    + AccessibleEventImplementation.ID_FUNCTION_SCRIPT_FIX
            ).first_result() is None:
                include_file = open(
                    os.path.join(
                        os.path.dirname(os.path.dirname(os.path.dirname(
                            os.path.realpath(__file__)
                        ))),
                        'js',
                        'include.js'
                    ),
                    'r'
                )
                local_include_script_content = include_file.read()
                include_file.close()

                script_function = self.parser.create_element('script')
                script_function.set_attribute(
                    'id',
                    AccessibleEventImplementation.ID_FUNCTION_SCRIPT_FIX
                )
                script_function.set_attribute('type', 'text/javascript')
                script_function.append_text(local_include_script_content)
                local.append_element(script_function)
        self.main_script_added = True

    def _add_event_in_element(self, element, event):
        """
        Add a type of event in element.

        :param element: The element.
        :type element: hatemile.util.html.htmldomelement.HTMLDOMElement
        :param event: The type of event.
        :type event: str
        """

        if not self.main_script_added:
            self._generate_main_scripts()

        if self.script_list is not None:
            self.id_generator.generate_id(element)
            self.script_list.append_text(
                event
                + "Elements.push('"
                + element.get_attribute('id')
                + "');"
            )

    def make_accessible_drop_events(self, element):
        element.set_attribute('aria-dropeffect', 'none')

        self._add_event_in_element(element, 'drop')

    def make_accessible_drag_events(self, element):
        self._keyboard_access(element)

        element.set_attribute('aria-grabbed', 'false')

        self._add_event_in_element(element, 'drag')

    def make_accessible_all_drag_and_drop_events(self):
        draggable_elements = self.parser.find(
            '[ondrag],[ondragstart],[ondragend]'
        ).list_results()
        for draggable_element in draggable_elements:
            if CommonFunctions.is_valid_element(draggable_element):
                self.make_accessible_drag_events(draggable_element)

        droppable_elements = self.parser.find(
            '[ondrop],[ondragenter],[ondragleave],[ondragover]'
        ).list_results()
        for droppable_element in droppable_elements:
            if CommonFunctions.is_valid_element(droppable_element):
                self.make_accessible_drop_events(droppable_element)

    def make_accessible_hover_events(self, element):
        self._keyboard_access(element)

        self._add_event_in_element(element, 'hover')

    def make_accessible_all_hover_events(self):
        elements = self.parser.find(
            '[onmouseover],[onmouseout]'
        ).list_results()
        for element in elements:
            if CommonFunctions.is_valid_element(element):
                self.make_accessible_hover_events(element)

    def make_accessible_click_events(self, element):
        self._keyboard_access(element)

        self._add_event_in_element(element, 'active')

    def make_accessible_all_click_events(self):
        elements = self.parser.find(
            '[onclick],[onmousedown],[onmouseup],[ondblclick]'
        ).list_results()
        for element in elements:
            if CommonFunctions.is_valid_element(element):
                self.make_accessible_click_events(element)
