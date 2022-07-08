from model_demodb import *

doc = MyDoc({'test': 123})
backend.save(doc)

v1 = hasattr(doc, 'foo')
v2 = hasattr(doc, 'updated_at')
backend.update(doc,{'foo' : 'I love IPA'})
backend.commit()
v3 = doc.foo
v4 = doc.updated_at


# print(v1)
# ...
# print(v4)
