import logging
from traceback import format_exc
import datetime

from schedule import Scheduler

logger = logging.getLogger('schedule')

class SafeScheduler(Scheduler):
    """
    失敗したジョブを捕捉し、そのログを記録する Scheduler の実装。　
    例外のトレースバックをエラーとし、
    オプションでジョブの再スケジューリングを行います。　
    他ののジョブが実行されるかどうか、
    スクリプト全体がクラッシュしないかどうかを、
    気にせずジョブを実行することができます。
    """

    def __init__(self, reschedule_on_failure=True):
        """
        reschedule_on_failure が True の場合は、
        ジョブは正常に終了したかのように、
        次の実行のために再スケジュールされます。
        """
        self.reschedule_on_failure = reschedule_on_failure
        super().__init__()

    def _run_job(self, job):
        try:
            super()._run_job(job)
        except Exception:
            logger.error(format_exc())
            job.last_run = datetime.datetime.now()
            job._schedule_next_run()

