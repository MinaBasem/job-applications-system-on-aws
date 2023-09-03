import psycopg2
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="333666222",
        host="job-application-db-2.com3yqtc5f7q.eu-west-2.rds.amazonaws.com",
        port="5432",
        sslmode="require"
    )
try:
    sql_query = "SELECT * FROM Applicants"
    cur = conn.cursor()
    #cur.execute(sql_query)
    applicant_df = pd.read_sql(sql_query, conn)
    print("Successfuly returned data from database.")
    cur.close()
except (Exception, psycopg2.DatabaseError) as error:
    print("No success:", error)
finally:
    if cur is not None:
        cur.close()

st.title('Job Application Analysis')
st.divider()
st.subheader("First we explore the DataFrame (Dummy Data)")
st.dataframe(applicant_df)

group_by_position_df = applicant_df.groupby('position')["first_name"].count().reset_index().rename(columns={'first_name':'Applicants'})
grouped_expected_salary_df = applicant_df.groupby('position')["expected_salary"].mean().astype(int)

st.divider()
st.subheader("Number of applicants in each position and their average expected salary")
col1, col2 = st.columns(2)
col1.dataframe(group_by_position_df)
col2.dataframe(grouped_expected_salary_df)

st.divider()

top_10 = (applicant_df.groupby("country")["position"].count().sort_values()) #top 10 countries
st.bar_chart(top_10)

st.divider()
st.subheader("Distribution of positions applied to by applicants")

labels = applicant_df['position'].unique()
sizes = applicant_df.groupby('position')['first_name'].count()

pie, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
st.pyplot(pie)

st.divider()
st.subheader("How did applicants find out about the job posting?")

labels2 = ['Facebook', 'Glassdoor', 'LinkedIn', 'Other']
sizes2 = applicant_df.groupby('survey')['survey'].count()

pie, ax2 = plt.subplots()
ax2.pie(sizes2, labels=labels2, autopct='%1.1f%%', startangle=90)
ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
st.pyplot(pie)

st.divider()
