def need_to_debug():
    # 何かのコード...
    from doit import tools
    tools.set_trace()
    # ここにもコード...

def task_X():
    return {'actions':[(need_to_debug,)]}
