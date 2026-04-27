"""Internationalization module for Betcon"""
import locale
import os
import builtins
import gettext

# Set locale
try:
    locale.setlocale(locale.LC_ALL, '')
    lang = locale.getlocale()[0]
except:
    lang = None

# Also check environment variables
if not lang or lang == 'C':
    lang = os.environ.get('LANGUAGE') or os.environ.get('LANG') or os.environ.get('LC_ALL')
    if lang:
        # Remove .UTF-8 suffix if present
        lang = lang.split('.')[0]

# Get language code
if lang and lang != 'C':
    # Extract base language (es_ES -> es)
    lang_code = lang.split('_')[0] if '_' in lang else lang
else:
    lang_code = 'es'  # Default to Spanish

# Get the base directory (betcon/src/lib -> betcon)
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
locale_dir = os.path.join(base_dir, "lang", "mo")

# Try to load translations
try:
    translation = gettext.translation('betcon', locale_dir, languages=[lang_code], fallback=True)
    _ = translation.gettext
except Exception as e:
    # Fallback to English
    _ = lambda s: s

# Make _ available globally
builtins._ = _
