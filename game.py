from pygame import *
from client import Client, Player, Enemy

init() # Инициализируем pygame

HOST, PORT = "26.175.0.122", 8080 # Адрес сервера

client = Client((HOST, PORT)) # Создаем объект клиента

enemies = sprite.Group()
bullets = sprite.Group()

for i in range(0, 6):
    newEnemy = Enemy([-500, -500])
    enemies.add(newEnemy)


sсreen = display.set_mode((800, 600)) # Создаем окно с разрешением 800x600
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'), (800, 600))
clock = time.Clock() # Создаем объект для работы со временем внутри игры
tick = 0
last_tick = 0

while True:
    for e in event.get():
        if e.type == QUIT:
            client.sock.close()
            exit()

    buttons = key.get_pressed()
    if buttons[K_a]:
        client.move("left")
    elif buttons[K_d]:
        client.move("right")
    # elif buttons[K_SPACE] and clock.get_ticks()-last_tick >= 15:
    #     last_tick = tick
    #     bullets.add(Bullet(, 550))

    sсreen.blit(background, (0,0))
    # if bullets:
        
    enemies.empty()
    for i in client.enemies:
        new = Enemy(pos=i)
        enemies.add(new)
    enemies.draw(sсreen)
    for i in client.players:
        player = Player((i["x"], 550))
        collides = sprite.spritecollide(player, enemies, True)
        if collides:
            client.sock.close()
            exit()
        sсreen.blit(player.image, player.rect) # Рисуем игрока

    if tick >= 100000:
        tick = 0
    tick += 1

    display.update() # Обновляем дисплей
 
    clock.tick(30) # Ограничиваем частоту кадров игры до 60
    
