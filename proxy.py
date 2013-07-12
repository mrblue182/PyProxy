from twisted.internet import protocol, reactor
import re

class ProxyClient(protocol.Protocol):
	def __init__(self, serverTransport):
		self.serverTransport = serverTransport
		self.data = ''

	def dataReceived(self, data):
		self.data += data

	def connectionLost(self, reason):
		self.data = self.process(self.data)

		self.serverTransport.write(self.data)
		self.serverTransport.loseConnection()

	def sendData(self, data):
		self.transport.write(data)

	def process(self, data):
		return data


class ProxyServer(protocol.Protocol):
	client = None

	def dataReceived(self, data):
		data = re.sub('\sAccept-Encoding: .*', '', data)
		self.data = re.sub('Connection: .*', 'Connection: close', data)

		host = re.search('Host: (\S*)', self.data).group(1)

		client = protocol.ClientCreator(reactor, self.client, self.transport)
		defer = client.connectTCP(host, 80)

		defer.addCallback(self.forwardToClient, client)

	def forwardToClient(self, client, data):
		client.sendData(self.data)
