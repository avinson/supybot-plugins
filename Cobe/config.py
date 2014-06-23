###

import supybot.conf as conf
import supybot.registry as registry
try:
    from supybot.i18n import PluginInternationalization
    from supybot.i18n import internationalizeDocstring
    _ = PluginInternationalization('Cobe')
except:
    _ = lambda x:x
    internationalizeDocstring = lambda x:x

def configure(advanced):
    # This will be called by supybot to configure this module.  advanced is
    # a bool that specifies whether the user identified himself as an advanced
    # user or not.  You should effect your configuration by manipulating the
    # registry as appropriate.
    from supybot.questions import expect, anything, something, yn
    conf.registerPlugin('Cobe', True)


Cobe = conf.registerPlugin('Cobe')
# This is where your configuration variables (if any) should go.  For example:
# conf.registerGlobalValue(Cobe, 'someConfigVariableName',
#     registry.Boolean(False, """Help for someConfigVariableName."""))

conf.registerGroup(Cobe, 'learn')
conf.registerGlobalValue(Cobe.learn, 'commands',
    registry.Boolean(False, _("""Determines whether the bot answers to messages
    beginning by a non-alphanumeric char.""")))
conf.registerGroup(Cobe, 'answer')
conf.registerChannelValue(Cobe.answer, 'commands',
    registry.Boolean(False, _("""Determines whether messages beginning by a
    non-alphanumeric char are learned.""")))
conf.registerChannelValue(Cobe.answer, 'probability',
    registry.Integer(10, _("""Determines the percent of messages the bot will
    answer (zero is recommended if you have a tiny database).""")))
conf.registerChannelValue(Cobe.answer, 'probabilityWhenAddressed',
    registry.Integer(100, _("""Determines the percent of messages adressed to
    the bot the bot will answer.""")))



# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
