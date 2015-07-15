from __future__ import with_statement
import os

homedir = os.environ[dict(posix='HOME',nt='USERPROFILE').get(os.name,'HOME')]

# return n random bytes; n in (6,8)
if os.name != 'posix':
  from struct import pack
  from random import randint
  def rand(n): return pack('>HI',randint(0,2**16-1),randint(0,2**32-1))[:n]
else:
  def rand(n):
    with open('/dev/urandom','rb') as f: return f.read(n)
