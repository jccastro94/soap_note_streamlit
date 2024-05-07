Drop Table if exists patient;
Drop Table if exists insurance;
Drop Table if exists medical_necessity;
Drop Table if exists appointments;
Drop Table if exists claim_information;
Drop Table if exists subluxation_details;
Drop Table if exists cmt;
Drop Table if exists subsequent_visits;
Drop Table if exists treatment_plan;

-- Create Patient Table
CREATE TABLE patient (
    id INTEGER PRIMARY KEY,
    patient_name TEXT NOT NULL,
    dob DATE NOT NULL,
    gender TEXT NOT NULL,
    marital_status TEXT,
    employment_status TEXT,
    medical_history TEXT,
    family_history TEXT
);

-- Create Insurance Table
CREATE TABLE insurance (
    id INTEGER PRIMARY KEY,
    insurance_name TEXT NOT NULL,
    insurance_form TEXT NOT NULL
);

-- Create Medical Necessity
CREATE TABLE medical_necessity (
    id INTEGER PRIMARY KEY,
    patient_id INTEGER NOT NULL,
    chief_complaint TEXT,
    mechanism_of_trauma TEXT,
    symptoms TEXT,
    quality_of_symptoms TEXT,
    onset TEXT,
    duration TEXT,
    intensity TEXT,
    frequency TEXT,
    pain_location TEXT,
    radiation TEXT,
    prior_interventions_treatments_medications_secondary TEXT,
    aggravating_factors TEXT,
    relieving_factors TEXT,
    prior_level_of_function TEXT,
    FOREIGN KEY (patient_id) REFERENCES patient (id)
);  

-- Create Appointments Table
CREATE TABLE appointments (
    id INTEGER PRIMARY KEY,
    patient_id INTEGER NOT NULL,
    appointment_date DATE NOT NULL,
    issue TEXT,
    notes TEXT,
    medical_necessity_id INTEGER,
    FOREIGN KEY (patient_id) REFERENCES patient (id),
    FOREIGN KEY (medical_necessity_id) REFERENCES medical_necessity (id)
);

-- Create Claim Information Table
CREATE TABLE claim_information (
    id INTEGER PRIMARY KEY,
    patient_id INTEGER NOT NULL,
    cpt_code TEXT,
    modifiers TEXT,
    initial_dos DATE,
    subluxation_cpt TEXT,
    second_diagnosis_code TEXT,
    FOREIGN KEY (patient_id) REFERENCES patient (id)
);

-- Create Subluxation Details Table
CREATE TABLE subluxation_details (
    id INTEGER PRIMARY KEY,
    claim_id INTEGER NOT NULL,
    cervical TEXT,
    thoracic TEXT,
    lumbar TEXT,
    sacrum_coccyx TEXT,
    pelvic TEXT,
    documentation_source TEXT,
    physical_exam_details TEXT,
    xray_details TEXT,
    FOREIGN KEY (claim_id) REFERENCES claim_information (id)
);

-- Create CMT Table
CREATE TABLE cmt (
    id INTEGER PRIMARY KEY,
    claim_id INTEGER NOT NULL,
    regions_treated_count INTEGER,
    regions_treated TEXT,
    FOREIGN KEY (claim_id) REFERENCES claim_information (id)
);



-- Create Subsequent Visits Table
CREATE TABLE subsequent_visits (
    id INTEGER PRIMARY KEY,
    patient_id INTEGER NOT NULL,
    review_of_chief_complaint BOOLEAN,
    changes_since_last_visit TEXT,
    system_review TEXT,
    exam_of_spine_area TEXT,
    assessment_of_change TEXT,
    evaluation_of_treatment_effectiveness TEXT,
    presence_absence_of_subluxation BOOLEAN,
    treatment_given BOOLEAN,
    progress_related_to_treatment_goals TEXT,
    medical_necessity_id INTEGER,
    FOREIGN KEY (patient_id) REFERENCES patient (id),
FOREIGN KEY (medical_necessity_id) REFERENCES medical_necessity (id)
);

-- Create Treatment Plan Table
CREATE TABLE treatment_plan (
    id INTEGER PRIMARY KEY,
    patient_id INTEGER NOT NULL,
    duration TEXT,
    frequency TEXT,
    specific_goals TEXT,
    objective_measures TEXT,
    expectation_of_recovery BOOLEAN,
    signed_and_dated BOOLEAN,
    FOREIGN KEY (patient_id) REFERENCES patient (id)
);
