castors_possible_names = ['Castors', 'CiLL', 'Castúdrigues', 'Castudrigues', 'Llúdrigues', 'castors', 'lludrigues']
dainops_possible_names = ['LLiD', 'LliD', 'Dainops', 'Llops', 'llops', 'Daines', 'daines']
ranguis_possible_names = ['RiNG', 'Ranguis', 'Ràngers', 'Rangers', 'Noies', 'Guia', 'rangers', 'ranguis']
pios_possible_names = ['Pios', 'PiC', 'Pioners', 'pioners', 'caravel·les', 'carave', 'pios']
truk_possible_names = ['truk', 'Truk', 'TRUK']


def custom_write(place, text: str, align: str = 'left', color: str = 'black', bold: bool = False, italic: bool = False, auto_detect_color: bool = False):
    """

    Args:
        place:
        text:
        align: can be ['center', 'left', 'right']
        color:
        bold:
        italic:
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
        return 'orange'
    elif any(a in text for a in dainops_possible_names):
        return 'yellow'
    elif any(a in text for a in ranguis_possible_names):
        return 'blue'
    elif any(a in text for a in pios_possible_names):
        return 'red'
    elif any(a in text for a in truk_possible_names):
        return 'green'
    return None

