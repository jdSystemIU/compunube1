import numpy as np
from flask import Flask, request, jsonify, render_template, url_for
import pickle
import sklearn
import streamlit as st
import pandas as pd
import polars as pl

# Path del modelo preentrenado
DATASET_PATH = "data/TestingMod.csv"
MODEL_PATH = 'models/pickle_model.pkl'


def main():
    @st.cache(persist=True)
    def load_dataset() -> pd.DataFrame:
        disease_df = pl.read_csv(DATASET_PATH, sep=';')
        disease_df = disease_df.to_pandas()
        disease_df = pd.DataFrame(np.sort(disease_df.values, axis=0),
                                index=disease_df.index,
                                columns=disease_df.columns)
        return disease_df
    # Título
    html_temp = """
    
    </div>
    """
    st.set_page_config(
        page_title="Diseases Prediction App",
        page_icon="images/perroDoctor.png"
    )
    st.title("Predicción de Enfermedades a partir de información de sintomatología")
    st.subheader("¿Presentas síntomas que te preocupan?"
"¡No te angusties! Esta aplicación te brindará una guía de diagnóstico")
    st.markdown(html_temp,unsafe_allow_html=True)
    st.sidebar.title("Seleccione sus síntomas")


    def user_input_features() -> pd.DataFrame:
        itching = st.sidebar.selectbox("Comezón", options=("No", "Si"))
        skin_rash = st.sidebar.selectbox("Erupción cutanea", options=("No", "Si"))
        nodal_skin_eruptions = st.sidebar.selectbox("Erupciones cutáneas nodulares", options=("No", "Si"))
        continuous_sneezing = st.sidebar.selectbox("Estornudos continuos", options=("No", "Si"))
        shivering = st.sidebar.selectbox("Temblores", options=("No", "Si"))
        chills = st.sidebar.selectbox("Escalofríos", options=("No", "Si"))
        joint_pain = st.sidebar.selectbox("Dolor en las articulaciones", options=("No", "Si"))
        stomach_pain = st.sidebar.selectbox("Dolor de estómago", options=("No", "Si"))
        acidity = st.sidebar.selectbox("Acidez estomacal ", options=("No", "Si"))
        ulcers_on_tongue = st.sidebar.selectbox("Úlceras en la lengua", options=("No", "Si"))
        muscle_wasting = st.sidebar.selectbox("Atrofia muscular", options=("No", "Si"))
        vomiting = st.sidebar.selectbox("Vómitos", options=("No", "Si"))
        burning_micturition = st.sidebar.selectbox("Ardor al orinar", options=("No", "Si"))
        spotting_urination = st.sidebar.selectbox("Manchas en la orina", options=("No", "Si"))
        fatigue = st.sidebar.selectbox("Fatiga", options=("No", "Si"))
        weight_gain = st.sidebar.selectbox("Aumento de peso", options=("No", "Si"))
        anxiety = st.sidebar.selectbox("Ansiedad", options=("No", "Si"))
        cold_hands_and_feets = st.sidebar.selectbox("Manos y pies fríos", options=("No", "Si"))
        mood_swings = st.sidebar.selectbox("Cambios de humor", options=("No", "Si"))
        weight_loss = st.sidebar.selectbox("Pérdida de peso", options=("No", "Si"))
        restlessness = st.sidebar.selectbox("Intranquilidad", options=("No", "Si"))
        lethargy = st.sidebar.selectbox("Letargos", options=("No", "Si"))
        patches_in_throat = st.sidebar.selectbox("Ulceras en la garganta", options=("No", "Si"))
        irregular_sugar_level = st.sidebar.selectbox("Nivel irregular de azúcar", options=("No", "Si"))
        cough = st.sidebar.selectbox("Tos", options=("No", "Si"))
        high_fever = st.sidebar.selectbox("Fiebre alta", options=("No", "Si"))
        sunken_eyes = st.sidebar.selectbox("Ojos hundidos", options=("No", "Si"))
        breathlessness = st.sidebar.selectbox("Dificultad para respirar", options=("No", "Si"))
        sweating = st.sidebar.selectbox("Transpiración", options=("No", "Si"))
        dehydration = st.sidebar.selectbox("Deshidración", options=("No", "Si"))
        indigestion = st.sidebar.selectbox("Indigestión", options=("No", "Si"))
        headache = st.sidebar.selectbox("Dolor de cabeza", options=("No", "Si"))
        yellowish_skin = st.sidebar.selectbox("Piel amarillenta", options=("No", "Si"))
        dark_urine = st.sidebar.selectbox("Orina oscura", options=("No", "Si"))
        nausea = st.sidebar.selectbox("Náuseas", options=("No", "Si"))
        loss_of_appetite = st.sidebar.selectbox("Pérdida de apetito", options=("No", "Si"))
        pain_behind_the_eyes = st.sidebar.selectbox("Dolor detrás de los ojos", options=("No", "Si"))
        back_pain = st.sidebar.selectbox("Dolor de espalda", options=("No", "Si"))
        constipation = st.sidebar.selectbox("Constipación", options=("No", "Si"))
        abdominal_pain = st.sidebar.selectbox("Dolor abdominal", options=("No", "Si"))
        diarrhoea = st.sidebar.selectbox("Diarrea", options=("No", "Si"))
        mild_fever = st.sidebar.selectbox("Fiebre leve", options=("No", "Si"))
        yellow_urine = st.sidebar.selectbox("Orina amarillenta", options=("No", "Si"))
        yellowing_of_eyes = st.sidebar.selectbox("Ojos amarillentos", options=("No", "Si"))
        acute_liver_failure = st.sidebar.selectbox("Insuficiencia hepática aguda", options=("No", "Si"))
        fluid_overload_toxic = st.sidebar.selectbox("Sobrecarga de toxinas", options=("No", "Si"))
        swelling_of_stomach = st.sidebar.selectbox("Hinchazón del estómago", options=("No", "Si"))
        swelled_lymph_nodes = st.sidebar.selectbox("Ganglios linfáticos inflamados", options=("No", "Si"))
        malaise = st.sidebar.selectbox("Malestar", options=("No", "Si"))
        blurred_and_distorted_vision = st.sidebar.selectbox("Visión borrosa y distorsionada", options=("No", "Si"))
        phlegm = st.sidebar.selectbox("Flema", options=("No", "Si"))
        throat_irritation = st.sidebar.selectbox("Irritación de garganta", options=("No", "Si"))
        redness_of_eyes = st.sidebar.selectbox("Enrojecimiento de los ojos", options=("No", "Si"))
        sinus_pressure = st.sidebar.selectbox("Presión en los senos", options=("No", "Si"))
        runny_nose = st.sidebar.selectbox("Rinorrea", options=("No", "Si"))
        congestion = st.sidebar.selectbox("Congestión", options=("No", "Si"))
        chest_pain = st.sidebar.selectbox("Dolor de pecho", options=("No", "Si"))
        weakness_in_limbs = st.sidebar.selectbox("Debilidad en las extremidades", options=("No", "Si"))
        fast_heart_rate = st.sidebar.selectbox("Frecuencia cardíaca rápida", options=("No", "Si"))
        pain_during_bowel_movements = st.sidebar.selectbox("Dolor durante las defecaciones", options=("No", "Si"))
        pain_in_anal_region = st.sidebar.selectbox("Dolor en la región anal", options=("No", "Si"))
        bloody_stool = st.sidebar.selectbox("Heces con sangre", options=("No", "Si"))
        irritation_in_anus = st.sidebar.selectbox("Irritación en el ano", options=("No", "Si"))
        neck_pain = st.sidebar.selectbox("Dolor de cuello", options=("No", "Si"))
        dizziness = st.sidebar.selectbox("Mareo", options=("No", "Si"))
        cramps = st.sidebar.selectbox("Calambres", options=("No", "Si"))
        bruising = st.sidebar.selectbox("Hematomas", options=("No", "Si"))
        obesity = st.sidebar.selectbox("Obesidad", options=("No", "Si"))
        swollen_legs = st.sidebar.selectbox("Piernas hinchadas", options=("No", "Si"))
        swollen_blood_vessels = st.sidebar.selectbox("Vasculitis", options=("No", "Si"))
        puffy_face_and_eyes = st.sidebar.selectbox("Cara y ojos hinchados", options=("No", "Si"))
        enlarged_thyroid = st.sidebar.selectbox("Tiroides agrandada", options=("No", "Si"))
        brittle_nails = st.sidebar.selectbox("Uñas quebradizas", options=("No", "Si"))
        swollen_extremeties = st.sidebar.selectbox("Extremidades hinchadas", options=("No", "Si"))
        excessive_hunger = st.sidebar.selectbox("Hambre excesiva", options=("No", "Si"))
        extra_marital_contacts = st.sidebar.selectbox("Contactos extramatrimoniales", options=("No", "Si"))
        drying_and_tingling_lips = st.sidebar.selectbox("Labios secos y presencia de hormigueo", options=("No", "Si"))
        slurred_speech = st.sidebar.selectbox("Habla lenta (letargo)", options=("No", "Si"))
        knee_pain = st.sidebar.selectbox("Dolor de rodilla", options=("No", "Si"))
        hip_joint_pain = st.sidebar.selectbox("Dolor de cadera", options=("No", "Si"))
        muscle_weakness = st.sidebar.selectbox("Debilidad muscular", options=("No", "Si"))
        stiff_neck = st.sidebar.selectbox("Rigidez en el cuello", options=("No", "Si"))
        swelling_joints = st.sidebar.selectbox("Articulaciones hinchadas", options=("No", "Si"))
        movement_stiffness = st.sidebar.selectbox("Rigidez articular", options=("No", "Si"))
        spinning_movements = st.sidebar.selectbox("Deficiencia de rotación interna articular", options=("No", "Si"))
        loss_of_balance = st.sidebar.selectbox("Pérdida del equilibrio", options=("No", "Si"))
        unsteadiness = st.sidebar.selectbox("Inestabilidad", options=("No", "Si"))
        weakness_of_one_body_side = st.sidebar.selectbox("Debilidad en un lado del cuerpo", options=("No", "Si"))
        loss_of_smell = st.sidebar.selectbox("Perdida del olfato", options=("No", "Si"))
        bladder_discomfort = st.sidebar.selectbox("Incomodidad de la vejiga", options=("No", "Si"))
        foul_smell_of_urine = st.sidebar.selectbox("Mal olor en la orina", options=("No", "Si"))
        continuous_feel_of_urine = st.sidebar.selectbox("Sensación continua de orina", options=("No", "Si"))
        passage_of_gases = st.sidebar.selectbox("Escape de gases", options=("No", "Si"))
        internal_itching = st.sidebar.selectbox("Picazón en la uretra", options=("No", "Si"))
        toxic_look_typhos = st.sidebar.selectbox("Fiebre tifoidea", options=("No", "Si"))
        depression = st.sidebar.selectbox("Depresión", options=("No", "Si"))
        irritability = st.sidebar.selectbox("Irritabilidad", options=("No", "Si"))
        muscle_pain = st.sidebar.selectbox("Dolor muscular", options=("No", "Si"))
        altered_sensorium = st.sidebar.selectbox("Alteracion sensorial", options=("No", "Si"))
        red_spots_over_body = st.sidebar.selectbox("Manchas rojas en el cuerpo", options=("No", "Si"))
        belly_pain = st.sidebar.selectbox("Dolor en el vientre", options=("No", "Si"))
        abnormal_menstruation = st.sidebar.selectbox("Menstruación anormal", options=("No", "Si"))
        dischromic_patches = st.sidebar.selectbox("Discromia", options=("No", "Si"))
        watering_from_eyes = st.sidebar.selectbox("Ojos llorosos", options=("No", "Si"))
        increased_appetite = st.sidebar.selectbox("Apetito incrementado", options=("No", "Si"))
        polyuria = st.sidebar.selectbox("Poliuria", options=("No", "Si"))
        family_history = st.sidebar.selectbox("Antecedentes familiares de poliuria", options=("No", "Si"))
        mucoid_sputum = st.sidebar.selectbox("Flema con moco", options=("No", "Si"))
        rusty_sputum = st.sidebar.selectbox("Flema amarilla", options=("No", "Si"))
        lack_of_concentration = st.sidebar.selectbox("Falta de concentración", options=("No", "Si"))
        visual_disturbances = st.sidebar.selectbox("Alteraciones visuales", options=("No", "Si"))
        receiving_blood_transfusion = st.sidebar.selectbox("¿Ha recibido transfusión de sangre?", options=("No", "Si"))
        receiving_unsterile_injections = st.sidebar.selectbox("¿Ha recibido inyecciones no estériles?", options=("No", "Si"))
        coma = st.sidebar.selectbox("Coma", options=("No", "Si"))
        stomach_bleeding = st.sidebar.selectbox("Sangrado estomacal", options=("No", "Si"))
        distention_of_abdomen = st.sidebar.selectbox("Distensión abdominal", options=("No", "Si"))
        history_of_alcohol_consumption = st.sidebar.selectbox("Consumo excesivo de alcohol", options=("No", "Si"))
        fluid_overload = st.sidebar.selectbox("Hipervolemia (Sobrecarga de líquidos)", options=("No", "Si"))
        blood_in_sputum = st.sidebar.selectbox("Flema con sangre", options=("No", "Si"))
        prominent_veins_on_calf = st.sidebar.selectbox("Venas varices", options=("No", "Si"))
        palpitations = st.sidebar.selectbox("Palpitaciones", options=("No", "Si"))
        painful_walking = st.sidebar.selectbox("Caminata dolorosa", options=("No", "Si"))
        pus_filled_pimples = st.sidebar.selectbox("Espinillas llenas de pus", options=("No", "Si"))
        blackheads = st.sidebar.selectbox("Puntos negros", options=("No", "Si"))
        scurring = st.sidebar.selectbox("Pústulas de acne", options=("No", "Si"))
        skin_peeling = st.sidebar.selectbox("Descamación de piel", options=("No", "Si"))
        silver_like_dusting = st.sidebar.selectbox("Contacto permanente con metales (plata)", options=("No", "Si"))
        small_dents_in_nails = st.sidebar.selectbox("Pequeñas abolladuras en las uñas", options=("No", "Si"))
        inflammatory_nails = st.sidebar.selectbox("Uñas inflamadas", options=("No", "Si"))
        blister = st.sidebar.selectbox("Ampollas", options=("No", "Si"))
        red_sore_around_nose = st.sidebar.selectbox("Llaga alrededor de la nariz", options=("No", "Si"))
        yellow_crust_ooze = st.sidebar.selectbox("Costra infectada supurando ", options=("No", "Si"))

        features = pd.DataFrame({
            "itching": [itching],
            "skin_rash": [skin_rash],
            "nodal_skin_eruptions": [nodal_skin_eruptions],
            "continuous_sneezing": [continuous_sneezing],
            "shivering": [shivering],
            "chills": [chills],
            "joint_pain": [joint_pain],
            "stomach_pain": [stomach_pain],
            "acidity": [acidity],
            "ulcers_on_tongue": [ulcers_on_tongue],
            "muscle_wasting": [muscle_wasting],
            "vomiting": [vomiting],
            "burning_micturition": [burning_micturition],
            "spotting_ urination": [spotting_urination],
            "fatigue": [fatigue],
            "weight_gain": [weight_gain],
            "anxiety": [anxiety],
            "cold_hands_and_feets": [cold_hands_and_feets],
            "mood_swings": [mood_swings],
            "weight_loss": [weight_loss],
            "restlessness": [restlessness],
            "lethargy": [lethargy],
            "patches_in_throat": [patches_in_throat],
            "irregular_sugar_level": [irregular_sugar_level],
            "cough": [cough],
            "high_fever": [high_fever],
            "sunken_eyes": [sunken_eyes],
            "breathlessness": [breathlessness],
            "sweating": [sweating],
            "dehydration": [dehydration],
            "indigestion": [indigestion],
            "headache": [headache],
            "yellowish_skin": [yellowish_skin],
            "dark_urine": [dark_urine],
            "nausea": [nausea],
            "loss_of_appetite": [loss_of_appetite],
            "pain_behind_the_eyes": [pain_behind_the_eyes],
            "back_pain": [back_pain],
            "constipation": [constipation],
            "abdominal_pain": [abdominal_pain],
            "diarrhoea": [diarrhoea],
            "mild_fever": [mild_fever],
            "yellow_urine": [yellow_urine],
            "yellowing_of_eyes": [yellowing_of_eyes],
            "acute_liver_failure": [acute_liver_failure],
            "fluid_overload_toxic": [fluid_overload_toxic],
            "swelling_of_stomach": [swelling_of_stomach],
            "swelled_lymph_nodes": [swelled_lymph_nodes],
            "malaise": [malaise],
            "blurred_and_distorted_vision": [blurred_and_distorted_vision],
            "phlegm": [phlegm],
            "throat_irritation": [throat_irritation],
            "redness_of_eyes": [redness_of_eyes],
            "sinus_pressure": [sinus_pressure],
            "runny_nose": [runny_nose],
            "congestion": [congestion],
            "chest_pain": [chest_pain],
            "weakness_in_limbs": [weakness_in_limbs],
            "fast_heart_rate": [fast_heart_rate],
            "pain_during_bowel_movements": [pain_during_bowel_movements],
            "pain_in_anal_region": [pain_in_anal_region],
            "bloody_stool": [bloody_stool],
            "irritation_in_anus": [irritation_in_anus],
            "neck_pain": [neck_pain],
            "dizziness": [dizziness],
            "cramps": [cramps],
            "bruising": [bruising],
            "obesity": [obesity],
            "swollen_legs": [swollen_legs],
            "swollen_blood_vessels": [swollen_blood_vessels],
            "puffy_face_and_eyes": [puffy_face_and_eyes],
            "enlarged_thyroid": [enlarged_thyroid],
            "brittle_nails": [brittle_nails],
            "swollen_extremeties": [swollen_extremeties],
            "excessive_hunger": [excessive_hunger],
            "extra_marital_contacts": [extra_marital_contacts],
            "drying_and_tingling_lips": [drying_and_tingling_lips],
            "slurred_speech": [slurred_speech],
            "knee_pain": [knee_pain],
            "hip_joint_pain": [hip_joint_pain],
            "muscle_weakness": [muscle_weakness],
            "stiff_neck": [stiff_neck],
            "swelling_joints": [swelling_joints],
            "movement_stiffness": [movement_stiffness],
            "spinning_movements": [spinning_movements],
            "loss_of_balance": [loss_of_balance],
            "unsteadiness": [unsteadiness],
            "weakness_of_one_body_side": [weakness_of_one_body_side],
            "loss_of_smell": [loss_of_smell],
            "bladder_discomfort": [bladder_discomfort],
            "foul_smell_of urine": [foul_smell_of_urine],
            "continuous_feel_of_urine": [continuous_feel_of_urine],
            "passage_of_gases": [passage_of_gases],
            "internal_itching": [internal_itching],
            "toxic_look_(typhos)": [toxic_look_typhos],
            "depression": [depression],
            "irritability": [irritability],
            "muscle_pain": [muscle_pain],
            "altered_sensorium": [altered_sensorium],
            "red_spots_over_body": [red_spots_over_body],
            "belly_pain": [belly_pain],
            "abnormal_menstruation": [abnormal_menstruation],
            "dischromic _patches": [dischromic_patches],
            "watering_from_eyes": [watering_from_eyes],
            "increased_appetite": [increased_appetite],
            "polyuria": [polyuria],
            "family_history": [family_history],
            "mucoid_sputum": [mucoid_sputum],
            "rusty_sputum": [rusty_sputum],
            "lack_of_concentration": [lack_of_concentration],
            "visual_disturbances": [visual_disturbances],
            "receiving_blood_transfusion": [receiving_blood_transfusion],
            "receiving_unsterile_injections": [receiving_unsterile_injections],
            "coma": [coma],
            "stomach_bleeding": [stomach_bleeding],
            "distention_of_abdomen": [distention_of_abdomen],
            "history_of_alcohol_consumption": [history_of_alcohol_consumption],
            "fluid_overload": [fluid_overload],
            "blood_in_sputum": [blood_in_sputum],
            "prominent_veins_on_calf": [prominent_veins_on_calf],
            "palpitations": [palpitations],
            "painful_walking": [painful_walking],
            "pus_filled_pimples": [pus_filled_pimples],
            "blackheads": [blackheads],
            "scurring": [scurring],
            "skin_peeling": [skin_peeling],
            "silver_like_dusting": [silver_like_dusting],
            "small_dents_in_nails": [small_dents_in_nails],
            "inflammatory_nails": [inflammatory_nails],
            "blister": [blister],
            "red_sore_around_nose": [red_sore_around_nose],
            "yellow_crust_ooze": [yellow_crust_ooze]
            })
        return features
    # Manejo de datos

    cat_cols = ["itching", "skin_rash", "nodal_skin_eruptions", "continuous_sneezing", 
                "shivering", "chills", "joint_pain", "stomach_pain", "acidity", "ulcers_on_tongue", 
                "muscle_wasting", "vomiting", "burning_micturition", "spotting_ urination", "fatigue", 
                "weight_gain", "anxiety", "cold_hands_and_feets", "mood_swings", "weight_loss", 
                "restlessness", "lethargy", "patches_in_throat", "irregular_sugar_level", "cough", 
                "high_fever", "sunken_eyes", "breathlessness", "sweating", "dehydration", "indigestion", 
                "headache", "yellowish_skin", "dark_urine", "nausea", "loss_of_appetite", 
                "pain_behind_the_eyes", "back_pain", "constipation", "abdominal_pain", "diarrhoea", 
                "mild_fever", "yellow_urine", "yellowing_of_eyes", "acute_liver_failure", 
                "fluid_overload_toxic", "swelling_of_stomach", "swelled_lymph_nodes", "malaise", 
                "blurred_and_distorted_vision", "phlegm", "throat_irritation", "redness_of_eyes", 
                "sinus_pressure", "runny_nose", "congestion", "chest_pain", "weakness_in_limbs", 
                "fast_heart_rate", "pain_during_bowel_movements", "pain_in_anal_region", "bloody_stool", 
                "irritation_in_anus", "neck_pain", "dizziness", "cramps", "bruising", "obesity",
                "swollen_legs", "swollen_blood_vessels", "puffy_face_and_eyes", "enlarged_thyroid", 
                "brittle_nails", "swollen_extremeties", "excessive_hunger", "extra_marital_contacts", 
                "drying_and_tingling_lips", "slurred_speech", "knee_pain", "hip_joint_pain", 
                "muscle_weakness", "stiff_neck", "swelling_joints", "movement_stiffness", 
                "spinning_movements", "loss_of_balance", "unsteadiness", "weakness_of_one_body_side", 
                "loss_of_smell", "bladder_discomfort", "foul_smell_of urine", "continuous_feel_of_urine", 
                "passage_of_gases", "internal_itching", "toxic_look_(typhos)", "depression", 
                "irritability", "muscle_pain", "altered_sensorium", "red_spots_over_body", "belly_pain", 
                "abnormal_menstruation", "dischromic _patches", "watering_from_eyes", 
                "increased_appetite", "polyuria", "family_history", "mucoid_sputum", "rusty_sputum", 
                "lack_of_concentration", "visual_disturbances", "receiving_blood_transfusion", 
                "receiving_unsterile_injections", "coma", "stomach_bleeding", "distention_of_abdomen", 
                "history_of_alcohol_consumption", "fluid_overload", "blood_in_sputum", 
                "prominent_veins_on_calf", "palpitations", "painful_walking", "pus_filled_pimples", 
                "blackheads", "scurring", "skin_peeling", "silver_like_dusting", "small_dents_in_nails", 
                "inflammatory_nails", "blister", "red_sore_around_nose", "yellow_crust_ooze"]

    df_dataset = load_dataset()
    #st.write(df_dataset)


    input_df = user_input_features()
    df = pd.concat([input_df, df_dataset], axis=0)
    df = df.drop(columns=["prognosis"])
    
    df=df.replace({"No": 0, "Si": 1})
    df = df[:1]
    #st.write(df)
    df.fillna(0, inplace=True)
    log_model = pickle.load(open(MODEL_PATH, "rb"))

    col1, col2 = st.columns([1, 2])

    with col2:
        st.markdown("""
            El aprendizaje automático ha promovido progresos en diversos campos, tales como finanzas, industria, robótica, marketing, distribución de recursos, entre otros. En este sentido, la capacidad de los modelos de aprendizaje automático para extraer información de los datos, junto con la centralidad de los datos en el cuidado de la salud, ha tenido un impacto crucial en el diagnóstico oportuno de enfermedades, manejo y seguimiento de tratamientos. 
            
            En esta aplicación, se construyó un modelo de regresión logística utilizando datos de información clínica con 132 síntomas y 4920 muestras, las cuales abarcan desde dolores físicos hasta signos de comportamiento, lo cual permite hacer un análisis de enfermedades de tipo cardiovascular, gastrointestinal, enfermedades tropicales, respiratorias, crónicas y otro tipo de patologías.
            Para obtener un diagnóstico de su enfermedad basado en sintomatología, siga los siguientes pasos:
            
            1)  Seleccione los síntomas que ha presentado en los últimos días con un “Si”. 
            2)  Presione el botón "Predecir" y espere el resultado. 

            ¡Recuerde que estos resultados no equivalen a un diagnóstico médico! Por lo tanto, se recomienda que consulte a un médico. 
            
            Autor: Daniela Restrepo G., Joseph David Gómez C. y Miguel Angel Caycedo R.
            """)
    with col1:
        st.image("images/perroDoctor.png",
                caption="Wowf! En que puedo ayudarte",
                width=200)
    # El botón predicción se usa para iniciar el procesamiento
    if st.button("Predicción :"): 
        prediction = log_model.predict(df)
        
        prediction = prediction[0]

        prueba = prediction.replace("Fungal infection", "Micosis").replace("Allergy", "Alergia").replace("GERD", "Reflujo gastroesofágico").replace("Chronic cholestasis", "Colestasis crónica").replace("Drug Reaction", "Reacción alérgica por drogas").replace("Peptic ulcer diseae", "Enfermedad de úlcera péptica").replace("AIDS", "SIDA").replace("Diabetes ", "Diabetes").replace("Gastroenteritis", "Gastroenteritis").replace("Bronchial Asthma", "Asma bronquial").replace("Hypertension ", "Hipertensión").replace("Migraine", "Migraña").replace("Cervical spondylosis", "Espondilosis cervical").replace("Paralysis (brain hemorrhage)", "Parálisis (hemorragia cerebral)").replace("Jaundice", "Ictericia").replace("Malaria", "Malaria").replace("Chicken pox", "Varicela").replace("Dengue", "Dengue").replace("Typhoid", "Tifoidea").replace("hepatitis A", "Hepatitis A").replace("Hepatitis B", "Hepatitis B").replace("Hepatitis C", "Hepatitis C").replace("Hepatitis D", "Hepatitis D").replace("Hepatitis E", "Hepatitis E").replace("Alcoholic hepatitis", "Hepatitis alcohólica").replace("Tuberculosis", "Tuberculosis").replace("Common Cold", "Resfriado comun").replace("Pneumonia", "Neumonía").replace("Dimorphic hemmorhoids(piles)", "Hemorroides dimórficas (almorranas)").replace("Heart attack", "Infarto de miocardio").replace("Varicose veins", "Venas varicosas").replace("Hypothyroidism", "Hipotiroidismo").replace("Hyperthyroidism", "Hipertiroidismo").replace("Hypoglycemia", "Hipoglucemia").replace("Osteoarthristis", "Osteoartritis").replace("Arthritis", "Artritis").replace("(vertigo) Paroymsal Positional Vertigo", "(Vértigo) Vértigo posicional paroxístico").replace("Acne", "Acné").replace("Urinary tract infection", "Infección del tracto urinario").replace("Psoriasis", "Psoriasis").replace("Impetigo", "Impétigo")
        #st.write(prediction)
        st.success('La enfermedad es: {}'.format(prueba).upper())
        #anterior forma
        #st.success('La enfermedad es: {}'.format(prediction[0]).upper())


if __name__ == '__main__':
    main()
