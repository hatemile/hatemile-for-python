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
Module of AccessibleDisplayImplementation class.
"""

import re
from hatemile import helper
from hatemile.accessibledisplay import AccessibleDisplay
from hatemile.util.commonfunctions import CommonFunctions
from hatemile.util.configure import Configure
from hatemile.util.idgenerator import IDGenerator
from hatemile.util.html.htmldomparser import HTMLDOMParser


class AccessibleDisplayImplementation(AccessibleDisplay):
    """
    The AccessibleDisplayImplementation class is official implementation of
    :py:class:`hatemile.accessibledisplay.AccessibleDisplay` for screen
    readers.
    """

    #: The id of list element that contains the description of shortcuts,
    #: before the whole content of page.
    ID_CONTAINER_SHORTCUTS_BEFORE = 'container-shortcuts-before'

    #: The id of list element that contains the description of shortcuts, after
    #: the whole content of page.
    ID_CONTAINER_SHORTCUTS_AFTER = 'container-shortcuts-after'

    #: The HTML class of text of description of container of shortcuts
    #: descriptions.
    CLASS_TEXT_SHORTCUTS = 'text-shortcuts'

    #: The HTML class of content to force the screen reader show the current
    #: state of element, before it.
    CLASS_FORCE_READ_BEFORE = 'force-read-before'

    #: The HTML class of content to force the screen reader show the current
    #: state of element, after it.
    CLASS_FORCE_READ_AFTER = 'force-read-after'

    #: The name of attribute that links the description of shortcut of element.
    DATA_ATTRIBUTE_ACCESSKEY_OF = 'data-attributeaccesskeyof'

    #: The name of attribute that links the content of download link.
    DATA_ATTRIBUTE_DOWNLOAD_OF = 'data-attributedownloadof'

    #: The name of attribute that links the content of header cell with the
    #: data cell.
    DATA_ATTRIBUTE_HEADERS_OF = 'data-headersof'

    #: The name of attribute that links the description of language with the
    #: element.
    DATA_ATTRIBUTE_LANGUAGE_OF = 'data-languageof'

    #: The name of attribute that links the content of link that open a new
    #: instance.
    DATA_ATTRIBUTE_TARGET_OF = 'data-attributetargetof'

    #: The name of attribute that links the content of title of element.
    DATA_ATTRIBUTE_TITLE_OF = 'data-attributetitleof'

    #: The name of attribute that links the content of autocomplete state of
    #: field.
    DATA_ARIA_AUTOCOMPLETE_OF = 'data-ariaautocompleteof'

    #: The name of attribute that links the content of busy state of element.
    DATA_ARIA_BUSY_OF = 'data-ariabusyof'

    #: The name of attribute that links the content of checked state field.
    DATA_ARIA_CHECKED_OF = 'data-ariacheckedof'

    #: The name of attribute that links the content of drop effect state of
    #: element.
    DATA_ARIA_DROPEFFECT_OF = 'data-ariadropeffectof'

    #: The name of attribute that links the content of expanded state of
    #: element.
    DATA_ARIA_EXPANDED_OF = 'data-ariaexpandedof'

    #: The name of attribute that links the content of grabbed state of
    #: element.
    DATA_ARIA_GRABBED_OF = 'data-ariagrabbedof'

    #: The name of attribute that links the content that show if the field has
    #: popup.
    DATA_ARIA_HASPOPUP_OF = 'data-ariahaspopupof'

    #: The name of attribute that links the content of level state of element.
    DATA_ARIA_LEVEL_OF = 'data-arialevelof'

    #: The name of attribute that links the content of orientation state of
    #: element.
    DATA_ARIA_ORIENTATION_OF = 'data-ariaorientationof'

    #: The name of attribute that links the content of pressed state of field.
    DATA_ARIA_PRESSED_OF = 'data-ariapressedof'

    #: The name of attribute that links the content of minimum range state of
    #: field.
    DATA_ARIA_RANGE_MIN_OF = 'data-attributevalueminof'

    #: The name of attribute that links the content of maximum range state of
    #: field.
    DATA_ARIA_RANGE_MAX_OF = 'data-attributevaluemaxof'

    #: The name of attribute that links the content of required state of field.
    DATA_ARIA_REQUIRED_OF = 'data-attributerequiredof'

    #: The name of attribute that links the content of selected state of field.
    DATA_ARIA_SELECTED_OF = 'data-ariaselectedof'

    #: The name of attribute that links the content of sort state of element.
    DATA_ARIA_SORT_OF = 'data-ariasortof'

    #: The name of attribute that links the content of role of element with the
    #: element.
    DATA_ROLE_OF = 'data-roleof'

    def __init__(self, parser, configure, user_agent=None):
        """
        Initializes a new object that manipulate the display for screen readers
        of parser.

        :param parser: The HTML parser.
        :type parser: hatemile.util.html.htmldomparser.HTMLDOMParser
        :param configure: The configuration of HaTeMiLe.
        :type configure: hatemile.util.configure.Configure
        :param user_agent: The user agent of the user.
        :type user_agent: str
        """

        helper.require_not_none(parser, configure)
        helper.require_valid_type(parser, HTMLDOMParser)
        helper.require_valid_type(configure, Configure)
        helper.require_valid_type(user_agent, str)

        self.parser = parser
        self.configure = configure
        self.id_generator = IDGenerator('display')
        self.shortcut_prefix = self._get_shortcut_prefix(
            user_agent,
            configure.get_parameter('attribute-accesskey-default')
        )
        self.attribute_accesskey_before = configure.get_parameter(
            'attribute-accesskey-before'
        )
        self.attribute_accesskey_after = configure.get_parameter(
            'attribute-accesskey-after'
        )
        self.attribute_accesskey_prefix_before = configure.get_parameter(
            'attribute-accesskey-prefix-before'
        )
        self.attribute_accesskey_suffix_before = configure.get_parameter(
            'attribute-accesskey-suffix-before'
        )
        self.attribute_accesskey_prefix_after = configure.get_parameter(
            'attribute-accesskey-prefix-after'
        )
        self.attribute_accesskey_suffix_after = configure.get_parameter(
            'attribute-accesskey-suffix-after'
        )
        self.attribute_download_before = configure.get_parameter(
            'attribute-download-before'
        )
        self.attribute_download_after = configure.get_parameter(
            'attribute-download-after'
        )
        self.attribute_headers_prefix_before = configure.get_parameter(
            'attribute-headers-prefix-before'
        )
        self.attribute_headers_suffix_before = configure.get_parameter(
            'attribute-headers-suffix-before'
        )
        self.attribute_headers_prefix_after = configure.get_parameter(
            'attribute-headers-prefix-after'
        )
        self.attribute_headers_suffix_after = configure.get_parameter(
            'attribute-headers-suffix-after'
        )
        self.attribute_language_prefix_before = configure.get_parameter(
            'attribute-language-prefix-before'
        )
        self.attribute_language_suffix_before = configure.get_parameter(
            'attribute-language-suffix-before'
        )
        self.attribute_language_prefix_after = configure.get_parameter(
            'attribute-language-prefix-after'
        )
        self.attribute_language_suffix_after = configure.get_parameter(
            'attribute-language-suffix-after'
        )
        self.attribute_role_prefix_before = configure.get_parameter(
            'attribute-role-prefix-before'
        )
        self.attribute_role_suffix_before = configure.get_parameter(
            'attribute-role-suffix-before'
        )
        self.attribute_role_prefix_after = configure.get_parameter(
            'attribute-role-prefix-after'
        )
        self.attribute_role_suffix_after = configure.get_parameter(
            'attribute-role-suffix-after'
        )
        self.attribute_target_blank_before = configure.get_parameter(
            'attribute-target-blank-before'
        )
        self.attribute_target_blank_after = configure.get_parameter(
            'attribute-target-blank-after'
        )
        self.attribute_title_prefix_before = configure.get_parameter(
            'attribute-title-prefix-before'
        )
        self.attribute_title_suffix_before = configure.get_parameter(
            'attribute-title-suffix-before'
        )
        self.attribute_title_prefix_after = configure.get_parameter(
            'attribute-title-prefix-after'
        )
        self.attribute_title_suffix_after = configure.get_parameter(
            'attribute-title-suffix-after'
        )
        self.aria_autocomplete_both_before = configure.get_parameter(
            'aria-autocomplete-both-before'
        )
        self.aria_autocomplete_both_after = configure.get_parameter(
            'aria-autocomplete-both-after'
        )
        self.aria_autocomplete_inline_before = configure.get_parameter(
            'aria-autocomplete-inline-before'
        )
        self.aria_autocomplete_inline_after = configure.get_parameter(
            'aria-autocomplete-inline-after'
        )
        self.aria_autocomplete_list_before = configure.get_parameter(
            'aria-autocomplete-list-before'
        )
        self.aria_autocomplete_list_after = configure.get_parameter(
            'aria-autocomplete-list-after'
        )
        self.aria_busy_true_before = configure.get_parameter(
            'aria-busy-true-before'
        )
        self.aria_busy_true_after = configure.get_parameter(
            'aria-busy-true-after'
        )
        self.aria_checked_false_before = configure.get_parameter(
            'aria-checked-false-before'
        )
        self.aria_checked_false_after = configure.get_parameter(
            'aria-checked-false-after'
        )
        self.aria_checked_mixed_before = configure.get_parameter(
            'aria-checked-mixed-before'
        )
        self.aria_checked_mixed_after = configure.get_parameter(
            'aria-checked-mixed-after'
        )
        self.aria_checked_true_before = configure.get_parameter(
            'aria-checked-true-before'
        )
        self.aria_checked_true_after = configure.get_parameter(
            'aria-checked-true-after'
        )
        self.aria_dropeffect_copy_before = configure.get_parameter(
            'aria-dropeffect-copy-before'
        )
        self.aria_dropeffect_copy_after = configure.get_parameter(
            'aria-dropeffect-copy-after'
        )
        self.aria_dropeffect_execute_before = configure.get_parameter(
            'aria-dropeffect-execute-before'
        )
        self.aria_dropeffect_execute_after = configure.get_parameter(
            'aria-dropeffect-execute-after'
        )
        self.aria_dropeffect_link_before = configure.get_parameter(
            'aria-dropeffect-link-before'
        )
        self.aria_dropeffect_link_after = configure.get_parameter(
            'aria-dropeffect-link-after'
        )
        self.aria_dropeffect_move_before = configure.get_parameter(
            'aria-dropeffect-move-before'
        )
        self.aria_dropeffect_move_after = configure.get_parameter(
            'aria-dropeffect-move-after'
        )
        self.aria_dropeffect_popup_before = configure.get_parameter(
            'aria-dropeffect-popup-before'
        )
        self.aria_dropeffect_popup_after = configure.get_parameter(
            'aria-dropeffect-popup-after'
        )
        self.aria_expanded_false_before = configure.get_parameter(
            'aria-expanded-false-before'
        )
        self.aria_expanded_false_after = configure.get_parameter(
            'aria-expanded-false-after'
        )
        self.aria_expanded_true_before = configure.get_parameter(
            'aria-expanded-true-before'
        )
        self.aria_expanded_true_after = configure.get_parameter(
            'aria-expanded-true-after'
        )
        self.aria_grabbed_false_before = configure.get_parameter(
            'aria-grabbed-false-before'
        )
        self.aria_grabbed_false_after = configure.get_parameter(
            'aria-grabbed-false-after'
        )
        self.aria_grabbed_true_before = configure.get_parameter(
            'aria-grabbed-true-before'
        )
        self.aria_grabbed_true_after = configure.get_parameter(
            'aria-grabbed-true-after'
        )
        self.aria_haspopup_true_before = configure.get_parameter(
            'aria-haspopup-true-before'
        )
        self.aria_haspopup_true_after = configure.get_parameter(
            'aria-haspopup-true-after'
        )
        self.aria_level_prefix_before = configure.get_parameter(
            'aria-level-prefix-before'
        )
        self.aria_level_suffix_before = configure.get_parameter(
            'aria-level-suffix-before'
        )
        self.aria_level_prefix_after = configure.get_parameter(
            'aria-level-prefix-after'
        )
        self.aria_level_suffix_after = configure.get_parameter(
            'aria-level-suffix-after'
        )
        self.aria_value_maximum_prefix_before = configure.get_parameter(
            'aria-value-maximum-prefix-before'
        )
        self.aria_value_maximum_suffix_before = configure.get_parameter(
            'aria-value-maximum-suffix-before'
        )
        self.aria_value_maximum_prefix_after = configure.get_parameter(
            'aria-value-maximum-prefix-after'
        )
        self.aria_value_maximum_suffix_after = configure.get_parameter(
            'aria-value-maximum-suffix-after'
        )
        self.aria_value_minimum_prefix_before = configure.get_parameter(
            'aria-value-minimum-prefix-before'
        )
        self.aria_value_minimum_suffix_before = configure.get_parameter(
            'aria-value-minimum-suffix-before'
        )
        self.aria_value_minimum_prefix_after = configure.get_parameter(
            'aria-value-minimum-prefix-after'
        )
        self.aria_value_minimum_suffix_after = configure.get_parameter(
            'aria-value-minimum-suffix-after'
        )
        self.aria_orientation_horizontal_before = configure.get_parameter(
            'aria-orientation-horizontal-before'
        )
        self.aria_orientation_horizontal_after = configure.get_parameter(
            'aria-orientation-horizontal-after'
        )
        self.aria_orientation_vertical_before = configure.get_parameter(
            'aria-orientation-vertical-before'
        )
        self.aria_orientation_vertical_after = configure.get_parameter(
            'aria-orientation-vertical-after'
        )
        self.aria_pressed_false_before = configure.get_parameter(
            'aria-pressed-false-before'
        )
        self.aria_pressed_false_after = configure.get_parameter(
            'aria-pressed-false-after'
        )
        self.aria_pressed_mixed_before = configure.get_parameter(
            'aria-pressed-mixed-before'
        )
        self.aria_pressed_mixed_after = configure.get_parameter(
            'aria-pressed-mixed-after'
        )
        self.aria_pressed_true_before = configure.get_parameter(
            'aria-pressed-true-before'
        )
        self.aria_pressed_true_after = configure.get_parameter(
            'aria-pressed-true-after'
        )
        self.aria_required_true_before = configure.get_parameter(
            'aria-required-true-before'
        )
        self.aria_required_true_after = configure.get_parameter(
            'aria-required-true-after'
        )
        self.aria_selected_false_before = configure.get_parameter(
            'aria-selected-false-before'
        )
        self.aria_selected_false_after = configure.get_parameter(
            'aria-selected-false-after'
        )
        self.aria_selected_true_before = configure.get_parameter(
            'aria-selected-true-before'
        )
        self.aria_selected_true_after = configure.get_parameter(
            'aria-selected-true-after'
        )
        self.aria_sort_ascending_before = configure.get_parameter(
            'aria-sort-ascending-before'
        )
        self.aria_sort_ascending_after = configure.get_parameter(
            'aria-sort-ascending-after'
        )
        self.aria_sort_descending_before = configure.get_parameter(
            'aria-sort-descending-before'
        )
        self.aria_sort_descending_after = configure.get_parameter(
            'aria-sort-descending-after'
        )
        self.aria_sort_other_before = configure.get_parameter(
            'aria-sort-other-before'
        )
        self.aria_sort_other_after = configure.get_parameter(
            'aria-sort-other-after'
        )
        self.list_shortcuts_added = False
        self.list_shortcuts_before = None
        self.list_shortcuts_after = None

    def _get_shortcut_prefix(self, user_agent, standart_prefix):
        """
        Returns the shortcut prefix of browser.

        :param user_agent: The user agent of browser.
        :type user_agent: str
        :param standart_prefix: The default prefix.
        :type standart_prefix: str
        :return: The shortcut prefix of browser.
        :rtype: str
        """
        # pylint: disable=no-self-use

        if user_agent is not None:
            user_agent = user_agent.lower()
            opera = 'opera' in user_agent
            mac = 'mac' in user_agent
            konqueror = 'konqueror' in user_agent
            spoofer = 'spoofer' in user_agent
            safari = 'applewebkit' in user_agent
            windows = 'windows' in user_agent
            chrome = 'chrome' in user_agent
            firefox = (
                ('firefox' in user_agent)
                or ('minefield' in user_agent)
            )
            internet_explorer = (
                ('msie' in user_agent)
                or ('trident' in user_agent)
            )

            if opera:
                return 'SHIFT + ESC'
            elif chrome and mac and (not spoofer):
                return 'CTRL + OPTION'
            elif safari and (not windows) and (not spoofer):
                return 'CTRL + ALT'
            elif (not windows) and (safari or mac or konqueror):
                return 'CTRL'
            elif firefox:
                return 'ALT + SHIFT'
            elif chrome or internet_explorer:
                return 'ALT'
            return standart_prefix
        return standart_prefix

    def _get_role_description(self, role):
        """
        Returns the description of role.

        :param role: The role.
        :type role: str
        :return: The description of role.
        :rtype: str
        """

        parameter = 'role-' + role.lower()
        if self.configure.has_parameter(parameter):
            return self.configure.get_parameter(parameter)
        return None

    def _get_language_description(self, language_code):
        """
        Returns the description of language.

        :param language_code: The BCP 47 code language.
        :type language_code: str
        :return: The description of language.
        :rtype: str
        """

        language = language_code.lower()
        parameter = 'language-' + language
        if self.configure.has_parameter(parameter):
            return self.configure.get_parameter(parameter)
        elif '-' in language:
            codes = re.split(r'\-', language)
            parameter = 'language-' + codes[0]
            if self.configure.has_parameter(parameter):
                return self.configure.get_parameter(parameter)
        return None

    def _get_description(self, element):
        """
        Returns the description of element.

        :param element: The element.
        :type element: hatemile.util.html.htmldomelement.HTMLDOMElement
        :return: The description of element.
        :rtype: str
        """

        description = None
        if element.has_attribute('title'):
            description = element.get_attribute('title')
        elif element.has_attribute('aria-label'):
            description = element.get_attribute('aria-label')
        elif element.has_attribute('alt'):
            description = element.get_attribute('alt')
        elif element.has_attribute('label'):
            description = element.get_attribute('label')
        elif (
            (element.has_attribute('aria-labelledby'))
            or (element.has_attribute('aria-describedby'))
        ):
            if element.has_attribute('aria-labelledby'):
                description_ids = re.split(
                    '[ \n\r\t]+',
                    element.get_attribute('aria-labelledby').strip()
                )
            else:
                description_ids = re.split(
                    '[ \n\r\t]+',
                    element.get_attribute('aria-describedby').strip()
                )
            for description_id in description_ids:
                element_description = self.parser.find(
                    '#' + description_id
                ).first_result()
                if element_description is not None:
                    description = element_description.get_text_content()
                    break
        elif (
            (element.get_tag_name() == 'INPUT')
            and (element.has_attribute('type'))
        ):
            type_attribute = element.get_attribute('type').lower()
            if (
                (
                    (type_attribute == 'button')
                    or (type_attribute == 'submit')
                    or (type_attribute == 'reset')
                )
                and (element.has_attribute('value'))
            ):
                description = element.get_attribute('value')
        if not bool(description):
            description = element.get_text_content()
        return re.sub('[ \n\r\t]+', ' ', description.strip())

    def _generate_list_shortcuts(self):
        """
        Generate the list of shortcuts of page.
        """

        id_container_shortcuts_before = (
            AccessibleDisplayImplementation.ID_CONTAINER_SHORTCUTS_BEFORE
        )
        id_container_shortcuts_after = (
            AccessibleDisplayImplementation.ID_CONTAINER_SHORTCUTS_AFTER
        )
        local = self.parser.find('body').first_result()
        if local is not None:
            container_before = self.parser.find(
                '#'
                + id_container_shortcuts_before
            ).first_result()
            if (
                (container_before is None)
                and (self.attribute_accesskey_before)
            ):
                container_before = self.parser.create_element('div')
                container_before.set_attribute(
                    'id',
                    id_container_shortcuts_before
                )

                text_container_before = self.parser.create_element('span')
                text_container_before.set_attribute(
                    'class',
                    AccessibleDisplayImplementation.CLASS_TEXT_SHORTCUTS
                )
                text_container_before.append_text(
                    self.attribute_accesskey_before
                )

                container_before.append_element(text_container_before)
                local.prepend_element(container_before)
            if container_before is not None:
                self.list_shortcuts_before = self.parser.find(
                    container_before
                ).find_children('ul').first_result()
                if self.list_shortcuts_before is None:
                    self.list_shortcuts_before = self.parser.create_element(
                        'ul'
                    )
                    container_before.append_element(self.list_shortcuts_before)

            container_after = self.parser.find(
                '#'
                + id_container_shortcuts_after
            ).first_result()
            if (
                (container_after is None)
                and (self.attribute_accesskey_after)
            ):
                container_after = self.parser.create_element('div')
                container_after.set_attribute(
                    'id',
                    id_container_shortcuts_after
                )

                text_container_after = self.parser.create_element('span')
                text_container_after.set_attribute(
                    'class',
                    AccessibleDisplayImplementation.CLASS_TEXT_SHORTCUTS
                )
                text_container_after.append_text(
                    self.attribute_accesskey_after
                )

                container_after.append_element(text_container_after)
                local.append_element(container_after)
            if container_after is not None:
                self.list_shortcuts_after = self.parser.find(
                    container_after
                ).find_children('ul').first_result()
                if self.list_shortcuts_after is None:
                    self.list_shortcuts_after = self.parser.create_element(
                        'ul'
                    )
                    container_after.append_element(self.list_shortcuts_after)
        self.list_shortcuts_added = True

    def _insert(self, element, new_element, before):
        """
        Insert a element before or after other element.

        :param element: The reference element.
        :type element: hatemile.util.html.htmldomelement.HTMLDOMElement
        :param new_element: The element that be inserted.
        :type new_element: hatemile.util.html.htmldomelement.HTMLDOMElement
        :param before: To insert the element before the other element.
        :type before: bool
        """

        tag_name = element.get_tag_name()
        append_tags = [
            'BODY',
            'A',
            'FIGCAPTION',
            'LI',
            'DT',
            'DD',
            'LABEL',
            'OPTION',
            'TD',
            'TH'
        ]
        controls = ['INPUT', 'SELECT', 'TEXTAREA']
        if tag_name == 'HTML':
            body = self.parser.find('body').first_result()
            if body is not None:
                self._insert(body, new_element, before)
        elif tag_name in append_tags:
            if before:
                element.prepend_element(new_element)
            else:
                element.append_element(new_element)
        elif tag_name in controls:
            labels = []
            if element.has_attribute('id'):
                labels = self.parser.find(
                    'label[for="'
                    + element.get_attribute('id')
                    + '"]'
                ).list_results()
            if not labels:
                labels = self.parser.find(element).find_ancestors(
                    'label'
                ).list_results()
            for label in labels:
                self._insert(label, new_element, before)
        elif before:
            element.insert_before(new_element)
        else:
            element.insert_after(new_element)

    def _force_read_simple(self, element, text_before, text_after, data_of):
        """
        Force the screen reader display an information of element.

        :param element: The reference element.
        :type element: hatemile.util.html.htmldomelement.HTMLDOMElement
        :param text_before: The text content to show before the element.
        :type text_before: str
        :param text_after: The text content to show after the element.
        :type text_after: str
        :param data_of: The name of attribute that links the content with
                        element.
        :type data_of: str
        """

        self.id_generator.generate_id(element)
        identifier = element.get_attribute('id')
        selector = '[' + data_of + '="' + identifier + '"]'

        reference_before = self.parser.find(
            '.'
            + AccessibleDisplayImplementation.CLASS_FORCE_READ_BEFORE
            + selector
        ).first_result()
        reference_after = self.parser.find(
            '.'
            + AccessibleDisplayImplementation.CLASS_FORCE_READ_AFTER
            + selector
        ).first_result()
        references = self.parser.find(selector).list_results()
        if reference_before in references:
            references.remove(reference_before)
        if reference_after in references:
            references.remove(reference_after)

        if not references:
            if text_before:
                if reference_before is not None:
                    reference_before.remove_node()

                span = self.parser.create_element('span')
                span.set_attribute(
                    'class',
                    AccessibleDisplayImplementation.CLASS_FORCE_READ_BEFORE
                )
                span.set_attribute(data_of, identifier)
                span.append_text(text_before)
                self._insert(element, span, True)
            if text_after:
                if reference_after is not None:
                    reference_after.remove_node()

                span = self.parser.create_element('span')
                span.set_attribute(
                    'class',
                    AccessibleDisplayImplementation.CLASS_FORCE_READ_AFTER
                )
                span.set_attribute(data_of, identifier)
                span.append_text(text_after)
                self._insert(element, span, False)

    def _force_read(
        self,
        element,
        value,
        text_prefix_before,
        text_suffix_before,
        text_prefix_after,
        text_suffix_after,
        data_of
    ):
        """
        Force the screen reader display an information of element with prefixes
        or suffixes.

        :param element: The reference element.
        :type element: hatemile.util.html.htmldomelement.HTMLDOMElement
        :param value: The value to be show.
        :type value: str
        :param text_prefix_before: The prefix of value to show before the
                                   element.
        :type text_prefix_before: str
        :param text_suffix_before: The suffix of value to show before the
                                   element.
        :type text_suffix_before: str
        :param text_prefix_after: The prefix of value to show after the
                                  element.
        :type text_prefix_after: str
        :param text_suffix_after: The suffix of value to show after the
                                  element.
        :type text_suffix_after: str
        :param data_of: The name of attribute that links the content with
                        element.
        :type data_of: str
        """

        if (text_prefix_before) or (text_suffix_before):
            text_before = text_prefix_before + value + text_suffix_before
        else:
            text_before = ''
        if (text_prefix_after) or (text_suffix_after):
            text_after = text_prefix_after + value + text_suffix_after
        else:
            text_after = ''
        self._force_read_simple(element, text_before, text_after, data_of)

    def display_shortcut(self, element):
        data_attribute_accesskey_of = (
            AccessibleDisplayImplementation.DATA_ATTRIBUTE_ACCESSKEY_OF
        )
        if element.has_attribute('accesskey'):
            description = self._get_description(element)
            if not element.has_attribute('title'):
                element.set_attribute('title', description)
                self.id_generator.generate_id(element)
                element.set_attribute(
                    AccessibleDisplayImplementation.DATA_ATTRIBUTE_TITLE_OF,
                    element.get_attribute('id')
                )

            if not self.list_shortcuts_added:
                self._generate_list_shortcuts()

            keys = re.split(
                '[ \n\t\r]+',
                element.get_attribute('accesskey').upper()
            )
            for key in keys:
                shortcut = self.shortcut_prefix + ' + ' + key
                self._force_read(
                    element,
                    shortcut,
                    self.attribute_accesskey_prefix_before,
                    self.attribute_accesskey_suffix_before,
                    self.attribute_accesskey_prefix_after,
                    self.attribute_accesskey_suffix_after,
                    data_attribute_accesskey_of
                )

                item = self.parser.create_element('li')
                item.set_attribute(data_attribute_accesskey_of, key)
                item.append_text(shortcut + ': ' + description)

                selector = (
                    '['
                    + data_attribute_accesskey_of
                    + '="'
                    + key
                    + '"]'
                )
                if (
                    (self.list_shortcuts_before is not None)
                    and (
                        self.parser.find(
                            self.list_shortcuts_before
                        ).find_children(selector).first_result() is None
                    )
                ):
                    self.list_shortcuts_before.append_element(
                        item.clone_element()
                    )
                if (
                    (self.list_shortcuts_after)
                    and (
                        self.parser.find(
                            self.list_shortcuts_after
                        ).find_children(selector).first_result() is None
                    )
                ):
                    self.list_shortcuts_after.append_element(
                        item.clone_element()
                    )

    def display_all_shortcuts(self):
        elements = self.parser.find('[accesskey]').list_results()
        for element in elements:
            if CommonFunctions.is_valid_element(element):
                self.display_shortcut(element)

    def display_role(self, element):
        if element.has_attribute('role'):
            role_description = self._get_role_description(
                element.get_attribute('role')
            )
            if role_description is not None:
                self._force_read(
                    element,
                    role_description,
                    self.attribute_role_prefix_before,
                    self.attribute_role_suffix_before,
                    self.attribute_role_prefix_after,
                    self.attribute_role_suffix_after,
                    AccessibleDisplayImplementation.DATA_ROLE_OF
                )

    def display_all_roles(self):
        elements = self.parser.find('[role]').list_results()
        for element in elements:
            if CommonFunctions.is_valid_element(element):
                self.display_role(element)

    def display_cell_header(self, table_cell):
        if table_cell.has_attribute('headers'):
            text_header = ''
            ids_headers = re.split(
                '[ \n\t\r]+',
                table_cell.get_attribute('headers')
            )
            for id_header in ids_headers:
                header = self.parser.find('#' + id_header).first_result()
                if header is not None:
                    if text_header == '':
                        text_header = header.get_text_content().strip()
                    else:
                        text_header = (
                            text_header
                            + ' '
                            + header.get_text_content().strip()
                        )
            if text_header.strip() != '':
                self._force_read(
                    table_cell,
                    text_header,
                    self.attribute_headers_prefix_before,
                    self.attribute_headers_suffix_before,
                    self.attribute_headers_prefix_after,
                    self.attribute_headers_suffix_after,
                    AccessibleDisplayImplementation.DATA_ATTRIBUTE_HEADERS_OF
                )

    def display_all_cell_headers(self):
        elements = self.parser.find('td[headers],th[headers]').list_results()
        for element in elements:
            if CommonFunctions.is_valid_element(element):
                self.display_cell_header(element)

    def display_waiaria_states(self, element):
        if (
            (element.has_attribute('aria-busy'))
            and (element.get_attribute('aria-busy') == 'true')
        ):
            self._force_read_simple(
                element,
                self.aria_busy_true_before,
                self.aria_busy_true_after,
                AccessibleDisplayImplementation.DATA_ARIA_BUSY_OF
            )
        if element.has_attribute('aria-checked'):
            attribute_value = element.get_attribute('aria-checked')
            if attribute_value == 'true':
                self._force_read_simple(
                    element,
                    self.aria_checked_true_before,
                    self.aria_checked_true_after,
                    AccessibleDisplayImplementation.DATA_ARIA_CHECKED_OF
                )
            elif attribute_value == 'false':
                self._force_read_simple(
                    element,
                    self.aria_checked_false_before,
                    self.aria_checked_false_after,
                    AccessibleDisplayImplementation.DATA_ARIA_CHECKED_OF
                )
            elif attribute_value == 'mixed':
                self._force_read_simple(
                    element,
                    self.aria_checked_mixed_before,
                    self.aria_checked_mixed_after,
                    AccessibleDisplayImplementation.DATA_ARIA_CHECKED_OF
                )
        if element.has_attribute('aria-expanded'):
            attribute_value = element.get_attribute('aria-expanded')
            if attribute_value == 'true':
                self._force_read_simple(
                    element,
                    self.aria_expanded_true_before,
                    self.aria_expanded_true_after,
                    AccessibleDisplayImplementation.DATA_ARIA_EXPANDED_OF
                )
            elif attribute_value == 'false':
                self._force_read_simple(
                    element,
                    self.aria_expanded_false_before,
                    self.aria_expanded_false_after,
                    AccessibleDisplayImplementation.DATA_ARIA_EXPANDED_OF
                )
        if (
            (element.has_attribute('aria-haspopup'))
            and (element.get_attribute('aria-haspopup') == 'true')
        ):
            self._force_read_simple(
                element,
                self.aria_haspopup_true_before,
                self.aria_haspopup_true_after,
                AccessibleDisplayImplementation.DATA_ARIA_HASPOPUP_OF
            )
        if element.has_attribute('aria-level'):
            self._force_read(
                element,
                element.get_attribute('aria-level'),
                self.aria_level_prefix_before,
                self.aria_level_suffix_before,
                self.aria_level_prefix_after,
                self.aria_level_suffix_after,
                AccessibleDisplayImplementation.DATA_ARIA_LEVEL_OF
            )
        if element.has_attribute('aria-orientation'):
            attribute_value = element.get_attribute('aria-orientation')
            if attribute_value == 'vertical':
                self._force_read_simple(
                    element,
                    self.aria_orientation_vertical_before,
                    self.aria_orientation_vertical_after,
                    AccessibleDisplayImplementation.DATA_ARIA_ORIENTATION_OF
                )
            elif attribute_value == 'horizontal':
                self._force_read_simple(
                    element,
                    self.aria_orientation_horizontal_before,
                    self.aria_orientation_horizontal_after,
                    AccessibleDisplayImplementation.DATA_ARIA_ORIENTATION_OF
                )
        if element.has_attribute('aria-pressed'):
            attribute_value = element.get_attribute('aria-pressed')
            if attribute_value == 'true':
                self._force_read_simple(
                    element,
                    self.aria_pressed_true_before,
                    self.aria_pressed_true_after,
                    AccessibleDisplayImplementation.DATA_ARIA_PRESSED_OF
                )
            elif attribute_value == 'false':
                self._force_read_simple(
                    element,
                    self.aria_pressed_false_before,
                    self.aria_pressed_false_after,
                    AccessibleDisplayImplementation.DATA_ARIA_PRESSED_OF
                )
            elif attribute_value == 'mixed':
                self._force_read_simple(
                    element,
                    self.aria_pressed_mixed_before,
                    self.aria_pressed_mixed_after,
                    AccessibleDisplayImplementation.DATA_ARIA_PRESSED_OF
                )
        if element.has_attribute('aria-selected'):
            attribute_value = element.get_attribute('aria-selected')
            if attribute_value == 'true':
                self._force_read_simple(
                    element,
                    self.aria_selected_true_before,
                    self.aria_selected_true_after,
                    AccessibleDisplayImplementation.DATA_ARIA_SELECTED_OF
                )
            elif attribute_value == 'false':
                self._force_read_simple(
                    element,
                    self.aria_selected_false_before,
                    self.aria_selected_false_after,
                    AccessibleDisplayImplementation.DATA_ARIA_SELECTED_OF
                )
        if element.has_attribute('aria-sort'):
            attribute_value = element.get_attribute('aria-sort')
            if attribute_value == 'ascending':
                self._force_read_simple(
                    element,
                    self.aria_sort_ascending_before,
                    self.aria_sort_ascending_after,
                    AccessibleDisplayImplementation.DATA_ARIA_SORT_OF
                )
            elif attribute_value == 'descending':
                self._force_read_simple(
                    element,
                    self.aria_sort_descending_before,
                    self.aria_sort_descending_after,
                    AccessibleDisplayImplementation.DATA_ARIA_SORT_OF
                )
            elif attribute_value == 'other':
                self._force_read_simple(
                    element,
                    self.aria_sort_other_before,
                    self.aria_sort_other_after,
                    AccessibleDisplayImplementation.DATA_ARIA_SORT_OF
                )
        if (
            (element.has_attribute('aria-required'))
            and (element.get_attribute('aria-required') == 'true')
        ):
            self._force_read_simple(
                element,
                self.aria_required_true_before,
                self.aria_required_true_after,
                AccessibleDisplayImplementation.DATA_ARIA_REQUIRED_OF
            )
        if element.has_attribute('aria-valuemin'):
            self._force_read(
                element,
                element.get_attribute('aria-valuemin'),
                self.aria_value_minimum_prefix_before,
                self.aria_value_minimum_suffix_before,
                self.aria_value_minimum_prefix_after,
                self.aria_value_minimum_suffix_after,
                AccessibleDisplayImplementation.DATA_ARIA_RANGE_MIN_OF
            )
        if element.has_attribute('aria-valuemax'):
            self._force_read(
                element,
                element.get_attribute('aria-valuemax'),
                self.aria_value_maximum_prefix_before,
                self.aria_value_maximum_suffix_before,
                self.aria_value_maximum_prefix_after,
                self.aria_value_maximum_suffix_after,
                AccessibleDisplayImplementation.DATA_ARIA_RANGE_MAX_OF
            )
        if element.has_attribute('aria-autocomplete'):
            attribute_value = element.get_attribute('aria-autocomplete')
            if attribute_value == 'both':
                self._force_read_simple(
                    element,
                    self.aria_autocomplete_both_before,
                    self.aria_autocomplete_both_after,
                    AccessibleDisplayImplementation.DATA_ARIA_AUTOCOMPLETE_OF
                )
            elif attribute_value == 'inline':
                self._force_read_simple(
                    element,
                    self.aria_autocomplete_list_before,
                    self.aria_autocomplete_list_after,
                    AccessibleDisplayImplementation.DATA_ARIA_AUTOCOMPLETE_OF
                )
            elif attribute_value == 'list':
                self._force_read_simple(
                    element,
                    self.aria_autocomplete_inline_before,
                    self.aria_autocomplete_inline_after,
                    AccessibleDisplayImplementation.DATA_ARIA_AUTOCOMPLETE_OF
                )
        if element.has_attribute('aria-dropeffect'):
            attribute_value = element.get_attribute('aria-dropeffect')
            if attribute_value == 'copy':
                self._force_read_simple(
                    element,
                    self.aria_dropeffect_copy_before,
                    self.aria_dropeffect_copy_after,
                    AccessibleDisplayImplementation.DATA_ARIA_DROPEFFECT_OF
                )
            elif attribute_value == 'move':
                self._force_read_simple(
                    element,
                    self.aria_dropeffect_move_before,
                    self.aria_dropeffect_move_after,
                    AccessibleDisplayImplementation.DATA_ARIA_DROPEFFECT_OF
                )
            elif attribute_value == 'link':
                self._force_read_simple(
                    element,
                    self.aria_dropeffect_link_before,
                    self.aria_dropeffect_link_after,
                    AccessibleDisplayImplementation.DATA_ARIA_DROPEFFECT_OF
                )
            elif attribute_value == 'execute':
                self._force_read_simple(
                    element,
                    self.aria_dropeffect_execute_before,
                    self.aria_dropeffect_execute_after,
                    AccessibleDisplayImplementation.DATA_ARIA_DROPEFFECT_OF
                )
            elif attribute_value == 'popup':
                self._force_read_simple(
                    element,
                    self.aria_dropeffect_popup_before,
                    self.aria_dropeffect_popup_after,
                    AccessibleDisplayImplementation.DATA_ARIA_DROPEFFECT_OF
                )
        if element.has_attribute('aria-grabbed'):
            attribute_value = element.get_attribute('aria-grabbed')
            if attribute_value == 'true':
                self._force_read_simple(
                    element,
                    self.aria_grabbed_true_before,
                    self.aria_grabbed_true_after,
                    AccessibleDisplayImplementation.DATA_ARIA_GRABBED_OF
                )
            elif attribute_value == 'false':
                self._force_read_simple(
                    element,
                    self.aria_grabbed_false_before,
                    self.aria_grabbed_false_after,
                    AccessibleDisplayImplementation.DATA_ARIA_GRABBED_OF
                )

    def display_all_waiaria_states(self):
        elements = self.parser.find(
            '[aria-busy=true],[aria-checked],[aria-dropeffect],'
            + '[aria-expanded],[aria-grabbed],[aria-haspopup],[aria-level],'
            + '[aria-orientation],[aria-pressed],[aria-selected],[aria-sort],'
            + '[aria-required=true],[aria-valuemin],[aria-valuemax],'
            + '[aria-autocomplete]'
        ).list_results()
        for element in elements:
            if CommonFunctions.is_valid_element(element):
                self.display_waiaria_states(element)

    def display_link_attributes(self, link):
        if link.has_attribute('download'):
            self._force_read_simple(
                link,
                self.attribute_download_before,
                self.attribute_download_after,
                AccessibleDisplayImplementation.DATA_ATTRIBUTE_DOWNLOAD_OF
            )
        if (
            (link.has_attribute('target'))
            and (link.get_attribute('target') == '_blank')
        ):
            self._force_read_simple(
                link,
                self.attribute_target_blank_before,
                self.attribute_target_blank_after,
                AccessibleDisplayImplementation.DATA_ATTRIBUTE_TARGET_OF
            )

    def display_all_links_attributes(self):
        elements = self.parser.find(
            'a[download],a[target="_blank"]'
        ).list_results()
        for element in elements:
            if CommonFunctions.is_valid_element(element):
                self.display_link_attributes(element)

    def display_title(self, element):
        if element.get_tag_name() == 'IMG':
            self.display_alternative_text_image(element)
        elif (
            (element.has_attribute('title'))
            and (element.get_attribute('title'))
        ):
            self._force_read(
                element,
                element.get_attribute('title'),
                self.attribute_title_prefix_before,
                self.attribute_title_suffix_before,
                self.attribute_title_prefix_after,
                self.attribute_title_suffix_after,
                AccessibleDisplayImplementation.DATA_ATTRIBUTE_TITLE_OF
            )

    def display_all_titles(self):
        elements = self.parser.find('body [title]').list_results()
        for element in elements:
            if CommonFunctions.is_valid_element(element):
                self.display_title(element)

    def display_language(self, element):
        language_code = None
        if element.has_attribute('lang'):
            language_code = element.get_attribute('lang')
        elif element.has_attribute('hreflang'):
            language_code = element.get_attribute('hreflang')
        language = self._get_language_description(language_code)
        if language is not None:
            self._force_read(
                element,
                language,
                self.attribute_language_prefix_before,
                self.attribute_language_suffix_before,
                self.attribute_language_prefix_after,
                self.attribute_language_suffix_after,
                AccessibleDisplayImplementation.DATA_ATTRIBUTE_LANGUAGE_OF
            )

    def display_all_languages(self):
        elements = self.parser.find(
            'html[lang],body[lang],body [lang],body [hreflang]'
        ).list_results()
        for element in elements:
            if CommonFunctions.is_valid_element(element):
                self.display_language(element)

    def display_alternative_text_image(self, image):
        if (image.has_attribute('alt')) or (image.has_attribute('title')):
            if (
                (image.has_attribute('alt'))
                and (not image.has_attribute('title'))
            ):
                image.set_attribute('title', image.get_attribute('alt'))
            elif (
                (image.has_attribute('title'))
                and (not image.has_attribute('alt'))
            ):
                image.set_attribute('alt', image.get_attribute('title'))
            self.id_generator.generate_id(image)
            image.set_attribute(
                AccessibleDisplayImplementation.DATA_ATTRIBUTE_TITLE_OF,
                image.get_attribute('id')
            )
        else:
            image.set_attribute('alt', '')
            image.set_attribute('role', 'presentation')
            image.set_attribute('aria-hidden', 'true')

    def display_all_alternative_text_images(self):
        images = self.parser.find('img').list_results()
        for image in images:
            if CommonFunctions.is_valid_element(image):
                self.display_alternative_text_image(image)
