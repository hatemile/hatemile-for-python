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


class AccessibleForm:
    """
    The AccessibleForm interface fixes accessibility problems associated with
    forms.
    """

    def fix_required_field(self, requiredField):
        """
        Display that the field is required.
        @param requiredField: The required field.
        @type requiredField: L{hatemile.util.HTMLDOMElement}
        """

        pass

    def fix_required_fields(self):
        """
        Display that the fields is required.
        """

        pass

    def fix_range_field(self, rangeField):
        """
        Display that the field have range.
        @param rangeField: The range field.
        @type rangeField: L{hatemile.util.HTMLDOMElement}
        """

        pass

    def fix_range_fields(self):
        """
        Display that the fields have range.
        """

        pass

    def fix_autocomplete_field(self, autoCompleteField):
        """
        Display that the field have autocomplete.
        @param autoCompleteField: The field with autocomplete.
        @type autoCompleteField: L{hatemile.util.HTMLDOMElement}
        """

        pass

    def fix_autocomplete_fields(self):
        """
        Display that the fields have autocomplete.
        """

        pass

    def fix_label(self, label):
        """
        Associate label with field.
        @param label: The label.
        @type label: L{hatemile.util.HTMLDOMElement}
        """

        pass

    def fix_labels(self):
        """
        Associate labels with fields.
        """

        pass
