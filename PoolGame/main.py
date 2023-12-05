import pygame
import pymunk
import pymunk.pygame_util
import math
def initialize_game():
    global clock ,space ,screen ,balls ,pockets ,pocket_dia,FPS,table_image,dia, BG, potted_balls, ball_images, screen_height, lives
    global cue ,max_force ,power_bar, font,WHITE,screen_width, bottom_panel ,draw_text, large_font, cue_ball_potted, game_running, powering_up, force, ball_rotations
    pygame.init()

    screen_width=1200
    screen_height=678
    bottom_panel=50
    #game window
    screen = pygame.display.set_mode((screen_width,screen_height+bottom_panel))
    pygame.display.set_caption("Singleplayer Pool Game")


    #pymunk

    space = pymunk.Space()
    static_body=space.static_body
    #clock
    clock = pygame.time.Clock()
    FPS=120
    #variables
    dia=36 #px of picture
    pocket_dia=66
    force=0
    max_force=10000
    force_direction=1
    lives = 3
    taking_shot = True
    cue_ball_potted = True
    powering_up=False
    game_running=True
    potted_balls=[]
    angle=0
    #colors
    BG = (50,50,50)
    RED=(255,0,0)
    WHITE=(255,255,255)
    #fonts
    font = pygame.font.SysFont('Arial',30)
    large_font = pygame.font.SysFont('Arial',80)
    #load images
    cue_image = pygame.image.load("Assets/cue.png").convert_alpha()
    table_image = pygame.image.load("Assets/table.png").convert_alpha()
    ball_images=[] #images list
    for i in range (1,17):
        ball_image=pygame.image.load(f"Assets/ball_{i}.png").convert_alpha()
        ball_images.append(ball_image)
    #Output text
    def draw_text(text,font,text_col,x,y):
        img = font.render(text,True,text_col)
        screen.blit(img,(x,y))
    # function for balls
    def create_ball (radius, pos):
        body = pymunk.Body()
        body.position =pos
        shape = pymunk.Circle(body, radius)
        shape.mass = 5
        shape.elasticity=1
        #pivot joint for friction
        pivot=pymunk.PivotJoint(static_body,body,(0,0),(0,0))
        pivot.max_bias=0 #disable joint correction
        pivot.max_force=2400 #emulate linear friction
        space.add(body, shape,pivot)
        return shape
    #setup balls
    balls= [] # ball objects
    rows = 5
    w, h = ball_image.get_size()
    #potting balls
    for col in range(5):
        for row in range(rows):
            pos = (250+(col*(dia+1)),267+(row*(dia+1))+(col*dia/2))
            new_ball = create_ball(dia/2,pos)
            balls.append(new_ball)
        rows -=1
    #cue ball
    pos =(888,screen_height/2)
    cue_ball=create_ball(dia/2,(pos))
    balls.append(cue_ball)
    ball_rotations = [0] * len(balls)
    pockets = [
    (55, 63),
    (592, 48),
    (1134, 64),
    (55, 616),
    (592, 629),
    (1134, 616)
    ]
    cushion = [
    [(88, 56), (109, 77), (555, 77), (564, 56)],
    [(621, 56), (630, 77), (1081, 77), (1102, 56)],
    [(89, 621), (110, 600),(556, 600), (564, 621)],
    [(622, 621), (630, 600), (1081, 600), (1102, 621)],
    [(56, 96), (77, 117), (77, 560), (56, 581)],
    [(1143, 96), (1122, 117), (1122, 560), (1143, 581)]
    ]
            
    #creating cushions
    def create_cushion(poly_dims):
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        shape = pymunk.Poly(body, poly_dims)
        space.add(body,shape) 
        shape.elasticity=0.8
    for c in cushion:
        create_cushion(c)
        
    #create pool cue
    class Cue():
        def __init__(self,pos):
            self.original_image = cue_image
            self.angle=0
            self.image=pygame.transform.rotate(self.original_image,self.angle)
            self.rect=self.image.get_rect()
            self.rect.center=pos
        def update(self, angle):
            self.angle=angle   
        def draw(self, surface):
            self.image=pygame.transform.rotate(self.original_image,self.angle)
            surface.blit(self.image,
                        ((self.rect.centerx-self.image.get_width()/2),
                        (self.rect.centery-self.image.get_height()/2)))
                
    cue=Cue(balls[-1].body.position)      
    #power bars for cue
    power_bar = pygame.Surface((10,20)) 
    power_bar.fill(RED)
    #run game loop
    game_running=True
    powering_up==True
