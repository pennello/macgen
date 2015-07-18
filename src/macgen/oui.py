# chris 071615 Code for dealing with organizationally-unique
# identifiers.

import errno
import os
import random
from collections import defaultdict
from contextlib import closing
from .util import makedirs

class OuiMgr(object):
  filename = 'oui'
  ieee = 'http://standards.ieee.org/regauth/oui/%s.txt' % filename
  # Token to identify lines with OUI and company name.
  token = '(hex)'
  # Threshold after which to consider a cached copy of the IEEE data
  # stale, requiring a re-fetch.
  thresh = 6 * 30 * 24 * 60 * 60

  def __init__(self,varpath):
    self.varpath = varpath
    self.cache = None

  def path(self): return os.path.join(self.varpath,filename)

  def choose(self):
    '''Return a randomly-chosen OUI.'''
    self.ensure()

    # Choose random index to fetch a manufacturer and its OUIs.  Favor
    # beginning of the list, as that's where all the popular companies
    # are.
    i = min(len(self.cache),int(round(abs(random.gauss(0,10)))))
    name,ouis = self.cache[i]
    return choice(ouis)

  def ensure(self):
    '''Ensure in-memory cache is available.'''
    if self.cache is None:
      self.cache = self.load()
      if self.cache is None:
        self.cache = self.fetch()
        self.save(self.cache)

  def load(self):
    '''
    Try to load OUI data into memory.  If local cache file is not
    present, return None.  If local cache file is present, but stale,
    delete it, and return None.
    '''
    try:
      with open(self.path(), 'rb') as f:
        st = os.fstat(f.fileno())
        if st.m_time > time.time() + self.thresh:
          os.unlink(self.path())
          return None
        return self.parse(f)
    except OSError,e:
      if e.errno == errno.ENOENT: return None
      raise

  def save(self,cache):
    '''Save in-memory cache data structure to on-disk cache file.'''
    makedirs(self.varpath,exist_ok=True)
    with open(self.path(), 'wb') as f:
      self.serialize(f,cache)

  @staticmethod
  def serializeoui(oui):
    '''Serialize in-memory representation of OUI to string.'''
    return '-'.join('%02x' % x for x in oui)

  @staticmethod
  def parseoui(oui):
    '''Parse OUI from string representation.'''
    return tuple(int(x,16) for x in oui.split('-'))

  @classmethod
  def serialize(cls,file,cache):
    '''Serialize in-memory cache data structure to open file.'''
    for name,ouis in cache:
      ouis = ' '.join(cls.serializeoui(oui) for oui in ouis)
      file.write('%s\t%s\n' % (name,ouis))

  @classmethod
  def parse(cls,file):
    '''Parse cache data from open file.'''
    cache = []
    for line in file:
      name,ouis = line.split('\t')
      ouis = ouis.strip().split(' ')
      ouis = [cls.parseoui(oui) for oui in ouis]
      cache.append((name,ouis))
    return cache

  @classmethod
  def fetch(cls):
    '''
    Fetch OUI data from IEEE, normalize, and return cache data
    structure:
      [(name,ouis), ...]
    where ouis is:
      [oui,...]
    where oui is:
      (int,int,int)
    '''
    ouis = defaultdict(list)
    names = {}

    # Fetch from IEEE.
    with closing(urlopen(cls.ieee)) as u:
      for line in u:
        if cls.token not in line: continue
        line = line.split(None,2)
        oui,name = line[0],line[2]
        if name == 'PRIVATE': continue
        oui = cls.parseoui(oui)
        # It would be nice to better normalize the organization names.
        norm = name.lower()[:13]
        ouis[norm].append(oui)
        names[norm] = name

    counts = [(len(v),norm) for norm,v in ouis.iteritems()]

    # Most popular OUIs come first.
    counts.sort(reverse=True)

    # Get rid of unpopular manufacturers.
    cache = [(names[norm],ouis[norm]) for c,norm in counts if c >= 3]

    return cache