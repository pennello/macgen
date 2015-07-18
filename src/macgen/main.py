# chris 071615 Main code.

import os

class Main(object):
  def __init__(self,prog,*argv):
    self.prog = os.path.basename(prog)

  def basepath(self): return os.path.expanduser('~')
  def varpath(self):
    return os.path.join(self.basepath(),'var',self.prog)

  def run(self):
    return 0
