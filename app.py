import streamlit as st
import json
import time
from models.schema import SurveyResponse
from services.engine import get_session
from utils.validation import validate_form

st.set_page_config(page_title="DineRate", page_icon="⭐")
st.title("⭐ DineRate")

with st.form("Survey Form", clear_on_submit=True):
    full_name = st.text_input("Full Name (optional)")
    col1, col2 = st.columns([1, 2])
    with col1:
        age = st.text_input("Age")
        date_of_visit = st.date_input("Date of Visit", value=None)
    with col2:
        email = st.text_input("E-mail (optional)")
        gender = st.radio("Gender", options=[
                          "Male", "Female", "Rather not say"], horizontal=True, index=None)

    st.subheader("Survey Questions")
    with open("data/survey_questions.json", "r") as content:
        questions = json.load(content)

    responses = {}
    for qid, value in questions.items():
        st.write(value["question"])
        if value["type"] == "rating":
            responses[qid] = st.feedback(key=qid, options="stars")
        elif value["type"] == "bool":
            responses[qid] = st.radio("Choices", options=[
                                      "Yes", "No"], label_visibility="collapsed", key=qid, index=None)
        else:
            responses[qid] = st.text_area(
                "Comments/Suggestions", label_visibility="collapsed", placeholder="Comments/Suggestions", key=qid)

    submitted = st.form_submit_button("Submit")

if submitted:
    error = validate_form(age, date_of_visit, gender, responses)
    if error:
        st.warning(error)
    else:
        with get_session() as session:
            for qid, answer in responses.items():
                if questions[qid]["type"] == "rating" and answer is not None:
                    answer = str(int(answer) + 1)
                db_entry = SurveyResponse(
                    full_name=full_name,
                    age=int(age),
                    email=email,
                    gender=gender,
                    date_of_visit=date_of_visit,
                    qid=qid,
                    question=questions[qid]["question"],
                    answer=str(answer)
                )
                session.add(db_entry)
            session.commit()

        success_msg = st.empty()
        success_msg.success(
            "Your response has been saved successfully! Thank you for answering!")
        time.sleep(2)
        success_msg.empty()
