from prompt_toolkit import PromptSession

# Create prompt object.
session = PromptSession()

# Do multiple input calls.
text1 = session.prompt('Input text1:')
text2 = session.prompt('Input text2:')

print(f'text1: {text1}, text2: {text2}')
