# ros2_websocket_server.py
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
import base64
import asyncio
import websockets
import cv2
from cv_bridge import CvBridge

class WebSocketServer(Node):
    def __init__(self):
        super().__init__('websocket_server')
        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.listener_callback,
            10)
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.bridge = CvBridge()
        self.loop = asyncio.get_event_loop()
        self.websocket_clients = set()
        self.loop.run_until_complete(self.websocket_server())

    def listener_callback(self, msg):
        cv_image = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        _, buffer = cv2.imencode('.jpg', cv_image)
        jpg_as_text = base64.b64encode(buffer).decode('utf-8')
        asyncio.run_coroutine_threadsafe(self.broadcast(jpg_as_text), self.loop)

    async def websocket_handler(self, websocket, path):
        self.websocket_clients.add(websocket)
        try:
            async for message in websocket:
                self.handle_command(message)
        finally:
            self.websocket_clients.remove(websocket)

    async def websocket_server(self):
        server = await websockets.serve(self.websocket_handler, 'localhost', 8765)
        await server.wait_closed()

    async def broadcast(self, message):
        #logica pra repassar a mensagem pra todos os clients conectados
        if self.websocket_clients:
            await asyncio.wait([client.send(message) for client in self.websocket_clients])

    def handle_command(self, message):
        twist = Twist()
        #Logica pra receber as mensagens do front end pra controlar o robô :3
        if message == 'forward':
            twist.linear.x = 0.5
        elif message == 'backward':
            twist.linear.x = -0.5
        elif message == 'left':
            twist.angular.z = 0.5
        elif message == 'right':
            twist.angular.z = -0.5
        elif message == 'stop':
            twist.linear.x = 0.0
            twist.angular.z = 0.0
        self.publisher.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    websocket_server = WebSocketServer()
    rclpy.spin(websocket_server)
    websocket_server.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
