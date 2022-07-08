from cmdkit.config import Namespace, Configuration

cfg = Configuration(A=Namespace({'x': 1, 'y': 2}),
                    B=Namespace({'x': 3, 'z': 4}))

v1 = cfg['x'], cfg['y'], cfg['z']
v2 = cfg.namespaces['A']['x']

# print(cfg)
# print(v1)
# print(v2)
