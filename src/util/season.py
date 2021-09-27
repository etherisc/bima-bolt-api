
import logging

# in  'LR2021'
# out 2021, 1
def get_season_year_from_id(season_id):
    year = int(season_id[-4:])

    if season_id[0] == 'L':
        return year, 1

    return year, 2

# in  2021, 1
# out 'LR2021'
def get_season_id_from_year_season(year, season):
    if season == 1:
        return 'LR{}'.format(year)

    return 'SR{}'.format(year) 