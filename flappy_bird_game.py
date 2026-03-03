import pygame
from pygame.locals import *
import random
import os

pygame.init()
pygame.mixer.init()

window_screen_width = 864
window_screen_height = 936

window_screen = pygame.display.set_mode((window_screen_width, window_screen_height))
pygame.display.set_caption('Flappy Bird')

font = pygame.font.SysFont('Bauhaus 93', 60)
score_font = pygame.font.SysFont('Bauhaus 93', 60)
color_white = (255, 255, 255)

clock = pygame.time.Clock()
frames_per_second = 60
scroll_ground = 0
scroll_speed = 4
flying_movement = False
game_ends = False
pipe_gap = 150
pipe_frequency_speed = 1500
last_pipe_created = pygame.time.get_ticks() - pipe_frequency_speed
user_score = 0
user_pass_pipe = False

bird_selected = False
selected_color = 'blue'

background_day = pygame.image.load('flappy_bird_asset_pack/flappy_bird_img_assets/day_background_img.png')
background_day = pygame.transform.scale(background_day, (window_screen_width, window_screen_height))

background_night = pygame.image.load('flappy_bird_asset_pack/flappy_bird_img_assets/night_background_img.png')
background_night = pygame.transform.scale(background_night, (window_screen_width, window_screen_height))

background_options = [background_day, background_night]
background_image = random.choice(background_options)

ground_image = pygame.image.load('flappy_bird_asset_pack/flappy_bird_img_assets/ground_img.png')
button_image = pygame.image.load('flappy_bird_asset_pack/flappy_bird_img_assets/restart_button_img.png')
instruction_manual_image = pygame.image.load('flappy_bird_asset_pack/flappy_bird_img_assets/user_manual_img.png')
game_over_image = pygame.image.load('flappy_bird_asset_pack/flappy_bird_img_assets/game_over_img.png')

flap_sound = pygame.mixer.Sound('flappy_bird_asset_pack/flappy_bird_sound_assets/audio_wing.wav')
hit_sound = pygame.mixer.Sound('flappy_bird_asset_pack/flappy_bird_sound_assets/audio_hit.wav')
dead_sound = pygame.mixer.Sound('flappy_bird_asset_pack/flappy_bird_sound_assets/audio_die.wav')
score_sound = pygame.mixer.Sound('flappy_bird_asset_pack/flappy_bird_sound_assets/audio_point.wav')

high_score_file = 'high_score.txt'

if os.path.exists(high_score_file):
    
    with open(high_score_file, 'r') as new_file:
        
        high_score = int(new_file.read())

else:
    
    high_score = 0

