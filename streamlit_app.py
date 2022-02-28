import streamlit as st
from streamlit_inspector import inspect


class Balloon:
    """This class represents a balloon 🎈

    Balloons are round objects made of rubber. They can be inflated and deflated.
    You can even make them float! Kids love balloons. Adults love balloons.
    Everyone loves balloons!!!

    Args:
        color (str): The color of the balloon.
        diameter (int): The size of the balloon.
    """

    def __init__(self, color, diameter=30):
        self.color = color
        self.diameter = diameter

    def __repr__(self):
        return f"Balloon(color='{self.color}', diameter={self.diameter})"

    def inflate(self, medium: str = "air"):
        """Inflates the balloon.

        Args:
            medium (str): The medium the balloon is inflated with.
        """
        pass

    def paint(self, new_color: str):
        """Paints the balloon in a new color.

        Args:
            new_color (str): The new color of the balloon.
        """
        pass


st.set_page_config("Demo for streamlit-inspect", "🕵️‍♂️")
"""
# Demo for [streamlit-inspect](https://github.com/jrieke/streamlit-inspect) 🕵️‍♂️

Imagine you're writing a Streamlit app and using a package to create balloons:

```python
from somepackage import create_balloon

b = create_balloon()
```

But what is `b`? That's where [streamlit-inspector](https://github.com/jrieke/streamlit-inspector) 
comes in:

```python
from streamlit_inspector import inspect

inspect(b)
```
    
This gives you an interactive description of `b`, including its type, attributes, 
and methods:

"""
b = Balloon("red")
inspect(b)


"""
---

Another example:
"""
with st.echo():
    inspect(["foo", "bar"])
