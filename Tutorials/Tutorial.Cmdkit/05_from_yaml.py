from cmdkit.config import Namespace
from pprint import pprint

ns = Namespace.from_yaml('config.yaml')

pprint(ns.items())
ns.MAIL_DEBUG = True

ns.to_yaml('config.yaml')

#!cat config.yaml
