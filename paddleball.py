"""
creates the movement and bouncing of the paddle and ball.

@author: kvlinden
@author: Samuel Haileselassie
"""
from random import randint

class Paddle():
    """Creates and moves the paddle in the pong game"""
    def __init__(self, x, y, width=500, height=500, length=50):
        """Instantiates the variables of the paddle"""
        
        self.x = width / 2
        self.y = height
        self.width = width
        self.height = height
        self.length = width / 10
        self.move_x = 30

    def render(self, canvas):
        """Renders and draws the paddle as a rectangle"""
        canvas.create_rectangle(self.x - self.length,
                                self.y - self.length / 2,
                                self.x + self.length,
                                self.y,
                                fill='lightblue' )
        
    def move(self, width):
        """Places the paddle at the center when the game starts"""
        self.move_x = 0

    def key_pressed(self, event, width):
        """Receives an event of key press and processes it to move the paddle left and right"""
        
        key = event.keysym
        
        #moves the paddle to the left if 'a' or 'left arrow' is pressed
        if key == "Left" or key == "a":
            self.move_x = 30
            if self.x - self.length - self.move_x > 0:
                self.x -= self.move_x
                
        #moves the paddle to the left if 'd' or 'right arrow' is pressed
        elif key == "Right" or key == "d":
            self.move_x = 30
            if self.x + self.length + self.move_x < self.width:
                self.x += self.move_x
        
    def bounce(self, ball):
        """Returns True if the ball is within the scope of the paddle"""
        if ball.x < self.x + self.length and ball.x > self.x - self.length:
            return True

    def check_height(self, ball):
        """Checks if the ball touches the bottom of the canvas and returns True"""
        if ball.y + ball.radius > self.height:
            return True

class Ball():
    """Creates and moves the ball in the pong game."""
    def __init__(self, Paddle, x=25, y=25, vel_x=1, vel_y=1, acc_x = 0.01, acc_y=0.2, radius=25):
        """Instantiates the variables of the Ball"""
        
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.acc_x = acc_x
        self.acc_y = acc_y
        self.radius = radius
        self.bounce = 0
        self.highest_score = 0
        self.color = self.random_color()     


    def render(self, canvas):
        """Renders the Ball as a circle and fills it with random color"""
        canvas.create_oval(self.x - self.radius,
                           self.y - self.radius,
                           self.x + self.radius,
                           self.y + self.radius,
                           fill=self.color)
        
    def move(self, width, height, paddle):
        """Change the ball's location/velocity, bouncing off walls, ceiling and the paddle only. Added complexity levels as bounce number increases."""
        
        self.x += self.vel_x
        self.y += self.vel_y
        
        #bounce off of the walls and the ceiling only
        if self.x + self.radius > width or self.x - self.radius < 0:
            self.vel_x *= -1
            self.x += self.vel_x
        
        #bounces off only from the paddle and counts its bounce
        if self.y + self.radius > height and paddle.bounce(self):
            self.vel_y *= -1
            self.y += self.vel_y
            self.color = self.random_color()
            
            #if the ball doesn't touch the bottom and bounces off the paddle, increment bounce
            if not paddle.check_height(self):
                self.bounce += 1

        #checks if the ball touches the bottom of the screen and stops the ball
        if paddle.check_height(self):
            self.vel_x = 0
            self.vel_y = 0
            self.score()
      
        #decreases the paddle's size every 5 bounces
        if self.bounce == 0:
            paddle.length = 50
            
        elif self.bounce == 5:
            paddle.length = 45
        
        elif self.bounce == 10:
            paddle.length = 40
            
        elif self.bounce == 10:
            paddle.length = 35
        
        elif self.bounce == 15:
            paddle.length = 30
            
        elif self.bounce == 20:
            paddle.length = 25
        
        elif self.bounce == 25:
            paddle.length = 20
            
        elif self.bounce == 30:
            paddle.length = 15
            
        elif self.bounce == 35:
            paddle.length = 10
        
        elif self.bounce > 50:
            paddle.length = 5

        self.vel_x += self.acc_x
        self.vel_y += self.acc_y
    
    #found this code on piazza posted as 'Section B Code'
    def random_color(self):
        """Creates a random color in hexadecimal format, found it on Piazza"""
        return '#{:02X}{:02X}{:02X}'.format(
        randint(0, 255),
        randint(0, 255),
        randint(0, 255)
    )
    
    def score(self):
        """ Checks the highscore and updates it every game."""
        
        current_score = self.bounce
        
        try:
            with open('scores.txt','r+') as file:
                
                file_score = file.read()
                
                if len(file_score) == 0:
                    self.highest_score = current_score
                    file.write(str(self.highest_score))
                else:
                    self.highest_score = int(file_score)

                    #compares current and highest score then clears and writes to file
                    if current_score > self.highest_score:
                        file.seek(0)
                        file.truncate()
                        
                        self.highest_score = current_score
                        file.write(str(self.highest_score))


        except (FileNotFoundError, ValueError):
            assert True

if __name__ == '__main__':
    
    #creates paddle and ball for testing
    paddle = Paddle(250, 250)
    ball = Ball(paddle)
    
    #checks that the paddle starts at the center
    assert paddle.x == 250
    assert paddle.y == 500

    #checks if the ball bounces by placing the ball on the paddle
    ball.x = 250
    ball.y = 500
    assert paddle.bounce(ball)
    
    #checks if the ball does not bounce by placing the ball away from the paddle
    ball.x = 500
    ball.y = 500
    assert not paddle.bounce(ball)

    #checks if the game is over(when ball touches the bottom of the canvas)
    ball.x = 100
    ball.y = 500
    assert paddle.check_height(ball)
    
    #checks if the game continues when the ball doesn't touch the bottom of the canvas
    ball.x = 100
    ball.y = 300
    assert not paddle.check_height(ball)        
