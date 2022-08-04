castors_possible_names = ['Castors', 'CiLL', 'Castúdrigues', 'Castudrigues', 'Llúdrigues', 'castors', 'lludrigues',
                          'CiLl', 'cill']
dainops_possible_names = ['LLiD', 'LliD', 'Dainops', 'Llops', 'llops', 'Daines', 'daines', 'llid']
ranguis_possible_names = ['RiNG', 'Ranguis', 'Ràngers', 'Rangers', 'Noies', 'Guia', 'rangers', 'ranguis', 'ring']
pios_possible_names = ['Pios', 'PiC', 'Pioners', 'pioners', 'caravel·les', 'carave', 'pios', 'pic', 'caraveles']
truk_possible_names = ['truk', 'Truk', 'TRUK', 'trk']

POSITIVE_WEIGHT, NEGATIVE_WEIGHT = 5, 50

def custom_write(place, text: str, align: str = 'left', color: str = 'black', bold: bool = False, italic: bool = False,
                 auto_detect_color: bool = False):
    """
    Args:
        place: streamlit container or column
        text: the text to be displayed
        align: can be ['center', 'left', 'right']
        color: supported by CSS color keywords
        bold: whether to write in bold style
        italic: whether to write in italic style
    """
    if auto_detect_color and get_color(text) is not None:
        color = get_color(text)
    if bold:
        text = "<strong>" + text + "</strong>"
    if italic:
        text = "<em>" + text + "</em>"
    place.markdown(f'<div style="text-align: {align}; color: {color}"> {text} </div>', unsafe_allow_html=True)


def endline(place):
    place.markdown(f'##')


def get_color(text):
    if any(a in text for a in castors_possible_names):
        return 'tomato'
    elif any(a in text for a in dainops_possible_names):
        return 'gold'
    elif any(a in text for a in ranguis_possible_names):
        return 'cornflowerblue'
    elif any(a in text for a in pios_possible_names):
        return 'crimson'
    elif any(a in text for a in truk_possible_names):
        return 'green'
    return None


caps_lldg = [
    ('Berta Zanuy', 4, 'Femení'),
    ('Helena Serra', 4, 'Femení'),
    ('Quim Rabella', 4, 'Masculí'),
    ('Clara Hosta', 4, 'Femení'),
    ('Eli Crego', 3, 'Femení'),
    ('Mateu Salvà', 3, 'Masculí'),
    ('Gina Pallares', 3, 'Femení'),
    ('Gerard Frigola', 3, 'Masculí'),
    # ('Mia Losantos', 2, 'Femení'),
    ('Clara Estrada', 2, 'Femení'),
    ('Sara Bonal', 2, 'Femení'),
    ('Júlia Franquesa', 2, 'Femení'),
    ('Mar Rovira', 2, 'Femení'),
    ('Arnau Escolà', 1, 'Masculí'),
    ('Pol Mer', 1, 'Masculí'),
    ('Lluc Roda', 1, 'Masculí'),
    ('Marta Rovira', 1, 'Femení'),
    ('Simone Garcia', 1, 'Femení'),
    ('Maurici Rabella', 1, 'Masculí'),
    ('Max Font', 1, 'Masculí'),
    ('Ivet Roig', 1, 'Femení'),
    ('Maria Salvà', 1, 'Femení'),
    ('Amic Lluc Roda', 1, 'Masculí')
]

default_min_caps = {'CiLL': 4, 'LLiD': 4, 'RiNG': 4, 'PiC': 3, 'Truk': 2}
default_max_caps = {'CiLL': 6, 'LLiD': 6, 'RiNG': 6, 'PiC': 5, 'Truk': 3}