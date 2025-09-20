import random
import pygame, sys
from pygame.locals import *

pygame.init()
fps=pygame.time.Clock()

#colors
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLACK = (0,0,0)

#game window
# WIDTH = 900
# HEIGHT = 720

#Display/window: Where the game is shown. (pygame.display.set_mode)
#window=pygame.display.set_mode((WIDTH,HEIGHT))


# Fullscreen window
# (0, 0) tells Pygame to use the current screen resolution.
# pygame.FULLSCREEN makes the window fullscreen
infoObject = pygame.display.Info()
WIDTH = infoObject.current_w
HEIGHT = infoObject.current_h

window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)


pygame.display.set_caption("Pong")      

#These define screen size, ball size, paddle size, and frame speed
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 120

#HALF_PAD_WIDTH and HALF_PAD_HEIGHT are used to calculate paddle positions easily.
HALF_PAD_WIDTH = PAD_WIDTH // 2
HALF_PAD_HEIGHT = PAD_HEIGHT // 2
ball_pos = [0,0]
ball_vel = [0,0]
paddle1_vel = 0
paddle2_vel = 0
l_score = 0
r_score = 0

class Ball:
    def __init__(self):
        #pos → [x, y] coordinates of the ball.
        self.pos = [WIDTH//2 , HEIGHT//2]
        #vel → velocity vector, how many pixels to move per frame in x and y
        self.vel = [0,0]

    def spawn(self,right=True):
        '''Spawns the ball in the middle of the table, with an initial velocity
        in a random direction. If right is True, the ball goes to the right, else left.'''
        
        horiz = random.randrange(4,6)
        vert = random.randrange(2,4)
        if not right:
            horiz = - horiz
        di=random.choice([-1,1])
        self.pos = [WIDTH//2,HEIGHT//2]
        self.vel = [horiz,di*vert]
    
    def update(self):
        '''Updates the ball position based on its velocity.'''
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

    def draw(self , surface):
        '''Draws the ball on the given surface.'''
        pygame.draw.circle(surface, WHITE, self.pos, BALL_RADIUS)

class Paddle:
    def __init__(self,x_pos):
        #x_pos is the x position of the paddle (either PAD_WIDTH//2 or WIDTH - PAD_WIDTH//2)
        self.pos = [x_pos,HEIGHT // 2]
        self.vel = 0

    def update(self):
        '''Updates the paddle position based on its velocity.
        Ensures the paddle stays on the screen(in if condition with 0 and height).'''
        if (self.pos[1] + self.vel - HALF_PAD_HEIGHT >= 0) and (self.pos[1] + self.vel + HALF_PAD_HEIGHT <= HEIGHT):
            self.pos[1] += self.vel
    
    def draw(self,surface):
        '''Draws the paddle on the given surface.'''
        pygame.draw.polygon(surface, WHITE, [[self.pos[0] - HALF_PAD_WIDTH, self.pos[1] - HALF_PAD_HEIGHT],
                                             [self.pos[0] - HALF_PAD_WIDTH, self.pos[1] + HALF_PAD_HEIGHT],
                                             [self.pos[0] + HALF_PAD_WIDTH, self.pos[1] + HALF_PAD_HEIGHT],
                                             [self.pos[0] + HALF_PAD_WIDTH, self.pos[1] - HALF_PAD_HEIGHT]])
        

class PongGame:
    def __init__(self):
        pygame.init()
        #Creates a window for the game.
        # Clock is used to control FPS
        self.window = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption("Pong")
        self.clock = pygame.time.Clock()

        self.ball = Ball()
        self.paddle1 =Paddle(HALF_PAD_WIDTH - 1)
        self.paddle2 = Paddle(WIDTH + 1 - HALF_PAD_WIDTH)
        self.l_score =0
        self.r_score =0
        
        # Spawn the ball to start the game, random direction right if true, left if false
        self.ball.spawn(random.choice([True,False]))

    def draw(self):
        '''Draws all game elements on the window.'''
        self.window.fill(BLACK)
        # Draw mid line and gutters
        pygame.draw.line(self.window, WHITE, [WIDTH // 2, 0],[WIDTH // 2, HEIGHT], 1)
        pygame.draw.line(self.window, WHITE, [PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1)
        pygame.draw.line(self.window, WHITE, [WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1)

        self.ball.draw(self.window)
        self.paddle1.draw(self.window)
        self.paddle2.draw(self.window)

        # Draw scores
        font = pygame.font.SysFont("Comic Sans MS", 30)
        score1 = font.render(str(self.l_score), True, WHITE)
        score2 = font.render(str(self.r_score), True, WHITE)
        self.window.blit(score1, (WIDTH // 4, 20))
        self.window.blit(score2, (WIDTH * 3 // 4, 20))
    
    def handle_collisions(self):
        '''Handles collisions of the ball with walls and paddles and updates scores.'''
        # Top and bottom wall collision
        if self.ball.pos[1] <= BALL_RADIUS or self.ball.pos[1] >= HEIGHT - BALL_RADIUS:
            self.ball.vel[1] = -self.ball.vel[1]
        
        # Left paddle collision
        if self.ball.pos[0] <= PAD_WIDTH + BALL_RADIUS:
            if self.paddle1.pos[1] - HALF_PAD_HEIGHT <= self.ball.pos[1] <= self.paddle1.pos[1] + HALF_PAD_HEIGHT:
                self.ball.vel[0] = -self.ball.vel[0] * 1.1
                self.ball.vel[1] = self.ball.vel[1] * 1.1
            else:
                self.r_score += 1
                self.ball.spawn(right=True)

        # Right paddle collision
        if self.ball.pos[0] >= WIDTH - PAD_WIDTH - BALL_RADIUS:
            if self.paddle2.pos[1] - HALF_PAD_HEIGHT <= self.ball.pos[1] <= self.paddle2.pos[1] + HALF_PAD_HEIGHT:
                self.ball.vel[0] = -self.ball.vel[0] * 1.1
                self.ball.vel[1] = self.ball.vel[1] * 1.1
            else:
                self.l_score += 1
                self.ball.spawn(right=False)
        
    def handle_input(self,event):
            '''Handles user input for paddle movement.'''
            if event.type == KEYDOWN:
                if event.key == K_w:
                    self.paddle1.vel = -6
                elif event.key == K_s:
                    self.paddle1.vel = 6
                elif event.key == K_UP:
                    self.paddle2.vel = -6
                elif event.key == K_DOWN:
                    self.paddle2.vel = 6
            elif event.type == KEYUP:
                if event.key in (K_w, K_s):
                    self.paddle1.vel = 0
                elif event.key in (K_UP, K_DOWN):
                    self.paddle2.vel = 0
    def update(self):
            '''Updates the game state: ball and paddle positions, handles collisions.'''
            self.ball.update()
            self.paddle1.update()
            self.paddle2.update()
            self.handle_collisions()

    def run(self):
            '''Main game loop.'''
            while True:
                for event in pygame.event.get():
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            pygame.quit()
                            sys.exit()
                    self.handle_input(event)
                
                self.update()
                self.draw()
                pygame.display.flip()
                self.clock.tick(60)  # Limit to 60 FPS

if __name__ == "__main__":
    game = PongGame()
    game.run()