import pygame
from pygame.locals import *
import random

pygame.init()

window_screen_width = 864
window_screen_height = 936

window_screen = pygame.display.set_mode((window_screen_width, window_screen_height))
pygame.display.set_caption('Flappy Bird')

font = pygame.font.SysFont('Bauhaus 93', 60)
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

background_image = pygame.image.load('flappy_bird_asset_pack/flappy_bird_img_assets/background_img.png')
ground_image = pygame.image.load('flappy_bird_asset_pack/flappy_bird_img_assets/ground_img.png')

def draw_text(text, font, text_color, x, y):
    
    image = font.render(text, True, text_color)
    window_screen.blit(image, (x, y))
    
class bird(pygame.sprite.Sprite):
    
    def __init__(self, x, y):
        
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        
        for num in range(1, 4):
            
            flappy_bird_image = pygame.image.load(f'flappy_bird_asset_pack/flappy_bird_img_assets/bird_anim{num}_img.png')
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

bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy_bird = bird(100, int(window_screen_height / 2))

bird_group.add(flappy_bird)

run_window = True

while run_window:
    
    clock.tick(frames_per_second)
    
    window_screen.blit(background_image, (0, 0))
    
    bird_group.draw(window_screen)
    bird_group.update()
    
    pipe_group.draw(window_screen)

    window_screen.blit(ground_image, (scroll_ground, 768))

    if len(pipe_group) > 0:
        
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
            and user_pass_pipe == False:
            
            user_pass_pipe = True
        
        if user_pass_pipe == True:
            
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                
                user_score += 1
                user_pass_pipe = False

    draw_text(str(user_score), font, color_white, int(window_screen_width / 2), 20)

    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy_bird.rect.top < 0:
        
        game_ends = True

    if flappy_bird.rect.bottom >= 768:
        
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
    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            
            run_window = False
        
        if event.type == pygame.MOUSEBUTTONDOWN and flying_movement == False and game_ends == False:
            
            flying_movement = True
    
    pygame.display.update()

pygame.quit()