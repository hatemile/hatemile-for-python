HaTeMiLe for Python
===================

HaTeMiLe (HTML Accessible) is a library that can convert a HTML code in a HTML code more accessible.

## Accessibility solutions

* [Associate HTML elements](https://github.com/hatemile/hatemile-for-python/wiki/Associate-HTML-elements);
* [Provide a polyfill to CSS Speech and CSS Aural properties](https://github.com/hatemile/hatemile-for-python/wiki/Provide-a-polyfill-to-CSS-Speech-and-CSS-Aural-properties);
* [Display inacessible informations of page](https://github.com/hatemile/hatemile-for-python/wiki/Display-inacessible-informations-of-page);
* [Enable all functionality of page available from a keyboard](https://github.com/hatemile/hatemile-for-python/wiki/Enable-all-functionality-of-page-available-from-a-keyboard);
* [Improve the acessibility of forms](https://github.com/hatemile/hatemile-for-python/wiki/Improve-the-acessibility-of-forms);
* [Provide accessibility resources to navigate](https://github.com/hatemile/hatemile-for-python/wiki/Provide-accessibility-resources-to-navigate).

## Documentation

To generate the full API documentation of HaTeMiLe of Python:

1. [Install, create and activate a virtualenv](https://packaging.python.org/guides/installing-using-pip-and-virtualenv/);
2. [Install dependencies](https://packaging.python.org/guides/installing-using-pip-and-virtualenv/#using-requirements-files);
3. [Execute the API docs of sphinx in `docs` directory](https://samnicholls.net/2016/06/15/how-to-sphinx-readthedocs/);
    ```bash
    sphinx-apidoc -e -f -o _modules/ ../hatemile
    make html
    ```
4. Open the `docs/_build/html/index.html` with an internet browser.

## Import the library to your project

To install the HaTeMiLe for Python library, execute these command in terminal:

```bash
pip install hatemile
```

## Usage

Import all needed classes:

```python
from hatemile.implementation.assoc import AccessibleAssociationImplementation
from hatemile.implementation.css import AccessibleCSSImplementation
from hatemile.implementation.display import AccessibleDisplayImplementation
from hatemile.implementation.event import AccessibleEventImplementation
from hatemile.implementation.form import AccessibleFormImplementation
from hatemile.implementation.navig import AccessibleNavigationImplementation
from hatemile.util.configure import Configure
from hatemile.util.css.tinycss.tinycssparser import TinyCSSParser
from hatemile.util.html.bs.bshtmldomparser import BeautifulSoupHTMLDOMParser
```
Instanciate the configuration, the parsers and solution classes and execute them:

```python    
configure = Configure()

parser = BeautifulSoupHTMLDOMParser(html_code)
css_parser = TinyCSSParser(parser, current_url)

event = AccessibleEventImplementation(parser)
css = AccessibleCSSImplementation(parser, css_parser, configure)
form = AccessibleFormImplementation(parser)
navigation = AccessibleNavigationImplementation(parser, configure)
association = AccessibleAssociationImplementation(parser)
display = AccessibleDisplayImplementation(parser, configure)

event.make_accessible_all_drag_and_drop_events()
event.make_accessible_all_click_events()
event.make_accessible_all_hover_events()

form.mark_all_required_fields()
form.mark_all_range_fields()
form.mark_all_autocomplete_fields()
form.mark_all_invalid_fields()

navigation.provide_navigation_by_all_headings()
navigation.provide_navigation_by_all_skippers()
navigation.provide_navigation_to_all_long_descriptions()

association.associate_all_data_cells_with_header_cells()
association.associate_all_labels_with_fields()

css.provide_all_speak_properties()

display.display_all_shortcuts()
display.display_all_roles()
display.display_all_cell_headers()
display.display_all_waiaria_states()
display.display_all_links_attributes()
display.display_all_titles()
display.display_all_languages()
display.display_all_alternative_text_images()

navigation.provide_navigation_by_all_skippers()
display.display_all_shortcuts()

print(parser.get_html())
```

## Contributing

If you want contribute with HaTeMiLe for Python, read [contributing guidelines](https://github.com/hatemile/hatemile-for-python/blob/master/CONTRIBUTING.md).

## See also
* [HaTeMiLe for CSS](https://github.com/hatemile/hatemile-for-css)
* [HaTeMiLe for JavaScript](https://github.com/hatemile/hatemile-for-javascript)
* [HaTeMiLe for Java](https://github.com/hatemile/hatemile-for-java)
* [HaTeMiLe for PHP](https://github.com/hatemile/hatemile-for-php)
* [HaTeMiLe for Ruby](https://github.com/hatemile/hatemile-for-ruby)
