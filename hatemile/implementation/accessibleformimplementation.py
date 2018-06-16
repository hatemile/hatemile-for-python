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

from hatemile.accessibleform import AccessibleForm
from hatemile.util.commonfunctions import CommonFunctions
from hatemile.util.idgenerator import IDGenerator


class AccessibleFormImplementation(AccessibleForm):
    """
    The AccessibleFormImplementation class is official implementation of
    :py:class:`hatemile.accessibleform.AccessibleForm`.
    """

    def __init__(self, parser):
        """
        Initializes a new object that manipulate the accessibility of the forms
        of parser.

        :param parser: The HTML parser.
        :type parser: hatemile.util.html.htmldomparser.HTMLDOMParser
        """

        self.parser = parser
        self.id_generator = IDGenerator('form')

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
        elements = self.parser.find(
            'input[autocomplete],textarea[autocomplete],'
            + 'form[autocomplete] input,form[autocomplete] textarea,'
            + '[list],[form]'
        ).list_results()
        for element in elements:
            if CommonFunctions.is_valid_element(element):
                self.mark_autocomplete_field(element)
