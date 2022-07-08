from cmdkit.config import Configuration
from pprint import pprint
from config import WatchConfig

from config import workdir, homedir, WatchConfig

conf = Configuration.from_local(
                 default = WatchConfig().__dict__,
                 env = False, prefix='',
                 system = '',
                 user = str(homedir / '.logwatcher.yml'),
                 local = str(workdir / 'logwatcher.yml'))

# pprint(conf)
