import os
import boto3
from dotenv import load_dotenv

load_dotenv()

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

companies_table = dynamodb.Table(os.environ.get('COMPANIES_TABLE', 'companies'))
institutions_table = dynamodb.Table(os.environ.get('INSTITUTIONS_TABLE', 'institutions'))
skills_table = dynamodb.Table(os.environ.get('SKILLS_TABLE', 'skills'))
contact_info_table = dynamodb.Table(os.environ.get('CONTACT_INFO_TABLE', 'contact_info'))
users_table = dynamodb.Table(os.environ.get('USERS_TABLE', 'users'))
blocklist_table = dynamodb.Table(os.environ.get('BLOCKLIST_TABLE', 'blocklist'))

# Add Contact Info
table_contact = {
    "id": "CONTACT_INFO",
    "name": "Rafael Brito",
    "email": "raffbrito@gmail.com",
    "phone": "+1-201-774-4844",
    "linkedin": "linkedin.com/in/rafaelbdesouza",
    "github": "github.com/raffbrito"
}
contact_info_table.put_item(Item=table_contact)

# Add Companies
companies = [
    {
        "id": "COMPANY#1",
        "name": "Bloomberg LP",
        "position": "Enterprise Data Support Specialist",
        "start_date": "2023-08-16",
        "end_date": "",
        "description": "Serve as a subject-matter expert for Bloomberg's Enterprise Data products, troubleshooting complex technical issues for institutional clients and ensuring seamless integration with their workflows. Act as the technical escalation point for strategic accounts, analyzing high-priority issues escalated from generalist representatives and participating in weekly calls with clients and Technical Account Managers (TAMs). Participate in pre-sales meetings to understand client business requirements, propose tailored solutions, and support sales opportunities. Provide deep technical expertise on REST/SOAP APIs, real-time market data APIs, SFTP, and cloud delivery technologies, focusing on optimization for clients already in production. Review client application code and logs to troubleshoot integration issues, improve product usage efficiency, and ensure compliance with Bloomberg data policies. Lead and contribute to ad-hoc projects. Coordinate and deliver team-wide training programs, mentor new hires, and drive consistent knowledge sharing to maintain high technical service standards."
    },
    {
        "id": "COMPANY#2",
        "name": "ICE Data Services",
        "position": "Client Support Specialist",
        "start_date": "2015-04-01",
        "end_date": "2023-08-01",
        "description": "Acted as the primary liaison between data collection, product development, and clients, ensuring timely resolution of reference data inquiries. Built analytical reports to identify trends and inefficiencies in data production workflows, leading to improved accuracy and turnaround time."
    },
    {
        "id": "COMPANY#3",
        "name": "InspIR Group",
        "position": "Sr BI Analyst",
        "start_date": "2020-03-01",
        "end_date": "2022-05-01",
        "description": "Designed shareholder base analyses, investor targeting reports, and market dashboards for corporate clients. Created automated stock performance and benchmarking reports using Excel, SQL, and Tableau."
    },
    {
        "id": "COMPANY#4",
        "name": "Issa PR",
        "position": "PR Executive",
        "start_date": "2014-11-01",
        "end_date": "2015-12-01",
        "description": "Managed media relations and secured press coverage for client events and campaigns. Produced client proposals, market research, and post-event analytics reports. Developed and maintained relationships with key media contacts to enhance brand visibility."
    },
    {
        "id": "COMPANY#5",
        "name": "Interactive Data",
        "position": "Data Research Specialist ",
        "start_date": "2012-06-01",
        "end_date": "2013-05-01",
        "description": "Processed corporate actions and reference data for equities, fixed income, and mutual funds. Extracted and validated data from debt indentures and financial disclosures."
    }
]
for company in companies:
    companies_table.put_item(Item=company)

# Add Institutions
institutions = [
    {
        "id": "INSTITUTION#1",
        "name": "The City College of New York",
        "degree": "Bachelor of Arts",
        "field": "Interdisciplinary Studies, Urban Studies & Public Administration",
        "start_date": "2016-01-01",
        "end_date": "2019-12-31",
        "description": "Graduated with honors in Interdisciplinary Studies, focusing on Urban Studies and Public Administration. Developed a strong foundation in data analysis, public policy, and urban planning. Engaged in various projects analyzing urban development and public service efficiency in New York City."
    },
    {
        "id": "INSTITUTION#2",
        "name": "FIA Business School",
        "degree": "MSc Data Analytics",
        "field": "Data Analytics & Machine Learning",
        "start_date": "2020-08-01",
        "end_date": "2022-12-31",
        "description": "Comprehensive program focusing on data analytics, machine learning, and statistical modeling. Developed skills in Python, R, SQL, and data visualization tools in Sao Paulo, Brazil. "
    }
]
for institution in institutions:
    institutions_table.put_item(Item=institution)

# Add Skills
tags = {
    "COMPANY#1": ["Python", "SQL", "R", "Data Analysis", "Machine Learning"],
    "COMPANY#2": ["Data Management", "Client Relations", "SFTP"],
    "COMPANY#3": ["Data Analysis", "Data Visualization", "SQL"],
    "COMPANY#4": ["Public Relations", "Media Relations", "Client Proposals"],
    "COMPANY#5": ["Data Research", "Corporate Actions", "Reference Data"],
    "INSTITUTION#1": ["Statistics", "Data Analysis"],
    "INSTITUTION#2": ["Data Analytics", "Machine Learning", "Statistical Modeling"]
}

skill_counter = 1
for item, skills in tags.items():
    for skill in skills:
        tag = {
            "id": f"{item}#SKILL#{skill_counter}",
            "tag_name": skill,
            "company_id": item if item.startswith("COMPANY") else None,
            "institution_id": item if item.startswith("INSTITUTION") else None
        }
        skills_table.put_item(Item=tag)
        skill_counter += 1

# Add Users (example)
users = [
    {
        "id": "USER#1",
        "username": "rafael",
        "password": "Rafael123"
    }
]
for user in users:
    users_table.put_item(Item=user)

# Add Blocklist (example)
blocklist_items = [
    {
        "id": "TOKEN#example",
        "user": "USER#1"
    }
]
for item in blocklist_items:
    blocklist_table.put_item(Item=item)

print("Seed data inserted successfully into DynamoDB.")
