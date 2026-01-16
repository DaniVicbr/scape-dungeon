import pgzrun
import random


TILE_SIZE = 64

WIDTH = TILE_SIZE * 12
HEIGHT = TILE_SIZE * 9
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2 


game_state = "MENU"

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

        speed = 4

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

hero = Player("hero", CENTER_X, CENTER_Y, num_frames=5)

btn_start = GameButton(CENTER_X, CENTER_Y - 50, "btn_start", "START")
btn_exit = GameButton(CENTER_X, CENTER_Y + 50, "btn_exit", "EXIT")
buttons = [btn_start, btn_exit]

enemies = []

for i in range(10):
    en = Enemy("enemy", random.randint(50, 70), random.randint(50, 550), num_frames=6)
    enemies.append(en)

def draw():
    screen.clear()

    if game_state == "MENU": 
        screen.draw.text("Fuja dos Ratos", center=(CENTER_X, 100), fontsize=60, color="white")
        for btn in buttons:
            btn.draw()

    if game_state == "GAMEOVER":
         screen.draw.text("GAME OVER", center=(CENTER_X, CENTER_Y), fontsize=60, color="red")

    if game_state == "GAME":
        for row in range(len(map)):
            for column in range(len(map[row])):
                x = column * TILE_SIZE
                y = row * TILE_SIZE
                title = tiles[map[row][column]]
                screen.blit(title, (x,y))

        hero.draw()
        for enemy in enemies:
            enemy.draw()


def update():
    global game_state

    if game_state == "GAME":
        hero.update()
    
        for enemy in enemies:
            enemy.update()

            if hero.actor.colliderect(enemy.actor):
                game_state = "GAMEOVER"

def on_mouse_down(pos):
    global game_state

    if game_state == "MENU":
        for btn in buttons:
            action = btn.check_click(pos)
            if action == "START":
                game_state = "GAME"
            elif action == "EXIT":
                quit()

pgzrun.go()



