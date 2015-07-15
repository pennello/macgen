# generate MAC addresses
# v1.2 non-posix support
# v1.1 select from only the most popular OUIs
# v1.0 initial version

from __future__ import with_statement
import os
import sys
from runpy import run_module
from random import gauss,choice
from cPickle import load
from optparse import OptionParser
from os.path import join
import util

parser = OptionParser(version='%prog 1.2',description='Generates a random '
  'and correctly-formatted MAC address.  The last three octets are always '
  'random.')
parser.add_option('-n','--no-oui',action='store_true',default=False,
  help="Don't use an Organizationally Unique Identifier.")
parser.add_option('-l','--locally-administered',action='store_true',
  default=False,help='Set locally administered bit in first octet.  '
  'Off by default.  If OUIs are being used, this bit is necessarily off.')
parser.add_option('-s','--no-separator',action='store_true',default=False,
  help="Disable `:' octet separator.")
parser.add_option('-v','--verbose',action='store_true',default=False,
  help='Enable verbose output.')
opt,args = parser.parse_args()

if not opt.no_oui:
  f = join(util.homedir,'.macgen')
  try: f = open(f,'rb')
  except IOError:
    if opt.verbose:
      sys.stderr.write('OUI data not found; fetching from the IEEE\n')
    run_module('getoui')
    f = open(f,'rb')
  data = load(f)
  f.close()

  # choose random index to fetch a manufacturer and its ouis
  # favor beginning of the list, as that's where all the popular companies are
  i = min(len(data),int(round(abs(gauss(0,10)))))
  name,ouis = data[i]
  oui = choice(ouis)
  loc = False
  n = 3

  if opt.verbose: sys.stderr.write('chose an OUI from ' + name + '\n')
else:
  oui = []
  loc = opt.locally_administered
  n = 6

b = oui + map(ord,util.rand(n))
if loc: b[0] |= 2
else: b[0] &= 0xfd

print ('' if opt.no_separator else ':').join(['%02x' % x for x in b])
