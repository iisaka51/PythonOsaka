LOGGING_CONFIG = {
  'version': 1,   # 必須
  'disable_existing_loggers': False,
  'formatters': {
    'simple': {
      'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
    }
  },
  'handlers': {
    'console': {
      'level': 'DEBUG',
      'class': 'logging.StreamHandler',
      'formatter': 'simple'
    }
  },
  'loggers': {
    'demo': {
      'level': 'DEBUG',
      'handlers': ['console']
    }
  }
}
