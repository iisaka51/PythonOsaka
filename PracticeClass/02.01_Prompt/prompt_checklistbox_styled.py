from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.shortcuts import checkboxlist_dialog, message_dialog
from prompt_toolkit.styles import Style

tui = checkboxlist_dialog(
    title="CheckboxList dialog",
    text="What would you like in your breakfast ?",
    values=[
        ("eggs", "Eggs"),
        ("bacon", HTML("<blue>Bacon</blue>")),
        ("croissants", "20 Croissants"),
        ("daily", "The breakfast of the day"),
    ],
    style=Style.from_dict(
        {
            "dialog": "bg:#cdbbb3",
            "button": "bg:#bf99a4",
            "checkbox": "#e8612c",
            "dialog.body": "bg:#a9cfd0",
            "dialog shadow": "bg:#c98982",
            "frame.label": "#fcaca3",
            "dialog.body label": "#fd8bb6",
        }
    ),
)

result = tui.run()
print(result)
selected_item = ','.join(result)
print(f'You selected: {selected_item}')
