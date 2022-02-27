from inspect import (
    cleandoc,
    getdoc,
    isclass,
    ismodule,
    signature,
)

import streamlit as st
import validators
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer


def wrap_expander(summary, details, indent=False):
    # Need to wrap details in div here so it appears on new line. We set summary to
    # display: inline-block above to reduce the hover surface to just the text. But this
    # unfortunately makes the details appear right behind the summary and not on a new
    # line.
    padding = "padding-left: 1.55rem;" if indent else ""
    return f'<details><summary>{summary}</summary><div style="{padding}">{details}<div></details>'


def shorten(s, length=300):
    s = s.replace("\n", " ")
    return s[:length] + "..." if len(s) > length else s


# Set up code formatter from pygments and write it's CSS to the app.
lexer = PythonLexer()
formatter = HtmlFormatter(style="autumn")
st.markdown(
    "<style>" + formatter.get_style_defs(".highlight") + "</style>",
    unsafe_allow_html=True,
)

# Write other CSS to the app.
st.markdown(
    """
    <style>
    
    /* Additional stuff for the formatter */
    .highlight {
        display: inline;
    }
    
    .highlight .stCodeBlock {
        margin: 0;
        display: inline;
    }
    
    .highlight a {
        color: inherit;
    }
    
    /* Basic elements */
    .gray-text {
        color: #84858c;
    }
    
    /* Hacky expander via details/summary tags. Used to show multiple paragraphs from docstrings. */
    details > summary {
        list-style: none;
        display: inline-block;
    }
    details > summary:hover {
        color: #ff4b4b !important;
    }
    details > summary:hover span {
        color: #ff4b4b !important;
    }
    summary::marker {
        display: none;
    }
    summary::after {
        content: " +";
    }
    details[open] summary:after {
        content: " -";
    }
    
    </style>
    """,
    unsafe_allow_html=True,
)


def _code_format(code):
    """Applies code formatting via pygments to a string."""
    return highlight(code, lexer, formatter).strip()


def _prettify_value(value):
    """Formats the value of an object and applies some nice tricks."""
    s = shorten(str(value))

    # Add quotation marks to strings.
    if '"' in s and "'" in s:
        quote_char = '"""'
    elif '"' in s:
        quote_char = "'"
    else:
        quote_char = '"'
    if isinstance(value, str):
        if validators.url(value):
            # Turn URLs into links.
            new_s = _code_format(f"{quote_char}{s}{quote_char}")
            s = new_s.replace(s, f'<a href="{value}">{s}</a>')
        else:
            s = _code_format(f"{quote_char}{s}{quote_char}")
    else:
        s = _code_format(s)
    return s


def _split_format_docstring(doc: str) -> str:
    """
    Splits and formats a docstring.

    Returns a tuple of the first paragraph and all following paragraphs.
    """
    first, _, following = doc.partition("\n\n")
    first = cleandoc(first).strip()
    following = cleandoc(following).strip()
    return first, following


def _get_signature(name, obj):
    """Returns the signature of a callable (method or class)."""
    try:
        _signature = str(signature(obj))
    except ValueError:
        _signature = "(...)"
    except TypeError:
        return None

    qualname = getattr(obj, "__name__", name)

    # If obj is a module, there may be classes (which are callable) to display
    if isclass(obj):
        prefix = "class"
    else:
        prefix = "def"

    return prefix + " " + qualname + _signature


class KeyValueTable:
    """
    Table to align key-value pairs on an = sign in the middle.

    E.g.:

      abc = 123
    abcde = 12345
        a = 1234567
       ab = 12

    Left side is the key, right side is the value.

    """

    def __init__(self):
        self.table_rows = []

    def add_row(self, key, value):
        self.table_rows.append(
            f"<tr><td align='right' style='white-space: nowrap;'>{key}</td><td>&nbsp;&nbsp;=&nbsp;&nbsp;</td><td align='left' style='text-overflow: ellipsis;'>{value}</td></tr>"
        )

    def __len__(self):
        return len(self.table_rows)

    def __str__(self):
        if len(self) == 0:
            return ""
        # Note: This needs to be without indentation! Otherwise it gets interpreted
        # as a code block.
        return f"""
<style>
.keyvaluetable {{
    word-break: break-all;
}}
.keyvaluetable tr, td {{
    border: none !important;
    padding: 0 !important;
}}
.keyvaluetable td {{
    vertical-align: baseline;
}}
</style>
<table class="keyvaluetable" cellspacing="0" cellpadding="0">
    {"".join(self.table_rows)}
</table>
        """


