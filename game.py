import random as rand
import numpy as np
import time

class game(object):
    def __init__(self, home_team, away_team, pause=0, prints=True):
        self.home_team = home_team
        self.away_team = away_team
        self.pause = pause
        self.prints = prints
        self.home_team.home = True
        self.away_team.home = False
        self.home_score = 0
        self.away_score = 0
        self.home_total_score = 0
        self.away_total_score = 0
        self.yard_line = 25
        self.down = 1
        self.to_go = 10
        self.marker = self.yard_line + 10
        self.plays = {"pass": self.pass_play, "rush": self.rush_play, "run or pass": self.run_or_pass, "punt": self.punt, "field goal": self.field_goal}
        self.time = 40*60
        self.offense = self.away_team
        self.defense = self.home_team
        self.has_ball = self.away_team
        self.states = ["rush", "pass complete", "pass incomplete", "Turnover", "Field Goal", "Touchdown", "punt", "kickoff", "game over", "game start"]
        self.strats = ["conservative", "aggressive", "tie", 'chew clock']
        self.situations = ['short yardage', 'long yardage', 'third and long', 'third and short', 'fourth and short', 'fourth and long']
        self.strategy = self.strats[0]
        self.situation = self.situations[0]
        self.game_state = self.states[-1]
        self.lead = self.has_ball.score - self.defense.score
        self.turnovers = 0

    def set_strat(self):
        #late game behind by more than a field goal
        self.lead = self.has_ball.score - self.defense.score
        if self.time <= 4*60.:
            if self.lead <= -4:
                self.strategy = "aggressive"
            elif -4 < self.lead <= -1:
                self.strategy = "tie"
        # tie game
            elif self.lead == 0:
                self.strategy = "conservative"
            elif self.lead > 0:
                self.strategy = "chew clock"
            else:
                self.strategy = "conservative"

        elif self.time > 4*60.:
            if self.lead <= -17:
                self.strategy = "comeback"
            elif self.lead >= 0:
                self.strategy = "conservative"

        #else:
            #self.strategy = "conservative"

    def set_situation(self):
        if self.down < 3 and self.to_go <= 5:
            return "short yardage"
        elif self.down < 3 and self.to_go > 5:
            return "long yardage"
        if self.down == 3 and self.to_go < 3:
            return "third and short"
        elif self.down == 3 and self.to_go >= 3:
            return "third and long"

        if self.down == 4 and self.yard_line >= 65:
            return "field goal"
        elif self.down == 4 and self.yard_line < 65:
            return "punt"

    def determine_play(self):
        if self.strategy == "comeback":
            return "pass"
        if self.strategy == "aggressive":
            if self.situation == "punt":
                return "punt"
            elif self.situation == "field goal":
                return "field goal"
            else:
                return "pass"
        if self.strategy == "chew clock":
            if self.situation == "punt":
                return "punt"
            elif self.situation == "field goal":
                return "field goal"
            else:
                return "rush"
        if self.strategy == "conservative":
            if self.situation == "punt":
                return "punt"
            if self.situation == "field goal":
                return "field goal"
            elif self.situation == "long yardage" or self.situation == "third and long":
                return "pass"
            else:
                return "run or pass"
        elif self.strategy == "tie":
            if self.situation == "field goal":
                return "field goal"
            if self.situation == "punt":
                return "punt"
            if self.situation == "short yardage":
                return "rush"
            if self.situation == "long yardage" or self.situation == "third and long":
                return "pass"
            else:
                return "run or pass"

    def check_td(self):
        if self.yard_line >= 100:
            self.game_state = "touchdown"
            if self.prints:
                print("Touchdown {}".format(self.has_ball.name))
            self.has_ball.score += 7
            self.has_ball.momentum += 0.0075
            self.defense.momentum -= 0.005
            self.change_poss()
            if self.prints:
                self.print_score()

    def check_turnover_on_downs(self):
        if self.down > 4:
            self.change_poss(on_downs=True)

    def update_yards(self, yards_gained):
        self.has_ball.total_yards += yards_gained

    def process_down(self):
        if self.yard_line >= self.marker:
            self.marker = self.yard_line + 10
            self.first_down()
        else:
            self.down += 1
            self.to_go = self.marker - self.yard_line

    def run_clock(self):
        if self.game_state == "rush":
            if self.strategy == "chew clock":
                self.time -= rand.randint(35, 39)
            else:
                self.time -= rand.randint(30, 35)
        if self.game_state == "pass complete":
            if self.strategy == "aggressive" or "comeback":
                self.time -= rand.randint(12, 19)
            else:
                self.time -= rand.randint(25, 39)
        else:
            self.time -= rand.randint(3, 15)

    def check_safety(self):
        if self.yard_line < 0:
            self.defense.score += 2
            self.change_poss()

    def run_play(self):
        self.set_strat()
        self.situation = self.set_situation()
        play_type = self.determine_play()
        if self.prints:
            self.print_status()
            #print("\n")
        self.plays[play_type]()
        self.has_ball.total_yards += self.has_ball.pass_yards + self.has_ball.rush_yards

        if self.game_state != "punt" and self.game_state != "field goal":
            self.has_ball.play_count += 1
            self.process_down()
        self.check_td()
        self.check_turnover_on_downs()
        self.check_safety()
        self.run_clock()

    def rush_play(self):
        rush = np.random.gamma(self.has_ball.ypRush + self.has_ball.momentum, 2.)
        allowed = np.random.gamma(self.defense.ypRush_def, 1.5)
        yards_gained = int((rush + allowed) / 2)
        yards_gained = int(yards_gained)
        self.yard_line += yards_gained
        self.game_state = "rush"
        if self.prints:
            print("Rush for a gain of {} yards.".format(yards_gained))
        self.has_ball.rush_yards += yards_gained
        self.has_ball.rush_plays += 1
        if yards_gained > 10:
            self.has_ball.momentum += 0.005
        elif yards_gained < 0:
            self.has_ball.momentum -= 0.005

    def pass_play(self):
        #determine if interception.
        pick_det = rand.random()
        if pick_det < self.has_ball.interception:
            if self.prints:
                print("INTERCEPTION!")
            self.has_ball.momentum -= .007
            self.defense.momentum += 0.09
            self.turnovers += 1
            if self.yard_line >= 80:
                self.change_poss(yard_line=25)
            else:
                self.change_poss(yard_line=(100 - self.yard_line + rand.randint(0, 19)))
        if self.down == 3:
            # average together third down efficiency and third down defense and add this to determination
            if (rand.random() - self.has_ball.momentum) < ((self.has_ball.comp_percentage + self.defense.comp_defense +
                                                           self.has_ball.third_down + self.defense.third_down_def) / 4):
                off = 0.5 * np.random.gamma(self.has_ball.ypPass, 3.5)
                defense = 0.5 * np.random.gamma(self.defense.ypPass_def, 1.1)
                yards_gained = int((off + defense) / 2)
                if self.prints:
                    print("Pass completed for a gain of {} yards.".format(yards_gained))
                self.game_state = "pass complete"
                self.yard_line += yards_gained
                self.has_ball.completions += 1
                self.has_ball.pass_yards += yards_gained
                self.has_ball.momentum += .001
                if yards_gained > 15:
                    self.has_ball.momentum += .003
        elif self.down < 3 and (np.random.normal(self.has_ball.comp_percentage) - self.has_ball.momentum) < (
                (self.has_ball.comp_percentage + self.defense.comp_defense) / 2):
            off = 0.5 * np.random.gamma(self.has_ball.ypPass, 3.3)
            defense = 0.5 * np.random.gamma(self.defense.ypPass_def, 1.1)
            yards_gained = int((off + defense) / 2)
            if self.prints:
                print("Pass completed for a gain of {} yards.".format(yards_gained))
            self.game_state = "pass complete"
            self.yard_line += yards_gained
            self.has_ball.completions += 1
            self.has_ball.pass_yards += yards_gained
            self.has_ball.momentum += .001
            if yards_gained > 15:
                self.has_ball.momentum += .003

        else:
            if self.prints:
                print("incomplete pass")
            self.game_state = "pass incomplete"
            self.has_ball.incompletions += 1
            self.has_ball.momentum -= .001
        self.has_ball.pass_plays += 1

    def field_goal(self):
        det = rand.uniform(0, 1)
        if det < self.yard_line / 100:
            self.has_ball.score += 3
            if self.prints:
                print("Field goal is good!")
                self.print_score()
            self.has_ball.momentum += 0.005
            self.change_poss()
        else:
            if self.prints:
                print("Field goal is no good!")
                self.print_score()
            self.change_poss(on_downs=True)
        self.game_state = "field goal"

    def first_down(self):
        self.down = 1
        self.marker = self.yard_line + 10
        self.to_go = 10

    def change_poss(self, on_downs=False, yard_line=25):
        if on_downs:
            self.yard_line = 100 - self.yard_line
            if self.has_ball == self.home_team:
                self.has_ball = self.away_team
                self.defense = self.home_team

            else:
                self.has_ball = self.home_team
                self.defense = self.away_team

        elif not on_downs:
            if self.has_ball == self.home_team:
                self.has_ball = self.away_team
                self.defense = self.home_team
                self.yard_line = yard_line

            else:
                self.has_ball = self.home_team
                self.defense = self.away_team
                self.yard_line = yard_line

        self.game_state = "turnover"
        self.first_down()

    def punt(self):
        punt_len = int(rand.randint(20, 60) * rand.uniform(.5, 1))
        #touchback...
        if self.yard_line + punt_len >= 100:
            self.has_ball.momentum -= 0.005
            self.change_poss()
            if self.prints:
                print("Punt for a touchback!")
        else:
            yard = 100 - (self.yard_line + punt_len)
            if self.prints:
                print("Punt (no touchback)")
            self.has_ball.momentum -= 0.005
            self.change_poss(yard_line=yard)
        self.game_state = "punt"

    def run_or_pass(self):
        det = rand.random()
        if det < self.has_ball.pass_tend:
            self.plays["pass"]()
        else:
            self.plays['rush']()

    def run_game(self):
        rand.seed(time.time)
        self.time = 40*60.
        self.yard_line = 25
        while self.time > 0:
            self.run_play()
            if self.pause > 0:
                time.sleep(self.pause)

    def run_games(self, num_games):
        for i in range(num_games):
            self.home_team.clear_stats()
            self.away_team.clear_stats()
            self.run_game()
            self.home_team.set_totals(self.home_team.score, self.home_team.pass_yards, self.home_team.rush_yards)
            self.away_team.set_totals(self.away_team.score, self.away_team.pass_yards, self.away_team.rush_yards)

        self.home_team.set_averages(num_games)
        self.away_team.set_averages(num_games)

    def print_score(self):
        print('{}: {}\n{}:{}\n'.format(self.home_team.name, self.home_team.score, self.away_team.name, self.away_team.score))

    def print_status(self):
        print('{} ball.'.format(self.has_ball.name))
        print('{} down, {} yards to go'.format(self.down, self.to_go))
        print('Ball at the {} yard line'.format(self.yard_line))
        print('{} seconds remaining'.format(self.time))
        print('{}: {}\n{}:{}\n'.format(self.home_team.name, self.home_team.score, self.away_team.name, self.away_team.score))
        #print("Momentum for {}: {}".format(self.has_ball.name, self.has_ball.momentum))
        #print("Strategy: {}*******Situation:{}".format(self.strategy, self.situation))

    def print_stats(self, team):
        print("{}".format(team.name))
        print('Completions: {} / {}'.format(team.completions, team.pass_plays))
        print('Completion Percentage: {}'.format(team.completions/team.pass_plays))
        print('Passing: {}'.format(team.pass_yards))
        print('Rushing: {}'.format(team.rush_yards))
        print('Total Yards: {}'.format(team.total_yards))
        print('YPP: {}'.format(team.total_yards/team.play_count))
        print('Total Plays: {}'.format(team.play_count))
        print("turnovers: {}".format(self.turnovers))
