""" Statically loaded data """


wind_scale = list()
eight_wind_directions = dict()

# Beaufor (wind) scale (https://en.wikipedia.org/wiki/Beaufort_scale) (the unit is meter/second)
def load_beaufor_scale() -> None:
    # 0
    wind_scale_section = dict()
    wind_scale_section['min'] = 0.0
    wind_scale_section['max'] = 0.4
    wind_scale_section['description'] = "Calm"
    wind_scale.append(wind_scale_section)
    # 1
    wind_scale_section = dict()
    wind_scale_section['min'] = 0.5
    wind_scale_section['max'] = 1.5
    wind_scale_section['description'] = "Light air"
    wind_scale.append(wind_scale_section)
    # 2
    wind_scale_section = dict()
    wind_scale_section['min'] = 1.6
    wind_scale_section['max'] = 3.3
    wind_scale_section['description'] = "Light breeze"
    wind_scale.append(wind_scale_section)
    # 3
    wind_scale_section = dict()
    wind_scale_section['min'] = 3.4
    wind_scale_section['max'] = 5.4
    wind_scale_section['description'] = "Gentle breeze"
    wind_scale.append(wind_scale_section)
    # 4
    wind_scale_section = dict()
    wind_scale_section['min'] = 5.5
    wind_scale_section['max'] = 7.9
    wind_scale_section['description'] = "Moderate breeze"
    wind_scale.append(wind_scale_section)
    # 5
    wind_scale_section = dict()
    wind_scale_section['min'] = 8.0
    wind_scale_section['max'] = 10.7
    wind_scale_section['description'] = "Fresh breeze"
    wind_scale.append(wind_scale_section)
    # 6
    wind_scale_section = dict()
    wind_scale_section['min'] = 10.8
    wind_scale_section['max'] = 13.8
    wind_scale_section['description'] = "Strong breeze"
    wind_scale.append(wind_scale_section)
    # 7
    wind_scale_section = dict()
    wind_scale_section['min'] = 13.9
    wind_scale_section['max'] = 17.1
    wind_scale_section['description'] = "Moderate gale"
    wind_scale.append(wind_scale_section)
    # 8
    wind_scale_section = dict()
    wind_scale_section['min'] = 17.2
    wind_scale_section['max'] = 20.7
    wind_scale_section['description'] = "Fresh gale"
    wind_scale.append(wind_scale_section)
    # 9
    wind_scale_section = dict()
    wind_scale_section['min'] = 20.8
    wind_scale_section['max'] = 24.4
    wind_scale_section['description'] = "Strong gale"
    wind_scale.append(wind_scale_section)
    # 10
    wind_scale_section = dict()
    wind_scale_section['min'] = 24.5
    wind_scale_section['max'] = 28.4
    wind_scale_section['description'] = "Whole gale"
    wind_scale.append(wind_scale_section)
    # 11
    wind_scale_section = dict()
    wind_scale_section['min'] = 28.5
    wind_scale_section['max'] = 32.6
    wind_scale_section['description'] = "Violent storm"
    wind_scale.append(wind_scale_section)
    # 12 
    """
    wind_scale_section['min'] = 32.7
    wind_scale_section['max'] = 
    wind_scale_section['description'] = "Hurricane force"
    wind_scale.append(wind_scale_section)
    """

# Cardinal(4) and ordinal(4) directions
def load_eight_wind_directions() -> None:
    eight_wind_directions[0]="N"
    eight_wind_directions[1]="NE"
    eight_wind_directions[2]="E"
    eight_wind_directions[3]="SE"
    eight_wind_directions[4]="S"
    eight_wind_directions[5]="SW"
    eight_wind_directions[6]="W"
    eight_wind_directions[7]="NW"
    eight_wind_directions[8]="N"