def inspect(obj):
    """Writes an interactive summary of `obj` to a Streamlit app.

    Args:
        obj: Any object.
    """

    # Divider that's placed between different sections (e.g. attributes and methods).
    divider = '<hr style="margin: 1rem -1rem">'

    # Add a surrounding div with border.
    s = '<div style="border: 1px solid #d6d6d8; border-radius: 0.25rem; padding: 1rem; margin-bottom: 1rem;">'

    # Add the string representation of the object itself.
    s += _code_format(repr(obj)) + divider

    # Get the type of the object.
    if isclass(obj) or callable(obj) or ismodule(obj):
        title = str(obj)
    else:
        title = str(type(obj).__name__)

    # Get the docstring of the object. Add the title + object to a new section.
    docstring = getdoc(obj)
    if docstring is not None:
        first, following = _split_format_docstring(docstring)
        if first and following:
            # If the docstring has > 1 paragraph, show the paragraphs beyond the 1st one
            # in an HTML expander.
            s += wrap_expander(
                f'<b>{title}:</b> <span class="gray-text">{first}</span>',
                f'<span class="gray-text">{following}</span>',
            )
        elif first:
            s += f'<b>{title}:</b> <span class="gray-text">{first}</span>'
        else:
            s += f"<b>{title}</b>"
    else:
        s += f"<b>{title}</b>"

    s += divider

    # TODO: Thhis is code copied from rich. Check out if I still want to use it.
    # keys = dir(obj)
    # total_items = len(keys)
    # # TODO: Would be cool if dunder and private weren't keywords, but private/dunder
    # # items were just shown within an expander, which is collapsed by default.
    # if not dunder:
    #     keys = [key for key in keys if not key.startswith("__")]
    # if not private:
    #     keys = [key for key in keys if not key.startswith("_")]
    # not_shown_count = total_items - len(keys)

    # def sort_items(item: Tuple[str, Any]) -> Tuple[bool, str]:
    #     key, (_error, value) = item
    #     return (callable(value), key.strip("_").lower())

    # def safe_getattr(attr_name: str) -> Tuple[Any, Any]:
    #     """Get attribute or any exception."""
    #     try:
    #         return (None, getattr(obj, attr_name))
    #     except Exception as error:
    #         return (error, None)
    # items = [(key, safe_getattr(key)) for key in keys]
    # # TODO: Should this even be a parameter? Can't think of situations where you wouldn't
    # # want to sort.
    # if sort:
    #     items.sort(key=sort_items)

    # Get all attributes from the object and put their names and values into a
    # KeyValueTable. Do not write the table to the app yet.
    attr_table = KeyValueTable()
    for attr in dir(obj):
        try:
            value = getattr(obj, attr)
        except:
            value = "Couldn't parse this attribute's value 😔"  # TODO: Make this nicer.
        if not attr.startswith("_") and not callable(value):
            if value is None:
                type_str = ""
            else:
                type_str = f'<span style="color: #01a9aa">{type(value).__name__}</span>'
            attr_table.add_row(
                f"{attr}{': ' if type_str else ''}{type_str}",
                _prettify_value(value),
            )
    attr_text = str(attr_table)

    # Get all methods from the object and put their signatures + docstrings into a
    # string. Do not write the string to the app yet.
    methods_text = ""
    for attr in dir(obj):
        if not attr.startswith("_") and callable(getattr(obj, attr)):
            value = getattr(obj, attr)
            value_text = _get_signature(attr, value)

            # Get the docstring of the method.
            docstring = getdoc(value)
            if docstring is not None:
                first, following = _split_format_docstring(docstring)
                if first and following:
                    # If the docstring has > 1 paragraph, show the paragraphs beyond the
                    # 1st one in an expander.
                    value_text = _code_format(value_text + ":")
                    value_text += f'<span style="color: #84858c">{first}</span>'
                    value_text = wrap_expander(
                        value_text,
                        f'<span style="color: #84858c">{following}</span>',
                        indent=True,
                    )
                elif first:
                    value_text = _code_format(value_text + ":")
                    value_text += f'<span style="color: #84858c">{first}</span>'
                else:
                    value_text = _code_format(value_text)
            else:
                value_text = _code_format(value_text)

            methods_text += "<div>" + value_text + "</div>"

    # Write the attribute and method strings to the app, and add a divider in between if
    # needed.
    s += attr_text
    if attr_text and methods_text:
        s += divider
    s += methods_text

    # Close the surrounding div that holds the border.
    s += "</div>"

    # Write everything to the app.
    st.write(s, unsafe_allow_html=True)
