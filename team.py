
import numpy as np

class team(object):
    def __init__(self, name, offense, defense, eff, tendency, comp, turnover, dvoa, home=False):
        self.name = name
        self.score = 0
        self.total_yards = 0
        self.sum_total_yards = 0
        self.total_pass = 0
        self.total_rush = 0
        self.total_score = 0
        self.average_score = 0
        self.average_pass = 0
        self.average_rush = 0
        self.home = home
        if self.home:
            self.ypPass = offense[0] + 0.1 + (dvoa[0] / 20)
            self.ypRush = offense[1] + 0.1 + (dvoa[0] / 10)
            self.ypPass_def = defense[0] - 0.15 - (dvoa[1] / 20)
            self.ypRush_def = defense[1] - 0.15 - (dvoa[1] / 10)
            self.third_down = eff[0]
            self.third_down_def = eff[1]
            self.pass_tend = tendency[0]
            self.run_percentage = tendency[1]
            self.comp_percentage = comp[0]
            self.comp_defense = comp[1]
            self.off_dvoa = dvoa[0]
            self.def_dvoa = dvoa[1]
        else:
            self.ypPass = offense[0] + (dvoa[0] / 22)
            self.ypRush = offense[1] + (dvoa[0] / 12)
            self.ypPass_def = defense[0] - (dvoa[1] / 22)
            self.ypRush_def = defense[1] - (dvoa[1] / 12)
            self.third_down = eff[0]
            self.third_down_def = eff[1]
            self.pass_tend = tendency[0]
            self.run_percentage = tendency[1]
            self.comp_percentage = comp[0]
            self.comp_defense = comp[1]
            self.off_dvoa = dvoa[0]
            self.def_dvoa = dvoa[1]
        #stats
        self.momentum = 0.0
        self.play_count = 0
        self.completions = 0
        self.incompletions = 0
        self.rush_plays = 0
        self.pass_plays = 0
        self.rush_yards = 0
        self.pass_yards = 0
        self.interception = turnover

    def clear_stats(self):
        self.momentum = 0.0
        self.play_count = 0
        self.completions = 0
        self.incompletions = 0
        self.rush_plays = 0
        self.pass_plays = 0
        self.rush_yards = 0
        self.pass_yards = 0
        self.score = 0
        #self.total_yards = 0
        #self.total_pass = 0
        #self.total_rush = 0

    def set_offense(self, ratings):
        self.ypPass = ratings[0]
        self.ypRush = ratings[1]

    def set_defense(self, ratings):
        self.ypPass_def = ratings[0]
        self.ypRush_def = ratings[1]

    def set_totals(self, score, passing, rushing):
        self.total_score += score
        self.total_pass += passing
        self.total_rush += rushing

    def set_averages(self, games):
        self.average_score = self.total_score / games
        self.average_pass = self.total_pass / games
        self.average_rush = self.total_rush / games

    def print_averages(self):
        print("**********{}***********".format(self.name))
        print('Avg Score: {}\nAvg Pass: {}\nAvg Rush: {}'.format(self.average_score, self.average_pass, self.average_rush))
