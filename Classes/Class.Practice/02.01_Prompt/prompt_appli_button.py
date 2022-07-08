#!/usr/bin/env python
"""
A simple example of a few buttons and click handlers.
"""
from prompt_toolkit.application import Application
from prompt_toolkit.application.current import get_app
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.bindings.focus import focus_next, focus_previous
from prompt_toolkit.layout import HSplit, Layout, VSplit
from prompt_toolkit.widgets import Box, Button, Frame, Label, TextArea


# Event handlers for all the buttons.
def button1_clicked():
    text_area.text = "Button 1 clicked"

def button2_clicked():
    text_area.text = "Button 2 clicked"

def button3_clicked():
    text_area.text = "Button 3 clicked"

def exit_clicked():
    get_app().exit()

button1 = Button("Button 1", handler=button1_clicked)
button2 = Button("Button 2", handler=button2_clicked)
button3 = Button("Button 3", handler=button3_clicked)
button4 = Button("Exit", handler=exit_clicked)
text_area = TextArea(focusable=True)

root_container = Box(
    HSplit(
        [
            Label(text="Press `Tab` to move the focus."),
            VSplit(
                [
                    Box(
                        body=HSplit([button1, button2, button3, button4],
                                    padding=1),
                        padding=1,
                    ),
                    Box(body=Frame(text_area), padding=1),
                ]
            ),
        ]
    ),
)

layout = Layout(container=root_container, focused_element=button1)

kb = KeyBindings()
kb.add("tab")(focus_next)
kb.add("s-tab")(focus_previous)

application = Application(layout=layout, key_bindings=kb, full_screen=True)


def main():
    application.run()

if __name__ == "__main__":
    main()
