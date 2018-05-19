"""
Main startup file for myGame
"""

from optparse import OptionParser

parser = OptionParser()

parser.add_option("-p", "--profile", dest="profile", default=False, action="store_true",
                    help="profile the game for speed")

(options, args) = parser.parse_args()

import game.main

if options.profile:
    import cProfile, pstats
    cProfile.run("game.main.run(options, args)", "profile")
    p = pstats.Stats("profile")
    print(p.sort_stats("cumulative").print_stats(100))
else:
    game.main.run(options, args)