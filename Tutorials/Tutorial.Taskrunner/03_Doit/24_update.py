def task_touch():
    return {
        'actions': ['touch foo.txt'],
        'targets': ['foo.txt'],
        # ターゲットが削除されない限り、
        # doitが常にタスクを最新の状態としてマークするように強制する
        'uptodate': [True],
        }
