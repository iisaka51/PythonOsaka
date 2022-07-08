Parent = type('Parent', (), {})
Child = type('Child', (Parent,), dict(name='Python'))

obj = Child()
print(obj.name)
