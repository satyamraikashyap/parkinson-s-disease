from sqlalchemy.orm import sessionmaker
from streamlit.elements.image_proto import image_to_url
from project_orm import UserInput,Prediction
from sqlalchemy import create_engine
import streamlit as st

engine = create_engine('sqlite:///project_db.sqlite3')
Session = sessionmaker(bind=engine)
sess = Session()

st.title("Data of Patients")

patient_id = st.number_input('enter id of patient',
                        max_value=10000,
                        min_value=1
                        )

patient_name = st.text_input('enter name of patient',
                        max_chars=500,
                        
                        )

age = st.number_input('age of patient',
                        max_value=500,
                        min_value=1
                        )
location = st.text_area("enter address")

submit = st.button("SAVE")

if submit and location:
    try:
        entry = UserInput(patient_id=patient_id,
                    patient_name=patient_name,
                    age = age,
                    location = location)
        sess.add(entry)
        sess.commit()
        st.success("Successful")
    except Exception as e:
        st.error(f"some error occurred : {e}")


if st.checkbox("view data"):
    results = sess.query(UserInput).all()
    for item in results:
        st.subheader(item.location)
        st.text(item.patient_name)
        st.text(item.age)
        st.text(item.patient_id)


