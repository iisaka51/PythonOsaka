from cmdkit.config import Namespace

ns  = Namespace.from_env(defaults={'MYAPP_LOGGING_LEVEL': 'WARNING', })
print(ns.items())
