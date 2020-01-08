from game import *
from team import *

#chiefs_off = [7.8, 4.2]
chiefs_off = [7.8, 4.2]
texans_off = [7.2, 4.6]

chiefs_def = [6.1, 4.9]
#chiefs_def = [1, 0.1]
Texans_def = [7.1, 4.9]

chiefs_eff = [47.59, 37.13]
texans_eff = [43.69, 48.88]

chiefs_tend = [.6158, .3842]
texans_tend = [.5684, .4316]

#chiefs_comp = [.6562, .6048]
chiefs_comp = [.6562, .6048]
texans_comp = [.6708, .6309]

chiefs_turnover = .0087
texans_turnover = .025

chiefs = team("Chiefs", chiefs_off, chiefs_def, chiefs_eff, chiefs_tend, chiefs_comp, chiefs_turnover, home=True)
texans = team("Texans", texans_off, Texans_def, texans_eff, texans_tend, texans_comp, texans_turnover, home=False)

new_game = game(chiefs, texans)
new_game.run_game()
new_game.print_score()
new_game.print_stats(chiefs)
new_game.print_stats(texans)