def main():
    initialize_game()
    run=True
    cue_ball_potted = True 
    

    global clock ,space ,screen ,balls ,pockets ,pocket_dia,FPS,table_image,dia, BG, potted_balls, ball_images, screen_height
    global cue ,max_force ,power_bar, font,WHITE,screen_width, bottom_panel ,draw_text, large_font,     game_running, powering_up, force, lives, ball_rotations
    while run:
        clock.tick(FPS)
        space.step(1/FPS)
        screen.fill(BG)
        
        #fill background
        #draw table
        screen.blit(table_image, (0,0))
        
        #check if inside pocket
        for i,ball in enumerate(balls):
            for pocket in pockets:
                ball_x_dist=abs(ball.body.position[0]-pocket[0])
                ball_y_dist=abs(ball.body.position[1]-pocket[1])
                ball_dist = math.sqrt((ball_x_dist**2)+(ball_y_dist**2))
                if ball_dist<=pocket_dia/2 :
                    #except cue ball
                    if i ==len(balls)-1: ## smaller by last index-cueball
                        cue_ball_potted= True
                        ball.body.position=(-100,-100)
                        ball.body.velocity=(0.0,0.0)
                        lives-=1
                    else:
                        space.remove(ball.body)
                        balls.remove(ball)
                        potted_balls.append(ball_images[i])
                        ball_images.pop(i)    
        for i, ball in enumerate(balls):
            velocity = ball.body.velocity
            speed = math.sqrt(velocity[0] ** 2 + velocity[1] ** 2)

            if speed > 0:  # Only rotate balls with non-zero speed

                # Update the ball's accumulated rotation angle based on speed
                rotation_speed = 0.08 + (speed*0.001)  # You can adjust this value for the desired rotation speed
                angle_change = rotation_speed * speed
                ball_rotations[i] += angle_change

                # Get the center of the image
                image = ball_images[i]
                image_rect = image.get_rect()
                rotation_point = image_rect.center

                # Rotate the image around its center
                rotated_image = pygame.transform.rotate(image, ball_rotations[i])

                # Get the rect for the rotated image
                rotated_rect = rotated_image.get_rect()

                # Update the position of the rotated image so it stays centered on the ball's position
                rotated_rect.center = ball.body.position

                # Blit (draw) the rotated image on the screen
                screen.blit(rotated_image, rotated_rect.topleft)

            else:
                # If speed is 0, just blit the original image
                screen.blit(ball_images[i], (ball.body.position[0] - ball.radius, ball.body.position[1] - ball.radius))


        #balls in move
        taking_shot = True
        # game_running = True
        for ball in balls:
            if int(ball.body.velocity[0]) !=0 or int(ball.body.velocity[1])!=0: #int to prevent not showing if close to 0speed but not 0 
                taking_shot = False
        #calc angle and draw cue stick
        if taking_shot is True and game_running is True:
            if  cue_ball_potted == True:
                #reposition of cue
                balls[-1].body.position = (888,screen_height/2)
                cue_ball_potted = False
            mouse_pos = pygame.mouse.get_pos()
            cue.rect.center=balls[-1].body.position
            x_dist=balls[-1].body.position[0]-mouse_pos[0]
            y_dist=-(balls[-1].body.position[1]-mouse_pos[1]) #- bc pygame y increase down screen
            cue_angle=math.degrees(math.atan2(y_dist,x_dist))
            cue.update(cue_angle)
            cue.draw(screen)



        if powering_up==True and game_running is True:
            force +=100 * force_direction
            if force >= max_force or force<=0:
                force_direction*=-1 ##increase to10000 then decrease to 0 
            #draw power bars
            for b in range(math.ceil(force/2000)):
                screen.blit(power_bar,(balls[-1].body.position[0]-30+(b*15),balls[-1].body.position[1]+30))
        #increase force
        elif powering_up==False and taking_shot==True:
            x_impulse=math.cos(math.radians(cue_angle))
            y_impulse=math.sin(math.radians(cue_angle))
            balls[-1].body.apply_impulse_at_local_point((force* -x_impulse,force*y_impulse),(0,0))
            force = 0
            force_direction=1
        #draw bottom panel
        pygame.draw.rect(screen,BG,(0,screen_height,screen_width,bottom_panel))
        #draw potted balls in bottom panel
        for i, ball in enumerate(potted_balls):
            screen.blit(ball,(10+(i*50),screen_height+5))    
        #text
        draw_text("Lives: "+ str(lives), font,WHITE,screen_width-200,screen_height+10)
        if lives <=0:
            draw_text("Game Over",large_font,WHITE,screen_width/2-150,screen_height/2-200)    
            draw_text("Press R to try again",font,WHITE,screen_width/2-145,screen_height/2-120)    
            game_running=False
        #all balls inside
        if len(balls) ==1:
            draw_text("VICTORY",large_font,WHITE,screen_width/2-150,screen_height/2-200) 
            draw_text("Press R to play",font,WHITE,screen_width/2-145,screen_height/2-120)    
            game_running=False
        for event in pygame.event.get():
            if event.type ==pygame.MOUSEBUTTONDOWN and taking_shot==True:
                powering_up=True
            if event.type ==pygame.MOUSEBUTTONUP and taking_shot==True: #as long as we hold mbutton
                powering_up=False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game_running == False:
                    initialize_game()
                    
            if event.type ==pygame.QUIT:
                run = False 
        pygame.display.update()
        
    pygame.quit()
if __name__ == "__main__":
    main()