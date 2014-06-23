
###

from supybot.test import *

class CobeTestCase(PluginTestCase):
    plugins = ('Cobe',)
    
    #def testCleanup(self):
    #    self.assertNotError('cleanup')
    
    def testAnswer(self):
        self.assertNotRegexp('foo', '.*not a valid.*')


# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
