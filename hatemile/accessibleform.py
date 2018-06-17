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
Module of AccessibleForm interface.
"""


class AccessibleForm:
    """
    The AccessibleForm interface improve the accessibility of forms.
    """

    def mark_required_field(self, required_field):
        """
        Mark that the field is required.

        :param required_field: The required field.
        :type required_field: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        pass

    def mark_all_required_fields(self):
        """
        Mark that the fields is required.
        """

        pass

    def mark_range_field(self, range_field):
        """
        Mark that the field have range.

        :param range_field: The range field.
        :type range_field: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        pass

    def mark_all_range_fields(self):
        """
        Mark that the fields have range.
        """

        pass

    def mark_autocomplete_field(self, field):
        """
        Mark that the field have autocomplete.

        :param field: The field with autocomplete.
        :type field: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

        pass

    def mark_all_autocomplete_fields(self):
        """
        Mark that the fields have autocomplete.
        """

        pass

    def mark_invalid_field(self, field):
        """
        Mark a solution to display that this field is invalid.

        :param field: The field.
        :type field: hatemile.util.html.htmldomelement.HTMLDOMElement
        """

    def mark_all_invalid_fields(self):
        """
        Mark a solution to display that a fields are invalid.
        """

        pass
