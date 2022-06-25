castors_possible_names = ['Castors', 'CiLL', 'Castúdrigues', 'Castudrigues', 'Llúdrigues', 'castors', 'lludrigues',
                          'CiLl', 'cill']
dainops_possible_names = ['LLiD', 'LliD', 'Dainops', 'Llops', 'llops', 'Daines', 'daines', 'llid']
ranguis_possible_names = ['RiNG', 'Ranguis', 'Ràngers', 'Rangers', 'Noies', 'Guia', 'rangers', 'ranguis', 'ring']
pios_possible_names = ['Pios', 'PiC', 'Pioners', 'pioners', 'caravel·les', 'carave', 'pios', 'pic', 'caraveles']
truk_possible_names = ['truk', 'Truk', 'TRUK', 'trk']


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
