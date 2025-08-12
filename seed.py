from app import create_app
from db import db
from models import ContactInfoModel, CompanyModel, InstitutionModel, CompanyTags, InstitutionTags

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    # Add Contact Info
    contact = ContactInfoModel(
        name="Rafael Brito",
        email="raffbrito@gmail.com",
        phone="+1-201-774-4844",
        linkedin="linkedin.com/in/rafaelbdesouza",
        github="github.com/raffbrito"
    )
    db.session.add(contact)

    # Add Companies
    company1 = CompanyModel(
        name="Bloomberg LP",
        position="Enterprise Data Support Specialist",
        start_date="2023-08-16",
        end_date="",
        description="Serve as a subject-matter expert for Bloomberg’s Enterprise Data products, troubleshooting complex technical issues for institutional clients and ensuring seamless integration with their workflows. Act as the technical escalation point for strategic accounts, analyzing high-priority issues escalated from generalist representatives and participating in weekly calls with clients and Technical Account Managers (TAMs). Participate in pre-sales meetings to understand client business requirements, propose tailored solutions, and support sales opportunities. Provide deep technical expertise on REST/SOAP APIs, real-time market data APIs, SFTP, and cloud delivery technologies, focusing on optimization for clients already in production. Review client application code and logs to troubleshoot integration issues, improve product usage efficiency, and ensure compliance with Bloomberg data policies. Lead and contribute to ad-hoc projects. Coordinate and deliver team-wide training programs, mentor new hires, and drive consistent knowledge sharing to maintain high technical service standards."
    )
    company2 = CompanyModel(
        name="ICE Data Services",
        position="Client Support Specialist",
        start_date="2015-04-01",
        end_date="2023-08-01",
        description="Acted as the primary liaison between data collection, product development, and clients, ensuring timely resolution of reference data inquiries. Built analytical reports to identify trends and inefficiencies in data production workflows, leading to improved accuracy and turnaround time."
    )
    company3 = CompanyModel(
        name="InspIR Group",
        position="Sr BI Analyst",
        start_date="2020-03-01",
        end_date="2022-05-01",
        description="Designed shareholder base analyses, investor targeting reports, and market dashboards for corporate clients. Created automated stock performance and benchmarking reports using Excel, SQL, and Tableau."
    )
    company4 = CompanyModel(
        name="Issa PR",
        position="PR Executive",
        start_date="2014-11-01",
        end_date="2015-12-01",
        description="Managed media relations and secured press coverage for client events and campaigns. Produced client proposals, market research, and post-event analytics reports. Developed and maintained relationships with key media contacts to enhance brand visibility."
    )
    company5 = CompanyModel(
        name="Interactive Data",
        position="Data Research Specialist ",
        start_date="2012-06-01",
        end_date="2013-05-01",
        description="Processed corporate actions and reference data for equities, fixed income, and mutual funds. Extracted and validated data from debt indentures and financial disclosures."
    )
    db.session.add(company1)
    db.session.add(company2)
    db.session.add(company3)
    db.session.add(company4)
    db.session.add(company5)
    db.session.commit()

    # Add Institutions
    institution1 = InstitutionModel(
        name="The City College of New York",
        degree="Bachelor of Arts",
        field="Interdisciplinary Studies, Urban Studies & Public Administration",
        start_date="2016-01-01",
        end_date="2019-12-31",
        description="Graduated with honors in Interdisciplinary Studies, focusing on Urban Studies and Public Administration. Developed a strong foundation in data analysis, public policy, and urban planning. Engaged in various projects analyzing urban development and public service efficiency in New York City."
    )
    institution2 = InstitutionModel(
        name="FIA Business School",
        degree="MSc Data Analytics",
        field="Data Analytics & Machine Learning",
        start_date="2020-08-01",
        end_date="2022-12-31",
        description="Completed a comprehensive program focusing on data analytics, machine learning, and statistical modeling. Developed skills in Python, R, SQL, and data visualization tools in Sao Paulo, Brazil. "
    )
    db.session.add(institution1)
    db.session.add(institution2)
    db.session.commit()

    # Add InstitutionTags
    itag1 = InstitutionTags(tag_name="Statistics", institution_id=institution1.id)
    itag2 = InstitutionTags(tag_name="Data Visualization", institution_id=institution2.id)
    db.session.add(itag1)
    db.session.add(itag2)

    # add skills
    companySkillsDict= {company1.id: ["Python", "SQL", "R", "Data Analysis", "Machine Learning"],
                        company2.id: ["Data Management", "Client Relations", "SFTP"],
                        company3.id: ["Data Analysis", "Data Visualization", "SQL"],
                        company4.id: ["Public Relations", "Media Relations", "Client Proposals"],
                        company5.id: ["Data Research", "Corporate Actions", "Reference Data"]}

    institutionSkillsDict = {institution1.id: ["Urban Studies", "Public Administration", "Data Analysis"],
                             institution2.id: ["Data Analytics", "Machine Learning", "Statistical Modeling"]}
    
    for company_id, skills in companySkillsDict.items():
        for skill in skills:
            tag = CompanyTags(
                tag_name=skill,
                company_id=company_id
            )
            Companyskills = CompanyTags(
                company_id=company_id,
                tag_name=skill
            )
            db.session.add(tag)
            db.session.add(Companyskills)
    for institution_id, skills in institutionSkillsDict.items():
        for skill in skills:
            tag = InstitutionTags(
                tag_name=skill,
                institution_id=institution_id
            )
            db.session.add(tag)
            institutionSkills = InstitutionTags(
                institution_id=institution_id,
                tag_name=skill
            )
            db.session.add(institutionSkills)

    db.session.commit()

print("Seed data inserted successfully.")
