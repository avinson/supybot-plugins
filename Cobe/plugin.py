###

import re
import os
import sys
import random
import supybot.conf as conf
import supybot.utils as utils
from cStringIO import StringIO
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks

try:
    from cobe.brain import Brain
except ImportError:
    raise callbacks.Error, 'Brain import error ' \

try:
    from supybot.i18n import PluginInternationalization
    from supybot.i18n import internationalizeDocstring
    _ = PluginInternationalization('Cobe')
except:
    # This are useless function that's allow to run the plugin on a bot
    # without the i18n plugin
    _ = lambda x:x
    internationalizeDocstring = lambda x:x

class Cobe(callbacks.Plugin):
    """This plugins provides a Cobe integration for Supybot.
    Cobe must be installed ('apt-get install brain' on Debian)"""
    callAfter = ['MoobotFactoids', 'Factoids', 'Infobot']
    callBefore = ['Dunno']

    def __init__(self, irc):
        # Call Supybot's scripts
        self.__parent = super(Cobe, self)
        self.__parent.__init__(irc)
        
        # Save state
        saved = (sys.stdout, os.getcwd())
        
        # Create proxy for Cobe
        os.chdir(conf.supybot.directories.data())
        sys.stdout = StringIO()
        
        # Initialize Cobe
        self.brain = Brain("cobe.store")
        
        # Restore state
        sys.stdout, cwd = saved
        os.chdir(cwd)
        
        random.seed()
    
    _dontKnow = [
                 'I don\'t know enough to answer you yet!',
                 'I am utterly speechless!',
                 'I forgot what I was going to say!'
                ]
    _translations = {
                     'I don\'t know enough to answer you yet!':
                         _('I don\'t know enough to answer you yet!'),
                     'I am utterly speechless!':
                         _('I am utterly speechless!'),
                     'I forgot what I was going to say!':
                         _('I forgot what I was going to say!'),
                    }

    def _response(self, msg, prb, reply):
        if random.randint(0, 100) < prb:
            response = self.brain.reply(unicode(msg))
            if self._translations.has_key(response):
                response = self._translations[response]
            reply(response, prefixNick=False)
        else:
            match = re.search(r'^\w+:|\+\+$|http:|https:', msg)
            if not match:
              self.brain.train(unicode(msg))

    def doPrivmsg(self, irc, msg):
        if not msg.args[0].startswith('#'): # It is a private message
            return
        message = msg.args[1]
        
        if message.startswith(irc.nick) or re.match('\W.*', message):
            # Managed by invalidCommand
            return
        
        probability = self.registryValue('answer.probability', msg.args[0])
        self._response(message, probability, irc.reply)

    def invalidCommand(self, irc, msg, tokens):
        if not msg.args[0].startswith('#'): # It is a private message
            # Actually, we would like to answer, but :
            # 1) It may be a mistyped identify command (or whatever)
            # 2) Cobe can't reply without learning
            return
        message = msg.args[1]
        usedToStartWithNick = False
        if message.startswith(message):
            parsed = re.match('(.+ |\W)?(?P<message>\w.*)', message)
            message = parsed.group('message')
            usedToStartWithNick = True
        if self.registryValue('answer.commands') or usedToStartWithNick:
            print msg.args[0]
            self._response(message,
                        self.registryValue('answer.probabilityWhenAddressed',
                                           msg.args[0]),
                        irc.reply)
        elif self.registryValue('learn.commands'):
            self.brain.train(unicode(message))
    
    @internationalizeDocstring
    def cleanup(self, irc, msg, args):
        """takes no argument
        
        Saves Cobe brain to disk."""
    #    brain.cleanup()
        irc.replySuccess()

Class = Cobe

