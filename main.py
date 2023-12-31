import streamlit as st
import pandas as pd
import numpy as np
import psycopg2
import boto3
from botocore.exceptions import ClientError

countries_list = [
    'Afghanistan','Albania','Algeria','Andorra','Angola','Antigua and Barbuda',
    'Argentina','Armenia','Australia','Austria','Azerbaijan','Bahamas','Bahrain','Bangladesh',
    'Barbados','Belarus','Belgium','Belize','Benin','Bhutan','Bolivia',
    'Bosnia and Herzegovina','Botswana','Brazil','Brunei','Bulgaria','Burkina Faso','Burundi','Cambodia','Cameroon','Canada','Cape Verde',
    'Central African Republic','Chad','Chile','China','Colombia','Comoros',
    'Congo, Democratic Republic of the','Congo, Republic of the','Costa Rica',
    'Côte d\'Ivoire (Ivory Coast)','Croatia','Cuba','Cyprus',
    'Czech Republic (Czechia)','Denmark','Djibouti','Dominica',
    'Dominican Republic','East Timor (Timor-Leste)','Ecuador','Egypt','El Salvador',
    'England','Equatorial Guinea','Eritrea','Estonia','Eswatini (formerly Swaziland)',
    'Ethiopia','Federated States of Micronesia','Fiji','Finland','France','Gabon',
    'Gambia, The','Georgia','Germany','Ghana','Greece','Grenada','Guatemala',
    'Guinea','Guinea-Bissau','Guyana','Haiti','Honduras',
    'Hungary','Iceland','India','Indonesia','Iran','Iraq','Ireland','Italy','Jamaica','Japan',
    'Jordan','Kazakhstan','Kenya','Kiribati','Kosovo','Kuwait','Kyrgyzstan','Laos','Latvia','Lebanon','Lesotho',
    'Liberia','Libya','Liechtenstein','Lithuania','Luxembourg','Macedonia, Republic of (North Macedonia)',
    'Madagascar','Malawi''Malaysia','Maldives','Mali','Malta','Marshall Islands', 'Mauritania', 'Mauritius','Mexico','Micronesia, Federated States of','Moldova','Monaco',
    'Mongolia','Montenegro','Morocco','Mozambique','Myanmar (Burma)','Namibia',
    'Nauru','Nepal','Netherlands','New Zealand','Nicaragua','Niger','Nigeria',
    'North Korea','Northern Ireland','Norway','Oman','Pakistan','Palau',"Palestine", 
    "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia", "Rwanda", 
    "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", 
    "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia", "Scotland", 
    "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", 
    "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Korea", "South Sudan", 
    "Spain", "Sri Lanka", "Sudan", "Suriname", "Swaziland (Eswatini)", "Sweden", "Switzerland", 
    "Syria", "Taiwan", "Tajikistan", "Tanzania", "Thailand", "Togo", "Tonga", "Trinidad and Tobago", 
    "Tunisia", "Türkiye (Turkey)", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", 
    "United Kingdom", "United States of America", "Uruguay", "Uzbekistan", "Vanuatu", "Vatican City", 
    "Venezuela", "Vietnam", "Wales", "Yemen", "Zambia", "Zimbabwe"]
positions_list = ['Software Engineer', 'Front-End Developer', 'Back-End Developer', 'Data Scientist', 'Data Engineer', 'Cloud Developer', 'IT Support', 'Embedded Engineer']

st.title('Job Application')

st.image("https://media.istockphoto.com/id/182444113/photo/office-building-exteriors.jpg?s=612x612&w=0&k=20&c=ecyKmK4ayad81hrKpYo6F8NAkzLeFINjyHTXWwQt2us=", use_column_width='always')
st.markdown('https://github.com/MinaBasem/job-applications-system-on-aws/tree/main')
col1, col2 = st.columns(2)
resume = col1.file_uploader('Upload your Resume')
cover_letter = col2.file_uploader('Upload a cover letter')

