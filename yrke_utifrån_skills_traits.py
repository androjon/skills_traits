import streamlit as st
import json
import itertools

@st.cache_data
def import_data(filename):
    with open(filename) as file:
        content = file.read()
    output = json.loads(content)
    return output

def show_initial_information():
    st.title("Hårda och mjuka kompetenser")
    initial_text = "Vill du starta om tryck cmd + r"
    extra_text = "Tänk på att hur begrepp är kopplade till vissa yrkesbenämningar, särskilt inom IT, inte är representativt för hela arbetsmarknaden."
    st.markdown(f"<p style='font-size:12px;'>{initial_text}</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:12px;'>{extra_text}</p>", unsafe_allow_html=True)

def hämta_hem_data():
    if "occupations_skills_traits" not in st.session_state:
        st.session_state.occupations_skills_traits = import_data("skills_traits_topplistor_min_200.json")
        st.session_state.alla_skills = import_data("valbara_skills_min_200.json")
        st.session_state.alla_traits = import_data("valbara_traits_min_200.json")

def matcha_mot_yrken_och_visa_tio(selected, typ):
    yrken_med_värden = {}
    for key, value in st.session_state.occupations_skills_traits.items():
        att_kolla = value[typ]
        värde = 0
        for s in selected:
            värde_selected = att_kolla.get(s)
            if värde_selected:
                värde += värde_selected
        yrken_med_värden[key] = värde
    yrken_med_värden = dict(sorted(yrken_med_värden.items(), key = lambda x:x[1], reverse = True))
    yrken_med_värden = dict(itertools.islice(yrken_med_värden.items(), 10))
    yrken_med_värden = {k: v for k, v in yrken_med_värden.items() if v}
    st.write(yrken_med_värden)

def välj_skills():
    selected_skills = st.multiselect(
        f"Här är en lista på ord relaterade till hårda kompetenser, arbetsuppgifter eller kunskaper som arbetsgivare ofta frågar efter i annonser.",
        (sorted(st.session_state.alla_skills)),)
    
    if selected_skills:
        matcha_mot_yrken_och_visa_tio(selected_skills, "skills")


def välj_traits():
    selected_traits = st.multiselect(
        f"Här är en lista på ord relaterade till mjuka kompetenser, förmågor eller egenskaper som arbetsgivare ofta frågar efter i annonser.",
        (sorted(st.session_state.alla_traits)),)

    if selected_traits:
        matcha_mot_yrken_och_visa_tio(selected_traits, "traits")

def choose_skills_traits():
    
    skills_or_traits = st.radio(
                f"Hitta liknande yrken utifrån skills och traits. Välj om du vill utgå från skills (hårda kompetenser, arbetsuppgifter eller kunskaper) eller traits (mjuka kompetenser, förmågor eller egenskaper).",
                ["skills", "traits"],
                horizontal = True, index = 1,
        )

    if skills_or_traits == "skills":
        välj_skills()

    if skills_or_traits == "traits":
        välj_traits()

def main ():
    hämta_hem_data()
    show_initial_information()
    choose_skills_traits()

if __name__ == '__main__':
    main ()
