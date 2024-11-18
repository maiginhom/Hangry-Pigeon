import pygame
import sys

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Screen dimensions and colors
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# sound effect
pygame.mixer.music.load('pokemon_route.mp3')
pygame.mixer.music.play(-1)  # Start playing in a loop
pygame.mixer.music.set_volume(0.5) 

start_sound = pygame.mixer.Sound('gamestart.mp3')
gameover_sound = pygame.mixer.Sound('gameover.mp3')
fall_sound = pygame.mixer.Sound('bump.mp3')
win_sound = pygame.mixer.Sound('victory.mp3')
pigeon_sound = pygame.mixer.Sound('pidgeot.mp3')
cry_sound = pygame.mixer.Sound('cry.mp3')

# Load bg images
background_image = pygame.image.load('background.png')
terrain_image = pygame.image.load('terrain1.png')

# Load images for the start menu
logo = pygame.image.load('logo.PNG')
normal_girl = pygame.image.load('human_img.PNG')
normal_girl = pygame.transform.scale(normal_girl, (160,160))
crying_girl = pygame.image.load('humancrying_img.PNG')
crying_girl = pygame.transform.scale(crying_girl, (160,160))
pigeon_notice = pygame.image.load('pigeonnotice_img.PNG')
pigeon_notice = pygame.transform.scale(pigeon_notice, (160,160))
pigeon_normal = pygame.image.load('pigeon_img.PNG')
pigeon_normal = pygame.transform.scale(pigeon_normal, (160,160))
bgstart_image = pygame.image.load('bgmenupygame.png')
bgstart_image = pygame.transform.scale(bgstart_image, (WIDTH, HEIGHT))
start_image = pygame.image.load('start_button.PNG')
start_rect = start_image.get_rect(center=(WIDTH // 2, 275))
logo_rect = logo.get_rect(center=(WIDTH // 2, 300))

# Frame delay and animation
frame_delay = 10
current_frame = 0
is_moving = False

# Background function
def background_sky(screen, image):
    size = pygame.transform.scale(image, (WIDTH, HEIGHT))
    screen.blit(size, (0, 0))

# Start Menu Class
class StartMenu:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.clock = pygame.time.Clock()
    
    def draw_menu(self):
        global current_frame, frame_delay, is_moving
        self.screen.blit(bgstart_image, (0, 0))
        self.screen.blit(logo, logo_rect)

        # Animate
        if current_frame >= frame_delay:
            is_moving = not is_moving
            current_frame = 0
        if is_moving:
            self.screen.blit(normal_girl, (100, 350))
            self.screen.blit(pigeon_notice, (525, 350))
        else:
            self.screen.blit(crying_girl, (100, 340))
            self.screen.blit(pigeon_normal, (525, 340))
        current_frame += 1

        # Draw start button
        self.screen.blit(start_image, start_rect)
        pygame.display.flip()

    def handle_events(self): # if button click
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_rect.collidepoint(event.pos):
                    start_sound.play()
                    self.running = False  # End menu loop to start game

    def run(self):
        while self.running:
            self.handle_events()
            self.draw_menu()
            self.clock.tick(60)

# Global settings
gravity = 0.5
log_width, log_height = 150, 15
block_size = 120
human_width, human_height = 120, 120
pigeon_width, pigeon_height = 120, 120  
food_width, food_height = 75, 75
button_width, button_height = 150, 40
cage_width, cage_height = 120, 120
human_move_speed = 5
terrain_height = 81  

# Classes
class Terrain:
    def __init__(self, pos, width, height, image):
        self.rect = pygame.Rect(*pos, width, height)
        self.image = pygame.transform.scale(image, (width, height))

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)


class Block: # block=cage
    def __init__(self, pos, block_type="human"):
        self.pos = pos
        self.block_type = block_type  # separate the cage above human and pigeon
        self.image = pygame.image.load('cage.png')
        self.image = pygame.transform.scale(self.image, (cage_width, cage_height))
        self.velocity = 0
        self.static = True  # cage fall when pin moved

    def apply_gravity(self, terrain):
        global fall_sound
        if not self.static and not self.pos[1] + cage_height >= terrain.rect.top:
            self.velocity += gravity
            self.pos[1] += self.velocity
            if self.pos[1] + cage_height >= terrain.rect.top:
                self.pos[1] = terrain.rect.top - cage_height 
                self.velocity = 0
                self.static = True  # Stop block when it hits the terrain

    def draw(self, screen):
        screen.blit(self.image, self.pos)
        

class Log:  # the naew-non one
    def __init__(self, pos):
        self.pos = pos
        self.active = True
        self.image = pygame.image.load('log_image.png')
        self.image = pygame.transform.scale(self.image, (log_width, log_height))  # resize

    def draw(self, screen):
        if self.active:
            screen.blit(self.image, self.pos) # Draw log (image, position)


class Pin: # the naew-tang one
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 15, 150)
        self.clicked = False
        self.image = pygame.image.load('pin_image.png')
        self.image = pygame.transform.scale(self.image, (15, 150))

    def move_up(self):
        if not self.clicked:
            self.rect.y -= 90
            self.clicked = True

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)


class Human:
    def __init__(self, pos):
        self.pos = pos # postion
        self.image = pygame.image.load('human_img.png')
        self.image = pygame.transform.scale(self.image, (human_width, human_height))

    def move_right(self):
        self.pos[0] += human_move_speed
        self.image = pygame.image.load('humanwalk_img.png')
        self.image = pygame.transform.scale(self.image, (human_width, human_height))

    def happy(self):
        self.image = pygame.image.load('humanhappy_img.png')
        self.image = pygame.transform.scale(self.image, (human_width, human_height))

    def sad(self):
        self.image = pygame.image.load('humancrying_img.png')
        self.image = pygame.transform.scale(self.image, (human_width, human_height))

    def draw(self, screen):
        screen.blit(self.image, self.pos) # Draw human


class Pigeon:
    def __init__(self, pos):
        self.pos = pos
        self.image = pygame.image.load('pigeon_img.png')
        self.image = pygame.transform.scale(self.image, (pigeon_width, pigeon_height))
        self.original_image = self.image  # waii flip
        self.blocked = False  # To check if pigeon is blocked

    def check_blocked(self, blocks):
        # Check if the pigeon is blocked by any falling block
        pigeon_rect = pygame.Rect(*self.pos, pigeon_width, pigeon_height)
        self.blocked = False  # pigeon is not blocked
        for block in blocks:
            block_rect = pygame.Rect(*block.pos, cage_width, cage_height)
            if pigeon_rect.colliderect(block_rect):
                self.blocked = True
                break  # Stop checking

    def move_towards_food(self, food_rect, blocks):
        # Move the pigeon towards the food if it's not blocked
        if self.blocked:
            return  # If the pigeon is blocked, don't move
        if self.pos[0] < food_rect.left - 75:
            self.pos[0] += 2  # Move right
            self.flip()  # Flip the pigeon when it moves towards the food
        elif self.pos[0] > food_rect.right + 75:
            self.pos[0] -= 2  # Move left7
            self.flip()  # Flip the pigeon when it moves towards the food
        if self.pos[0] >= food_rect.left - 75: # Pigeon eat the food when it reached
            self.eat()

    def eat(self):
        self.image = pygame.image.load('pigeoneating_img.png')
        self.image = pygame.transform.scale(self.image, (pigeon_width, pigeon_height))

    def notice(self):
        self.image = pygame.image.load('pigeonnotice_img.png')
        self.image = pygame.transform.scale(self.image, (pigeon_width, pigeon_height))

    def knife(self):
        self.image = pygame.image.load('pigeonknife_img.png')
        self.image = pygame.transform.scale(self.image, (pigeon_width, pigeon_height))

    def flip(self):
        # Flip the pigeon image horizontally
        self.image = pygame.transform.flip(self.original_image, True, False)

    def draw(self, screen):
        screen.blit(self.image, self.pos)
        

class Food:
    def __init__(self, pos):
        self.pos = pos
        self.image = pygame.image.load('food_img.png')
        self.image = pygame.transform.scale(self.image, (food_width, food_height))

    def draw(self, screen):
        screen.blit(self.image, self.pos)
    

class Game:
    def __init__(self):
        # set defualt
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Hangry Pigeon")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False
        self.win = False

         # Original positions for reset
        self.terrain = Terrain((0, HEIGHT - terrain_height), WIDTH, terrain_height, terrain_image)
        self.original_block_positions = [[WIDTH // 4 - block_size // 2, HEIGHT - 347], [3 * WIDTH // 5 - block_size // 2, HEIGHT - 423]]
        self.original_log_positions = [(WIDTH // 4 - log_width // 2, HEIGHT - 235),(3 * WIDTH // 5 - log_width // 2, HEIGHT - 310)]
        self.original_human_position = [WIDTH // 4 - human_width // 2, HEIGHT - terrain_height - human_height + 17]
        self.original_pigeon_position = [3 * WIDTH // 5 - 70, HEIGHT - terrain_height - pigeon_height + 17]
        self.original_food_position = [3 * WIDTH // 4 , HEIGHT - terrain_height - food_height]
        
        # pin position
        self.original_second_pin_position = [WIDTH // 2 + 150, HEIGHT - terrain_height - food_height - 75] #betweeen pigeon and food
        self.original_pin_position = [WIDTH // 2 - 30, (self.original_human_position[1] + self.original_pigeon_position[1]) // 2 - 50] #betwwen pigeon and human

        #set page for different situation
        self.game_over_image = pygame.image.load('gameover_image.png')
        self.win_image = pygame.image.load('win_image.png')

        # reset game
        self.reset_game()

    def reset_game(self):
        pygame.mixer.music.play(-1) # bg music on loop 
        # set everything to original postition
        self.blocks = [Block(self.original_block_positions[0].copy(), block_type="human"), Block(self.original_block_positions[1].copy(), block_type="pigeon") ]
        self.logs = [Log(pos) for pos in self.original_log_positions]
        self.human_left = Human(self.original_human_position.copy())
        self.pigeon_right = Pigeon(self.original_pigeon_position.copy())
        self.food_right = Food(self.original_food_position.copy())
        self.pin = Pin(*self.original_pin_position)
        self.second_pin = Pin(*self.original_second_pin_position)  # New pin
        self.terrain = Terrain((0, HEIGHT - terrain_height), WIDTH, terrain_height, terrain_image)
        
        # Reset game state
        self.game_over = False
        self.win=False
        self.second_pin_clicked = False  # Track if the second pin is clicked
        self.first_pin_clicked = False   # Track if the first pin is clicked
        self.human_moves_towards_food = False  # Flag for when human should move towards food

    def check_collisions(self):
        # Check if the pigeon reached the food
        pigeon_rect = pygame.Rect(*self.pigeon_right.pos, pigeon_width, pigeon_height)
        food_rect = pygame.Rect(*self.food_right.pos, food_width, food_height)

        # If pigeon eat food, game over
        if pigeon_rect.colliderect(food_rect):
            self.human_left.sad()
            pigeon_sound.play()
            self.game_over = True

        # Check if a block falls onto human
        human_rect = pygame.Rect(*self.human_left.pos, human_width, human_height)

        for block in self.blocks:
            block.apply_gravity(self.terrain)  # apply gravity to block
            block_rect = pygame.Rect(*block.pos, cage_width, cage_height)

            # only the cage above human can effect human
            if block.block_type == "human" and block_rect.colliderect(human_rect):
                self.human_left.sad()
                self.game_over = True

            # Pigeon cage affects only the pigeon
            if block.block_type == "pigeon" and block_rect.colliderect(pigeon_rect):
                self.pigeon_right.blocked = True  # Stop pigeon from moving

        # Only check for human-pigeon boom boom if the pigeon is NOT blocked
        if not self.pigeon_right.blocked and human_rect.colliderect(pigeon_rect):
            # check if the pigeon jik human
            self.pigeon_right.knife()
            pigeon_sound.play()
            self.human_left.sad()
            self.game_over = True  

        # Check if the human reaches the food
        if human_rect.colliderect(food_rect):
            self.win = True 

    def draw_game(self):
        # Draw background image
        background_sky(self.screen, background_image)

        # Draw terrain, logs, blocks, human, pigeon, pins, and food
        self.terrain.draw(self.screen)

        for log in self.logs:
            log.draw(self.screen)
        self.human_left.draw(self.screen)
        self.food_right.draw(self.screen)
        self.pigeon_right.draw(self.screen)
        for block in self.blocks:
            block.draw(self.screen)
        self.pin.draw(self.screen)
        self.second_pin.draw(self.screen)  # Draw the new pin
        
        # Game over, show the gameover logo and retry button
        if self.game_over:
            self.screen.blit(self.game_over_image,(0,0))
            pygame.draw.rect(self.screen, BLACK, (WIDTH // 2 - button_width // 2, HEIGHT // 2 - button_height // 2, button_width, button_height))
            font = pygame.font.Font(None, 36)
            text = font.render("Retry", True, WHITE)
            self.screen.blit(text, (WIDTH // 2 - 30, HEIGHT // 2 - 15))
            pygame.mixer.music.stop()
            cry_sound.play()
            gameover_sound.play()

        # Game win
        if self.win:
            self.screen.blit(self.win_image,(0,0))
            pygame.mixer.music.stop()
            win_sound.play()

        pygame.display.flip()

    def handle_events(self): # to check the if the pin/log on-click
        global fall_sound

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if self.pin.rect.collidepoint(mouse_pos): # Check for second pin
                    self.pin.move_up()
                    fall_sound.play()
                    self.first_pin_clicked = True  # first pin as clicked
                if self.second_pin.rect.collidepoint(mouse_pos):  
                    fall_sound.play()
                    self.second_pin.move_up()
                    self.second_pin_clicked = True 
                if self.game_over: 
                    retry_button = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 - button_height // 2, button_width, button_height)
                    if retry_button.collidepoint(mouse_pos):
                        self.reset_game()
                else:
                    for i, log in enumerate(self.logs): # check logs
                        log_rect = pygame.Rect(*log.pos, log_width, log_height)
                        if log_rect.collidepoint(mouse_pos) and log.active:
                            fall_sound.play()
                            log.active = False
                            self.blocks[i].static = False
                            
    def run(self):
        while self.running:
            self.handle_events()
            # human move if the first pin click
            if self.first_pin_clicked and self.human_left.pos[0] < self.pigeon_right.pos[0]-75:
                self.pigeon_right.notice()
                self.human_left.move_right()

            # pigeon move if the second pin click
            if self.second_pin_clicked:
                # if pigeon blocked by cage if can't move
                self.pigeon_right.check_blocked(self.blocks)
                # pigeon move if if not blocked
                food_rect = pygame.Rect(*self.food_right.pos, food_width, food_height)
                self.pigeon_right.move_towards_food(food_rect, self.blocks)
                # human to continue moving towards the food if the first pin was clicked
                if self.first_pin_clicked and self.human_left.pos[0] < self.food_right.pos[0]-75:
                    self.human_left.move_right()
                    self.human_left.happy()

            self.check_collisions()  # Check for collisions (block falling on human, pigeon reaching food, human walking into pigeon)
            self.draw_game()
            self.clock.tick(30)

# Main program
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Hangry Pigeon")

    # Show the start menu
    start_menu = StartMenu(screen)
    start_menu.run()

    # Run the main game
    game = Game()
    game.run()

if __name__ == '__main__':
    main()
