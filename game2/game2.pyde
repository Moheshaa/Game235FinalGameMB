#-----PARTICLE CLASS-----
class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 5
        self.lifespan = 255

    def update(self):
        self.y -= 2
        self.lifespan -= 5

    def draw(self):
        fill(255, self.lifespan)
        ellipse(self.x, self.y, self.size, self.size)
        fill(255)
        
# -----PLAYER CLASS-----
class Player:
    def __init__(self):
        self.size = 30
        #self.x_pos = width // 2  # Initial x position
        self.lives = 3

    def update(self):
         self.x_pos = constrain(mouseX, 15, width - 15)

    def draw(self):
        image(player_image, self.x_pos, height - 50, self.size, self.size)
    

#-----BULLET CLASS-----
class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 5
        self.height = 10

    def draw(self):
        rect(self.x, self.y, self.width, self.height)

#-----ENEMY CLASS-----
class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 30

    def draw(self):
        image(enemy_image, self.x, self.y, self.size, self.size)

#-----TREASURE BOX CLASS-----
class TreasureBox:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 30

    def draw(self):
        image(treasure_box_image, self.x, self.y, self.size, self.size)


# -----GLOBAL VARIABLES-----
title_screen = True
player = Player()
bullets = []
enemies = []
treasure_boxes = []
particles = []
score = 0
game_over_triggered = False

#-----SETUP FUNCTION-----
def setup():
    size(800, 600)
    textAlign(CENTER, CENTER)
    textSize(50)
    #--Images--
    global title_screen_background, enemy_image, player_image, treasure_box_image
    title_screen_background = loadImage("1.png")
    enemy_image = loadImage("2.png")
    player_image = loadImage("3.png")
    treasure_box_image = loadImage("4.png")
    title_screen_background.resize(width, height)
    enemy_image.resize(30, 30)
    player_image.resize(30, 30)
    treasure_box_image.resize(30, 30)

#----- DRAW TITLE SCREEN FUNCTION-----
def draw_title_screen():
    image(title_screen_background, 0, 0)  # Draw the background image
    text("Kill 'em all!", width/2, height/2)
    textSize(25)
    text("Press A to start", width/2, height/2 + 50)
    textSize(50)

# -----DRAW GAME SCREEN FUNCTION-----
def draw_game_screen():
    if player.lives > 0:
        player.update()
        # Draw the background image
        image(title_screen_background, 0, 0)
        draw_particles()
        draw_bullets()
        draw_enemies()
        draw_treasure_boxes()
        player.draw()
        draw_score()
        draw_lives()
    else:
        draw_game_over_screen()

    
# -----DRAW LIVES FUNCTION-----
def draw_lives():
    fill(255)
    textSize(20)
    text("Lives: " + str(player.lives), 20, 40)

#----- DRAW BULLETS FUNCTION-----
def draw_bullets():
    for bullet in bullets:
        bullet.draw()
        bullet.y -= 10

    #--Remove bullets that are off-screen--
    bullets[:] = [bullet for bullet in bullets if bullet.y > 0]

# -----DRAW ENEMIES FUNCTION-----
def draw_enemies():
    global score
    for enemy in enemies:
        enemy.draw()

        # Check for collision with bullets
        for bullet in bullets:
            if (
                bullet.x < enemy.x + 30
                and bullet.x + 5 > enemy.x
                and bullet.y < enemy.y + 30
                and bullet.y + 10 > enemy.y
            ):
                enemies.remove(enemy)
                score += 1
                create_particles(enemy.x + 15, enemy.y + 15)  # Create particles at the enemy's center

# -----DRAW TREASURE BOX FUNCTION-----
def draw_treasure_boxes():
    global score, game_over_triggered
    to_remove = []  # List to store items that need to be removed
    for box in treasure_boxes:
        box.draw()

        # Check for collision with bullets
        for bullet in bullets:
            if (
                bullet.x < box.x + box.size
                and bullet.x + 5 > box.x
                and bullet.y < box.y + box.size
                and bullet.y + 10 > box.y
            ):
                to_remove.append(box)
                score += 1
                player.lives -= 1  # Player loses a life when hitting a treasure box
                create_particles(box.x + box.size / 2, box.y + box.size / 2)  # Create particles at the box's center
                
                # Check if lives are 0 and trigger game over
                if player.lives == 0 and not game_over_triggered:
                    print("check1")
                    game_over_triggered = True
                    game_over()
                    draw_game_over_screen()  # Switch to the game over screen

    
    # Remove items after the iteration is complete
    for item in to_remove:
        if len(treasure_boxes)>0:
            treasure_boxes.remove(item)
        
        
                    
# -----GAME OVER FUNCTION-----
def game_over():
    global title_screen, player, bullets, enemies, treasure_boxes, particles, score, game_over_triggered
    bullets = []
    enemies = []
    treasure_boxes = []
    particles = []
    #score = 0


            
# -----DRAW GAME OVER SCREEN FUNCTION-----
def draw_game_over_screen():
    image(title_screen_background, 0, 0)  # Draw the background image
    textSize(50)
    fill(255)
    text("Game Over", width/2, height/2 - 50)
    textSize(25)
    text("Score: " + str(score), width/2, height/2)
    text("Press R to restart", width/2, height/2 + 50)
                
# -----CREATE PARTICLES FUNCTION-----
def create_particles(x, y):
    global particles
    for _ in range(50):  # Adjust the number of particles as needed
        particles.append(Particle(x, y))

def draw_particles():
    global particles
    for particle in particles:
        particle.update()
        particle.draw()

    particles = [particle for particle in particles if particle.lifespan > 0]

#-----SCORE FUNCTION-----
def draw_score():
    textSize(20)
    text("Score: " + str(score), 20, 20)

# -----KEYPRESSES-----
def keyPressed():
    global title_screen, game_over_triggered, bullets, score

    if title_screen:
        if key == 'a' or key == 'A':
            title_screen = not title_screen
    else:
        if key == 'r' or key == 'R':
            game_over_triggered = False
            player.lives = 3
            bullets = []
            enemies = []
            treasure_boxes = []
            particles = []
            score = 0
            title_screen = True
        elif keyCode == UP:
            bullets.append(Bullet(player.x_pos + player.size/2, height - 50))




#-----DRAW-----
def draw():

    if title_screen:
        draw_title_screen()
    elif game_over_triggered:
        draw_game_over_screen()
        
    else:
        draw_game_screen()

        # Generate a new enemy randomly
        if random(1) < 0.02:  # The probability of enemy
            enemies.append(Enemy(random(50, width - 50), random(height - 200)))

        # Generate a new treasure box randomly with lower probability
        if random(1) < 0.005:  # The probability of treasure boxes
            treasure_boxes.append(TreasureBox(random(50, width-50), random(height - 200)))
