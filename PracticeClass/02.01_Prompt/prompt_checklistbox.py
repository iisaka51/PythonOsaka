from prompt_toolkit.shortcuts import checkboxlist_dialog, message_dialog
from prompt_toolkit.styles import Style

result = checkboxlist_dialog(
    title="CheckboxList dialog",
    text="What would you like in your breakfast ?",
    values=[
        ("eggs", "Eggs"),
        ("bacon", "Bacon"),
        ("croissants", "20 Croissants"),
        ("daily", "The breakfast of the day"),
    ],
).run()

selected_item = ','.join(result)
print(f'You selected: {selected_item}')
