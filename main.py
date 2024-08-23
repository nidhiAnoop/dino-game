import pygame
import random
import sys
import os # for high score implementation

pygame.init() # initialize the game
screen = pygame.display.set_mode((1280 , 720)) # setting the width and height
clock = pygame.time.Clock() # initializing the clock
pygame.display.set_caption('Dino Game')


game_font = pygame.font.Font('/Users/mbpro/Desktop/dino_game/assets/PressStart2P-Regular.ttf' , 24)
small_game_font = pygame.font.Font('/Users/mbpro/Desktop/dino_game/assets/PressStart2P-Regular.ttf' , 18)
# cloud, dino, cactus, ground, ptero --> classes

# CLASSES

class Cloud(pygame.sprite.Sprite): # inheriting funtionalities from already present pygame Sprite
    def __init__(self, image, x_pos, y_pos):
        super().__init__() # taking the init method/attribute of the pygame prite class and using it or our own sprite
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.image.get_rect(center = (self.x_pos, self.y_pos)) # making a rectangle using coordinates

    def update(self):
        self.rect.x -= 1 # making the cloud move

class Dino(pygame.sprite.Sprite): # inheriting funtionalities from already present pygame Sprite
    def __init__(self, x_pos, y_pos):
        super().__init__() # taking the init method of the pygame prite class and using it or our own sprite
        self.running_sprites = []
        self.ducking_sprites = []

        self.running_sprites.append(pygame.transform.scale(
            pygame.image.load('/Users/mbpro/Desktop/dino_game/assets/Dino1.png'), (80, 100)
        )) # transforming the height an width of the dino image uning transform.scale

        self.running_sprites.append(pygame.transform.scale(
            pygame.image.load('/Users/mbpro/Desktop/dino_game/assets/Dino2.png'), (80, 100)
        )) # transforming the height an width of the dino image uning transform.scale

        self.ducking_sprites.append(pygame.transform.scale(
            pygame.image.load(f'/Users/mbpro/Desktop/dino_game/assets/DinoDucking1.png'), (110, 60)
        ))

        self.ducking_sprites.append(pygame.transform.scale(
            pygame.image.load(f'/Users/mbpro/Desktop/dino_game/assets/DinoDucking2.png'), (110, 60)
        ))

        self.x_pos = x_pos # setting x an y position
        self.y_pos = y_pos
        self.current_image = 0 # index of the sprites list. starts from 0 so we start from first image
        self.image = self.running_sprites[self.current_image]#
        self.rect = self.image.get_rect(center = (self.x_pos, self.y_pos))
        # filled the dino inside it
        self.velocity = 80# its just a constant velocity
        # increased velocity so that it stays in the air for longer
        self.gravity = 3.3
        # Decrease gravity to slow down the descent
        self.ducking = False # its a running dino image

    def jump(self):
        jump_sfx.play() # playing jump sound
        if self.rect.centery >= 360:
            while self.rect.centery - self.velocity > 40: # its keeps on jumping until the person is pressing
                self.rect.centery -= 1 #jump

    def duck(self):
        self.ducking = True # now the dino is ducking
        self.rect.centery = 380

    def unduck(self):
        self.ducking = False # running dino again
        self.rect.centery = 360

    def apply_gravity(self):
        if self.rect.centery <= 360: # dino is jumping
            self.rect.centery += self.gravity # adding gravity

    def update(self):
        self.animate()
        self.apply_gravity()

    def animate(self):
        self.current_image += 0.15  # Increase this value from 0.05 to .1 to speed up the animation and make the dino run faster
        if self.current_image >= 2: # out of the list of dinos, then go to the zero index dino again.
            self.current_image = 0
        
        if self.ducking: # if dino is a ducking dino
            self.image = self.ducking_sprites[int(self.current_image)]
        else: # if dino is a running dino
            self.image = self.running_sprites[int(self.current_image)]

