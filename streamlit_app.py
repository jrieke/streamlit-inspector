import streamlit as st
from streamlit_inspect import inspect


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


"""
# 🕵️‍♂️ streamlit-inspect

Imagine you installed a package to create balloons:

```python
from somepackage import create_balloon

b = create_balloon()
```

You can quickly figure out that `b` is of type `Balloon`. 
But what can you do with it? This is where [streamlit-inspect](https://github.com/jrieke/streamlit-inspect) 
comes in!

Just write:

```python
from streamlit_inspect import inspect

inspect(b)
```
    
and you get an interactive preview of the object:

"""
b = Balloon("red")
inspect(b)


"""
---

Another example:
"""
with st.echo():
    inspect(["foo", "bar"])
