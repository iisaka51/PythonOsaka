from model_demodb import *

doc = MyDoc({'test': 123})
v1 = hasattr(doc, 'foo')
backend.save(doc)
v2 = hasattr(doc, 'foo')
backend.commit()

loaded_doc = backend.get(MyDoc,{'pk' : doc.pk})
v3 = hasattr(loaded_doc, 'foo')

# print(v1)
# print(v2)
# print(v3)
# print(doc.foo)
# print(loaded_doc.foo)
