import socket
from threading import Thread
import json
from random import randint
from time import sleep

HOST, PORT = '109.191.136.194', 8080 # Адрес сервера
MAX_PLAYERS = 2 # Максимальное кол-во подключений

class Server:

    def __init__(self, addr, max_conn):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(addr) # запускаем сервер от заданного адреса

        self.max_players = max_conn
        self.players = [] # создаем массив из игроков на сервере
        self.enemies = [] # тут враги
        self.bullets = []
        self.generate()
        self.sock.listen(self.max_players) # устанавливаем максимальное кол-во прослушиваний на сервере
        print(f'server started at {HOST}:{PORT}')
        self.listen() # вызываем цикл, который отслеживает подключения к серверу

    def generate(self):
        for i in range(0, 6):
            newEnemy = [randint(0, 790), 0]
            self.enemies.append(newEnemy)

    def update(self):
        while True:
            for i in self.enemies:
                i[1] += 2
                if i[1]>=600:
                    i[0] = randint(0, 790)
                    i[1]=0
            sleep(1/30)

    def listen(self):
        while True:
            if not len(self.players) >= self.max_players: # проверяем не превышен ли лимит
                 # одобряем подключение, получаем взамен адрес и другую информацию о клиенте
                conn, addr = self.sock.accept()

                print("New connection", addr[0])

                Thread(target=self.handle_client, args=(conn, addr,)).start() # Запускаем в новом потоке проверку действий игрока
                if len(self.players)==1:
                    Thread(target=self.update).start()

    def handle_client(self, conn, addr):

        # Настраиваем стандартные данные для игрока
        self.player = {
            "id": addr,
            "x": 400,
            "y": 550
        }
        self.players.append(self.player) # добавляем его в массив игроков

        while True:
            try:
                data = conn.recv(4096) # ждем запросов от клиента

                if not data: # если запросы перестали поступать, то отключаем игрока от сервера
                    print(f"Disconnected: {addr[0]}")
                    break

                # загружаем данные в json формате
                data = json.loads(data.decode('utf-8'))

                # запрос на получение игроков на сервере
                if data["request"] == "get_players":
                    conn.sendall(bytes(json.dumps({
                        "players": self.players,
                        "enemies": self.enemies
                    }), 'UTF-8'))

                # движение
                if data["request"] == "move":
                    for player in self.players:
                        if addr == player["id"]:
                            if data["move"] == "left" and player["x"] >=10:
                                player["x"] -= 10
                            if data["move"] == "right" and player["x"] <= 790:
                                player["x"] += 10
                    
            except Exception as e:
                print(f"Disconnected: {addr}")
                self.players.remove(self.player)
                exit()

        self.players.remove(self.player) # если вышел или выкинуло с сервера - удалить персонажа

if __name__ == "__main__":
    server = Server((HOST, PORT), MAX_PLAYERS)