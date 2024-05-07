import streamlit as st
import os
import json
import openai
from functions.st_functions import create_components, go_back
from functions.db_functions import search_by_id, insert_data
from functions.prompts import schema_form_filler_prompt, form_fill_prompt, form_grader_prompt
from functions.functions import log_txt
import re

if 'current_screen' not in st.session_state:
    st.session_state.current_screen = 'start'

# Screen 1: New or returning client
if st.session_state.current_screen == 'start':
    st.title('SOAP NOTE')
    st.write('Welcome Back!')
    client_type = st.radio(
        'New or returning client?',
        ['Returning Client', 'New Client'])

    if client_type == 'Returning Client':
        with st.form(key='client_search_form'):
            patient_id = st.number_input('Enter Client ID', min_value=1)
            submit_button = st.form_submit_button(label='Search')

        if submit_button:
            results = search_by_id('soap.db', "patient", patient_id)
            if not results.empty:
                st.write(results)
                st.session_state['patient_id'] = results['id'].values[0]
                st.session_state['current_screen'] = 'visit_type'

    elif client_type == 'New Client':
        with open('schemas/new_client_schema.json') as f:
            components_json = json.load(f)
        user_responses = create_components(components_json)

        if st.button('Create New Client'):
            patient_id = insert_data('soap.db', 'patient', user_responses)
            if patient_id:
                st.session_state['patient_id'] = patient_id
                st.session_state['current_screen'] = 'medical_necessity'
            else:
                st.error("Failed to create new patient.")

            '''
            Must check first if the client already exists in the database.
            If the client exists, we will display a message to the user and
            ask them to enter a different name or ID.
            If the client does not exist, we will proceed to the next step.
            '''

# Screen 2: New issue or subsequent visit
elif st.session_state['current_screen'] == 'visit_type':
    with st.form(key='get_issue_type'):
        issue_type = st.selectbox(
            'Is this a new issue or subsequent visit?',
            ('Subsequent Visit', 'New Issue'))
        submit_issue_type = st.form_submit_button(label='Start SOAP Note')

    if submit_issue_type:
        if issue_type == 'New Issue':
            st.session_state['current_screen'] = 'medical_necessity'
        elif issue_type == 'Preexisting Condition':
            st.session_state['current_screen'] = 'subsequent_visit'


# Screen 3: Medical necessity
elif st.session_state['current_screen'] == 'medical_necessity':
    if st.button('Start Over'):
        go_back()

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{
            "role": "assistant",
            "content": "Let's begin! Can you describe the chief complaint?"}]

    if "medical_necessity" not in st.session_state:
        with open('schemas/medical_necessity_schema.json') as f:
            medical_necessity_json = json.load(f)
        st.session_state['chat_schema'] = medical_necessity_json

    st.title("Medical Necessity")
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        response = schema_form_filler_prompt(
            st.session_state.messages,
            st.session_state.chat_schema)

        print(response)
        if isinstance(response, str):
            st.session_state['final_response'] = json.loads(response)
            assistant_response = st.session_state['final_response']['next_message']

        st.session_state.messages.append(
            {"role": "assistant",
             "content": assistant_response}
            )
        st.chat_message("assistant").write(assistant_response)

    if st.button("Next"):
        log_txt(st.session_state.messages,
                st.session_state.patient_id)
        st.session_state["chat_schema"] = None
        st.session_state["messages"] = [{
            "role": "assistant",
            "content": "Let's begin!"}]
        
        st.session_state['final_response']['patient_id'] = st.session_state['patient_id']
        del st.session_state['final_response']['next_message']
        del st.session_state['final_response']['completed']

        print(st.session_state['final_response'])

        medical_necessity_id = insert_data(
            'soap.db', 'medical_necessity', st.session_state['final_response']
            )
        st.session_state['medical_necessity_id'] = medical_necessity_id

        '''
        We should go to subjective screen but for demonstration purposes,
        we will go to the review screen. 
        '''
        st.session_state['current_screen'] = 'review'

# Screen 9: Review
elif st.session_state['current_screen'] == 'review':
    st.title('Review')

    data = search_by_id(
        'soap.db',
        'medical_necessity',
        st.session_state['medical_necessity_id']
        )

    with open('schemas/medical_necessity_examples.json') as f:
        examples = json.load(f)

    response_form = form_fill_prompt(examples, data)

    pattern = r"<form>(.*?)</form>"
    match = re.search(pattern, response_form, re.DOTALL)

    if match:
        extracted_content = match.group(1)
        print(extracted_content)
    else:
        print("No <form> tags found in the string.")

    st.write(extracted_content)

    with open('schemas/medical_necessity_grader.txt', encoding="UTF-8") as f:
        grading_schema = f.read()
    form_grade = form_grader_prompt(grading_schema, extracted_content)

    st.write(form_grade)

    log_txt(grading_schema + "\n" + form_grade, st.session_state.patient_id)

    if st.button('Next'):
        st.session_state['current_screen'] = 'sign_and_submit'

# Screen 10: Sign and Submit
elif st.session_state['current_screen'] == 'sign_and_submit':
    st.title('Sign and Submit')
    with open('sign_and_submit_schema.json') as f:
        components_json = json.load(f)
    user_responses = create_components(components_json)

    if st.button('Submit'):
        st.session_state['current_screen'] = 'new_or_returning_client'
