import warnings
import pickle
from datetime import date

class LottoException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class GameConf:
    def __init__(
        self,
        game_name="Lotto",
        min_number=1,
        max_number=49,
        keep_order=False,
        choose_special_on_play=False,
        special_name="Bonus Ball",
        special_min_number=1,
        special_max_number=49,
        number_qty_required = 6
        ):
        if self._validate_string([game_name, special_name]):
            self.game_name = game_name
            self.special_name = special_name
        else:
            raise LottoException("Invalid String Detected.")
        if lv.validation_numbers([min_number, max_number, special_min_number, special_max_number, number_qty_required]):
            self.min_number = min_number
            self.max_number = max_number
            self.special_min_number = special_min_number
            self.special_max_number = special_max_number
            self.number_qty_required = number_qty_required
        else:
            raise LottoException("Invalid Integer Detected.")
        self.keep_order = keep_order
        self.choose_special_on_play = choose_special_on_play
    def _validate_string(self, strs_to_test):
        if isinstance(strs_to_test, list):
            if len(strs_to_test) > 0:
                for s in strs_to_test:
                    if not isinstance(s, str):
                        return False
                    if not len(s) > 3:
                        return False
        return True
    def __repr__(self):
        s = "Game '%s' requires %s balls to be played with values between %s and %s " % (self.game_name, self.number_qty_required, self.min_number, self.max_number)
        if self.choose_special_on_play:
            s += " and a special ball (aka PowerBall) must be choosen between the values of %s and %s" % (self.special_min_number, self.special_max_number)
        return s


class Ball:
    def __init__(self, value, gameConf, isSpecial=False, isBallDrawnInGame=False):
        if not isinstance(gameConf, GameConf):
            raise LottoException("Invalid GameConf")
        if not isinstance(value, int):
            raise LottoException("Value must be an Integer")
        self.isSpecial = isSpecial
        if not isSpecial:
            if value >= gameConf.min_number and value <= gameConf.max_number:
                self.value = value
            else:
                raise LottoException("Invalid value for Ball.")
        else:
            if not gameConf.choose_special_on_play and not isBallDrawnInGame:
                raise LottoException("The special ball cannot be choosen while selecting balls")
            if value >= gameConf.special_min_number and value <= gameConf.special_max_number:
                self.value = value
            else:
                raise LottoException("Invalid value for special Ball")
    def __repr__(self):
        return "Ball has a value of %s" % self.value

class DivisionalWinner:
    def __init__(
        self,
        div_number=1,
        qty_winners=0,
        winning_value_per_winner=0,
        div_description="No description provided",
        number_of_correct_balls_required=1,
        special_ball_required=False
        ):
        if lv.validation_numbers([div_number,qty_winners,winning_value_per_winner,number_of_correct_balls_required]):
            self.div_number = div_number
            self.qty_winners = qty_winners
            self.winning_value_per_winner = winning_value_per_winner
            self.number_of_correct_balls_required = number_of_correct_balls_required
        else:
            raise LottoException("Number validation failed")
        if isinstance(div_description, str):
            self.div_description = div_description
        else:
            raise LottoException("Description must be a String")
        self.special_ball_required = special_ball_required
    def __repr__(self):
        s = "Division %s requires %s correct numbers " % (self.div_number, self.number_of_correct_balls_required)
        if self.special_ball_required:
            s += "and requires the special ball (aka PowerBall)"
        return s


