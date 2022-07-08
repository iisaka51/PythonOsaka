import shutil
from pathlib import Path

def task_cleanup_cache():
    """clean up __pycache__"""
    def clear_cache():
        shutil.rmtree('__pycache__')

    return {
        'actions': [clear_cache()]
    }

def task_cleanup_pyc():
    """clean up .pyc"""
    def clear_pyc():
         for p in Path('.').glob('*.pyc'):
             p.unlink()

    return {
        'actions': [clear_pyc()]
    }