def draw_text(text, font, text_color, x_axis, y_axis, center = False):
    
    image = font.render(text, True, text_color)
    
    if center:
        x_axis = (window_screen_height // 2) - (image.get_width() // 2)
    window_screen.blit(image, (x_axis, y_axis))

def reset_game():
    
    global background_image
    background_image = random.choice(background_options)
    
    pipe_group.empty()
    bird_group.empty()
    
    return 0

class bird(pygame.sprite.Sprite):
    
    def __init__(self, x, y, color):
        
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        
        for num in range(1, 4):
            
            flappy_bird_image = pygame.image.load(f'flappy_bird_asset_pack/flappy_bird_img_assets/{color}_bird_anim{num}_img.png')
            self.images.append(flappy_bird_image)
        
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        
        self.velocity = 0
        self.clicked = False
    
    def update(self):
        
        if flying_movement == True:
            
            self.velocity += 0.5
            
            if self.velocity > 8:
                
                self.velocity = 8
            
            if self.rect.bottom < 768:
                
                self.rect.y += int(self.velocity)
        
        if game_ends == False:
            
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                
                self.clicked = True
                self.velocity = -10
                flap_sound.play()
            
            if pygame.mouse.get_pressed()[0] == 0:
                
                self.clicked = False
            
            self.counter += 1
            flap_cooldown = 5
            
            if self.counter > flap_cooldown:
                
                self.counter = 0
                self.index += 1
                
                if self.index >= len(self.images):
                    
                    self.index = 0
            
            self.image = self.images[self.index]
            
            self.image = pygame.transform.rotate(self.images[self.index], self.velocity * -2)

        else:
            
            self.image = pygame.transform.rotate(self.images[self.index], -90)

class pipe(pygame.sprite.Sprite):
    
    def __init__(self, x, y, position):
        
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('flappy_bird_asset_pack/flappy_bird_img_assets/pipe_img.png') 
        self.rect = self.image.get_rect()
        
        if position == 1:
            
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        
        if position == -1:
            
            self.rect.topleft = [x, y + int(pipe_gap / 2)]
    
    def update(self):
        
        self.rect.x -= scroll_speed
        
        if self.rect.right < 0:
            
            self.kill()

class button():
    
    def __init__(self, x, y, image):
        
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
    def draw(self):
        
        user_action = False
        
        mouse_position = pygame.mouse.get_pos()
        
        if self.rect.collidepoint(mouse_position):
            
            if pygame.mouse.get_pressed()[0] == 1:
                
                user_action = True
        
        window_screen.blit(self.image, (self.rect.x, self.rect.y))
        
        return user_action

def bird_selection():
    
    window_screen.blit(background_image, (0, 0))
    draw_text('CHOOSE BIRD', font, color_white, 0, 150, center = True)

    colors = ['blue', 'red', 'yellow']
    
    positions = [window_screen_width // 4, window_screen_width //2, (window_screen_width // 4) * 3]
    rects = []
    
    for i, color in enumerate(colors):
        
        bird_image = pygame.image.load(f'flappy_bird_asset_pack/flappy_bird_img_assets/{color}_bird_anim1_img.png')
        bird_rect = bird_image.get_rect(center = (positions[i], 468))
        window_screen.blit(bird_image, bird_rect)
        rects.append((bird_rect, color))
    
    return rects

bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()
restart_button = button(window_screen_width // 2 - 50, window_screen_height // 2 - 100, button_image)

run_window = True

while run_window:
    
    clock.tick(frames_per_second)
    
    
    if bird_selected == False:
        
        selection_rects = bird_selection()
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                
                run_window = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                for rect, color in selection_rects:
                    
                    if rect.collidepoint(event.pos):
                        
                        flappy_bird = bird(100, int(window_screen_height / 2), color)
                        bird_group.add(flappy_bird)
                        bird_selected = True
    
    else:
        
        window_screen.blit(background_image, (0, 0))
    
        bird_group.draw(window_screen)
        bird_group.update()
        pipe_group.draw(window_screen)
        
        window_screen.blit(ground_image, (scroll_ground, 768))

        if flying_movement == False and game_ends == False:
            
            instantiate_x_axis = (window_screen_width // 2) - (instruction_manual_image.get_width() // 2)
            window_screen.blit(instruction_manual_image, (instantiate_x_axis, window_screen_height // 2 - 150))

        if len(pipe_group) > 0:
            
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right and user_pass_pipe == False:
                
                user_pass_pipe = True
            
            if user_pass_pipe == True:
                
                if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                    
                    user_score += 1
                    score_sound.play()
                    user_pass_pipe = False

        draw_text(str(user_score), font, color_white, 0, 20, center = True)

        if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy_bird.rect.top < 0:
            
            if game_ends == False:
                
                hit_sound.play()
            
                if user_score > high_score:
                    
                    high_score = user_score
                    
                    with open(high_score_file, 'w') as new_file:
                        
                        new_file.write(str(high_score))
            
            game_ends = True

        if flappy_bird.rect.bottom >= 768:
            
            if game_ends == False:
                
                dead_sound.play()
                
                if user_score > high_score:
                    
                    high_score = user_score
                    
                    with open(high_score_file, 'w') as new_file:
                        
                        new_file.write(str(high_score))
            
            game_ends = True
            flying_movement = False
        
        if game_ends == False and flying_movement == True:
            
            time_now = pygame.time.get_ticks()
            
            if time_now - last_pipe_created > pipe_frequency_speed:
                
                pipe_height = random.randint(-100, 100)
                
                bottom_pipe = pipe(window_screen_width, int(window_screen_height / 2) + pipe_height, -1)
                top_pipe = pipe(window_screen_width, int(window_screen_height / 2) + pipe_height, 1)

                pipe_group.add(bottom_pipe)
                pipe_group.add(top_pipe)
                
                last_pipe_created = time_now
            
            scroll_ground -= scroll_speed
            
            if abs(scroll_ground) > 35:
                
                scroll_ground = 0
                
            pipe_group.update()

        if game_ends == True:
            
            game_over_x_axis = (window_screen_width // 2) - (game_over_image.get_width() // 2)
            window_screen.blit(game_over_image, (game_over_x_axis, window_screen_height // 2 - 300))
            
            draw_text(f'HIGH SCORE: {high_score}', score_font, color_white, 0, window_screen_height // 3 - 50, center = True)
            
            restart_button.rect.x = (window_screen_width // 2) - (button_image.get_width() // 2)
            
            if restart_button.draw() == True:
                
                game_ends = False
                user_score = reset_game()
                bird_selected = False

        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                
                run_window = False
            
            if event.type == pygame.MOUSEBUTTONDOWN and flying_movement == False and game_ends == False:
                
                flying_movement = True

    pygame.display.update()

pygame.quit()