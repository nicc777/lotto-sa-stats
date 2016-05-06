import sys, codecs, traceback, re

LOTTO_TEMPLATE_LINE = "b__BALL__ = Ball(__VALUE__, gc_lotto)"
POWERBALL_TEMPLATE_LINE1 = "b__BALL__ = Ball(__VALUE__, gc_powerball)"
POWERBALL_TEMPLATE_LINE2 = "b__BALL__ = Ball(__VALUE__, gc_powerball, isSpecial=True)"

pbre = re.compile("(Powerball:)")
spre = re.compile("\s+")

lotto_balls = []
lotto_boards = []
powerball_balls = []
powerball_boards = []
all_boards = []

print("from lotto import *")
print("gc_lotto = GameConf()")
print("gc_powerball = GameConf(game_name=\"PowerBall\",min_number=1,max_number=45,keep_order=False,choose_special_on_play=True,special_name=\"PowerBall\",special_min_number=1,special_max_number=20,number_qty_required = 5)")
print("p = Persistance()")
print("")

try:
    sys.stdin = codecs.getreader('utf8')(sys.stdin.detach(), errors='ignore')
    f = open(sys.argv[1]) if len(sys.argv) > 1 else sys.stdin
    for line in f:
        fields = spre.split(line)
        powerball_check = fields[7]
        print("# field length: %s [%s]" % (len(fields), fields))
        board_name = fields[1]
        if pbre.match(powerball_check):
            # Powerball
            print("powerball_board_%s = Board(board_name=\"%s\", balls=[], gameConf=gc_powerball)" % ( board_name, board_name))
            all_boards.append("powerball_board_%s" % board_name)
            for i in range(5):
                ball_number = str(i + 1)
                ball_value = fields[2+i]
                ball = re.sub("__BALL__", ball_number, POWERBALL_TEMPLATE_LINE1)
                ball = re.sub("__VALUE__", ball_value, ball)
                board = "powerball_board_%s.add_ball(b%s)" % (board_name, ball_number)
                powerball_balls.append(ball)
                powerball_boards.append(board)
            ball_number = "6"
            ball_value = fields[8]
            ball = re.sub("__BALL__", ball_number, POWERBALL_TEMPLATE_LINE2)
            ball = re.sub("__VALUE__", ball_value, ball)
            board = "powerball_board_%s.add_ball(b%s)" % (board_name, ball_number)
            powerball_balls.append(ball)
            powerball_boards.append(board)
            for l in powerball_balls:
                print(l)
            for l in powerball_boards:
                print(l)
            powerball_balls = []
            powerball_boards = []

        else:
            # lotto
            print("lotto_board_%s = Board(board_name=\"%s\", balls=[], gameConf=gc_lotto)" % ( board_name, board_name))
            all_boards.append("lotto_board_%s" % board_name)
            for i in range(6):
                ball_number = str(i + 1)
                ball_value = fields[2+i]
                ball = re.sub("__BALL__", ball_number, LOTTO_TEMPLATE_LINE)
                ball = re.sub("__VALUE__", ball_value, ball)
                board = "lotto_board_%s.add_ball(b%s)" % (board_name, ball_number)
                lotto_balls.append(ball)
                lotto_boards.append(board)
            for l in lotto_balls:
                print(l)
            for l in lotto_boards:
                print(l)
            lotto_balls = []
            lotto_boards = []

except:
    print("EXCEPTION")
    traceback.print_exc(file=sys.stdout)

print("all_boards = []")
for b in all_boards:
    print("all_boards.append(%s)" % b)
print("p.save(\"all_boards.pickle\", all_boards)")

