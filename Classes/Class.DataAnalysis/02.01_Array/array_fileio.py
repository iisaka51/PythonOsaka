import array
import binascii
import tempfile

data = array.array('i', range(5))
print(f'Original data:{data}')

output = tempfile.NamedTemporaryFile()
data.tofile(output.file)
output.flush()

input = open(output.name, 'rb')
raw_data = input.read()
print(f'Raw Data: {binascii.hexlify(raw_data)}')

input.seek(0)
read_data = array.array('i')
read_data.fromfile(input, len(data))
print(f'Read Data: {read_data}')
