from model_demodb import *

doc = MyDoc({'test': 123})
doc.pk = 1
v1 = hasattr(doc, 'foo')
backend.delete(doc)
v2 = hasattr(doc, 'foo')

# print(v1)
# print(v2)
# print(doc.foo)
