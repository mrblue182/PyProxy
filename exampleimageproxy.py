from twisted.internet import protocol, reactor
import proxy
import re

class ImageProxyClient(proxy.ProxyClient):
	def process(self, data):
		return re.sub('<img src=".*?"', '<img src="http://images.nationalgeographic.com/wpf/media-live/photos/000/005/cache/domestic-cat_516_600x450.jpg"', data)

class ImageProxyServer(proxy.ProxyServer):
	client = ImageProxyClient

class ImageProxyServerFactory(protocol.Factory):
	protocol = ImageProxyServer


reactor.listenTCP(1234, ImageProxyServerFactory())
reactor.run()
