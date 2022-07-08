from stringcolor import *

# a few examples without background colors.
# for color names see CLI usage below.
print(cs("here we go", "orchid"))
print(cs("away to space!", "DeepPink3"))
print(cs("final fantasy", "#ffff87"))
print()

# bold and underline also available.
print(cs("purple number 4, bold", "purple4").bold())
print(cs("blue, underlined", "blue").underline())
print(bold("bold AND underlined!").underline().cs("red", "gold"))
print(underline("the bottom line."))
print()

# yellow text with a red background.
# color names, hex values, and ansi numbers will work.
print(cs("warning!", "yellow", "#ff0000"))
print()

# concat
print(cs("wild", "pink")+" stuff")
print("nothing "+cs("something", "DarkViolet2", "lightgrey6"))
print()

# use any working rgb or hex values.
# it will find the closest color available.
print(cs("this will show up red", "#ff0009"))
print(cs("so will this", "rgb(254, 0, 1)"))
print()

# use with format and f-strings
print(f"this is a test {cs('to check formatting with f-strings', 'yellow', 'grey').bold().underline()}")
print("this is a test {}".format(cs('to check the format function', 'purple', 'lightgrey11').bold().underline()))
