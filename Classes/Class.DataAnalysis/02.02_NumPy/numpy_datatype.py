import numpy as np

dt_1 = np.dtype(np.int32)
dt_2 = np.dtype('i4')
dt_3 = np.dtype([('age',np.int8)])
dt_4 = np.dtype("i4, (2,3)f8, f4")

a = np.array([(10,),(20,),(30,)], dtype = dt_3)
employee = np.dtype([('name','S20'), ('age', 'i1'), ('salary', 'f4')])

print(dt_1)
print(dt_2)
print(dt_3)
print(dt_4)

print(a.dtype)
print(employee)
