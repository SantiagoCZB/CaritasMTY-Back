from app import create_app

app = create_app()

API_CERT = '/home/user01/realmadswift.tc2007b.tec.mx.cer'
API_KEY = '/home/user01/realmadswift.tc2007b.tec.mx.key'
if __name__ == '__main__':
	import ssl
	context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
	context.load_cert_chain(API_CERT, API_KEY)
	app.run(host='0.0.0.0', port=10206, ssl_context=context, debug=True)