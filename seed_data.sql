Delete from patient;
Delete from insurance;

INSERT INTO patient (id, patient_name, dob, gender, marital_status, employment_status, medical_history, family_history) VALUES
(1, 'John Doe', '1980-04-15', 'Male', 'Married', 'Employed', 'Diabetes', 'Heart Disease'),
(2, 'Jane Smith', '1992-08-21', 'Female', 'Single', 'Student', 'Asthma', 'None'),
(3, 'Michael Johnson', '1975-12-09', 'Male', 'Married', 'Self-Employed', 'Hypertension', 'Diabetes'),
(4, 'Emily Davis', '1988-03-30', 'Female', 'Married', 'Employed', 'None', 'Cancer'),
(5, 'David Brown', '1999-07-19', 'Male', 'Single', 'Unemployed', 'Allergies', 'None'),
(6, 'Jessica Wilson', '2003-05-22', 'Female', 'Single', 'Student', 'Epilepsy', 'Epilepsy'),
(7, 'Daniel Martinez', '1960-11-01', 'Male', 'Divorced', 'Retired', 'Arthritis', 'Heart Disease'),
(8, 'Sarah Taylor', '1985-09-14', 'Female', 'Widowed', 'Employed', 'Migraines', 'Diabetes'),
(9, 'Carlos Hernandez', '1994-02-05', 'Male', 'Married', 'Self-Employed', 'None', 'None'),
(10, 'Elizabeth Moore', '1965-06-27', 'Female', 'Married', 'Part-Time', 'Obesity', 'Cancer'),
(11, 'James White', '2001-10-13', 'Male', 'Single', 'Student', 'None', 'Heart Disease'),
(12, 'Lauren Garcia', '1978-01-26', 'Female', 'Divorced', 'Unemployed', 'Depression', 'None'),
(13, 'Robert Anderson', '1963-04-17', 'Male', 'Married', 'Employed', 'Asthma', 'Diabetes'),
(14, 'Sophia Jackson', '2005-12-31', 'Female', 'Single', 'Student', 'None', 'None'),
(15, 'William Lee', '1986-07-20', 'Male', 'Married', 'Self-Employed', 'Hypertension', 'Heart Disease'),
(16, 'Anna Thompson', '1990-03-15', 'Female', 'Single', 'Employed', 'None', 'Cancer'),
(17, 'Christopher Martinez', '2002-05-09', 'Male', 'Single', 'Student', 'Diabetes', 'None'),
(18, 'Isabella Rodriguez', '1996-11-23', 'Female', 'Married', 'Part-Time', 'Allergies', 'None'),
(19, 'Andrew Harris', '1972-08-30', 'Male', 'Married', 'Employed', 'None', 'Heart Disease'),
(20, 'Maria Clark', '1981-02-16', 'Female', 'Divorced', 'Freelancer', 'Migraines', 'None');

INSERT INTO insurance (id, insurance_name, insurance_form) VALUES
(1, 'Medicare', 'CMS-1500'),
(2, 'Medicaid', 'CMS-1500'),
(3, 'Blue Cross Blue Shield', '4F1-19049');


