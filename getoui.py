# get OUI listing from the IEEE and generate code for macgen to use
# store pickled data in $HOME/.macgen

from __future__ import with_statement
from os import environ
from cPickle import dump
from urllib2 import urlopen
from collections import defaultdict
from os.path import join
import util

u = urlopen('http://standards.ieee.org/regauth/oui/oui.txt')
data = u.read().strip().split('\n')
u.close()

ouis = defaultdict(list)
names = {}
counts = defaultdict(int)

for line in data:
  if '(hex)' not in line: continue
  line = line.split(None,2)
  oui,name = line[0],line[2]
  if name == 'PRIVATE': continue
  oui = [int(b,16) for b in oui.split('-')]
  # XXX would be nice to better normalize the organization names
  norm = name.lower()[:13]

  ouis[norm].append(oui)
  names[norm] = name
  counts[norm] += 1

counts = [(c,n) for n,c in counts.iteritems()]
# most popular ouis come first
counts.sort(reverse=True)
# also get rid of unpopular manufacturers 
data = [(names[n],ouis[n]) for c,n in counts if c >= 3]

with open(join(util.homedir,'.macgen'),'wb') as f: dump(data,f,-1)
