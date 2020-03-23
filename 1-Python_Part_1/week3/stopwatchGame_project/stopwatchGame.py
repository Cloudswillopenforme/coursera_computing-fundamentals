!#/usr/bin/python2
# "Stopwatch: The Game"

import simplegui

## globals
game_on = False

message = "Press start"
time = 0
interval = 100

game_status = "0 / 0"
win_stops = 0
total_stops = 0

## helpers

# format milliseconds to "A:BC.D"
def format(t):
    
    A = t // 600
    
    if A == 0:
        B = t // 100
    else:
        B = (t % 600) // 100
        
    if (A or B) == 0:
        C = t // 10
    else:
        C = (t % 100) // 10
        
    if (A or B or C) == 0:
        D = t 
    else:
        D = (t % 10)
    
    t = str(A) + ":" + str(B) + str(C) + "." + str(D)
    return t

# functions to keep track of game status
def track_game():
    global win_stops, total_stops, time, game_on
    if game_on:
        total_stops += 1
        if not time % 10:
            win_stops +=1
        
    update_game_status()

def update_game_status():
    global game_status, win_stops, total_stops
    game_status = str(win_stops) + " / " + str(total_stops)

# functions to reset values
def reset_game():
    global win_stops, total_stops
    win_stops = 0
    total_stops = 0
    update_game_status()
    
def reset_time():
    global time, message
    time = 0
    message = format(time)
    
## handlers
def start_handler():
    global game_on
    game_on = True
    timer.start()
    
def stop_handler():
    global game_on
    timer.stop()
    track_game()
    game_on = False
    
def reset_handler():
    stop_handler()
    reset_game()
    reset_time()
    
def timer_handler():
    global message, time
    time += 1
    message = format(time)
    
    # more than 10 mins is not allowed
    if time >= 10 * 600:
        stop_handler()
    
def draw_handler(canvas):
    canvas.draw_text(message, [110, 170], 54, "White")
    canvas.draw_text(game_status, [310, 60], 42, "Green")

    
## frame
frame = simplegui.create_frame("Stopwatch", 400, 300)
frame.add_button("Start", start_handler, 200)
frame.add_button("Stop", stop_handler, 200)
frame.add_button("Reset", reset_handler, 200)
frame.set_draw_handler(draw_handler)
timer = simplegui.create_timer(interval, timer_handler)


frame.start()

