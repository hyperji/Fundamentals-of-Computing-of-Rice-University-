# implementation of card game - Memory

import simplegui
import random

# helper function to initialize globals
def new_game():
    global states, card_desk, card_desk1,exposed, turns, state, previous
    card_desk = [0,1,2,3,4,5,6,7]
    card_desk.extend([0,1,2,3,4,5,6,7])
    random.shuffle(card_desk)
    exposed = 16 * [False]
    turns = 0
    state = 0
    previous = []
    

# define event handlers
def mouseclick(pos):
    # add game state logic here
    global state, exposed, turns, previous, card_desk
    i = int(list(pos)[0]//50)
    if state == 0:
        if exposed[i] == False:
            exposed[i] = True
            previous.append(i)
        state = 1
    elif state == 1:
        if exposed[i] == False:
            exposed[i] = True
            turns += 1
            previous.append(i)
            if card_desk[previous[len(previous)-2]] == card_desk[i]:
                state = 0
            else:
                state = 2
    else:
        if exposed[i] == False:
            exposed[i] = True
            exposed[previous[len(previous)-2]] = False
            exposed[previous[len(previous)-1]] = False
            exposed[i] = True
            previous.append(i)
            state = 1
    label.set_text("Turns = %d"%turns)
                       
# cards are logically 50x100 pixels in size    
def draw(canvas):
    for i in range(16):
        if exposed[i] == True:
            canvas.draw_text("%d"%card_desk[i], [50*i+15,65],40,"Red")
        else:
            canvas.draw_polygon([[50*i,0], [50*i,100], [50*(i+1),100], [50*(i+1),0]], 1, 'Yellow', 'Green')
    label.set_text("Turns = %d"%turns)
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric
