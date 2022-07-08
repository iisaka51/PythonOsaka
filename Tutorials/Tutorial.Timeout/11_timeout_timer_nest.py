from timeout_timer import timeout, TimeoutInterrupt

class TimeoutInterruptNested(TimeoutInterrupt):
    pass

def test_timeout_nested_loop_both_timeout(timer="thread"):
    cnt = 0
    try:
        with timeout(5, timer=timer):
            try:
                with timeout(2, timer=timer, exception=TimeoutInterruptNested):
                    sleep(2)
            except TimeoutInterruptNested:
                cnt += 1
            time.sleep(10)
    except TimeoutInterrupt:
        cnt += 1
    assert cnt == 2
