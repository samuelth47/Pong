"""
Creates the gui of the pong game.

@author: kvlinden
@author: Samuel Haileselassie
"""

from tkinter import *
from paddleball import Paddle, Ball

class Ponggame:
    """Creates a pong game where a ball bounces off a paddle."""
    
    def __init__(self, window, width=1000, height=500):
        """Instantiate the simulation GUI window, creates the widgets and displays text."""
        
        self.window = window
        self.width = width
        self.height = height
        self.delay = 5

        self.canvas = Canvas(self.window, bg = 'black',
                             width=self.width, height=self.height)
        self.canvas.pack()

        control_frame = Frame(window)
        control_frame.pack()
        
        #creates the newgame and quit buttons
        self.startgame_button = Button(control_frame, text="Start game", command=self.start_game, bg = "Blue", state=ACTIVE)
        self.startgame_button.pack(side=LEFT)
        
        self.newgame_button = Button(control_frame, text="New game", command=self.new_game, bg = "green", state=DISABLED)
        self.newgame_button.pack(side=LEFT)
        
        self.quit_button = Button(control_frame, text="Quit", command=root.destroy, bg = "red")
        self.quit_button.pack(side=LEFT)
        
        #creates a label for the highest score
        self.highest_score = Label(window, text='Highscore:', bg = "dimgray")
        self.highest_score.pack(side=LEFT)
        self.highest_score = IntVar()
        self.highest_score_label = Label(window, textvariable=self.highest_score, bg = "darkgrey")
        self.highest_score_label.pack(side=LEFT)
        
        #creates a label for the current score 
        self.current_score = IntVar()
        self.current_score_label = Label(window, textvariable=self.current_score, bg = "darkgrey")
        self.current_score_label.pack(side=RIGHT)
        self.current_score_label = Label(window, text='Current score:', bg = "dimgray")
        self.current_score_label.pack(side=RIGHT)
        
        #binds the arrow keys
        self.window.bind("<Key>", self.key)
        
        #creates the paddle
        self.paddle = Paddle(250,250,width,height)
        self.paddle.render(self.canvas)
        
        #creates the ball
        self.ball = Ball(self.paddle)
        
        #calls the highscore method
        self.highscore()
        
        #displays the welcome text
        self.canvas.create_text(self.width/2, self.height/2 ,fill="green",font="Ariel 20 bold",
                        text="Let's play pong!")


    def animation(self):
        """Controls the animation of the game"""

        self.canvas.delete(ALL)
        self.paddle.render(self.canvas)
        self.paddle.move(self.width)
        
        self.ball.move(self.width, self.height, self.paddle)
        self.ball.render(self.canvas)
        
        self.display_score()
        self.highscore()
        
        #checks if game is over(when ball touches the bottom of canvas) or not and displays message or re-runs the game
        if not self.paddle.check_height(self.ball):
            self.window.after(self.delay, self.animation)
        else:
            self.canvas.create_text(self.width/2, self.height/2 ,fill="red",font="Ariel 35 bold",
                        text="Game Over!")
            self.canvas.create_text(self.width/2, (self.height * 2) / 3 ,fill="green",font="Ariel 10 bold",
                        text="Click New game to play again")
            self.highscore()
        
    def start_game(self):
        """ Initiates the game"""
        self.animation()
        self.startgame_button.config(state='disabled')
        self.newgame_button.config(state='active')
         
    def key(self, event):
        """Receives the event and calls the key_pressed function"""
        self.paddle.key_pressed(event, self.width)

    def new_game(self):
        """Starts a new game when the button is clicked"""
        
        self.canvas.delete(ALL)
        
        self.paddle = Paddle(250,250,self.width,self.height)
        self.paddle.render(self.canvas)
        
        self.ball = Ball(self.paddle)
        
        #callls the score function at the start of a new game
        self.display_score()
        self.highscore()
        self.window.after(self.delay, self.animation)
        
        #sets initial value of current score to 0
        self.bounce = 0
        self.current_score.set(0)
        
    def display_score(self):
        """Displays the current score of the player"""
        self.current_score.set(self.ball.bounce)
        
    def highscore(self):
        """Sets the label to the highest score by reading off of the file"""
        with open('scores.txt','r') as file:
            for line in file:
                self.highest_score.set(str(line))
                

if __name__ == '__main__':
    root = Tk()
    root.title('Pong')    
    app = Ponggame(root)
    root.mainloop()
        