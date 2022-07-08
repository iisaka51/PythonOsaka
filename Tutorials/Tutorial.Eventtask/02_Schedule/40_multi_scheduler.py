import time
import schedule

def fooJob():
    print("Foo")

def barJob():
    print("Bar")

# 新しいスケジューラーを作成
scheduler1 = schedule.Scheduler()

# 作成したスケジューラーにジョブを登録
scheduler1.every().hour.do(fooJob)
scheduler1.every().hour.do(barJob)

# 2つ目のスケジューラーを作成
# 必要な数だけ作成することができる
scheduler2 = schedule.Scheduler()
scheduler2.every().second.do(fooJob)
scheduler2.every().second.do(barJob)

while True:
    # run_pending() はすべてのスケジューラで呼び出される必要があります。
    scheduler1.run_pending()
    scheduler2.run_pending()
    time.sleep(1)