class Cactus(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.sprites = [] # list to store cactus sprites

        for i in range(1,7):
            current_sprite = pygame.transform.scale(
                pygame.image.load(f"/Users/mbpro/Desktop/dino_game/assets/cacti/cactus{i}.png") , (100,100)
            )
            self.sprites.append(current_sprite)
        self.image = random.choice(self.sprites)
        self.rect = self.image.get_rect(center = (self.x_pos, self.y_pos))

    def update(self):
        self.x_pos -= game_speed
        self.rect = self.image.get_rect(center = (self.x_pos , self.y_pos))

class Ptero(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x_pos = 1300
        self.y_pos = random.choice([280, 295, 350])
        self.sprites = []

        self.sprites.append(
            pygame.transform.scale(
                pygame.image.load("/Users/mbpro/Desktop/dino_game/assets/Ptero1.png"), (84, 62)
            )
        )
        self.sprites.append(
            pygame.transform.scale(
                pygame.image.load("/Users/mbpro/Desktop/dino_game/assets/Ptero2.png"), (84, 62)
            )
        )
        self.current_image = 0
        self.image = self.sprites[self.current_image]
        self.rect = self.image.get_rect(center = (self.x_pos, self.y_pos))

    def animate(self):
        self.current_image += 0.025
        if self.current_image >= 2:
            self.current_image = 0
            
        self.image = self.sprites[int(self.current_image)]
    def update(self):
        self.animate()
        self.x_pos -= game_speed
        self.rect = self.image.get_rect(center =(self.x_pos , self.y_pos))

def display_score_and_high_score():
    # Display current player score
    player_score_surface = game_font.render(str(int(player_score)), True, "black")
    screen.blit(player_score_surface, (1150, 10))
    
    # Display high score
    high_score_surface = game_font.render(f"High Score: {high_score}", True, "black")
    screen.blit(high_score_surface, (500, 10))  # Display high score on screen



# Global variables

#jump_sfx = pygame.mixer.Sound('/Users/mbpro/Desktop/dino_game/assets/sfx/jump.mp3')
game_speed = 5
jump_count = 10
player_score = 0
high_score = 0
high_score_file = 'high_score.txt'
high_score_sound_played = False

# Load the high score from the file if it exists

if os.path.exists(high_score_file):
    with open(high_score_file, 'r') as file:
        content = file.read().strip()  # Read the file and # strip() removes unnecessary whitespaces or any other charecters
        if content:  # Check if content is not empty
            try:
                high_score = int(content)  # Try converting the content to an integer
            except ValueError:
                high_score = 0  # If conversion fails, set high score to 0

game_over = False
obstacle_timer = 0
obstacle_spawn = False
obstacle_cooldown = 1400

# Surfaces

ground = pygame.image.load("/Users/mbpro/Desktop/dino_game/assets/ground.png")
ground = pygame.transform.scale(ground, (1280, 20)) 
ground_x = 0
ground_rect = ground.get_rect(center = (640, 400))

cloud = pygame.image.load("/Users/mbpro/Desktop/dino_game/assets/cloud.png")
cloud = pygame.transform.scale(cloud, (200, 80))

# Groups

cloud_group = pygame.sprite.Group()
obstacle_group = pygame.sprite.Group()
dino_group = pygame.sprite.GroupSingle() # all dino's will be in a single group
ptero_group = pygame.sprite.Group()

# objects

dinosaur = Dino(50, 360)
dino_group.add(dinosaur)

# sounds/sfx

death_sfx = pygame.mixer.Sound("/Users/mbpro/Desktop/dino_game/assets/sfx/lose.mp3")
points_sfx = pygame.mixer.Sound("/Users/mbpro/Desktop/dino_game/assets/sfx/100points.mp3")
jump_sfx = pygame.mixer.Sound("/Users/mbpro/Desktop/dino_game/assets/sfx/jump.mp3")


# events

CLOUD_EVENT = pygame.USEREVENT # compulsory to set timer.
pygame.time.set_timer(CLOUD_EVENT, 4000) # clouds will appear on screen ever 3 secs
# clouds will come after every 3 secs on the screen


# FUNCTIONS


def end_game():
    global player_score, game_speed , high_score
    
    # Check if current score is higher than high score
    if player_score > high_score:
        high_score = int(player_score)

        # Save new high score to the text file
        with open(high_score_file , 'w') as file:
            file.write(str(high_score))


    game_over_text = game_font.render("Game Over!", True, "black")
    game_over_rect = game_over_text.get_rect(center=(640, 300))

    score_text = game_font.render(f"Score: {int(player_score)}", True, "black")
    score_rect = score_text.get_rect(center=(640, 340))
    
    ins_text = small_game_font.render("Press SPACE to restart" , True, "grey")
    ins_rect = ins_text.get_rect(center = (640 , 490))

    high_score_text = game_font.render(f"High Score: {high_score}", True, "black")
    high_score_rect = high_score_text.get_rect(center=(640, 380))

    screen.blit(game_over_text, game_over_rect)
    screen.blit(score_text, score_rect)
    screen.blit(high_score_text, high_score_rect)
    screen.blit(ins_text, ins_rect)


    game_speed = 5
    cloud_group.empty()
    obstacle_group.empty()



# infinite group
while True:
    keys = pygame.key.get_pressed() # a key got pressed by the user
    if keys[pygame.K_DOWN]: # if down arrow key is pressed dino ducks
        dinosaur.duck()
    else:
        if dinosaur.ducking:
            dinosaur.unduck()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == CLOUD_EVENT:
            current_cloud_y = random.randint(50,300) # y_pos of cloud
            current_cloud = Cloud(cloud, 1380, current_cloud_y)
            cloud_group.add(current_cloud)
        # if user pressed any key...
        if event.type == pygame.KEYDOWN:
            # if user pressed key is spacebar or up arrow key
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                dinosaur.jump()
                # restrarting if dino id dead
                if game_over:
                    game_over = False
                    game_speed = 5
                    player_score = 0

    screen.fill("white")


    # COLLISIONS
    if pygame.sprite.spritecollide(dino_group.sprite, obstacle_group, False):
        game_over = True
        death_sfx.play()

    if game_over:
        end_game()
    
    if not game_over:
        game_speed += 0.0025 # to increase speed of game and make the game more challenging
        obstacle_cooldown +=0.0005

        if round(player_score, 1) % 100 == 0 and int(player_score) >0:
            points_sfx.play()
        
        # High score sfx logic

        if player_score > high_score and not high_score_sound_played: # if high score crossed
            points_sfx.play() # Play the high score sound
            high_score_sound_played = True # ensure the sound is played only
        
        if pygame.time.get_ticks() - obstacle_timer >= obstacle_cooldown:
            obstacle_spawn = True
        
        if obstacle_spawn:
            obstacle_random = random.randint(1,50)
            if obstacle_random in range(1,7):
                new_obstacle = Cactus(1280, 340) # 340 on y axis means actual ground - 1280 means end of the screen()righmost side
                obstacle_group.add(new_obstacle)
                obstacle_timer = pygame.time.get_ticks()
                obstacle_spawn = False
            elif obstacle_random in range(7,10):
                new_obstacle = Ptero()
                obstacle_group.add(new_obstacle) # if not working change line to "obstacle_group.add(new_obstacle)"
                obstacle_timer = pygame.time.get_ticks()
                obstacle_spawn = False
        
        player_score += 0.1

        display_score_and_high_score()

        cloud_group.update()
        cloud_group.draw(screen)

        ptero_group.update()
        ptero_group.draw(screen)

        dino_group.update()
        dino_group.draw(screen)

        obstacle_group.update()
        obstacle_group.draw(screen)

        ground_x -= game_speed

        screen.blit(ground, (ground_x, 360))
        screen.blit(ground, (ground_x + 1280, 360))

        if ground_x <= -1280:
            ground_x = 0

    
    clock.tick(100) # og = 60
    pygame.display.update()
obstacle_group.empty()