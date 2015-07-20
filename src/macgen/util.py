# chris 071815

import errno
import os
import random
import sys

enablelog = False

# TODO Deprecate when moved to Python 3?
def makedirs(name,mode=0o777,exist_ok=False):
  '''Like Python 3's makedirs with exist_ok.'''
  try: os.makedirs(name,mode)
  except os.error,e:
    if not exist_ok or e.errno != errno.EEXIST: raise

def randbytes(n):
  '''Return n random bytes.'''
  return [random.randint(0,255) for _ in xrange(n)]

def log(x):
  if not enablelog: return
  sys.stderr.write('%s\n' % x)
  sys.stderr.flush()
