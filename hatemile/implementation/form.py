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
Module of AccessibleFormImplementation class.
"""

import os
from hatemile import helper
from hatemile.accessibleform import AccessibleForm
from hatemile.util.commonfunctions import CommonFunctions
from hatemile.util.idgenerator import IDGenerator
from hatemile.util.html.htmldomparser import HTMLDOMParser
from .event import AccessibleEventImplementation


class AccessibleFormImplementation(AccessibleForm):
    """
    The AccessibleFormImplementation class is official implementation of
    :py:class:`hatemile.accessibleform.AccessibleForm`.
    """

    #: The ID of script element that contains the list of IDs of fields with
    #: validation.
    ID_SCRIPT_LIST_VALIDATION_FIELDS = 'hatemile-scriptlist-validation-fields'

    #: The ID of script element that execute validations on fields.
    ID_SCRIPT_EXECUTE_VALIDATION = 'hatemile-validation-script'

    #: The client-site required fields list.
    REQUIRED_FIELDS_LIST = 'required_fields'

    #: The client-site pattern fields list.
    PATTERN_FIELDS_LIST = 'pattern_fields'

    #: The client-site fields with length list.
    LIMITED_FIELDS_LIST = 'fields_with_length'

    #: The client-site range fields list.
    RANGE_FIELDS_LIST = 'range_fields'

    #: The client-site week fields list.
    WEEK_FIELDS_LIST = 'week_fields'

    #: The client-site month fields list.
    MONTH_FIELDS_LIST = 'month_fields'

    #: The client-site datetime fields list.
    DATETIME_FIELDS_LIST = 'datetime_fields'

    #: The client-site time fields list.
    TIME_FIELDS_LIST = 'time_fields'

    #: The client-site date fields list.
    DATE_FIELDS_LIST = 'date_fields'

    #: The client-site email fields list.
    EMAIL_FIELDS_LIST = 'email_fields'

    #: The client-site URL fields list.
    URL_FIELDS_LIST = 'url_fields'

    def __init__(self, parser):
        """
        Initializes a new object that manipulate the accessibility of the forms
        of parser.

        :param parser: The HTML parser.
        :type parser: hatemile.util.html.htmldomparser.HTMLDOMParser
        """

        helper.require_not_none(parser)
        helper.require_valid_type(parser, HTMLDOMParser)

        self.parser = parser
        self.id_generator = IDGenerator('form')
        self.scripts_added = False
        self.script_list_fields_with_validation = None

    def _get_aria_autocomplete(self, field):
        """
        Returns the appropriate value for attribute aria-autocomplete of field.

        :param field: The field.
        :type field: hatemile.util.html.htmldomelement.HTMLDOMElement
        :return: The ARIA value of field.
        :rtype: str
        """

        tag_name = field.get_tag_name()
        input_type = None
        if field.has_attribute('type'):
            input_type = field.get_attribute('type').lower()
        if (
            (tag_name == 'TEXTAREA')
            or (
                (tag_name == 'INPUT')
                and (not (
                    (input_type == 'button')
                    or (input_type == 'submit')
                    or (input_type == 'reset')
                    or (input_type == 'image')
                    or (input_type == 'file')
                    or (input_type == 'checkbox')
                    or (input_type == 'radio')
                    or (input_type == 'hidden')
                ))
            )
        ):
            value = None
            if field.has_attribute('autocomplete'):
                value = field.get_attribute('autocomplete').lower()
            else:
                form = self.parser.find(field).find_ancestors(
                    'form'
                ).first_result()
                if (form is None) and (field.has_attribute('form')):
                    form = self.parser.find(
                        '#' + field.get_attribute('form')
                    ).first_result()
                if (form is not None) and (form.has_attribute('autocomplete')):
                    value = form.get_attribute('autocomplete').lower()
            if value == 'on':
                return 'both'
            elif (
                (field.has_attribute('list'))
                and (self.parser.find(
                    'datalist[id="' + field.get_attribute('list') + '"]'
                ).first_result() is not None)
            ):
                return 'list'
            elif value == 'off':
                return 'none'
        return None

    def _generate_validation_scripts(self):
        """
        Include the scripts used by solutions.
        """

        id_script_list_validation_fields = (
            AccessibleFormImplementation.ID_SCRIPT_LIST_VALIDATION_FIELDS
        )
        local = self.parser.find('head,body').first_result()
        if local is not None:
            if (
                self.parser.find(
                    '#'
                    + AccessibleEventImplementation.ID_SCRIPT_COMMON_FUNCTIONS
                ).first_result() is None
            ):
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
                local.prepend_element(common_functions_script)

            self.script_list_fields_with_validation = self.parser.find(
                '#'
                + id_script_list_validation_fields
            ).first_result()
            if self.script_list_fields_with_validation is None:
                script_list_file = open(
                    os.path.join(
                        os.path.dirname(os.path.dirname(os.path.dirname(
                            os.path.realpath(__file__)
                        ))),
                        'js',
                        'scriptlist_validation_fields.js'
                    ),
                    'r'
                )
                script_list_content = script_list_file.read()
                script_list_file.close()

                self.script_list_fields_with_validation = (
                    self.parser.create_element('script')
                )
                self.script_list_fields_with_validation.set_attribute(
                    'id',
                    id_script_list_validation_fields
                )
                self.script_list_fields_with_validation.set_attribute(
                    'type',
                    'text/javascript'
                )
                self.script_list_fields_with_validation.append_text(
                    script_list_content
                )
                local.append_element(self.script_list_fields_with_validation)
            if (
                self.parser.find(
                    '#'
                    + AccessibleFormImplementation.ID_SCRIPT_EXECUTE_VALIDATION
                ).first_result() is None
            ):
                script_function_file = open(
                    os.path.join(
                        os.path.dirname(os.path.dirname(os.path.dirname(
                            os.path.realpath(__file__)
                        ))),
                        'js',
                        'validation.js'
                    ),
                    'r'
                )
                script_function_content = script_function_file.read()
                script_function_file.close()

                script_function = self.parser.create_element('script')
                script_function.set_attribute(
                    'id',
                    AccessibleFormImplementation.ID_SCRIPT_EXECUTE_VALIDATION
                )
                script_function.set_attribute('type', 'text/javascript')
                script_function.append_text(script_function_content)
                self.parser.find('body').first_result().append_element(
                    script_function
                )
        self.scripts_added = True

    def _validate(self, field, list_attribute):
        """
        Validate the field when its value change.

        :param field: The field.
        :param list_attribute: The list attribute of field with validation.
        """

        if not self.scripts_added:
            self._generate_validation_scripts()
        self.id_generator.generate_id(field)
        self.script_list_fields_with_validation.append_text(
            'hatemileValidationList.'
            + list_attribute
            + '.push("'
            + field.get_attribute('id')
            + '");'
        )

    def mark_required_field(self, required_field):
        if required_field.has_attribute('required'):
            required_field.set_attribute('aria-required', 'true')

    def mark_all_required_fields(self):
        required_fields = self.parser.find('[required]').list_results()
        for required_field in required_fields:
            if CommonFunctions.is_valid_element(required_field):
                self.mark_required_field(required_field)

    def mark_range_field(self, range_field):
        if range_field.has_attribute('min'):
            range_field.set_attribute(
                'aria-valuemin',
                range_field.get_attribute('min')
            )
        if range_field.has_attribute('max'):
            range_field.set_attribute(
                'aria-valuemax',
                range_field.get_attribute('max')
            )

    def mark_all_range_fields(self):
        range_fields = self.parser.find('[min],[max]').list_results()
        for range_field in range_fields:
            if CommonFunctions.is_valid_element(range_field):
                self.mark_range_field(range_field)

    def mark_autocomplete_field(self, field):
        aria_autocomplete = self._get_aria_autocomplete(field)
        if aria_autocomplete is not None:
            field.set_attribute(
                'aria-autocomplete',
                aria_autocomplete
            )

    def mark_all_autocomplete_fields(self):
        fields = self.parser.find(
            'input[autocomplete],textarea[autocomplete],'
            + 'form[autocomplete] input,form[autocomplete] textarea,'
            + '[list],[form]'
        ).list_results()
        for field in fields:
            if CommonFunctions.is_valid_element(field):
                self.mark_autocomplete_field(field)

    def mark_invalid_field(self, field):
        if (
            (field.has_attribute('required'))
            or (
                (field.has_attribute('aria-required'))
                and (field.get_attribute('aria-required').lower() == 'true')
            )
        ):
            self._validate(
                field,
                AccessibleFormImplementation.REQUIRED_FIELDS_LIST
            )
        if field.has_attribute('pattern'):
            self._validate(
                field,
                AccessibleFormImplementation.PATTERN_FIELDS_LIST
            )
        if (
            (field.has_attribute('minlength'))
            or (field.has_attribute('maxlength'))
        ):
            self._validate(
                field,
                AccessibleFormImplementation.LIMITED_FIELDS_LIST
            )
        if (
            (field.has_attribute('aria-valuemin'))
            or (field.has_attribute('aria-valuemax'))
        ):
            self._validate(
                field,
                AccessibleFormImplementation.RANGE_FIELDS_LIST
            )
        if field.has_attribute('type'):
            type_field = field.get_attribute('type').lower()
            if type_field == 'week':
                self._validate(
                    field,
                    AccessibleFormImplementation.WEEK_FIELDS_LIST
                )
            elif type_field == 'month':
                self._validate(
                    field,
                    AccessibleFormImplementation.MONTH_FIELDS_LIST
                )
            elif (
                (type_field == 'datetime-local')
                or (type_field == 'datetime')
            ):
                self._validate(
                    field,
                    AccessibleFormImplementation.DATETIME_FIELDS_LIST
                )
            elif type_field == 'time':
                self._validate(
                    field,
                    AccessibleFormImplementation.TIME_FIELDS_LIST
                )
            elif type_field == 'date':
                self._validate(
                    field,
                    AccessibleFormImplementation.DATE_FIELDS_LIST
                )
            elif (type_field == 'number') or (type_field == 'range'):
                self._validate(
                    field,
                    AccessibleFormImplementation.RANGE_FIELDS_LIST
                )
            elif type_field == 'email':
                self._validate(
                    field,
                    AccessibleFormImplementation.EMAIL_FIELDS_LIST
                )
            elif type_field == 'url':
                self._validate(
                    field,
                    AccessibleFormImplementation.URL_FIELDS_LIST
                )

    def mark_all_invalid_fields(self):
        fields = self.parser.find(
            '[required],input[pattern],input[minlength],input[maxlength],'
            + 'textarea[minlength],textarea[maxlength],input[type=week],'
            + 'input[type=month],input[type=datetime-local],'
            + 'input[type=datetime],input[type=time],input[type=date],'
            + 'input[type=number],input[type=range],input[type=email],'
            + 'input[type=url],[aria-required=true],input[aria-valuemin],'
            + 'input[aria-valuemax]'
        ).list_results()
        for field in fields:
            if CommonFunctions.is_valid_element(field):
                self.mark_invalid_field(field)
