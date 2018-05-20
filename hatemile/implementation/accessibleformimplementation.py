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
        self.prefixId = configure.getParameter('prefix-generated-ids')
        self.prefixRequiredField = configure.getParameter('prefix-required-field')
        self.suffixRequiredField = configure.getParameter('suffix-required-field')
        self.prefixRangeMinField = configure.getParameter('prefix-range-min-field')
        self.suffixRangeMinField = configure.getParameter('suffix-range-min-field')
        self.prefixRangeMaxField = configure.getParameter('prefix-range-max-field')
        self.suffixRangeMaxField = configure.getParameter('suffix-range-max-field')
        self.prefixAutoCompleteField = configure.getParameter('prefix-autocomplete-field')
        self.suffixAutoCompleteField = configure.getParameter('suffix-autocomplete-field')
        self.textAutoCompleteValueBoth = configure.getParameter('text-autocomplete-value-both')
        self.textAutoCompleteValueList = configure.getParameter('text-autocomplete-value-list')
        self.textAutoCompleteValueInline = configure.getParameter('text-autocomplete-value-inline')
        self.textAutoCompleteValueNone = configure.getParameter('text-autocomplete-value-none')

    def _addPrefixSuffix(self, label, field, prefix, suffix, dataPrefix, dataSuffix):
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

        contentLabel = field.getAttribute('aria-label')
        if prefix != '':
            label.setAttribute(dataPrefix, prefix)
            if prefix not in contentLabel:
                contentLabel = prefix + ' ' + contentLabel
        if suffix != '':
            label.setAttribute(dataSuffix, suffix)
            if suffix not in contentLabel:
                contentLabel = contentLabel + ' ' + suffix
        field.setAttribute('aria-label', contentLabel) 

    def _fixLabelRequiredField(self, label, requiredField):
        """
        Display in label the information if the field is required.
        @param label: The label.
        @type label: L{hatemile.util.HTMLDOMElement}
        @param requiredField: The required field.
        @type requiredField: L{hatemile.util.HTMLDOMElement}
        """

        if ((requiredField.hasAttribute('required')) or ((requiredField.hasAttribute('aria-required')) and (requiredField.getAttribute('aria-required').lower() == 'true'))) and (requiredField.hasAttribute('aria-label')) and (not label.hasAttribute(self.dataLabelPrefixRequiredField)) and (not label.hasAttribute(self.dataLabelSuffixRequiredField)):
            self._addPrefixSuffix(label, requiredField, self.prefixRequiredField, self.suffixRequiredField, self.dataLabelPrefixRequiredField, self.dataLabelSuffixRequiredField)

    def _fixLabelRangeField(self, label, rangeField):
        """
        Display in label the information of range of field.
        @param label: The label.
        @type label: L{hatemile.util.HTMLDOMElement}
        @param rangeField: The range field.
        @type rangeField: L{hatemile.util.HTMLDOMElement}
        """

        if rangeField.hasAttribute('aria-label'):
            if (rangeField.hasAttribute('min') or rangeField.hasAttribute('aria-valuemin')) and (not label.hasAttribute(self.dataLabelPrefixRangeMinField)) and (not label.hasAttribute(self.dataLabelSuffixRangeMinField)):
                if rangeField.hasAttribute('min'):
                    value = rangeField.getAttribute('min')
                else:
                    value = rangeField.getAttribute('aria-valuemin')
                self._addPrefixSuffix(label, rangeField, re.sub('{{value}}', value, self.prefixRangeMinField)
                        , re.sub('{{value}}', value, self.suffixRangeMinField)
                        , self.dataLabelPrefixRangeMinField, self.dataLabelSuffixRangeMinField)
            if (rangeField.hasAttribute('max') or rangeField.hasAttribute('aria-valuemax')) and (not label.hasAttribute(self.dataLabelPrefixRangeMaxField)) and (not label.hasAttribute(self.dataLabelSuffixRangeMaxField)):
                if rangeField.hasAttribute('max'):
                    value = rangeField.getAttribute('max')
                else:
                    value = rangeField.getAttribute('aria-valuemax')
                self._addPrefixSuffix(label, rangeField, re.sub('{{value}}', value, self.prefixRangeMaxField)
                        , re.sub('{{value}}', value, self.suffixRangeMaxField)
                        , self.dataLabelPrefixRangeMaxField, self.dataLabelSuffixRangeMaxField)

    def _fixLabelAutoCompleteField(self, label, autoCompleteField):
        """
        Display in label the information if the field has autocomplete.
        @param label: The label.
        @type label: L{hatemile.util.HTMLDOMElement}
        @param autoCompleteField: The autocomplete field.
        @type autoCompleteField: L{hatemile.util.HTMLDOMElement}
        """

        prefixAutoCompleteFieldModified = ''
        suffixAutoCompleteFieldModified = ''
        if (autoCompleteField.hasAttribute('aria-label')) and (not label.hasAttribute(self.dataLabelPrefixAutoCompleteField)) and (not label.hasAttribute(self.dataLabelSuffixAutoCompleteField)):
            ariaAutocomplete = self._getARIAAutoComplete(autoCompleteField)
            if ariaAutocomplete is not None:
                if ariaAutocomplete == 'both':
                    if self.prefixAutoCompleteField != '':
                        prefixAutoCompleteFieldModified = re.sub('{{value}}', self.textAutoCompleteValueBoth, self.prefixAutoCompleteField)
                    if self.suffixAutoCompleteField != '':
                        suffixAutoCompleteFieldModified = re.sub('{{value}}', self.textAutoCompleteValueBoth, self.suffixAutoCompleteField)
                elif ariaAutocomplete == 'none':
                    if self.prefixAutoCompleteField != '':
                        prefixAutoCompleteFieldModified = re.sub('{{value}}', self.textAutoCompleteValueNone, self.prefixAutoCompleteField)
                    if self.suffixAutoCompleteField != '':
                        suffixAutoCompleteFieldModified = re.sub('{{value}}', self.textAutoCompleteValueNone, self.suffixAutoCompleteField)
                elif ariaAutocomplete == 'list':
                    if self.prefixAutoCompleteField != '':
                        prefixAutoCompleteFieldModified = re.sub('{{value}}', self.textAutoCompleteValueList, self.prefixAutoCompleteField)
                    if self.suffixAutoCompleteField != '':
                        suffixAutoCompleteFieldModified = re.sub('{{value}}', self.textAutoCompleteValueList, self.suffixAutoCompleteField)
                self._addPrefixSuffix(label, autoCompleteField, prefixAutoCompleteFieldModified
                        , suffixAutoCompleteFieldModified, self.dataLabelPrefixAutoCompleteField
                        , self.dataLabelSuffixAutoCompleteField)

    def _getARIAAutoComplete(self, field):
        """
        Returns the appropriate value for attribute aria-autocomplete of field.
        @param field: The field.
        @type field: L{hatemile.util.HTMLDOMElement}
        @return: The ARIA value of field.
        @rtype: str
        """

        tagName = field.getTagName()
        inputType = None
        if field.hasAttribute('type'):
            inputType = field.getAttribute('type').lower()
        if (tagName == 'TEXTAREA') or ((tagName == 'INPUT') and (not (('button' == inputType) or ('submit' == inputType) or ('reset' == inputType) or ('image' == inputType) or ('file' == inputType) or ('checkbox' == inputType) or ('radio' == inputType) or ('hidden' == inputType)))):
            value = None
            if field.hasAttribute('autocomplete'):
                value = field.getAttribute('autocomplete').lower()
            else:
                form = self.parser.find(field).findAncestors('form').firstResult()
                if (form is None) and (field.hasAttribute('form')):
                    form = self.parser.find('#' + field.getAttribute('form')).firstResult()
                if (form is not None) and (form.hasAttribute('autocomplete')):
                    value = form.getAttribute('autocomplete').lower()
            if 'on' == value:
                return 'both'
            elif (field.hasAttribute('list')) and (self.parser.find('datalist[id="' + field.getAttribute('list') + '"]').firstResult() is not None):
                return 'list'
            elif 'off' == value:
                return 'none'
        return None

    def _getLabels(self, field):
        """
        Returns the labels of field.
        @param field: The field.
        @type field: L{hatemile.util.HTMLDOMElement}
        @return: The labels of field.
        @rtype: array.L{hatemile.util.HTMLDOMElement}
        """

        labels = None
        if field.hasAttribute('id'):
            labels = self.parser.find('label[for="' + field.getAttribute('id') + '"]').listResults()
        if (labels is None) or (len(labels) == 0):
            labels = self.parser.find(field).findAncestors('label').listResults()
        return labels

    def fixRequiredField(self, requiredField):
        if requiredField.hasAttribute('required'):
            requiredField.setAttribute('aria-required', 'true')

            labels = self._getLabels(requiredField)
            for label in labels:
                self._fixLabelRequiredField(label, requiredField)

    def fixRequiredFields(self):
        requiredFields = self.parser.find('[required]').listResults()
        for requiredField in requiredFields:
            if not requiredField.hasAttribute(self.dataIgnore):
                self.fixRequiredField(requiredField)

    def fixRangeField(self, rangeField):
        if rangeField.hasAttribute('min'):
            rangeField.setAttribute('aria-valuemin', rangeField.getAttribute('min'))
        if rangeField.hasAttribute('max'):
            rangeField.setAttribute('aria-valuemax', rangeField.getAttribute('max'))
        labels = self._getLabels(rangeField)
        for label in labels:
            self._fixLabelRangeField(label, rangeField)

    def fixRangeFields(self):
        rangeFields = self.parser.find('[min],[max]').listResults()
        for rangeField in rangeFields:
            if not rangeField.hasAttribute(self.dataIgnore):
                self.fixRangeField(rangeField)

    def fixAutoCompleteField(self, autoCompleteField):
        ariaAutoComplete = self._getARIAAutoComplete(autoCompleteField)
        if ariaAutoComplete is not None:
            autoCompleteField.setAttribute('aria-autocomplete', ariaAutoComplete)

            labels = self._getLabels(autoCompleteField)
            for label in labels:
                self._fixLabelAutoCompleteField(label, autoCompleteField)

    def fixAutoCompleteFields(self):
        elements = self.parser.find('input[autocomplete],textarea[autocomplete],form[autocomplete] input,form[autocomplete] textarea,[list],[form]').listResults()
        for element in elements:
            if not element.hasAttribute(self.dataIgnore):
                self.fixAutoCompleteField(element)

    def fixLabel(self, label):
        if label.getTagName() == 'LABEL':
            if label.hasAttribute('for'):
                field = self.parser.find('#' + label.getAttribute('for')).firstResult()
            else:
                field = self.parser.find(label).findDescendants('input,select,textarea').firstResult()

                if field is not None:
                    CommonFunctions.generateId(field, self.prefixId)
                    label.setAttribute('for', field.getAttribute('id'))
            if field is not None:
                if not field.hasAttribute('aria-label'):
                    field.setAttribute('aria-label', re.sub('[ \n\r\t]+', ' ', label.getTextContent().strip()))

                self._fixLabelRequiredField(label, field)
                self._fixLabelRangeField(label, field)
                self._fixLabelAutoCompleteField(label, field)

                CommonFunctions.generateId(label, self.prefixId)
                field.setAttribute('aria-labelledby', CommonFunctions.increaseInList(field.getAttribute('aria-labelledby'), label.getAttribute('id')))

    def fixLabels(self):
        labels = self.parser.find('label').listResults()
        for label in labels:
            if not label.hasAttribute(self.dataIgnore):
                self.fixLabel(label)
