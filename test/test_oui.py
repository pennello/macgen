# chris 071915

import random
import shutil
import tempfile
import time
import unittest

from cStringIO import StringIO
from contextlib import closing,contextmanager
from functools import partial

from macgen.oui import OuiMgr

# Short local cache file expiry threshold to use in testing.  In
# seconds.
shortthresh = 1

# Whether or not to do network tests.  The IEEE site isn't that fast,
# and the OUI data file is over three megabytes.  It thus usually isn't
# that helpful to do network-related tests.  Maybe good to enable
# manually and test out once and a while.
donetwork = False

@contextmanager
def testctx():
  '''
  Little context manager to test OuiMgr instances with a temporary
  directory instead of a permanent varpath and a much shorter expiry
  threshold.
  '''
  oldthresh = OuiMgr.thresh
  OuiMgr.thresh = shortthresh
  tmpdir = tempfile.mkdtemp(prefix='test_oui_tmp_')
  try: yield tmpdir
  finally:
    OuiMgr.thresh = oldthresh
    shutil.rmtree(tmpdir)

def smokecache(self,cache):
  '''
  Sanity check for cache data structure.  Meant to be used in test
  cases.
  '''
  self.assertTrue(len(cache) >= 10)
  for name,ouis in cache:
    self.assertTrue(name)
    self.assertTrue(len(ouis) >= 3)

def smokechoice(self,choice):
  '''
  Sanity check for output of OuiMgr.choose.  Meant to be used in test
  cases.
  '''

  def smokeoui(self,oui):
    self.assertIs(type(oui),tuple)
    self.assertEquals(len(oui),3)
    for x in oui:
      self.assertIs(type(x),int)
      self.assertTrue(0 <= x <= 255)

  self.assertIs(type(choice),tuple)
  self.assertEquals(len(choice),2)
  name,oui = choice
  self.assertIs(type(name),str)
  self.assertTrue(name)
  smokeoui(self,oui)

class Random(object):
  '''Class namespace for routines to generate random test data.'''

  @staticmethod
  def oui():
    r = partial(random.randint,0,255)
    return r(),r(),r()

  @classmethod
  def soui(cls): return '%02x-%02x-%02x' % cls.oui()

  @staticmethod
  def name():
    name = u''
    def randascii(): return chr(random.randint(65,127))
    def randuni(): return unichr(random.randint(65,0xffff))
    n = random.randint(7,15)
    for _ in xrange(n // 2): name += randascii()
    name += ' '
    for _ in xrange(n - n // 2 - 1): name += randuni()
    return name.encode('utf8')

  @classmethod
  def cache(cls):
    cache = []
    n = random.randint(10,100)
    for _ in xrange(n):
      ouis = []
      nouis = random.randint(5,10)
      for _ in xrange(nouis):
        ouis.append(Random.oui())
      cache.append((cls.name(),ouis))
    return cache

class ClassTest(unittest.TestCase):
  '''Non-instance tests for OuiMgr class.'''

  def test_serializeoui(self):
    x = OuiMgr.serializeoui((0,16,255))
    expect = '00-10-ff'
    self.assertEquals(x,expect)

  def test_parseoui(self):
    x = OuiMgr.parseoui('00-10-ff')
    expect = 0,16,255
    self.assertEquals(x,expect)

  def test_compose_oui(self):
    for _ in xrange(1000):
      oui = Random.oui()
      x = OuiMgr.parseoui(OuiMgr.serializeoui(oui))
      self.assertEquals(oui,x)

      soui = Random.soui()
      x = OuiMgr.serializeoui(OuiMgr.parseoui(soui))
      self.assertEquals(soui,x)

  def test_serialize(self):
    name = 'Way Cool, TM, Inc.'
    cache = [(name,[(1,2,3),(0,16,255)])]
    with closing(StringIO()) as io:
      OuiMgr.serialize(io,cache)
      expect = '%s\t01-02-03 00-10-ff\n' % name
      self.assertEquals(io.getvalue(),expect)

  def test_parse(self):
    name = 'Way Cool, TM, Inc.'
    x = '%s\t01-02-03 00-10-ff\n' % name
    with closing(StringIO()) as io:
      io.write(x)
      io.seek(0)
      cache = OuiMgr.parse(io)
    self.assertEquals(cache,[(name,[(1,2,3),(0,16,255)])])

  def test_compose_parse(self):
    for _ in xrange(100):
      cache = Random.cache()
      with closing(StringIO()) as io:
        OuiMgr.serialize(io,cache)
        io.seek(0)
        x = OuiMgr.parse(io)
        self.assertEquals(x,cache)

  def test_fetch_network(self):
    if not donetwork: return
    smokecache(self,OuiMgr.fetch())

class InstanceTest(unittest.TestCase):
  '''Instance-oriented tests for OuiMgr class.'''

  def test_load(self):
    with testctx() as tmpdir:
      ouimgr = OuiMgr(tmpdir)
      self.assertIs(ouimgr.load(),None)

  def test_save(self):
    with testctx() as tmpdir:
      ouimgr = OuiMgr(tmpdir)
      cache = Random.cache()
      ouimgr.save(cache)
      x = ouimgr.load()
      smokecache(self,x)
      self.assertEquals(x,cache)

  def test_expire(self):
    with testctx() as tmpdir:
      ouimgr = OuiMgr(tmpdir)
      cache = Random.cache()
      ouimgr.save(cache)
      # Let it expire.
      time.sleep(shortthresh + 1)
      self.assertIs(ouimgr.load(),None)

  def test_ensure_nonetwork(self):
    with testctx() as tmpdir:
      ouimgr = OuiMgr(tmpdir)
      cache = Random.cache()
      ouimgr.save(cache)
      ouimgr = OuiMgr(tmpdir)
      ouimgr.ensure()
      smokecache(self,ouimgr.cache)

  def test_ensure_network(self):
    if not donetwork: return
    with testctx() as tmpdir:
      ouimgr = OuiMgr(tmpdir)
      ouimgr.ensure()
      smokecache(self,ouimgr.cache)

  def test_choose_nonetwork(self):
    with testctx() as tmpdir:
      ouimgr = OuiMgr(tmpdir)
      cache = Random.cache()
      ouimgr.save(cache)
      smokechoice(self,ouimgr.choose())
