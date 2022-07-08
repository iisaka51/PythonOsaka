import parsl
from parsl.monitoring.monitoring import MonitoringHub
from parsl.config import Config
from parsl.executors import HighThroughputExecutor
from parsl.addresses import address_by_hostname

import logging

config = Config(
   executors=[
       HighThroughputExecutor(
           label="local_htex",
           cores_per_worker=1,
           max_workers=4,
           address=address_by_hostname(),
       )
   ],
   monitoring=MonitoringHub(
       hub_address=address_by_hostname(),
       hub_port=55055,
       monitoring_debug=False,
       resource_monitoring_interval=10,
   ),
   strategy=None
)
