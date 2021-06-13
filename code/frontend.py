from sqlalchemy.orm import sessionmaker
from project_orm import UserInput,Prediction
from sqlalchemy import create_engine
import streamlit as st
import os
from PIL import Image
from predict_parkinson import predict

def db():
    engine = create_engine('sqlite:///project_db.sqlite3')
    Session = sessionmaker(bind=engine)
    return Session()

st.sidebar.header("Parkinson Disease Prediction")
menu = ("Add patients",'Prediction','about project','instructions')
choice = st.sidebar.radio("Project menu",menu)
if choice == 'Add patients':
    st.title("Data of Patients")
    # form
    patient_id = st.number_input('enter id of patient',max_value=10000,min_value=1)
    patient_name = st.text_input('enter name of patient',max_chars=500,)
    age = st.number_input('age of patient',max_value=500,min_value=1)
    location = st.text_area("enter address")
    submit = st.button("SAVE")

    if submit and location:
        try:
            entry = UserInput(patient_id=patient_id,patient_name=patient_name,age = age,location = location)
            sess = db()
            sess.add(entry)
            sess.commit()
            st.success("Successful")
            sess.close()
        except Exception as e:
            st.error(f"some error occurred : {e}")
    else:
        st.info('please fill the data')

if choice == 'Prediction':
    sess = db()
    results = sess.query(UserInput).all()
    if results:
        patients = [obj for obj in results]
        sess.close()
        pt = st.sidebar.selectbox("select a patient to test",patients)
        sp_img = wv_img =  None
        st.title("Patient Parkinson Test")
        st.markdown(f'''
                    <table>
                        <tr><th colspan="2">Patient details</th></tr>
                        <tr><td>ID</td><td>{pt.patient_id}</td></tr>
                        <tr><td>ID</td><td>{pt.patient_name}</td></tr>
                        <tr><td>Age</td><td>{pt.age}</td></tr>
                        <tr><td>Location</td><td>{pt.location}</td></tr>
                    </table>
                    ''',unsafe_allow_html=True)

        BASE_DIR = os.path.join('uploads',str(pt.patient_id))
        if not os.path.exists(BASE_DIR):
            os.mkdir(BASE_DIR)
            os.mkdir(os.path.join(BASE_DIR,'spiral'))
            os.mkdir(os.path.join(BASE_DIR,'wave'))
        st.subheader("Upload image for spiral test")
        spiral_img = st.file_uploader("Spiral Test image",type=('png'))
        if spiral_img:
            sp_img = spiral_img.read()
            st.image(sp_img)
        
        st.subheader("Upload image for wave test")
        wave_img = st.file_uploader("wave Test image",type=('png'))
        if wave_img:
            wv_img = wave_img.read()
            st.image(wv_img)

        clicked = st.button('Click to use AI prediction')
        if clicked and wv_img and sp_img:
            with st.spinner('Please wait while we process data'):
                Image.open(wave_img).save(os.path.join(BASE_DIR,'wave','wave.png'))
                Image.open(spiral_img).save(os.path.join(BASE_DIR,'spiral','spiral.png'))
                base=os.getcwd()
                spiralpath=os.path.join(BASE_DIR,'wave','wave.png')
                wavepath=os.path.join(BASE_DIR,'spiral','spiral.png')
                out = predict(spiralpath,wavepath)
                st.success("Predictions")
                st.image(out[0])
                st.image(out[1])
                st.balloons()
                

if choice == 'about project':
    pass      

if choice =="instructions":
    pass