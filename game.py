from pygame import *
from client import Client, Player, Enemy, Bullet
import traceback

init() # Инициализируем pygame

HOST, PORT = "109.191.136.194", 8080 # Адрес сервера - 109.191.136.194

client = Client((HOST, PORT)) # Создаем объект клиента

print(client.me)

enemies = sprite.Group()
bullets = sprite.Group()

for i in range(0, 6):
    newEnemy = Enemy([-500, -500])
    enemies.add(newEnemy)



for p in client.players:
    print(client.me, "me")
    print(p["id"], "id")
    if p["id"][0] == client.me:
        print("got me")
        me = Player((p["x"], 550))
        break

screen = display.set_mode((800, 600)) # Создаем окно с разрешением 800x600
display.set_caption('Шутер')
background = transform.scale(image.load('textures\\galaxy.jpg'), (800, 600))
clock = time.Clock() # Создаем объект для работы со временем внутри игры
tick = 0
last_tick = 0

while True:
    try:
        for e in event.get():
            if e.type == QUIT:
                client.sock.close()
                exit()

        buttons = key.get_pressed()
        if buttons[K_a]:
            client.move("left")
        elif buttons[K_d]:
            client.move("right")
        elif buttons[K_SPACE] and tick-last_tick >= 5:
            last_tick = tick
            for p in client.players:
                if p["id"][0] == client.me:
                    pos = (p["x"], p["y"])
            bullets.add(Bullet((pos[0], pos[1])))
            print('shot')

        screen.blit(background, (0,0))

        if bullets:
            for bullet in bullets:
                client.bullets.append(bullet.pos)
            client.sendBullets(bullets)

        enemies.empty()
        for i in client.enemies:
            new = Enemy(pos=i)
            enemies.add(new)
        enemies.draw(screen)

        bullets.empty()
        for bulletPos in client.bullets:
            newBullet = Bullet(pos=bulletPos)
            bullets.add(newBullet)
            for bullet in bullets:
                bullet.update()  # Обновление позиции пули
            print(bullets)

        bullets.draw(screen)

        for i in client.players:
            player = Player((i["x"], 550))
            collides = sprite.spritecollide(player, enemies, True)
            if collides:
                client.sock.close()
                exit()
            screen.blit(player.image, player.rect) # Рисуем игрока

        if tick >= 100000:
            tick = 0
        tick += 1

        display.update() # Обновляем дисплей
     
        clock.tick(30) # Ограничиваем частоту кадров игры до 60
    except Exception as e:
        traceback.print_exc()
        break
