from twisted.words.protocols import irc
from twisted.internet import protocol
from twisted.internet import reactor
import sys
import sitscrape

class DinnerBot(irc.IRCClient):
	def _get_nickname(self):
		return self.factory.nickname
	nickname = property(_get_nickname)
	
	def signedOn(self):
		self.join(self.factory.channel)
		print "Signed on as %s." % (self.nickname,)
	
	def joined(self, channel):
		print "Joined %s." % (channel,)
	
	def privmsg(self, user, channel, msg):
		if not user:
			return
		if "!middag" in msg:
			sites = { "Realfag":"http://www.sit.no/content/36447/Ukas-middagsmeny-pa-Realfag", 
					"Hangaren":"http://www.sit.no/content/36444/Ukas-middagsmeny-pa-Hangaren"}
			#TODO rate limit this, and cache...
			menu_lines = sitscrape.todays_menu(sites)
			self.msg(self.factory.channel, "Todays menu is..")
			for line in menu_lines:
				self.msg(self.factory.channel, line)

class DinnerBotFactory(protocol.ClientFactory):
    protocol = DinnerBot
    def __init__(self, channel, nickname='habeebs'):
        self.channel = channel
        self.nickname = nickname
        
    def clientConnectionLost(self, connector, reason):
        print "Lost connection (%s), reconnecting." % (reason,)
        connector.connect()
        
    def clientConnectionFailed(self, connector, reason):
        print "Could not connect: %s" % (reason,)

if __name__ == "__main__":
    try:
        chan = sys.argv[1]
    except:
        print "Usage:"
        print "python sit-dinner-bot.py channel"
    reactor.connectTCP('irc.freenode.net', 6667, DinnerBotFactory('#' + chan, 'dinnerbot'))
    reactor.run()
