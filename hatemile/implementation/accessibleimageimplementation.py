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
from hatemile.accessibleimage import AccessibleImage


class AccessibleImageImplementation(AccessibleImage):
    """
    The AccessibleImageImplementation class is official implementation of
    AccessibleImage interface.
    """

    def __init__(self, parser, configure):
        """
        Initializes a new object that manipulate the accessibility of the
        images of parser.
        @param parser: The HTML parser.
        @type parser: L{hatemile.util.HTMLDOMParser}
        @param configure: The configuration of HaTeMiLe.
        @type configure: L{hatemile.util.Configure}
        """

        self.parser = parser
        self.prefixId = configure.getParameter('prefix-generated-ids')
        self.classLongDescriptionLink = 'longdescription-link'
        self.dataLongDescriptionForImage = 'data-longdescriptionfor'
        self.dataIgnore = 'data-ignoreaccessibilityfix'
        self.prefixLongDescriptionLink = configure.getParameter('prefix-longdescription')
        self.suffixLongDescriptionLink = configure.getParameter('suffix-longdescription')

    def fixLongDescription(self, element):
        if element.hasAttribute('longdesc'):
            CommonFunctions.generateId(element, self.prefixId)
            idElement = element.getAttribute('id')
            if self.parser.find('[' + self.dataLongDescriptionForImage + '="' + idElement + '"]').firstResult() is None:
                if element.hasAttribute('alt'):
                    text = self.prefixLongDescriptionLink + ' ' + element.getAttribute('alt') + ' ' + self.suffixLongDescriptionLink
                else:
                    text = self.prefixLongDescriptionLink + ' ' + self.suffixLongDescriptionLink
                anchor = self.parser.createElement('a')
                anchor.setAttribute('href', element.getAttribute('longdesc'))
                anchor.setAttribute('target', '_blank')
                anchor.setAttribute(self.dataLongDescriptionForImage, idElement)
                anchor.setAttribute('class', self.classLongDescriptionLink)
                anchor.appendText(text.strip())
                element.insertAfter(anchor)

    def fixLongDescriptions(self):
        elements = self.parser.find('[longdesc]').listResults()
        for element in elements:
            if not element.hasAttribute(self.dataIgnore):
                self.fixLongDescription(element)
