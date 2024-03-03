import socket
import json
from threading import Thread, Lock
import pygame
from time import sleep

lock = Lock()

class Client:

    def __init__(self, addr):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(addr) # подключаемся к айпи адресу сервера

        self.players = [] # Создаем массив для хранения данных об игроках
        self.enemies = [] # тут враги

        Thread(target=self.get_players).start() # Делаем новый поток с циклом, в которым берем данные об игроках

    def get_players(self):
        while True:
            with lock:
                self.sock.sendall(bytes(json.dumps({
                    "request": "get_players"
                    #"bullets": 
                }), 'UTF-8')) # Отправляем серверу запрос для получения игроков

            with lock:  # Используем блокировку при доступе к ресурсу
                received = json.loads(self.sock.recv(4096).decode('UTF-8'))
                self.players = received["players"]
                self.enemies = received["enemies"]

            sleep(1/30)


    def move(self, side):
        with lock:  # Используем блокировку при доступе к ресурсу
            self.sock.sendall(bytes(json.dumps(
                {"request": "move", 
                "move": side}), 
                'UTF-8'))
        sleep(1/30)
    def sendBullets(self, bullets):
        with lock:
                self.sock.sendall(bytes(json.dumps({
                    "request": "bullets",
                    "bullets": bullets
                }), 'UTF-8'))

# Создаем класс, который взаимствован от класса Sprite внутри pygame
class Player(pygame.sprite.Sprite):

    # Инициализация
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)

        # Загружаем спрайт игрока
        self.image = pygame.transform.scale(pygame.image.load("src/rocket.png"), (40, 60))
        self.rect = self.image.get_rect(center=pos)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)

        # Загружаем спрайт игрока
        self.image = pygame.transform.scale(pygame.image.load("src/ufo.png"), (80, 40))
        self.rect = self.image.get_rect(center=pos)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)

        # Загружаем спрайт игрока
        self.image = pygame.transform.scale(pygame.image.load("src/bullet.png"), (20, 60))
        self.rect = self.image.get_rect(center=pos)
