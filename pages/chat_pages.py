'''

# Screen 4: Subjective
elif  st.session_state['current_screen'] == 'subjective':
    st.title('Subjective')
    with open('subjective_schema.json') as f:
        components_json = json.load(f)
    user_responses = create_components(components_json)

    if st.button('Next'):
        st.session_state['current_screen'] = 'objective'

# Screen 5: Objective        
elif  st.session_state['current_screen'] == 'objective':
    st.title('Objective')
    with open('objective_schema.json') as f:
        components_json = json.load(f)
    user_responses = create_components(components_json)

    if st.button('Next'):
        st.session_state['current_screen'] = 'assessment'

# Screen 6: Assessment
elif  st.session_state['current_screen'] == 'assessment':
    st.title('Assessment')
    with open('assessment_schema.json') as f:
        components_json = json.load(f)
    user_responses = create_components(components_json)

    if st.button('Next'):
        st.session_state['current_screen'] = 'plan'

# Screen 7: Plan
elif  st.session_state['current_screen'] == 'plan':
    st.title('Plan')
    with open('plan_schema.json') as f:
        components_json = json.load(f)
    user_responses = create_components(components_json)

    if st.button('Next'):
        st.session_state['current_screen'] = 'follow_up'

# Screen 8: Follow Up
elif  st.session_state['current_screen'] == 'follow_up':
    st.title('Follow Up')
    with open('follow_up_schema.json') as f:
        components_json = json.load(f)
    user_responses = create_components(components_json)

    if st.button('Next'):
        st.session_state['current_screen'] = 'review'
'''