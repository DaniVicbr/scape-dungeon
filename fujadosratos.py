import pgzrun
import random


TILE_SIZE = 64

WIDTH = TILE_SIZE * 12
HEIGHT = TILE_SIZE * 9
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2 
TITLE = "RAT SLAYER"

game_state = "MENU"
image_name = "gameoverimg"
actorimg = Actor(image_name, center=(CENTER_X, CENTER_Y))
menuimg = Actor("menuimg", center=(CENTER_X, CENTER_Y))

class GameButton: 
    def __init__(self, x, y, image, action_name):
        self.actor = Actor(image, center=(x,y))
        self.action_name = action_name
 
    def draw(self):
        self.actor.draw()

    def check_click(self, pos):
        if self.actor.collidepoint(pos):
            return self.action_name
        return None


tiles = ["tile001", "tile002", "tile003", "tile004", "tile005", "tile006", "key", "door"]

map = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

class GameObject: 
    def __init__(self, image_base, x, y, num_frames):
        self.direction = "down"
        self.actor = Actor(f"{image_base}_walk{self.direction}_0", (x, y))
        self.x = x 
        self.y = y
        self.image_base = image_base
        self.num_frames = num_frames

        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = 10
        self.is_moving = False

    def animate(self): 

        self.animation_timer += 1
        
        if self.is_moving:
            action = "walk" 
        else:
            "idle"

        if self.animation_timer > self.animation_speed: 
            self.animation_timer = 0

            self.frame_index +=1 

            self.frame_index = self.frame_index % self.num_frames

            try: 
                img_name = f"{self.image_base}_{action}{self.direction}_{self.frame_index}"
                self.actor.image = img_name
            except:
                pass

    def draw(self):
        self.actor.draw()

class Player(GameObject):
    def update(self):
        self.is_moving = False

        speed = 4.5

        if keyboard.left or keyboard.a and self.actor.left > 0:
            self.actor.x -= speed
            self.is_moving = True
            self.direction = "left"
        if keyboard.right or keyboard.d and self.actor.right < WIDTH:
            self.actor.x += speed 
            self.is_moving = True
            self.direction = "right"
        if keyboard.up or keyboard.w and self.actor.top > 0:
            self.actor.y -= speed
            self.is_moving = True
            self.direction = "up"
        if keyboard.down or keyboard.s and self.actor.bottom < HEIGHT:
            self.actor.y += speed 
            self.is_moving = True
            self.direction = "down"
        
        self.animate()

class Enemy(GameObject):
    def __init__(self, image_base, x, y, num_frames):
        super().__init__(image_base, x, y, num_frames)
        
        self.move_timer = 0     
        self.current_action = 0  
        
    def update(self):
        speed = 6 
        

        self.move_timer -= 1
        

        if self.move_timer <= 0:

            self.current_action = random.randint(0, 4)
        
            self.move_timer = random.randint(30, 120)
      
        self.is_moving = True 
        
        if self.current_action == 0:

            self.is_moving = False
            
        elif self.current_action == 1 and self.actor.top > 0:
            self.actor.y -= speed
            self.direction = "up"
            
        elif self.current_action == 2 and self.actor.bottom < HEIGHT:
            self.actor.y += speed
            self.direction = "down"
            
        elif self.current_action == 3 and self.actor.left > 0:
            self.actor.x -= speed
            # self.direction = "left" 
            
        elif self.current_action == 4 and self.actor.right < WIDTH:
            self.actor.x += speed
            # self.direction = "right"
            
        self.animate()

class Itens():
    def __init__(self, item_name, x, y):
        self.actor = Actor(f"{item_name}", center=(x, y))
        self.item_name = item_name
        self.x = x 
        self.y = y

    def draw(self):
        self.actor.draw()


hero = Player("hero", CENTER_X, CENTER_Y, num_frames=5)
coin = Itens("coin", CENTER_X + 200, CENTER_Y + 200)

btn_start = GameButton(CENTER_X - 150, CENTER_Y + 200, "btn_start", "START")
btn_exit = GameButton(CENTER_X + 150, CENTER_Y + 200, "btn_exit", "EXIT")
btn_continue = GameButton(CENTER_X, HEIGHT - 80, "btn_continue", "CONTINUE")
buttons = [btn_start, btn_exit]

enemies = []

for i in range(10):
    en = Enemy("enemy", random.randint(50, 70), random.randint(50, 550), num_frames=6)
    enemies.append(en)

def reset_game():
    hero.actor.x = CENTER_X
    hero.actor.y = CENTER_Y

    for enemy in enemies:
        enemy.actor.x = random.randint(20, 30)
        enemy.actor.y = random.randint(20, 30)

#Funcao que desenha a posicao aleatória da moeda:
def random_coin():
    coin.actor.x = random.randint(50, WIDTH - 50)
    coin.actor.y = random.randint(50, HEIGHT - 50)

def draw():
    screen.clear()

    if game_state == "MENU": 
        screen.draw.text("Fuja dos Ratos", center=(CENTER_X, 100), fontsize=60, color="white")
        menuimg.draw()
        for btn in buttons:
            btn.draw()
            

    if game_state == "GAMEOVER":
        #  screen.draw.text("GAME OVER", center=(CENTER_X, CENTER_Y), fontsize=60, color="red")
         actorimg.draw()
         btn_continue.draw()
         music.stop()

    if game_state == "GAME":
        for row in range(len(map)):
            for column in range(len(map[row])):
                x = column * TILE_SIZE
                y = row * TILE_SIZE
                title = tiles[map[row][column]]
                screen.blit(title, (x,y))

        hero.draw()
        coin.draw()
        for enemy in enemies:
            enemy.draw()


def update():
    global game_state

    if game_state == "GAME":
        hero.update()

        if hero.actor.colliderect(coin.actor):
            random_coin()
            sounds.coin.play()

        for enemy in enemies:
            enemy.update()

            if hero.actor.colliderect(enemy.actor):
                pass
                game_state = "GAMEOVER"
                sounds.gameovervoice.play()
                sounds.scream.play()
                # sounds.leratan.play()

def on_mouse_down(pos):
    global game_state

    if game_state == "MENU":
        for btn in buttons:
            action = btn.check_click(pos)
            if action == "START":
                music.stop()
                music.play("pixelatemenu")
                reset_game()
                game_state = "GAME"
            elif action == "EXIT":
                quit()

    if game_state == "GAMEOVER":
        # music.stop()
        music.play("menu2")
        action = btn_continue.check_click(pos)
        if action == "CONTINUE":
            game_state = "MENU"
            music.play("gameovermusic")
            music.set_volume(0.8)

music.play("gameovermusic")
music.set_volume(0.8)
pgzrun.go()