class Draw:
    def __init__(self, draw_date, draw_number, balls_drawn=[], special_ball=None, divisional_winners=[], gameConf=None, boards_played=[]):
        if gameConf is None:
            raise LottoException("gameConf must be defined")
        adjusted_balls_drawn = []
        if special_ball is None:
            for ball in balls_drawn:
                if ball.isSpecial:
                    special_ball = ball
                else:
                    adjusted_balls_drawn.append(ball)
        else:
            for ball in balls_drawn:
                if not ball.isSpecial:
                    adjusted_balls_drawn.append(ball)
        balls_drawn = adjusted_balls_drawn
        if not lv.validate_balls(gameConf, balls_drawn):
            raise LottoException("Ball validation failed")
        if not lv.validate_balls(gameConf, [special_ball]):
            raise LottoException("Special ball validation failed")
        if not lv.validation_numbers(draw_number):
            raise LottoException("Draw number must be like a number...")
        if not isinstance(draw_date, date):
            raise LottoException("Draw date must be a date object from datetime class.")
        if not isinstance(divisional_winners, list):
            raise LottoException("Divisional winners must be a list")
        else:
            for dw in divisional_winners:
                if not isinstance(dw, DivisionalWinner):
                    raise LottoException("Divisional winner was not defined as a DivisionalWinner class")
        if not isinstance(boards_played, list):
            raise LottoException("Boards played must be a list")
        else:
            for bp in boards_played:
                if not isinstance(bp, Board):
                    raise LottoException("Board was not defined as a Board class")
        self.draw_date = draw_date
        self.draw_number = draw_number
        self.balls_drawn = balls_drawn
        self.special_ball = special_ball
        self.divisional_winners = divisional_winners
        self.boards_played = boards_played
        self.gameConf = gameConf
    def add_divisional_winner(self, dw):
        if not isinstance(dw, DivisionalWinner):
            raise LottoException("Must be a DivisionalWinner class")
        dwl = []
        if len(self.divisional_winners) > 0:
            for d in self.divisional_winners:
                if d.div_number == dw.div_number:
                    raise LottoException("Divisional winner was already defined.")
                dwl.append(d)
        dwl.append(dw)
        self.divisional_winners = dwl
    def add_board_played(self, brd):
        if not isinstance(brd, Board):
            raise LottoException("Expecting a Board class")
        bl = []
        if len(self.boards_played) > 0:
            for b in self.boards_played:
                if b.board_name == brd.board_name:
                    raise LottoException("Board already played")
                bl.append(b)
        bl.append(brd)
        self.boards_played = bl
    def get_all_board_results(self):
        result = {}
        if len(self.boards_played) > 0:
            if len(self.divisional_winners) > 0:
                winning_ball_qty = 0
                special_ball_qty = 0
                winning_value = 0
                winning_div = 0
                tBalls = []
                for board in self.boards_played:
                    for ball in board.balls:
                        tBalls.append(ball.value)
                        if ball.value in self.balls_drawn:
                            winning_ball_qty += 1
                    if self.gameConf.choose_special_on_play:
                        if board.special_ball.value == self.special_ball.value:
                            special_ball_qty = 1
                    else:
                        if self.special_ball.value in tBalls:
                            special_ball_qty = 1
                    for dw in self.divisional_winners:
                        if dw.number_of_correct_balls_required == winning_ball_qty:
                            winning_div = dw.div_number
                            winning_value = dw.winning_value_per_winner
                    result[board.board_name] = [winning_ball_qty, special_ball_qty, winning_div, winning_value]
            else:
                raise LottoException("No divisional winners defined yet, so we cannot calculate the board winners")
        else:
            raise LottoException("No boards to analyse")
        return result


class LottoValidations:
    def validate_balls(self, gameConf, balls=[]):
        balls_seen = []
        if len(balls) > 0:
            for ball in balls:
                if not isinstance(ball, Ball):
                    warnings.warn("ball must be of type Ball")
                    return False
                if ball.value < gameConf.min_number or ball.value > gameConf.max_number:
                    wS = "Ball with value %s was outside the min value of %s or the max value of %s" % (ball.value, gameConf.min_number, gameConf.max_number)
                    warnings.warn(wS)
                    return False
                if ball.value in balls_seen:
                    warnings.warn("ball already defined")
                    return False
                if not ball.isSpecial:
                    balls_seen.append(ball)
                if len(balls_seen) > gameConf.number_qty_required:
                    warnings.warn("Too many balls for game: %s balls seen and max. value is set to %s" % (len(balls_seen), gameConf.number_qty_required))
                    return False
        else:
            return True
        return True
    def validation_numbers(self, numbers=[]):
        if isinstance(numbers, list):
            for n in numbers:
                if not isinstance(n, int):
                    warnings.warn("Expected an Integer")
                    return False
                if n < 0:
                    warnings.warn("Expected a positive Integer")
                    return False
        return True

