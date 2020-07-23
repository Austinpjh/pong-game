from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout


class Ball(Widget):
    velocity_x = NumericProperty(0)  # velocity of ball in the x axis begins at an increment of 10
    velocity_y = NumericProperty(0)  # velocity of ball in the y axis begins at an increment of 2
    velocity = ReferenceListProperty(velocity_x, velocity_y)  # Combining velocity_x and velocity_y into one property

    # move function causes ball to travel from one point to another
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos  # Vector function makes velocity property a 2D Vector


class Paddle(Widget):
    score = NumericProperty(0)

    def hit_paddle(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced
            ball.velocity = vel.x, vel.y + offset

class Winner(FloatLayout):
    # def __init__(self,**kwargs):
    #     super(Winner,self).__init__(**kwargs)

    @staticmethod
    def label(str):
        return "Player " + str + " Won!"



class Rules(FloatLayout):
    txt = """Classic Pong Game Rules:
    1) Player 2 serve first
    2) Get the ball pass the paddle of the other player
    3) First to score 7 points wins the game"""
    button=ObjectProperty(None)

def rules_popup():
    content=Rules()
    pop =Popup(title="Basic Rules", content=content,size_hint=(None,None),size=(500,500))
    pop.open()
    content.button.bind(on_release=pop.dismiss)

def winner_popup(str):
    txt="Player " + str + " Won!"
    pop = Popup(title="Result", content=Label(text=txt, font_size=50), size_hint=(None,None), size=(500,500))
    pop.open()

class PongGame(Widget):
    ball=ObjectProperty(None)  # links class Ball to class Game in Python Script
    left=ObjectProperty(None)  # links class Paddle to class Game in Python Script
    right=ObjectProperty(None)  # links class Paddle to class Game in Python Script

    def __init__(self, **kwargs):
        super(PongGame,self).__init__(**kwargs)
        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def serve_ball(self, vel=(10, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, dt):
        self.ball.move()
        # bouncing off top and bottom walls
        if self.ball.y < 0 or self.ball.y > self.height-50:
            self.ball.velocity_y *= -1
        # bouncing off left and increasing right score
        if self.ball.x < 0:
            self.right.score += 1
            self.ball.center = self.center
            self.serve_ball(vel=(-10,0))

        # bouncing off right and increasing left score
        if self.ball.x > self.width:
            self.left.score += 1
            self.ball.center = self.center
            self.serve_ball(vel=(10, 0))

        self.left.hit_paddle(self.ball)
        self.right.hit_paddle(self.ball)
        if self.left.score == 7:
            winner_popup("1")

        if self.right.score == 7:
            winner_popup("2")



    # Controls movement of paddles
    def on_touch_move(self, touch):  # Existing method in Widget Class, hence do not need to call in build()

        # Restrict movement of paddles in this area
        if touch.x < self.width * (1/4):
            self.left.center_y = touch.y
        if touch.x > self.width * (3/4):
            self.right.center_y = touch.y


class WindowManager(ScreenManager):
    def btn_rule(self):
        rules_popup()


class MyApp(App):
    def build(self):
        return WindowManager(transition=FadeTransition())


if __name__ == '__main__':
    MyApp().run()
