import streamlit as st
from itertools import product

def convert_text_to_list(text):
    """Convertit le texte en liste en séparant par les retours à la ligne"""
    return [x.strip() for x in text.split('\n') if x.strip()]

def generate_combinations(lists_data, separator=' '):
    """Génère toutes les combinaisons possibles des termes avec le séparateur choisi"""
    non_empty_lists = []
    for col_data in lists_data.values():
        if col_data:
            non_empty_lists.append(col_data)
        else:
            non_empty_lists.append([''])
    
    combinations = product(*non_empty_lists)
    return [separator.join(filter(None, combo)) for combo in combinations]

def main():
    st.title("Merge Word - Fusion de termes")
    
    # Initialisation de la session state pour les résultats
    if 'result_text' not in st.session_state:
        st.session_state.result_text = ""
    
    # Configuration du nombre de colonnes
    num_cols = st.number_input(
        "Nombre de colonnes",
        min_value=2,
        max_value=10,
        value=4
    )
    
    # Option pour afficher les paramètres avancés
    show_options = st.checkbox("Afficher les options avancées")
    
    # Sélection du séparateur si les options avancées sont affichées
    separator = ' '  # Séparateur par défaut
    if show_options:
        st.subheader("Options de séparation")
        separator_option = st.radio(
            "Choisissez le type de séparateur :",
            ["Espace", "Aucun", "Tiret (-)", "Plus (+)", "Personnalisé"]
        )
        
        if separator_option == "Espace":
            separator = ' '
        elif separator_option == "Aucun":
            separator = ''
        elif separator_option == "Tiret (-)":
            separator = '-'
        elif separator_option == "Plus (+)":
            separator = '+'
        else:  # Personnalisé
            separator = st.text_input("Entrez votre séparateur personnalisé :", value=" ")
    
    # Création des colonnes avec des zones de texte
    col_data = {}
    columns = st.columns(num_cols)
    
    for i, col in enumerate(columns):
        with col:
            st.subheader(f"Colonne {i+1}")
            col_data[f"Colonne_{i+1}"] = st.text_area(
                f"Entrez les termes (un par ligne)",
                height=200,
                key=f"col_{i}",
                help="Entrez un terme par ligne"
            )
    
    if st.button("Fusionner les termes"):
        # Conversion des textes en listes
        lists_data = {
            col: convert_text_to_list(text)
            for col, text in col_data.items()
        }
        
        # Générer toutes les combinaisons avec le séparateur choisi
        merged_results = generate_combinations(lists_data, separator)
        st.session_state.result_text = '\n'.join(merged_results)
    
     # Affichage des résultats dans une zone de texte
    if st.session_state.result_text:
        st.subheader("Résultats de la fusion")
        
        # Affichage des résultats
        st.code(st.session_state.result_text)
        
        # Conversion du texte en format CSV
        csv_data = "Résultats\n" + "\n".join(st.session_state.result_text.split('\n'))
        
        # Bouton de téléchargement en CSV
        st.download_button(
            label="📥 Télécharger les résultats",
            data=csv_data,
            file_name="resultats_fusion.csv",
            mime="text/csv"
        )
    
    # Instructions d'utilisation
    st.markdown("""
    ### Instructions d'utilisation :
    1. Choisissez le nombre de colonnes souhaité
    2. Si besoin, cochez "Afficher les options avancées" pour personnaliser le séparateur
    3. Dans chaque colonne, entrez vos termes (un par ligne)
    4. Cliquez sur "Fusionner les termes"
    5. Les résultats fusionnés s'afficheront dans la zone de texte en bas
    6. Utilisez Ctrl+C (ou Cmd+C sur Mac) pour copier les résultats
    
    **Note** : 
    - Les lignes vides sont automatiquement ignorées
    - Le script génère toutes les combinaisons possibles entre les termes des différentes colonnes
    - Vous pouvez personnaliser le séparateur entre les termes via les options avancées
    """)

if __name__ == "__main__":
    main()
