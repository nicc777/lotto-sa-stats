from lotto import *
from datetime import date, datetime

p = Persistance()
draw_date = datetime.strptime(input("Draw Date [yyyy-mm-dd]: "), "%Y-%m-%d")


def getBallsDrawn(gameConf=GameConf()):
    done = False
    balls_drawn = []
    ball_number = 1;
    while not done:
        ball = ballInput(gameConf, ball_number)
        if ball is not None:
            balls_drawn.append(ball)
            ball_number += 1
            if ball_number > gameConf.number_qty_required:
                done = True
    done = False
    while not done:
        ball = ballInput(gameConf, ball_number, isSpecial=True)
        if ball is not None:
            balls_drawn.append(ball)
            done = True
    return balls_drawn
        

def ballInput(gameConf, ball_number, isSpecial=False):
    try:
        bi = None
        if isSpecial:
            bi = input("Special Ball drawn value: ")
        else:
    	    bi = input("Ball number %s drawn value: " % ball_number)
        biv = int(bi)
        if not isSpecial:
            if biv < gameConf.min_number or biv > gameConf.max_number:
                print("Invalid number. Try again.")
                return None
        else:
            if biv < gameConf.special_min_number or biv > gameConf.special_max_number:
                print("Invalid number. Try again.")
                return None
        return Ball(value=biv, gameConf=gameConf, isSpecial=isSpecial, isBallDrawnInGame=True)
    except:
        print("Enter a valid number")
    return None


done = False
while not done:
    gc = GameConf()
    game = input("Game: 1=Lotto or 2=Powerball [1]: ")
    if game == "2":
        gc = GameConf(game_name="PowerBall",min_number=1,max_number=45,keep_order=False,choose_special_on_play=True,special_name="PowerBall",special_min_number=1,special_max_number=20,number_qty_required = 5)
    balls_drawn = getBallsDrawn(gc)

    balls_drawn_filename = "balls_drawn_game_%s_on_%s.pickle" % (gc.game_name.lower(),draw_date.isoformat())
    p.save(balls_drawn_filename, balls_drawn)
    isDone = input("Done? y=Yes or n=No [y]: ")
    if isDone is not "n":
        done = True
