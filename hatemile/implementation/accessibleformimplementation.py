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
from hatemile.accessibleform import AccessibleForm
import re


class AccessibleFormImplementation(AccessibleForm):
    """
    The AccessibleFormImplementation class is official implementation of
    AccessibleForm interface.
    """

    def __init__(self, parser, configure):
        """
        Initializes a new object that manipulate the accessibility of the forms
        of parser.
        @param parser: The HTML parser.
        @type parser: L{hatemile.util.HTMLDOMParser}
        @param configure: The configuration of HaTeMiLe.
        @type configure: L{hatemile.util.Configure}
        """

        self.parser = parser
        self.dataLabelPrefixRequiredField = 'data-prefixrequiredfield'
        self.dataLabelSuffixRequiredField = 'data-suffixrequiredfield'
        self.dataLabelPrefixRangeMinField = 'data-prefixvalueminfield'
        self.dataLabelSuffixRangeMinField = 'data-suffixvalueminfield'
        self.dataLabelPrefixRangeMaxField = 'data-prefixvaluemaxfield'
        self.dataLabelSuffixRangeMaxField = 'data-suffixvaluemaxfield'
        self.dataLabelPrefixAutoCompleteField = 'data-prefixautocompletefield'
        self.dataLabelSuffixAutoCompleteField = 'data-suffixautocompletefield'
        self.dataIgnore = 'data-ignoreaccessibilityfix'
        self.prefixId = configure.get_parameter('prefix-generated-ids')
        self.prefixRequiredField = configure.get_parameter(
            'prefix-required-field'
        )
        self.suffixRequiredField = configure.get_parameter(
            'suffix-required-field'
        )
        self.prefixRangeMinField = configure.get_parameter(
            'prefix-range-min-field'
        )
        self.suffixRangeMinField = configure.get_parameter(
            'suffix-range-min-field'
        )
        self.prefixRangeMaxField = configure.get_parameter(
            'prefix-range-max-field'
        )
        self.suffixRangeMaxField = configure.get_parameter(
            'suffix-range-max-field'
        )
        self.prefixAutoCompleteField = configure.get_parameter(
            'prefix-autocomplete-field'
        )
        self.suffixAutoCompleteField = configure.get_parameter(
            'suffix-autocomplete-field'
        )
        self.textAutoCompleteValueBoth = configure.get_parameter(
            'text-autocomplete-value-both'
        )
        self.textAutoCompleteValueList = configure.get_parameter(
            'text-autocomplete-value-list'
        )
        self.textAutoCompleteValueInline = configure.get_parameter(
            'text-autocomplete-value-inline'
        )
        self.textAutoCompleteValueNone = configure.get_parameter(
            'text-autocomplete-value-none'
        )

    def _add_prefix_suffix(
        self,
        label,
        field,
        prefix,
        suffix,
        dataPrefix,
        dataSuffix
    ):
        """
        Display in label the information of field.
        @param label: The label.
        @type label: L{hatemile.util.HTMLDOMElement}
        @param field: The field.
        @type field: L{hatemile.util.HTMLDOMElement}
        @param prefix: The prefix.
        @type prefix: str
        @param suffix: The suffix.
        @type suffix: str
        @param dataPrefix: The name of prefix attribute.
        @type dataPrefix: str
        @param dataSuffix: The name of suffix attribute.
        @type dataSuffix: str
        """

        contentLabel = field.get_attribute('aria-label')
        if prefix != '':
            label.set_attribute(dataPrefix, prefix)
            if prefix not in contentLabel:
                contentLabel = prefix + ' ' + contentLabel
        if suffix != '':
            label.set_attribute(dataSuffix, suffix)
            if suffix not in contentLabel:
                contentLabel = contentLabel + ' ' + suffix
        field.set_attribute('aria-label', contentLabel)

    def _fix_label_required_field(self, label, requiredField):
        """
        Display in label the information if the field is required.
        @param label: The label.
        @type label: L{hatemile.util.HTMLDOMElement}
        @param requiredField: The required field.
        @type requiredField: L{hatemile.util.HTMLDOMElement}
        """

        if (
            (
                (requiredField.has_attribute('required'))
                or (
                    (requiredField.has_attribute('aria-required'))
                    and (requiredField.get_attribute(
                        'aria-required'
                    ).lower() == 'true')
                )
            )
            and (requiredField.has_attribute('aria-label'))
            and (not label.has_attribute(self.dataLabelPrefixRequiredField))
            and (not label.has_attribute(self.dataLabelSuffixRequiredField))
        ):
            self._add_prefix_suffix(
                label,
                requiredField,
                self.prefixRequiredField,
                self.suffixRequiredField,
                self.dataLabelPrefixRequiredField,
                self.dataLabelSuffixRequiredField
            )

    def _fix_label_range_field(self, label, rangeField):
        """
        Display in label the information of range of field.
        @param label: The label.
        @type label: L{hatemile.util.HTMLDOMElement}
        @param rangeField: The range field.
        @type rangeField: L{hatemile.util.HTMLDOMElement}
        """

        if rangeField.has_attribute('aria-label'):
            if (
                (
                    rangeField.has_attribute('min')
                    or rangeField.has_attribute('aria-valuemin')
                )
                and (not label.has_attribute(
                    self.dataLabelPrefixRangeMinField
                ))
                and (not label.has_attribute(
                    self.dataLabelSuffixRangeMinField
                ))
            ):
                if rangeField.has_attribute('min'):
                    value = rangeField.get_attribute('min')
                else:
                    value = rangeField.get_attribute('aria-valuemin')
                self._add_prefix_suffix(
                    label,
                    rangeField,
                    re.sub(
                        '{{value}}',
                        value,
                        self.prefixRangeMinField
                    ),
                    re.sub(
                        '{{value}}',
                        value,
                        self.suffixRangeMinField
                    ),
                    self.dataLabelPrefixRangeMinField,
                    self.dataLabelSuffixRangeMinField
                )
            if (
                (
                    rangeField.has_attribute('max')
                    or rangeField.has_attribute('aria-valuemax')
                )
                and (not label.has_attribute(
                    self.dataLabelPrefixRangeMaxField
                ))
                and (not label.has_attribute(
                    self.dataLabelSuffixRangeMaxField
                ))
            ):
                if rangeField.has_attribute('max'):
                    value = rangeField.get_attribute('max')
                else:
                    value = rangeField.get_attribute('aria-valuemax')
                self._add_prefix_suffix(
                    label,
                    rangeField,
                    re.sub(
                        '{{value}}',
                        value,
                        self.prefixRangeMaxField
                    ),
                    re.sub(
                        '{{value}}',
                        value,
                        self.suffixRangeMaxField
                    ),
                    self.dataLabelPrefixRangeMaxField,
                    self.dataLabelSuffixRangeMaxField
                )

    def _fix_label_autocomplete_field(self, label, autoCompleteField):
        """
        Display in label the information if the field has autocomplete.
        @param label: The label.
        @type label: L{hatemile.util.HTMLDOMElement}
        @param autoCompleteField: The autocomplete field.
        @type autoCompleteField: L{hatemile.util.HTMLDOMElement}
        """

        prefixAutoCompleteFieldModified = ''
        suffixAutoCompleteFieldModified = ''
        if (
            (autoCompleteField.has_attribute('aria-label'))
            and (not label.has_attribute(
                self.dataLabelPrefixAutoCompleteField
            ))
            and (not label.has_attribute(
                self.dataLabelSuffixAutoCompleteField
            ))
        ):
            ariaAutocomplete = self._get_aria_autocomplete(autoCompleteField)
            if ariaAutocomplete is not None:
                if ariaAutocomplete == 'both':
                    if self.prefixAutoCompleteField != '':
                        prefixAutoCompleteFieldModified = re.sub(
                            '{{value}}',
                            self.textAutoCompleteValueBoth,
                            self.prefixAutoCompleteField
                        )
                    if self.suffixAutoCompleteField != '':
                        suffixAutoCompleteFieldModified = re.sub(
                            '{{value}}',
                            self.textAutoCompleteValueBoth,
                            self.suffixAutoCompleteField
                        )
                elif ariaAutocomplete == 'none':
                    if self.prefixAutoCompleteField != '':
                        prefixAutoCompleteFieldModified = re.sub(
                            '{{value}}',
                            self.textAutoCompleteValueNone,
                            self.prefixAutoCompleteField
                        )
                    if self.suffixAutoCompleteField != '':
                        suffixAutoCompleteFieldModified = re.sub(
                            '{{value}}',
                            self.textAutoCompleteValueNone,
                            self.suffixAutoCompleteField
                        )
                elif ariaAutocomplete == 'list':
                    if self.prefixAutoCompleteField != '':
                        prefixAutoCompleteFieldModified = re.sub(
                            '{{value}}',
                            self.textAutoCompleteValueList,
                            self.prefixAutoCompleteField
                        )
                    if self.suffixAutoCompleteField != '':
                        suffixAutoCompleteFieldModified = re.sub(
                            '{{value}}',
                            self.textAutoCompleteValueList,
                            self.suffixAutoCompleteField
                        )
                self._add_prefix_suffix(
                    label,
                    autoCompleteField,
                    prefixAutoCompleteFieldModified,
                    suffixAutoCompleteFieldModified,
                    self.dataLabelPrefixAutoCompleteField,
                    self.dataLabelSuffixAutoCompleteField
                )

    def _get_aria_autocomplete(self, field):
        """
        Returns the appropriate value for attribute aria-autocomplete of field.
        @param field: The field.
        @type field: L{hatemile.util.HTMLDOMElement}
        @return: The ARIA value of field.
        @rtype: str
        """

        tagName = field.get_tag_name()
        inputType = None
        if field.has_attribute('type'):
            inputType = field.get_attribute('type').lower()
        if (
            (tagName == 'TEXTAREA')
            or (
                (tagName == 'INPUT')
                and (not (
                    ('button' == inputType)
                    or ('submit' == inputType)
                    or ('reset' == inputType)
                    or ('image' == inputType)
                    or ('file' == inputType)
                    or ('checkbox' == inputType)
                    or ('radio' == inputType)
                    or ('hidden' == inputType)
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
            if 'on' == value:
                return 'both'
            elif (
                (field.has_attribute('list'))
                and (self.parser.find(
                    'datalist[id="' + field.get_attribute('list') + '"]'
                ).first_result() is not None)
            ):
                return 'list'
            elif 'off' == value:
                return 'none'
        return None

    def _get_labels(self, field):
        """
        Returns the labels of field.
        @param field: The field.
        @type field: L{hatemile.util.HTMLDOMElement}
        @return: The labels of field.
        @rtype: array.L{hatemile.util.HTMLDOMElement}
        """

        labels = None
        if field.has_attribute('id'):
            labels = self.parser.find(
                'label[for="' + field.get_attribute('id') + '"]'
            ).list_results()
        if (labels is None) or (len(labels) == 0):
            labels = self.parser.find(field).find_ancestors(
                'label'
            ).list_results()
        return labels

    def fix_required_field(self, requiredField):
        if requiredField.has_attribute('required'):
            requiredField.set_attribute('aria-required', 'true')

            labels = self._get_labels(requiredField)
            for label in labels:
                self._fix_label_required_field(label, requiredField)

    def fix_required_fields(self):
        requiredFields = self.parser.find('[required]').list_results()
        for requiredField in requiredFields:
            if not requiredField.has_attribute(self.dataIgnore):
                self.fix_required_field(requiredField)

    def fix_range_field(self, rangeField):
        if rangeField.has_attribute('min'):
            rangeField.set_attribute(
                'aria-valuemin',
                rangeField.get_attribute('min')
            )
        if rangeField.has_attribute('max'):
            rangeField.set_attribute(
                'aria-valuemax',
                rangeField.get_attribute('max')
            )
        labels = self._get_labels(rangeField)
        for label in labels:
            self._fix_label_range_field(label, rangeField)

    def fix_range_fields(self):
        rangeFields = self.parser.find('[min],[max]').list_results()
        for rangeField in rangeFields:
            if not rangeField.has_attribute(self.dataIgnore):
                self.fix_range_field(rangeField)

    def fix_autocomplete_field(self, autoCompleteField):
        ariaAutoComplete = self._get_aria_autocomplete(autoCompleteField)
        if ariaAutoComplete is not None:
            autoCompleteField.set_attribute(
                'aria-autocomplete',
                ariaAutoComplete
            )

            labels = self._get_labels(autoCompleteField)
            for label in labels:
                self._fix_label_autocomplete_field(label, autoCompleteField)

    def fix_autocomplete_fields(self):
        elements = self.parser.find(
            'input[autocomplete],textarea[autocomplete],'
            + 'form[autocomplete] input,form[autocomplete] textarea,'
            + '[list],[form]'
        ).list_results()
        for element in elements:
            if not element.has_attribute(self.dataIgnore):
                self.fix_autocomplete_field(element)

    def fix_label(self, label):
        if label.get_tag_name() == 'LABEL':
            if label.has_attribute('for'):
                field = self.parser.find(
                    '#' + label.get_attribute('for')
                ).first_result()
            else:
                field = self.parser.find(label).find_descendants(
                    'input,select,textarea'
                ).first_result()

                if field is not None:
                    CommonFunctions.generate_id(field, self.prefixId)
                    label.set_attribute('for', field.get_attribute('id'))
            if field is not None:
                if not field.has_attribute('aria-label'):
                    field.set_attribute(
                        'aria-label',
                        re.sub(
                            '[ \n\r\t]+',
                            ' ',
                            label.get_text_content().strip()
                        )
                    )

                self._fix_label_required_field(label, field)
                self._fix_label_range_field(label, field)
                self._fix_label_autocomplete_field(label, field)

                CommonFunctions.generate_id(label, self.prefixId)
                field.set_attribute(
                    'aria-labelledby',
                    CommonFunctions.increase_in_list(
                        field.get_attribute('aria-labelledby'),
                        label.get_attribute('id')
                    )
                )

    def fix_labels(self):
        labels = self.parser.find('label').list_results()
        for label in labels:
            if not label.has_attribute(self.dataIgnore):
                self.fix_label(label)
