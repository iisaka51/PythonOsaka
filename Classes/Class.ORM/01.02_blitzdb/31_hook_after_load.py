from model_demodb import *

doc = MyDoc({'test': 123})
backend.save(doc)
backend.commit()

v1 = hasattr(doc, 'bar')
loaded_doc = backend.get(MyDoc,{'pk' : doc.pk})
v2 = hasattr(loaded_doc, 'bar')

# print(doc)
# print(v1)
# print(loaded_doc.bar)
