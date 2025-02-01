# Steps I followed

1. First, extract the translatable strings:
```bash
xgettext -o locale/messages.pot scene.py
```

```txt
Directory structure:
project/
├── locale/
│   ├── ar/
│   │   └── LC_MESSAGES/
│   │       ├── base.mo
│   │       └── base.po
│   └── en/
│       └── LC_MESSAGES/
│           ├── base.mo
│           └── base.po
├── main.py
└── messages.pot
```

2. Create the directory structure for each language:
```bash
mkdir -p locale/en/LC_MESSAGES
mkdir -p locale/ar/LC_MESSAGES
```

3. Initialize the PO files for each language:
```bash
msginit -i locale/base.pot -o locale/en/LC_MESSAGES/base.po -l en
msginit -i locale/base.pot -o locale/ar/LC_MESSAGES/base.po -l ar
```

4. Edit the PO files with your translations 

5. Compile the PO files to MO files:
```bash
msgfmt locale/en/LC_MESSAGES/base.po -o locale/en/LC_MESSAGES/base.mo
msgfmt locale/ar/LC_MESSAGES/base.po -o locale/ar/LC_MESSAGES/base.mo
```

To switch languages in your code, just change the language parameter in `setup_i18n()`:
```python
def setup_i18n(language):
    # Set up the translation
    localedir = os.path.join(os.path.dirname(__file__), 'locale')
    translation = gettext.translation('base', localedir, languages=[language], fallback=True)
    translation.install()
    return translation.gettext

_ = setup_i18n('en')  # For English
_ = setup_i18n('ar')  # For Arabic
```
