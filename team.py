
import numpy as np

class team(object):
    def __init__(self, name, offense, defense, eff, tendency, comp, turnover, home=True):
        self.name = name
        self.score = 0
        self.total_yards = 0
        if home:
            self.ypPass = offense[0] + 0.5
            self.ypRush = offense[1] + 0.5
            self.ypPass_def = defense[0] + 0.75
            self.ypRush_def = defense[1] + 0.5
            self.third_down = eff[0]
            self.third_down_def = eff[1]
            self.pass_tend = tendency[0]
            self.run_percentage = tendency[1]
            self.comp_percentage = comp[0]
            self.comp_defense = comp[1]
        else:
            self.ypPass = offense[0]
            self.ypRush = offense[1]
            self.ypPass_def = defense[0]
            self.ypRush_def = defense[1]
            self.third_down = eff[0]
            self.third_down_def = eff[1]
            self.pass_tend = tendency[0]
            self.run_percentage = tendency[1]
            self.comp_percentage = comp[0]
            self.comp_defense = comp[1]
        self.momentum = 0.0
        self.play_count = 0
        self.completions = 0
        self.incompletions = 0
        self.rush_plays = 0
        self.pass_plays = 0
        self.rush_yards = 0
        self.pass_yards = 0
        self.interception = turnover


    def set_offense(self, ratings):
        self.ypPass = ratings[0]
        self.ypRush = ratings[1]

    def set_defense(self, ratings):
        self.ypPass_def = ratings[0]
        self.ypRush_def = ratings[1]
