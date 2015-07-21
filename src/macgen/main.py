# chris 071615

'''Main application logic.'''

import os
import struct
import sys

from argparse import ArgumentParser

from . import util
from .oui import OuiMgr

class Main(object):
  '''Class encapsulating main application logic.'''

  def __init__(self,prog,*argv):
    '''
    Pass the main program name (argv[0]) and the rest of the
    command-line arguments.
    '''
    self.prog = os.path.basename(prog)
    descr = ('Generates a random and correctly-formatted MAC address. '
      'The last three octets are always random.')
    parser = ArgumentParser(prog=self.prog,description=descr)
    parser.add_argument('-n','--no-oui',dest='use_oui',action='store_false',
      default=True,help="don't use an organizationally unique identifier")
    parser.add_argument('-l','--local',action='store_true',
      default=False,help='enable locally administered bit in first octet; '
      'if OUIs are being used, this bit is necessarily off')
    parser.add_argument('-s','--no-separator',dest='use_separator',
      action='store_false',default=True,help='disable : octet separator')
    parser.add_argument('-v','--verbose',action='store_true',default=False,
      help='enable debug output to standard error')
    parser.add_argument('-r','--raw',action='store_true',default=False,
      help='output raw OUI bytes; implies -s')
    self.args = parser.parse_args(argv)

    util.enablelog = self.args.verbose

  def basepath(self):
    '''Base path for on-disk cached data.'''
    return os.path.expanduser('~')
  def varpath(self):
    '''Path to var dir for locally-cached data.'''
    return os.path.join(self.basepath(),'var',self.prog)

  def run(self):
    '''Run main application logic.'''
    if self.args.use_oui:
      name,oui = OuiMgr(self.varpath()).choose()
      util.log('chose an oui from %s' % name)
    else:
      oui = util.randbytes(3)
      if self.args.local: oui[0] |= 2
      else: oui[0] &= 0xfd

    mac = list(oui) + util.randbytes(3)

    if self.args.raw:
      sys.stdout.write(struct.pack('>BBBBBB',*mac))
    else:
      sep = ':' if self.args.use_separator else ''
      print(sep.join('%02x' % x for x in mac))
