
"""
See Also:
 * How can I detect if a file is binary (non-text) in Python?
   - https://stackoverflow.com/questions/898669/how-can-i-detect-if-a-file-is-binary-non-text-in-python
"""

def is_binary(filepath):
    with open(filepath, 'rb') as f:
        if b'\0' in f.read(4096):
            return True
        else:
            return False
