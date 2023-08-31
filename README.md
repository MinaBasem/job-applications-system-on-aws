# Job Applications System Hosted On AWS

A job applications simulation hosted on AWS, starting from the application form to applicants analysis.

![System Layout](https://github.com/MinaBasem/job-applications-system-on-aws/assets/42482261/398aacf9-8275-4a1f-ab4f-f778b912d4c7)


# Components

## 1. Streamlit Web App (Input)

<img align="right" width="175" height="100" src="https://cdn.analyticsvidhya.com/wp-content/uploads/2020/10/image4.jpg">
The application form is a web application created using Streamlit, a Python library that allows easy creation and deployment of web apps.
The application form can be found <a href="https://job-applications.streamlit.app/" target="_blank">here</a>.

## Inputs:

### Uploads:

<img width="460" align="right" alt="Screen Shot 2023-08-31 at 3 17 27 PM" src="https://github.com/MinaBasem/job-applications-system-on-aws/assets/42482261/ffd529f4-5bcb-4204-b785-60207edd0baf">

- Resume file
- Cover letter file

### Personal Information:

<img align="right" width="500" alt="image" src="https://github.com/MinaBasem/job-applications-system-on-aws/assets/42482261/8c41b78f-b729-4bb0-9743-4f745bff8de9">

- First name
- Last name
- Email
- Phone number
- Address
- Country

### Technical Information:
  
- Position (technical field)
- Years of experience
- Applicant details
- Expected salary

<br/><br/>

---
## 2. Custom Data Generator (Optional input for database population)

<img align="right" width="200" alt="Screen Shot 2023-08-31 at 3 21 25 PM" src="https://github.com/MinaBasem/job-applications-system-on-aws/assets/42482261/0efb401e-46dc-44a8-8e80-666e4b34c0b2">

[data-generator.py](https://github.com/MinaBasem/fake-data-generator) generates all required data points randomly, the script is looped using a cron job that runs 
every _5 minutes_ 
> Crontab denoting "every 5 minutes" ---> */5 * * * *

The script is hosted on an EC2 instance where it is installed, along with all required dependencies.
An example of the generated data points can be seen below.

<br/><br/>

<img width="1338" alt="Screen Shot 2023-08-31 at 3 52 37 PM" src="https://github.com/MinaBasem/job-applications-system-on-aws/assets/42482261/185c3c49-8f46-4516-a9e0-55af13d63c47">

### Bonus: AI generated data point

Thanks to [Daniel Park](https://github.com/dsdanielpark)'s [Bard-API](https://github.com/dsdanielpark/Bard-API) Python package which utilizes Google's Bard LLM to generate answers programmatically, i was able to generate custom answers for each "Imaginary" applicant according to their years of experience, technical position, and the company they "work" for.

(First record is of my own)
<img width="1315" alt="Screen Shot 2023-08-31 at 4 03 48 PM" src="https://github.com/MinaBasem/job-applications-system-on-aws/assets/42482261/80b13e6a-6bf2-44f3-8873-a6b84013dd87">


Here's how it looks under the hood:

![Screen Shot 2023-08-31 at 4 12 34 PM](https://github.com/MinaBasem/job-applications-system-on-aws/assets/42482261/9cab39bc-9af4-47a2-9f38-14fd06847770)

Here's a full example answer:

<img width="811" alt="Screen Shot 2023-08-31 at 4 23 00 PM" src="https://github.com/MinaBasem/job-applications-system-on-aws/assets/42482261/824b518c-1014-47e5-84a1-2953cd3b21c7">








