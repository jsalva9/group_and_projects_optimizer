import streamlit as st


def intro():
    st.title("L'assistent de la tria de caps")
    st.markdown(
        """
        Aquesta app està pensada per aquells caus i esplais que cada any es troben la problemàtica de fer uns nous 
        equips de caps.
        El problema és complex perquè cadascú té preferències:
        - A nivell unitat (prefereixo ser cap de Llops, no vull ser animador de Truk)
        - A nivell personal (prefereixo anar amb la Marta, no vull anar amb en Robert)
        
        Aquesta aplicació es nodreix d'un motor d'optimització que maximitza el benestar del consell tenint en compte
        les preferències anteriors satisfent a algunes restriccions funcionals (min / max) nombre de persones
        a un equip, mínim d'experiència, paritat de gènere...
        
        Espero que us sigui útil! 
        """
    )