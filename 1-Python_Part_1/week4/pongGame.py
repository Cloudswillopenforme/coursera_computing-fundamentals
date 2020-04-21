!#/usr/bin/python2
# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
LEFT = False
RIGHT = True

ball_pos = [0, 0]
ball_vel = [0, 0] 

paddle1_pos = 0
paddle2_pos = 0
paddle1_vel = 0
paddle2_vel = 0
paddle_speed = 10

score1 = 0
score2 = 0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(right):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    if right:
        ball_vel = [random.randrange(120, 240) // 60, -random.randrange(60, 180) // 60]
    else:
        ball_vel = [-random.randrange(120, 240) // 60, -random.randrange(60, 180) // 60]


# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2 # these are ints
    
    # depends on who won last time
    if score1 >= score2:
        direction = RIGHT
    else: 
        direction = LEFT
        
    score1 = 0
    score2 = 0
    paddle1_pos = 0
    paddle2_pos = 0
    paddle1_vel = 0
    paddle2_vel = 0
    
    spawn_ball(direction)

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
        
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "White")
    
    # update paddle's vertical position, keep paddle on the screen
    if (paddle1_pos + paddle1_vel) >= 0 and (paddle1_pos + paddle1_vel + PAD_HEIGHT) <= HEIGHT:
        paddle1_pos+= paddle1_vel
        
    if (paddle2_pos + paddle2_vel) >= 0 and (paddle2_pos + paddle2_vel + PAD_HEIGHT) <= HEIGHT:
        paddle2_pos += paddle2_vel
        
    
    # draw paddles
    canvas.draw_line([0 + HALF_PAD_WIDTH, paddle1_pos], [0 + HALF_PAD_WIDTH, paddle1_pos + PAD_HEIGHT], PAD_WIDTH, 'White')
    canvas.draw_line([600 - HALF_PAD_WIDTH, paddle2_pos], [600 - HALF_PAD_WIDTH, paddle2_pos + PAD_HEIGHT], PAD_WIDTH, 'White')
    
    # determine whether paddle and ball collide
    ## top-down collision
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
        
    ## left-sided collision
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
        if ball_pos[1] > paddle1_pos and ball_pos[1] < paddle1_pos + PAD_HEIGHT:
            ball_vel[0] *= -1.1
            ball_vel[1] *= 1.1
            score1 += 1
        else:
            score2 += 1
            spawn_ball(RIGHT)
            
    ## right-sided collision
    if ball_pos[0] >= WIDTH - (BALL_RADIUS + PAD_WIDTH):
        if ball_pos[1] > paddle2_pos and ball_pos[1] < paddle2_pos + PAD_HEIGHT:
            ball_vel[0] *= -1.1
            ball_vel[1] *= 1.1
            score2 += 1
        else:
            score1 += 1
            spawn_ball(LEFT)
    
    # draw scores
    canvas.draw_text(str(score1), [100, 50], 48, "White")
    canvas.draw_text(str(score2), [500, 50], 48, "White")
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel -= paddle_speed
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel += paddle_speed
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel -= paddle_speed
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel += paddle_speed
   
def keyup(key):
    global paddle1_vel, paddle2_vel
   
    if key == simplegui.KEY_MAP["s"] or key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["up"] or key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('Restart game', new_game, 200)


# start frame
new_game()
frame.start()
