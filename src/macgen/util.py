# chris 071815

import errno
import os

# TODO Deprecate when moved to Python 3?
def makedirs(name,mode=0o777,exist_ok=False):
  '''Like Python 3's makedirs with exist_ok.'''
  try: os.makedirs(name,mode)
  except os.error,e:
    if not exist_ok or e.errno != errno.EEXIST: raise