class Board:
    def __init__(self, board_name="A", balls=[], special_ball=None, gameConf=None):
        if gameConf is None:
            raise LottoException("The gameConf cannot be NONE")
        if not isinstance(gameConf, GameConf):
            raise LottoException("gameConf must be of type GameConf")
        self.gameConf = gameConf
        if not isinstance(board_name, str):
            raise LottoException("The board_name must be a String")
        if len(board_name) != 1:
            raise LottoException("The board_name must be only 1 character")
        self.board_name = board_name.capitalize()
        if not isinstance(balls, list):
            raise LottoException("The balls must be passed as a list")
        if len(balls) > 0:
            tBalls = []
            for ball in balls:
                if not ball.isSpecial:
                    tBalls.append(ball)
                else:
                    if not special_ball:
                        special_ball = ball
            if lv.validate_balls(gameConf, balls):
                self.balls = tBalls
            else:
                raise LottoException("Balls did not pass validation")
        else:
            self.balls = []
        if gameConf.choose_special_on_play:
            if special_ball is not None:
                if isinstance(special_ball, Ball):
                    if special_ball.isSpecial:
                        self.special_ball = special_ball
                    else:
                        raise LottoException("Special ball must be special")
                else:
                    raise LottoException("Special ball MUST be a Ball, ok?")
            else:
                self.special_ball = None
        else:
            self.special_ball = None
        #else:
        #    raise LottoException("Special ball play violation detected. Ensure you only play a special ball if the game allows it.")

    def add_ball(self, ball):
        if not isinstance(ball, Ball):
            raise LottoException("ball is not a Ball")
        if not lv.validate_balls(self.gameConf,[ball]):
            raise LottoException("Ball validation failed")
        if self.gameConf.choose_special_on_play and ball.isSpecial:
            if self.special_ball is None:
                self.special_ball = ball
        else:
            tBalls = []
            for b in self.balls:
                tBalls.append(b)
            tBalls.append(ball)
            self.balls = tBalls

    def print_balls_sorted(self):
        bls = []
        for ball in self.balls:
            bls.append(ball.value)
        bls.sort()
        for b in bls:
            print("%s  " % b, end="")
        if self.special_ball is not None:
            if self.gameConf.choose_special_on_play:
                print("Powerball: %s" % self.special_ball, end="")
        print()

    def __repr__(self):
        ballsAsStr = "Playing game %s. no balls. " % self.gameConf.game_name
        if len(self.balls) > 0:
            ballsAsStr = "Playing game %s. " % self.gameConf.game_name
            for ball in self.balls:
                ballsAsStr += "%s   " % ball.value
        if self.special_ball is not None:
            if self.gameConf.choose_special_on_play:
                ballsAsStr += "Powerball: %s   " % self.special_ball.value
        else:
            if self.gameConf.choose_special_on_play:
                ballsAsStr += "Powerball: not choosen yet"
        return "Board %s has the following balls: %s" % (self.board_name, ballsAsStr)

class Persistance:
    def save(self, filename="unnamed.pickle", class_to_save=None):
        if class_to_save is not None:
            pickle.dump( class_to_save, open( filename, "wb" ) )
        else:
            raise LottoException("Cannot persist nothing, because....")
    def load(self, filename):
        return pickle.load( open( filename, "rb" ) )

lv = LottoValidations()
