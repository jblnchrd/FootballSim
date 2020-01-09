from game import *
from team import *

ravens_off = [7.3, 5.5]
ravens_def = [6.1, 4.4]
ravens_eff = [.4706, .3711]
ravens_tend = [.5602, .4398]
ravens_comp = [.6595, .5846]
ravens_turnover = 0.0182

titans_off = [7.9, 5.0]
titans_def = [6.8, 4.1]
titans_eff = [.3858, .3641]
titans_tend = [.5179, .4821]
titans_comp = [.6595, .6394]
titans_to = 0.0194

chiefs_off = [7.8, 4.2]
texans_off = [7.2, 4.6]

chiefs_def = [6.1, 4.9]
Texans_def = [7.1, 4.9]

chiefs_eff = [47.59, 37.13]
texans_eff = [43.69, 48.88]

chiefs_tend = [.6158, .3842]
texans_tend = [.5684, .4316]

chiefs_comp = [.6562, .6048]
texans_comp = [.6708, .6309]

chiefs_turnover = .0087
texans_turnover = .025

chiefs = team("Chiefs", chiefs_off, chiefs_def, chiefs_eff, chiefs_tend, chiefs_comp, chiefs_turnover, home=True)
texans = team("Texans", texans_off, Texans_def, texans_eff, texans_tend, texans_comp, texans_turnover, home=False)
ravens = team('Ravens', ravens_off, ravens_def, ravens_eff, ravens_tend, ravens_comp, ravens_turnover, home=True)
titans = team("Titans", titans_off, titans_def, titans_eff, titans_tend, titans_comp, titans_to)

new_game = game(ravens, titans)
new_game.run_game()
#new_game.run_games(100)
new_game.home_team.print_averages()
new_game.away_team.print_averages()