st.subheader('Personal Information')
applicant_first_name = st.text_input('First Name')
applicant_last_name = st.text_input('Last Name')
applicant_email = st.text_input('Email')
applicant_phone_number = st.text_input('Phone Number')
applicant_address = st.text_input('Address')
applicant_country = st.selectbox('Country', countries_list)
st.divider()
applicant_position = st.selectbox('Position applying to', positions_list)
applicant_years_of_experience = st.radio('Years of experience in the field', ['1', '2', '3', '4', '5+'], horizontal=True)
applicant_tell_us_more = st.text_area('Tell us more about yourself')
applicant_desired_salary = st.slider('Expected salary (in USD)', 50000, 150000, step=500, disabled=False)
st.warning('Your choice of expected salary is variable and depends on many factors, and does not guarantee actual salary.')
st.divider()
how_did_you_find_this = st.radio('How did you hear about us?', ['LinkedIn', 'Glassdoor', 'Facebook', 'Other'], horizontal=True)
st.divider()
applicant_applied_before = st.checkbox('Have you applied to a position in our company before?')
applicant_accurate_information = st.checkbox('I understand that submiting inaccurate information could disqualify me from the job.')
applicant_agree_to_terms = st.checkbox('I agree to the terms and conditions.')

submit_disabled = True
if applicant_accurate_information == True & applicant_agree_to_terms == True:
    submit_disabled = False

st.info('Once you apply a confirmation E-mail with further instructions will be sent to your mailbox.')

submission_query = """INSERT INTO applicants (first_name, last_name, email, phone_number, address, country, position, years_experience, applicant_details, expected_salary, survey, applied_before) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
data = (applicant_first_name, applicant_last_name, applicant_email, applicant_phone_number, applicant_address, applicant_country, applicant_position, applicant_years_of_experience, applicant_tell_us_more, applicant_desired_salary, how_did_you_find_this, applicant_applied_before)

def execute_query():

    bar = st.progress(20)
    if resume is not None:
        s3_client = boto3.client('s3',
        aws_access_key_id='*****',
        aws_secret_access_key='*****'
        )

        id = str(applicant_first_name + "_" + applicant_last_name)
        bucket_name = "job-application-resume-bucket"
        name = str(str(id) + "_resume.pdf")
        s3_client.upload_fileobj(resume, bucket_name, str("Resumes/" + name))

    if cover_letter is not None:
        s3_client = boto3.client('s3',
        aws_access_key_id='*****',
        aws_secret_access_key='*****'
        )

        id = str(applicant_first_name + "_" + applicant_last_name)
        bucket_name = "job-application-resume-bucket"
        name = str(str(id) + "_cover_letter.pdf")
        s3_client.upload_fileobj(cover_letter, bucket_name, str("Cover_letters/" + name))

    bar.progress(50)
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="*****",
        host="*****",
        port="5432",
        sslmode="require"
    )
    try:
        bar.progress(70)
        sql_query = submission_query
        cur = conn.cursor()
        cur.execute(sql_query, data)
        conn.commit()
        print("Successfuly submitted data to database.")
        cur.close()
        bar.progress(100)
        st.info('Data submitted.')
    except (Exception, psycopg2.DatabaseError) as error:
        print("No success:", error)
    finally:
        if cur is not None:
            cur.close()

    SENDER = "Sender Name <***@outlook.com>"
    RECIPIENT = "***.***.***@gmail.com"

    AWS_REGION = "eu-west-2"
    SUBJECT = "Job Application received."
    BODY_TEXT = ("Amazon SES Test (Python)\r\n"
                "This email was sent with Amazon SES using the "
                "AWS SDK for Python (Boto).")
                
    BODY_HTML = """
    <html>
        <head></head>
        <body>
            <h1>Confirmation Email for your %s role</h1>
            <p>
                Hello %s %s, This email was sent as a confirmation that we have received your application
                for a %s role at our company.
                We will be in contact with you as soon as possible. 
                Stay tuned!.
            </p>
        </body>
    </html>
    """.format(applicant_position, applicant_first_name, applicant_last_name, applicant_position)           
    CHARSET = "UTF-8"

    client = boto3.client('ses', region_name=AWS_REGION, aws_access_key_id="*****", aws_secret_access_key="*****")

    try:
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:" + response['MessageId'])

st.button("Submit Application", on_click=execute_query, disabled=submit_disabled)



