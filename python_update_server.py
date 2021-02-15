import socketserver

from node_mcu_update_server import NodeMCUUpdateServer

handler_object = NodeMCUUpdateServer

PORT = 9999
my_server = socketserver.TCPServer(("", PORT), handler_object)
my_server.serve_forever()
