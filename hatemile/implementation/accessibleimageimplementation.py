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
        self.prefixId = configure.get_parameter('prefix-generated-ids')
        self.classLongDescriptionLink = 'longdescription-link'
        self.dataLongDescriptionForImage = 'data-longdescriptionfor'
        self.dataIgnore = 'data-ignoreaccessibilityfix'
        self.prefixLongDescriptionLink = configure.get_parameter(
            'prefix-longdescription'
        )
        self.suffixLongDescriptionLink = configure.get_parameter(
            'suffix-longdescription'
        )

    def fix_long_description(self, element):
        if element.has_attribute('longdesc'):
            CommonFunctions.generate_id(element, self.prefixId)
            idElement = element.get_attribute('id')
            if self.parser.find(
                '['
                + self.dataLongDescriptionForImage
                + '="'
                + idElement
                + '"]'
            ).first_result() is None:
                if element.has_attribute('alt'):
                    text = (
                        self.prefixLongDescriptionLink
                        + ' '
                        + element.get_attribute('alt')
                        + ' '
                        + self.suffixLongDescriptionLink
                    )
                else:
                    text = (
                        self.prefixLongDescriptionLink
                        + ' '
                        + self.suffixLongDescriptionLink
                    )
                anchor = self.parser.create_element('a')
                anchor.set_attribute('href', element.get_attribute('longdesc'))
                anchor.set_attribute('target', '_blank')
                anchor.set_attribute(
                    self.dataLongDescriptionForImage,
                    idElement
                )
                anchor.set_attribute('class', self.classLongDescriptionLink)
                anchor.append_text(text.strip())
                element.insert_after(anchor)

    def fix_long_descriptions(self):
        elements = self.parser.find('[longdesc]').list_results()
        for element in elements:
            if not element.has_attribute(self.dataIgnore):
                self.fix_long_description(element)
