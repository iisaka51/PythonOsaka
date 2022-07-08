def task_publish():
  """Publish to AWS S3"""
  return {
    "actions": [
        'echo aws s3 sync _built/html s3://buck/et --exclude "*" --include "*.html"'
    ]
  }

