from cmdkit.config import Namespace
from pprint import pprint

ns = Namespace.from_toml('config.toml')

pprint(ns.items())
