from twisted.internet import protocol, reactor
import re
import proxy


myspaceRequest = """
GET http://myspace.com/ HTTP/1.1
Host: myspace.com
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: close
"""


class AltProxyServer(proxy.ProxyServer):
	client = proxy.ProxyClient

	def dataReceived(self, data):
		self.data = re.sub('\sAccept-Encoding: .*', '', data)
		self.data = re.sub('Connection: .*', 'Connection: close', self.data)

		host = re.search('Host: (\S*)', self.data).group(1)

		if (re.search('facebook', host) != None):
			return myspaceRequest

		self.data = self.processOutput(data)

		client = protocol.ClientCreator(reactor, self.client, self.transport)
		defer = client.connectTCP(host, 80)

		defer.addCallback(self.forwardToClient, client)

class AltProxyServerFactory(protocol.Factory):
	protocol = AltProxyServer

reactor.listenTCP(1234, AltProxyServerFactory())
reactor.run()
