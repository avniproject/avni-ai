

# File: ./case-studies/2019-09-02-prescription-tool.md

---
templateKey: case-study
title: "Prescription tool for community health workers - A simple use of\_Avni"
date: 2019-09-02T06:33:06.442Z
description: >-
  Avni used for generating prescription, for common health complaints, based on
  a few data inputs provided by the village health worker - to fill some gaps
  caused by extreme remoteness of some villages.
featuredstudy: false
tags:
  - Health
  - Case Study
---
There are parts of India where the road connectivity from the villages to the nearest block headquarter is quite poor. One such place (tehsil, i.e. block or sub-district) is <a href="https://www.mapsofindia.com/villages/maharashtra/gadchiroli/bhamragad/" target="_blank" rel="noopener noreferrer">Bhamraghad</a>. <a href="http://www.lokbiradariprakalp.org/" target="_blank" rel="noopener noreferrer">Lokbiradari Prakalp</a> (LBP), in village Hemalkasa, is the literal lifeline of this and neighbouring blocks, because it has a hospital (do go to the home page of Lokbiradari Prakalp and see the photos to get the feel of the place and the hospital).

For many months of the year, getting to the hospital from the villages in the same block can be quite difficult. One may need to wade through knee/waist height water for a couple of hours, to reach the hospital. For certain illnesses seeing the doctor is the only option. But in many conditions like fever, headache, diarrhoea, vomiting, acidity, scabies, etc - going or taking someone to the hospital, losing one day of employment is not feasible. Ordinarily, in the public health system, there is nearby <a href="http://nrhmmeghalaya.nic.in/sub-centres-scs" target="_blank" rel="noopener noreferrer">subcenter</a> with a trained nurse whom one can go to. But these subcenters are only partially operational - leaving people with fewer options.

To resolve this problem LBP along with the village representatives, decided to run health centres for every 6 villages. These health centres to have medicines, and a few other basic facilities like weighing machine, BP machine, etc. These pharmacies were to be run by a selected person from one of these villages - called arogyadoots or community health workers (CHWs).

Overall the CHWs were responsible for:

1. categorise the complaint into one or more of 16 types
2. compute the quantity, form and number of doses of the medicine based on age, weight, gender & complaints
3. making referral in some cases instead of dispensing the medicines
4. note down the details for monitoring purpose

2 & 3 above are error-prone and monitoring of the work from the paper records was difficult. There was a need for a solution that could do 2,3 & 4; from a mobile device, offline. Also, consolidate all this data in a central place for analysis.

- - -

While many data collection products allow for forms with user-defined fields, skip logic etc. We wanted to allow for the insertion of programmable logic in various parts of the workflow. This programmable logic being specific only to that implementation. This ability differentiates Avni from other products. Avni allows for JavaScript-based rules, a language that has the most number of programmers - hence it is easy to find them.

This was the first use-case of Avni (then called OpenCHS). Avni provided a simple mobile form which on completion did 2 & 3 based on rules configured for this implementation. On every interaction with the patient, the CHW would fill one form with 8–10 questions (there were other form questions like BP, Temperature, Pallor, Pedal Edema, Skin Condition, etc for later analysis).

This field app has been in use for the last three years now, by 6 health workers covering 30 villages of a total of 15,000 population. The health workers have almost no connectivity in the field. They travel to LBP once a month, for monthly discussions and at this point, they sync the data with the server. (This is an extremely low resource setup where in the villages the Internet has not reached, in most villages in India now, the Internet is of low quality but present. In such cases the data can be synchronised regularly.) At the time of writing, this is the only implementation of Avni that runs on the server on-premise. We made that decision because the Internet connectivity even from the hospital is not reliable.

![](/img/lbp-case-study-1-.png "Deployment of Avni at Lok Biradari Prakalp")

- - -

The software-based approach allowed LBP to change the prescription logic, medicines, for some of the complaints.

Currently, LBP plans to roll out another program, for maternal and child health - which has been configured and tested, as of now.

_ps: the health program has been described in more detail on LBP's website here._

- - -

**Credit for icons**

"designed by - https://www.flaticon.com/authors/roundicons, https://www.flaticon.com/authors/pixel-buddha, https://www.flaticon.com/authors/freepik, https://www.flaticon.com/authors/eucalyp - from Flaticon"


# File: ./case-studies/2024-05-22-empowering-vision-care-chashma-tech4dev.md

---
templateKey: case-study
title: Empowering Vision Care Project Chashma’s Transformation with Avni Platform
date: 2024-05-22T20:30:00.000Z
author: The Avni Team
description:
featuredpost: false
featuredimage:
tags:
  - Health
  - Case Study
---


## Executive Summary
Sarva Mangal Family Trust (SMFT), a non-profit organization, in collaboration with Bhansali Trust, also a non-profit organization working in healthcare, initiated Project Chashma with the ambitious goal of delivering eye care services to 20 million individuals within five years through partnerships with grassroots NGOs. However, the project encountered operational inefficiencies, especially in data management, during its initial stages, hindering its scalability and effectiveness. With the adoption of an open-source data collection and case management platform, Avni, these challenges were addressed, leading to streamlined data management and enhanced overall operational efficiency.

## The Challenges
Bhansali Trust’s expertise in organizing eye care camps, especially for cataract surgeries across diverse Indian regions, positioned them well to lead Project Chashma. Beginning with remote villages in North Gujarat, the project aimed to deliver comprehensive eye care services, encompassing patient registration, eye examinations & consultation, eyeglass distribution, patient referrals & follow-up for eye ailment treatment, and impact monitoring. However, as the project scaled, it encountered significant operational challenges:

- **Crowd Management and Data Collection**: The influx of patients led to overcrowded camps, making patient registration and data collection challenging. Manual data entry, due to its slow pace and susceptibility to errors, significantly hampered the project’s ability to effectively serve the community.
- **Data Management**: The manual data entry process resulted in inaccuracies and inefficiencies, causing a cumbersome transition to digital records.
- **Process Inefficiencies**: The initial setup lacked a streamlined process for patient flow and data collection, resulting in delays and a compromised patient experience.
- **Reporting & Evaluation**: The absence of automated reporting delayed insights and impeded the project’s ability to adapt and enhance its operations.
- **Impact Assessment**: Manual processes hindered timely and precise evaluation of the project’s impact, limiting the ability to make data-driven adjustments.
- **Routine Follow-up**: The project required a system for ongoing patient follow-ups to ensure the sustained impact of the treatments administered.

To overcome these challenges and streamline processes, the Trust sought a digital solution tailored for remote village settings where network connectivity is limited. A customized offline mobile application was developed on the Avni platform for data collection and real-time monitoring at different stages of the process.

## Implementation
In response, the project team revamped the patient flow and data collection processes, integrating the Avni platform for its robust offline capabilities and comprehensive data management tools.

Avni is an open-source platform for on-field service delivery and data collection. Designed for the development sector, Avni strengthens field capacity for non-profits and governments across sectors like health, water, education, and social welfare.

<div style="width: 50%">
    <img src="/img/2024-05-22-Empowering-vision-care-Chashma-tech4dev/avni-block-diagram.png"><pre>**Avni Block Diagram**</pre>
</div>
<div style="width: 50%">
        <img src="/img/2024-05-22-Empowering-vision-care-Chashma-tech4dev/dashboard-patient-registration.png"><pre>**Avni Mobile App Dashboard & Patient Registration**</pre>
</div>
<div style="width: 50%">
        <img src="/img/2024-05-22-Empowering-vision-care-Chashma-tech4dev/dashboard-patient-registration.png"><pre>**Avni Mobile App Dashboard & Patient Registration**</pre>
</div>
<div style="width: 50%">
        <img src="/img/2024-05-22-Empowering-vision-care-Chashma-tech4dev/participation-gender-age-group.png"><pre>**Patients Participation in the Eye-camp by Gender & Age-Group**</pre>
</div>
<div style="width: 50%">
        <img src="/img/2024-05-22-Empowering-vision-care-Chashma-tech4dev/percentage-of-student-need-eyeglasses.png"><pre>**Patients Participation and Percentage of Adults and Students Need Eyeglasses**</pre>
</div>

## Impact

The strategic enhancements facilitated by the Avni digital solution resulted in notable improvements in operational efficiency throughout the project:

- **Token System for Crowd Management**: Introducing a token system improved patient flow and organization at the camps, mitigating overcrowding and streamlining the registration process.
- **Digital Data Collection**: The offline data collection feature of Avni streamlined and expedited the data collection process, ensuring consistent and precise patient records. This facilitated a more reliable assessment of eye care needs and interventions.
- **Automated Reporting**: The customizable reports and analytics features of Avni facilitated timely and automated impact assessments, reducing the need for manual labor and enabling a more profound understanding of the project’s effectiveness.
- **Enhanced Impact Assessment**: The integration of real-time data collection and analysis capabilities enabled the project to accurately measure its impact, facilitating prompt adjustments to better meet community needs. Additionally, real-time data access and user-friendly dashboards enhanced transparency and collaboration, enabling informed decision-making at all organizational levels.
- **Improved Patient Outcomes**: By leveraging efficient monitoring and routine follow-up capabilities of the solution, the project ensured that patients received timely and appropriate care, thereby enhancing its overall impact on community health.
- **Staff Training and Upskilling**: Focused training sessions equipped staff with the skills needed to effectively utilize the Avni platform, facilitating a seamless transition to digital data management.

The Avni platform not only resolved the project’s immediate data management challenges but also established a scalable model for future expansion, with the potential for adoption by other grassroots organizations. With real-time access to data and enhanced process efficiencies, the project was able to effectively serve a larger population, marking a significant advancement in its mission.

## Conclusion
The integration of the Avni platform into Project Chashma’s operations has been transformative, addressing critical challenges in crowd management, data collection, staff upskilling, and impact assessment. The improvements in process efficiency and data management capabilities have not only bolstered the project’s effectiveness but have also set a new standard for leveraging technology in nonprofit initiatives. Project Chashma’s experience underscores the potential of digital tools to enhance service delivery and expand impact, serving as a valuable blueprint for other NGOs aiming to scale their efforts in underserved communities.



*Tech4Dev has published this insightful article detailing the transformative impact of the Avni platform on Project Chashma, led by Sarva Mangal Family Trust (SMFT) and Bhansali Trust. The article tells how Avni's offline capabilities and robust data management tools have improved patient registration, eye exams, eyeglass distribution, follow-up treatments, and overall project impact assessment, setting a new benchmark for technology in non-profit initiatives.*


# File: ./case-studies/2024-09-19-Scaling-Rural-Education.md

---
templateKey: case-study
title: Scaling Rural Education - How Schools And Anganwadis Are Building Lifelong Skills Beyond the Classroom
date: 2024-09-19T20:30:00.000Z
author: The Avni Team
description:
featuredpost: false
featuredimage: /img/2024-09-19-Scaling-Rural-Education/CInI-1.png
tags:
  - Education
  - Case Study
---


In the heart of rural India, education is getting a fresh makeover. It’s not just about reading and writing anymore; it’s about giving children the skills they need for life. The Collectives for Integrated Livelihood Initiatives (CInI), part of Tata Trusts, is leading this change, reaching over 250,000 students in rural and tribal areas in Odisha and Jharkhand. They blend traditional learning with practical experiences to help these children build a brighter future.

<div style="width: 60%">
    <img src="/img/2024-09-19-Scaling-Rural-Education/CInI-1.png">
</div>

## CInI’s Vision: Empowering Through Education

CInI, started in 2007, aims to improve the lives of tribal households in Central India. Their education program is unique, combining book learning with hands-on activities. Here’s what they’re doing:

- **Systems Strengthening**: Collaborating with departments of Education to establish itself as a resource for community strengthening and Foundational Literacy and Numeracy.
- **Making School Environments Vibrant**: Making classrooms visually engaging and fun through creating print rich environment, developing kitchen gardens to teach kids about responsibility and sustainable living, engaging children through libraries, and integrating technology.
- **Academic Enrichment**: Focus on improving Foundational Literacy and Numeracy through academic interventions and teacher support.
- **Community Engagement**: Involve SMCs, Panchayati Raj Institutions (PRIs) and parents in children’s education and school development through a strong model of engagement. 
- **Continuous Assessments**: Helping students understand key concepts and find areas where they need more help.

CInI focuses on timely interventions to continuously improve the classroom environment and overall quality of education. It's amazing to see how these initiatives are shaping a self-sustaining future for these kids!

<div style="width: 70%">
    <img src="/img/2024-09-19-Scaling-Rural-Education/CInI-2.png">
</div>

## Avni’s Role in Enhancing Education Outcomes

CInI recognised the need for efficient data collection to monitor and improve its education initiatives. The challenge was to streamline the process and make use of data to track progress in real time. Avni has become an integral tool in addressing this need, offering a user-friendly, low-code mechanism for field data collection. Our platform supports CInI in tracking various aspects of their programs, including:

- **Professional Development and Classroom Practices**: Training for teachers and headmasters, and monitoring updated classroom practices.
- **Student Assessments and Readiness**: Evaluating language, math, and science skills, and readiness for school.
- **School and Library Management**: Involvement of school management committees and profiling library activities.
- **On-Site Support and Monitoring**: Providing demo classes, on-site support for teachers, and monitoring classroom quality and student attendance.
- **Early Childhood and FLN (Foundational Learning and Numeracy) Programs**: Observing Anganwadis, monitoring Early Childhood Care and Education programs, and the FLN program.

By enabling real-time data collection and analysis, Avni allows us to make informed, data-driven decisions, ultimately enhancing education outcomes.

## Impact of Digital Adoption on the Program

The digital shift brought several benefits to CInI’s education program:

- **Streamlined Data Collection**: Avni enables real-time data entry through mobile devices, ensuring that information about student attendance, assessments, and classroom conditions is captured efficiently.
- **Data Accuracy**: Custom-designed digital forms with single and multi-select options reduce manual errors, providing more reliable insights.
- **Automated Scheduling and Follow-ups**: Avni’s platform automates visit schedules and follow-ups for coordinators, ensuring consistent monitoring across schools and Anganwadis.

Here are few clips of the CInI program in the Avni app:

<div style="width: 80%">
    <img src="/img/2024-09-19-Scaling-Rural-Education/CInI-3.gif">
</div>

## The People Behind the Data: User Personas

Here are some key personas using Avni in the field:

- **Field Coordinators**: Responsible for visiting schools and Anganwadis, Field Coordinators use Avni to schedule visits, track progress, and report on any issues or improvements needed.
- **Cluster Coordinators**: Overseeing several field coordinators, Cluster Coordinators monitor the overall progress of multiple schools and Anganwadis within their designated clusters, ensuring that reports are timely and accurate.
- **State Coordinators**: At a higher level, State Coordinators manage the education program across several districts. They use Avni to analyse field data, assess overall program performance, and provide strategic input to improve the education initiatives in their region.

## The Journey So Far

As of July 2024, Avni is being used in three districts of Odisha and eight districts of Jharkhand. The platform supports over 2,500 schools, 4,500 school teachers, 490 Anganwadis, and 520 Anganwadi Workers, each of whom is now empowered to capture and act on data like never before.

<div style="width: 50%">
    <img src="/img/2024-09-19-Scaling-Rural-Education/CInI-4.png">
</div>

CInI and its more than 150 users are working on the ground to elevate the quality of education. By prioritising robust assessments, Academic Enrichment has recorded an average of 30%  improvement in language and in math. CInI has successfully set up more than 1200 libraries in the schools and Anganwadis so far.


# File: ./case-studies/2024-11-11-jal-jeevan-mission-arghyam.md

---
templateKey: case-study
title: Jal Jeevan Mission – Arghyam 
date: 2024-11-11T19:35:00.000Z
author: Siddhant Singh, Project Tech4Dev
description:
featuredpost: false
featuredimage: /img/2024-11-11-jal-jeevan-mission-arghyam/1.webp
tags:
  - Water
  - Government
  - Case Study
---

<div style="width: 100%">
    <img src="/img/2024-11-11-jal-jeevan-mission-arghyam/1.webp">
</div>


The Jal Jeevan Mission (JJM), launched by the Government of India in 2019, aims to provide safe and adequate drinking water through individual household tap connections to every rural household by 2024. At its inception, only 3.23 crore (17%) rural households had tap water connections, but the mission has set an ambitious goal of adding nearly 16 crore additional households, benefiting over 19 crore rural families. As of August 2024, JJM has achieved significant progress, providing tap water connections to 11.82 crore more rural households, raising total coverage to over 15.07 crore households, or 77.98% of all rural households. The mission emphasizes a community-based approach, encouraging local ownership through contributions of cash, kind, or labor (shramdaan) and prioritizes sustainable water supply systems, infrastructure functionality, and resource maintenance. Additionally, it focuses on developing skilled human resources in construction, plumbing, water quality management, and catchment protection, creating a lasting impact on health, quality of life, and rural empowerment.

<div style="width: 100%">
    <img src="/img/2024-11-11-jal-jeevan-mission-arghyam/2.webp">
</div>

Arghyam supports JJM’s objectives in partnership with Civil Society Organizations (CSOs) and government departments, working to establish sustainable water supply systems across Indian states. With JJM’s remarkable national coverage expansion from 16% to over 78%, Arghyam has aligned its efforts through three thematic divisions: **Operations & Maintenance**, **Water Quality**, and **Source Sustainability**. These areas of focus help ensure the longevity and quality of rural water systems. Additionally, Arghyam runs the **India Water Portal (IWP)**, an online platform providing a space for academia, researchers, and practitioners to share insights, foster public discourse, and address issues in water, sanitation, and climate change, further advancing the mission’s transformative impact on India’s rural landscape.

Currently, three states in India are being focused on through projects that are developed based on geohydrological contexts as well as the priorities and approach of these state governments regarding water supply and management in rural areas.

| Sl No | State       | Thematic Focus Area     |
|-------|-------------|-------------------------|
| 1     | Assam       | Water Quality          |
| 2     | Bihar       | O&M                    |
| 3     | Karnataka   | Source Sustainability  |

Besides these thematic priorities and focused geographies, Arghyam’s strategy is aimed at working at scale by leveraging technology as an enabler and integrating robust social processes to strengthen the system. Each of the Arghyam projects is designed with digital deployment and tech innovation as the mainstay of the intervention.

## Data Collection Method  
**Avni** is an open-source task tracker tool, which has been developed by Samanvay – Learning and Development Foundation. The tool has been used in different sectors, such as education and health, especially by frontline functionaries such as ASHA, teachers, CSO workers, and program managers to deliver and monitor their programmes across multiple states of India.

In Bihar, Avni has been rolled out by Arghyam partner agency **Aga Khan Rural Support Programme India (AKRSP-I)** to track the mandated tasks at the pipe water supply level by its PWS operators, also known as **Anurakshak/Pump-operator**. Through the Avni app, five tasks are being captured at PWS (pipe water supply system) by Anuarakshak, which are as follows:

### Tank Cleaning  
**Purpose:** To document the regular cleaning of water tanks, which is essential for maintaining water quality and safety.  
**Data Collected:**  
- Date of tank cleaning  
- Notification to the community about cleaning (photo)  
- Tank cleaning process (photos)  
- WIMC (Ward Implementation & Management Committee) members’ participation (photos)  
- Additional comments if needed  
**Frequency:** Biannual  
**Importance:** Ensures tanks are cleaned on schedule, the community is informed and involved, and records are digitized safely.  

### WIMC Meeting (Record Keeping)  
**Purpose:** To keep track of WIMC meetings, attendance, and key discussions, which foster community participation in water management.  
**Data Collected:**  
- Meeting date  
- Meeting attendance with photo evidence  
- Meeting minutes (photo of register)  
- Total attendance and female attendance count  
- Additional comments  
**Frequency:** Monthly  
**Importance:** Highlights community participation and the engagement of both male and female members in water management decisions.  

### Jal Chaupal Record Keeping  
**Purpose:** To document community gatherings (Jal Chaupal) that discuss water issues, providing a platform for feedback and ideas from locals.  
**Data Collected:**  
- Date of Jal Chaupal  
- Attendance (photo and count)  
- Proceedings (photo)  
- Breakdown of participants by total count and female count  
- Attendance of specific officials and community representatives  
- Additional comments  
**Frequency:** As organized by the community  
**Importance:** Ensures transparency and inclusiveness, showing that community feedback is formally acknowledged.  

### Log Book  
**Purpose:** To log daily details on water supply, noting any interruptions and reasons for service disruptions.  
**Data Collected:**  
- Date  
- Reporting month  
- Days of “no water supply”  
- Reasons for interruptions (such as power issues, pipeline breakage)  
- Monthly logbook photo  
**Frequency:** Monthly  
**Importance:** Ensures that all disruptions are recorded and analyzed, which can guide future improvements and maintenance actions.  

### Water Quality Testing  
**Purpose:** To monitor water quality by testing for chemical and biological contaminants, ensuring the safety of drinking water.  
**Data Collected:**  
- Dates of entry, sample collection, and testing  
- Sampling points (source, household, institution, etc.)  
- Chemical parameters: pH, Total Hardness, Alkalinity, Chloride, Nitrate, Arsenic, Fluoride, Iron  
- Biological parameter: Bacteriological contamination  
**Frequency:** As per the testing schedule  
**Importance:** Provides critical data on water safety, enabling quick responses to contamination issues and ensuring compliance with health standards.  
Each form in the Avni app thus plays a key role in PWS functionality, supporting both operational tracking and community engagement for a sustainable and safe water supply system.

As of now, Anuarakshaks have used Avni in 3 blocks of Muzaffarpur and efforts are on to take it to 7 districts and 8 blocks. Also, simultaneous efforts are being made to influence the government by advocating its utility and relevance through trusted data generation and improved visibility made available through the Anuarakshak dashboard. 

### mGramSeva:

mGramseva is a portal developed by the eGovernment Foundation for managing income and expenditure at the PWS level digitally. Through its partners, Arghyam has rolled out mGramseva to 3 blocks of the Muzaffarpur district of Bihar, and efforts are being made to scale this to 10 blocks across 7 districts of Bihar.

mGramSeva allows Anurakshaks to track the financial management of the  water connections in their area of coverage, the consumers for these connections, and these consumers’ billing and payment histories. It also helps them track the expenses they incurred on the operation and maintenance of the pipe water supply system such as remuneration to pump operator, plumbing cost , consumables for FTK /water testing , repair cost , electricity bill etc . 

**Engagement with DALGO on developing Integrated Dashboard:-**Arghyam has partnered with DALGO to develop an integrated dashboard from PWS physical and financial performance by pulling data from the both apps. The team has already developed unified Avni and mGramSeva dashboards. The final step remaining is to integrate these dashboards into the mGramSeva application.

## Dalgo Adoption

### Challenges Before

1. **Problem with Consolidation and Visualization:** The key challenge was consolidating and visualizing data from Avni and mGramSeva into a unified dashboard for Anurakshaks. Although there was a silo dashboard for AVNI in the metabase but that doesn’t give a unified dashboard across two sources. 

2. **Unique Access Requirement:** Each Anurakshak requires a unique URL for personalized access, allowing them to view only their own dashboard and this needs to integrate with mGramSeva users to see their dashboard.
mGramSeva will help them with unique username in the url parameters to map it with their logins. 

3. **Power BI Licensing Cost:** Power BI proved to be cost-prohibitive for multiple users accessing the visualization, making it infeasible for this use case.

### Solution

<div style="width: 100%">
    <img src="/img/2024-11-11-jal-jeevan-mission-arghyam/3.png">
</div>

1. **Data Integration:** We leveraged Dalgo to integrate data from multiple sources, including Avni and mGramSeva, streamlining data management.
2. **Custom Connector:** Developed an in-house connector for mGramSeva, a unique feature that’s hard to find in other tools, enhancing our system’s versatility.
3. **Unique URL Solution:** Addressed the multiple unique URL issue, which you can read more about [here], ensuring smoother navigation and access.
4. **Scalable User Onboarding:** Using open-source versions of Superset allows us to onboard an unlimited number of users, with hosting on AWS as our only cost.


## Superset Visualization
With the help of a unique URL an Anurakshak can see their activities. 

<div style="width: 100%">
    <img src="/img/2024-11-11-jal-jeevan-mission-arghyam/4.png">
</div>
<div style="width: 100%">
    <img src="/img/2024-11-11-jal-jeevan-mission-arghyam/5.png">
</div>

## Monitoring Pipeline
User can check the status of their data pipeline here  
Sync is running on the daily basis for avni and weekly for mGramSeva and if something fails users can receive a discord notification and an email notification on the failures. 

<div style="width: 100%">
    <img src="/img/2024-11-11-jal-jeevan-mission-arghyam/6.png">
</div>

## Data Quality Tests
We have written a few test cases which can identify data problems in your data. Like not null, unique columns, and type checks for the column. 
If something fails with the test cases you’ll be notified by the yellow line which you can see above.

<div style="width: 100%">
    <img src="/img/2024-11-11-jal-jeevan-mission-arghyam/7.png">
</div>

## Conclusion 
Keeping in mind the Arghyam strategy of leveraging the power of technology as an enabler and working on scale, we are trying to establish a sustainable PWS operation and maintenance model, which is amenable to govt and replicable and scalable through their system.

Integrated dashboard of both these digital tools Avni & mGramseva try to address quite critical aspects of PWS operation and management by ensuring trusted data generation through the participation of frontline workers which could be utilised to improve decision making to strengthen the system for better accountability and transparency. For the frontline, this dashboard helps them to understand their performance by looking at one single dashboard that is readily available, sharable and retrievable and is not prone to physical damage to be misplaced or lost which are the main challenges they face while maintaining physical records.




# File: ./case-studies/2024-11-27-Project-Potential-Bihar-Health-Access-Digitisation-Case-study.md

---
templateKey: case-study
title: Empowering Healthcare Access in Kishanganj - Digitizing Data Collection with the Avni Platform
date: 2024-11-27T20:30:00.000Z
author: A Ashok Kumar
description:
featuredpost: true
featuredimage: /img/2024-11-27-Project-Potential-Bihar-Health-Access-Digitisation-Case-study/featured.jpg
tags:
  - Social Security
  - Case Study
---

<div style="width: 100%">
    <img src="/img/2024-11-27-Project-Potential-Bihar-Health-Access-Digitisation-Case-study/community.jpeg">
</div>

## About Project Potential
[Project Potential](https://www.projectpotential.org/), based in Kishanganj, Bihar, was founded in 2014 with a vision to end poverty sustainably and inclusively in India’s poorest districts. The organization envisions enabling intergenerational social mobility by addressing systemic challenges in health, education, and employment.
To achieve its goals, Project Potential has actively worked to empower youth through skill development, employment opportunities, and solving critical community issues. Over the years, their efforts have created an impact on more than **7.5 lakh people**, transforming lives through innovative and community-driven solutions.

## About the Health Access Program
Every year, an estimated **6.3 crore Indians** fall below the poverty line due to high healthcare costs<sup>1</sup>, despite government programs like universal health insurance and maternal support schemes.
In Bihar, **36% of the population** faces multidimensional poverty, struggling with inadequate healthcare, poor education, and low living standards. This translates to a staggering population of over **4 crore** people in need of urgent interventions.
To address the financial burden of healthcare, the Government of India introduced the **Pradhan Mantri Jan Arogya Yojana (PMJAY)**, providing health coverage of **₹5,00,000 per family per year** for secondary and tertiary care. Despite its benefits, the lack of awareness and infrastructure has hindered many eligible individuals from registering for this life-changing scheme.

To overcome these challenges, Project Potential has launched an integrated implementation system aimed at increasing access to health schemes like **Ayushman Bharat Yojana (PMJAY)** across the Kishanganj district. Starting with **Thakurganj, Pothia, and Bahadurganj** blocks, the project focuses on awareness campaigns and end-to-end processes, from registration to card distribution.

### Key Achievements:
- Access to health cards has been provided to over **20,000 beneficiaries** so far.
### Goals and Targets:
- Building a PMJAY model panchayat in Besarbati (Thakurganj Block), targeting 100% health card enrollment for over 10,000 eligible beneficiaries providing benefits worth over Rs 100 crores.
- Extending impact to 5,000 beneficiaries in the adjacent Bhatgaon Panchayat.

1 https://www.indiaspend.com/data-viz/three-charts-on-ayushman-bharats-achievements-and-shortfalls-878004


## Why Digitization is Needed
In today’s data-driven world, reliable and accessible information is the cornerstone of effective decision-making—especially in healthcare. The paper-based system along with the limited use of Google Forms, which we were using for tracking healthcare access and beneficiary data, were often prone to errors, duplication, and inefficiency. These limitations resulted in missed opportunities to connect eligible individuals with vital health schemes like Ayushman Bharat Yojana (PMJAY).

Digitization transforms these challenges into opportunities by streamlining data collection, ensuring real-time accessibility, and enhancing accuracy. In Kishanganj, one of India’s poorest regions, healthcare gaps are significant, making digital solutions indispensable for bridging the divide between policy and practice. By embracing digitization, we ensure that every eligible beneficiary can access the benefits they are entitled to.

<div style="width: 100%">
    <img src="/img/2024-11-27-Project-Potential-Bihar-Health-Access-Digitisation-Case-study/work.jpg">
</div>

## Exploring Tools for Digitization
Before choosing Avni, we explored other tools for digitization. However, most options were either too rigid to adapt to our needs of working offline or required expensive customization. Avni stood out for its open-source nature, flexibility, and user-friendly design, allowing seamless integration with program requirements.

## Why Avni?
The Avni platform was selected for its open-source platform, flexibility, scalability, and ease of use. Key reasons include:

1. **Customizability for Local Needs:** Seamlessly integrates with processes like PMJAY’s eKYC, tracking card printing, and ensuring card distribution to beneficiaries.
2. **Offline Functionality:** Ensures uninterrupted data collection even in areas with limited internet access.
3. **Data Analytics:** Provides actionable insights to identify healthcare gaps and prioritize interventions effectively.
4. **Multilingual Support:** Avni’s availability in Hindi and English makes it accessible to on-ground teams, facilitating smooth operations.

Key features tailored for this implementation included scheduled follow-up visits to beneficiaries, households with reminders, offline report cards and longitudinal reports to track the progress at the individual field coordinators’ level, and customized  dashboards using the integrated metabase platform for tracking the program’s progress

## Self-Servicing Avni
We adopted a self-service mode to implement Avni, **empowering** us to operate the platform without depending on external consultants. This approach ensures:
- **Sustainability:** Internal capacity-building enables long-term scalability.
- **Local Ownership:** Greater accountability and community involvement in implementation.
- **Cost Efficiency:** Eliminates the need for costly external implementation teams.

## Experience of Self-Servicing Avni
The journey of self-servicing Avni demonstrated how focused training, determined effort, and collaboration can lead to transformative change within a short span and with minimal resources.

**Training and Empowerment:** Over the course of six intensive training sessions held within three weeks, I gained a comprehensive understanding of the Avni platform. This hands-on learning equipped me with the skills needed to independently set up, configure, and adapt the system, significantly boosting my confidence and ensuring I could manage the platform effectively.

**Strong Support from the Samanvay Team for a Quick Rollout:** The training, coupled with dedicated support from the Samanvay team, enabled us to take the solution live within a month. This collaborative effort ensured an efficient and cost-effective rollout, proving that even with limited resources, it’s possible to achieve significant outcomes.

**Community Adaptation:** Transitioning from being trained to training others with limited exposure to digital tools required a strategically planned approach. The platform was piloted and tested multiple times to ensure its reliability. After fine-tuning it to meet the practical needs of program managers, field coordinators, panchayat coordinators, data operators, and ward mobilizers, the platform was ready for field implementation. This step ensured that the system was both relevant and user-friendly, enabling seamless data-driven decision-making.


<div style="width: 100%">
    <img src="/img/2024-11-27-Project-Potential-Bihar-Health-Access-Digitisation-Case-study/self-service.png">
</div>
<br/>
<span style="color:#ff470f">This self-service journey underscores the power of localized capacity building and collaboration in accelerating the adoption of digital tools for improving healthcare access. It stands as a testament to what can be achieved through teamwork, strategic support, and a commitment to innovation.</span>

## Digitisation using Avni and it's impact
Central to the program’s success is the Avni platform, an open-source mobile application tailored to community health initiatives. It enables:
- Efficient beneficiary registration.
- Tracking of beneficiaries and follow-ups.
- Real-time, digitized data collection, replacing cumbersome paper records.

By leveraging Avni, Project Potential ensures no beneficiary is left behind, whether during health card creation camps, household visits, or awareness campaigns. This digital transformation is reshaping healthcare access in Kishanganj.

Since implementing Avni, the program has achieved remarkable milestones:
1. **Enhanced Coverage:** Over **1,000** beneficiaries registered within a month, providing access to Health cards that can be used for critical health services.
2. **Timely Follow-Ups:** Automated reminders ensure consistent outreach by the field team, even remotely.
3. **Data Accuracy:** Digitized records have minimized errors and reduced instances of duplication or fraud.
4. **Empowered Field Teams:** Local workers are equipped to manage processes independently, improving productivity.

<div style="width: 100%">
    <img src="/img/2024-11-27-Project-Potential-Bihar-Health-Access-Digitisation-Case-study/impact.png">
</div>

## Impact Story: Changing Lives Through Health Cards
One such story is of Ram, a 50-year-old resident of Hathiduba village of Besarbati Panchayat. He had been suffering from chronic health issues but could not afford treatment. During a health card registration drive, Ram’s family was registered under PMJAY using Avni. Within weeks, he underwent heart surgery at a hospital in Patna with 2 lakh utilisation from Ayushman card. Today, Ram is healthy and grateful for the access to quality healthcare that was made possible through this initiative. His story is a testament to the life-changing potential of digitised healthcare access.

## What users are saying
Rumi , a field supervisor, says:

*अवनी ऐप की मदद से हम ऑनलाइन और ऑफलाइन दोनों तरीकों से डेटा कलेक्ट कर सकते हैं। यह उन क्षेत्रों में बहुत मददगार है जहाँ इंटरनेट कनेक्टिविटी नहीं है। हिंदी और अंग्रेज़ी दोनों में उपलब्ध होने से हमारी टीम का काम बहुत आसान हो गया है*

Translated in English : *With Avni app data can be collected in both online and offline modes which helps in continuing work in remote areas where there is limited or no internet connectivity. It is available in both Hindi and English which makes work easier for the on-field team.*

Poornima, a panchayat coordinator, shares:

*"With Avni, health card registration has become so streamlined. I can work offline, edit and track everything—right from eKYC to card distribution. This has reduced our workload significantly."*

Another Panchayat coordinator shares:

*"Avni has made my work much easier. I can register beneficiaries and ensure they get their health cards on time. "*

<div style="width: 100%">
    <img src="/img/2024-11-27-Project-Potential-Bihar-Health-Access-Digitisation-Case-study/testimonial.png">
</div>

## Planning for Other Projects
Building on the initial success of the Health Access Program, we are excited to expand Avni’s application to other critical areas of community development. Future plans include:
- **Students’ Progress Tracking:** Leveraging Avni to monitor student attendance, academic performance, and overall development, ensuring timely interventions to improve programming-based skilled outcomes.
- **Youth Database Creation and Monitoring:** Using the platform to build and manage a comprehensive database of youth for skill training and employment programs, enabling better tracking of their progress and matching them with suitable opportunities.

Avni’s adaptability and customizability makes it an ideal choice for these initiatives, ensuring that it can seamlessly address the unique needs of diverse community-driven programs. By integrating Avni into these projects, we aim to enhance efficiency, accountability, and the impact of our efforts across various sectors.

## Conclusion
The digitization of data collection through Avni is transforming healthcare access in Kishanganj, starting with **Besarbati Panchayat**. By empowering local teams and adopting a self-service approach, the program has laid the foundation for sustainable and scalable healthcare delivery.
As Project Potential refines and expands this model, Kishanganj is becoming a beacon for technology-driven, community-led healthcare access. This journey not only enhances healthcare outcomes but also creates a replicable blueprint for other regions of Bihar and India.

**Together, technology and community efforts are bridging healthcare gaps—one digital record at a time.**

_About the Author : [A Ashok Kumar](https://www.linkedin.com/in/a-ashok-kumar/), Associate Director - Program Strategy & Operations, Project Potential, is passionate about creating meaningful impact in healthcare, youth development, and leadership. With a strong focus on improving Monitoring and Evaluation (M&E) systems, he is committed to driving scalable and sustainable change in underserved communities._


# File: ./case-studies/2025-04-30-restoring-waterbodies-avni-atecf.md

---
templateKey: case-study
title: Restoring Waterbodies How the Avni Gramin App, in Collaboration with ATECF, is Making a Lasting Impact
date: 2025-04-30T10:00:00.000Z
author: Anjali Bhagabati
description: With India's growing water crisis, the Rejuvenation of Waterbodies Project by ATECF 
  and the Avni Gramin App are bringing lasting change by streamlining restoration efforts 
  through technology, empowering rural communities, and ensuring sustainable water access.
featuredpost: false
tags: 
    - Water
featuredimage: /img/2025-04-30-restoring-waterbodies-avni-atecf/R1.webp
---

<p>
India is facing an escalating water crisis. With the country’s water supply rapidly dwindling,
<a href="https://economictimes.indiatimes.com/news/economy/agriculture/by-2030-indias-water-demand-to-be-twice-the-available-supply-indicating-severe-water-scarcity-report/articleshow/64679218.cms?from=mdr" target="_blank" rel="noopener noreferrer">
experts have warned that by 2030, India may fall into the category of "water-stressed nations"
</a>,
with per capita water availability dropping below sustainable levels.
</p>

<p>
To address this issue, the Rejuvenation of Waterbodies (RWB) Project by the
<a href="https://www.ategroup.com/csr/#tab2" target="_blank" rel="noopener noreferrer">
A.T.E. Chandra Foundation
</a> (ATECF) is making strides in restoring neglected water bodies throughout India.
ATECF focuses on revitalising ponds, lakes, and other water bodies that have been neglected due to sedimentation and other issues,
helping to increase their storage capacity and improve access to water for rural communities.
</p>

<div style="width: 70%">
    <img src="/img/2025-04-30-restoring-waterbodies-avni-atecf/R1.webp">
</div>


It has been driving large-scale waterbody rejuvenation efforts across nine states in India, including Maharashtra, Rajasthan, Uttar Pradesh, and more.


## Need for Digitisation:

As the efforts to restore water bodies grow, the need for a streamlined, transparent way to manage and track the progress of restoration activities becomes crucial.

<p>
To solve this,
<a href="https://projecttech4dev.org/waterbody-rejuvenation-project-a-t-e-chandra-foundation/" target="_blank" rel="noopener noreferrer">
ATECF collaborated with Avni and started using the Avni Gramin App
</a>
as a digital tool for data collection for their Community Resource Persons (CRPs) working in the field.
</p>


The Avni-Gramin App makes it easier to collect, store, and manage data related to waterbody restoration, such as silt removal, bund strengthening, and other critical interventions. The app’s simple interface and offline functionality ensure that even in areas with limited connectivity, data can still be recorded and updated.

<div style="width: 70%">
    <img src="/img/2025-04-30-restoring-waterbodies-avni-atecf/R3.webp">
</div>


<h2>📹Case Study: ATECF Rejuvenating Water Bodies | Open-sourced Tool in Solving India's Water Crisis</h2>

<a href="https://www.youtube.com/watch?v=TRXE63EmLGY" target="_blank" rel="noopener noreferrer">
  Click here to watch the video!
</a>


## Avni-Gramin: Empowering Communities, Simplifying Data

Avni-Gramin is an open-source, Android-based mobile app for recording real-time information about the various on-the-ground activities associated with a waterbody rejuvenation project. The app is a part of Avni, a digital tool that helps social impact organisations simplify workflows, track program progress, and make better decisions based on accurate, structured data.

<div style="width: 70%">
    <img src="/img/2025-04-30-restoring-waterbodies-avni-atecf/78.webp">
</div>

### Key Features of Avni-Gramin:

- **Real-Time Data Collection:** CRPs can collect data on restoration activities immediately and upload it to the system, ensuring real-time tracking of project progress.
- **Offline Functionality:** No internet connection? No problem. Avni-Gramin works offline, allowing users to continue collecting data even in remote areas with no connectivity. Once a connection is available, the data is synced automatically.
- **User-Friendly Interface:** Designed with simplicity in mind, Avni-Gramin is easy to use, even for those with minimal experience with smartphones, making it accessible to a broad range of rural users.
- **Geotagging and GPS Tracking:** The app enables tracking GPS coordinates (latitude and longitude) of a site to check coordinates accuracy.
- **WhatsApp Chatbot for Quick Support:** With Glific integration, the app is linked to a WhatsApp chatbot that provides instant assistance to the field users, answering questions about data entry or project details.
- **Mobile Number Uniqueness:** A check is done on mobile number uniqueness to identify potential duplicates or fraudulent entries.
- **OTP Verification:** A One-Time Password (OTP) verification system ensures that all user data is secure and verified, enhancing the overall trustworthiness of the platform.
- **Structured Data Entry:** Customisable forms make it easy to enter data in a structured and consistent manner, ensuring accuracy in reporting and decision-making.


## Integration of Avni and Dalgo: Expanding Reach

<p>
To further enhance the power of Avni, it integrates seamlessly with
<a href="https://dalgo.org/" target="_blank" rel="noopener noreferrer">
Dalgo
</a>,
a data aggregation tool that helps NGOs and community organisations scale their operations.
This integration allows for deeper insights into the data collected and facilitates better decision-making across large-scale projects.
The synergy between Avni-Gramin and Dalgo offers comprehensive tracking, reporting, and analysis capabilities, ensuring that organisations can manage their projects efficiently and effectively.
</p>


<div style="width: 70%">
    <img src="/img/2025-04-30-restoring-waterbodies-avni-atecf/R2.webp">
</div>

## Avni-Glific Integration:

<p>
The integration between Avni and
<a href="https://glific.org/" target="_blank" rel="noopener noreferrer">
Glific
</a>
empowers NGOs to enhance their engagement efforts by leveraging WhatsApp for communication, enabling organisations to automate and personalise interactions with beneficiaries.
Glific supports interactive chats, allowing beneficiaries to respond, ask questions, or provide feedback through platforms like WhatsApp.
</p>

<blockquote>
For a visual demonstration of how Avni and Glific work together,
<a href="https://www.youtube.com/watch?v=MufJOHVUQh0" target="_blank" rel="noopener noreferrer">
do watch this video
</a>.
</blockquote>

---
## Scale and Credibility

<p>
The Rejuvenating Water Bodies (RWB) project and the Avni platform were featured in the
<a href="https://www.indiabudget.gov.in/economicsurvey/doc/eschapter/echap09.pdf" target="_blank" rel="noopener noreferrer">
Economic Survey of India 2024–25
</a>
as a model of how grassroots efforts can be amplified through digital innovation.
While RWB brings large-scale impact through community-led waterbody restoration, Avni enables this scale with structured, real-time data collection—even in remote areas.
Their combined approach is now gaining national and global recognition as a replicable model for tech-enabled rural development.

</p>

<div style="width: 70%">
    <img src="/img/2025-04-30-restoring-waterbodies-avni-atecf/ATECF_ES.jpeg">
</div>

---

## Can Avni Benefit You?

If you are part of an NGO or a community-focused organisation working on projects such as waterbody restoration, health, education, or social welfare, Avni can help you streamline your data collection and management efforts. By providing real-time tracking, offline functionality, and structured data collection, Avni can help you:

- Ensure hassle-free and timely data collection
- Improve transparency and accountability in your projects
- Make informed decisions based on reliable data
- Scale your operations with ease, even in remote or underserved areas

Join the growing number of organisations that are using Avni to make a difference in communities across India. Whether you are working on waterbody rejuvenation, improving access to health services, or addressing social security issues, Avni can help you achieve your goals more efficiently.

If you're interested in adopting a similar approach or want to learn more about how the Avni platform can support your initiatives:

<p>
👉 <a href="https://calendly.com/avnisupport-samanvayfoundation/product-demo-and-discussion?embed_domain=avniproject.org&embed_type=PopupText" target="_blank" rel="noopener noreferrer">
Schedule a call with us
</a>
</p>

<p>
📬 <a href="https://avniproject.us17.list-manage.com/subscribe?u=5f3876f49a7603817af2856b9&id=c9fdedc9e7" target="_blank" rel="noopener noreferrer">
Subscribe to our newsletter to stay updated on new case studies, features, and implementation stories.
</a>
</p>


---


# File: ./case-studies/2025-05-02-ihmp-strengthening-adolescent-health.md

---
templateKey: case-study
title: Strengthening Adolescent Health through Community-Led Digital Interventions
date: 2025-05-02T10:00:00.000Z
author: Avni Team
description: >-
  Explore how the Institute of Health Management Pachod (IHMP) enhanced adolescent health 
  outcomes by digitizing frontline healthcare delivery in urban slums and rural communities 
  using the Avni platform.
featuredpost: false
featuredimage: 
tags:
  - Health
---

## Introduction

Over the last 45 years, the Institute of Health Management Pachod (IHMP) – a non-profit
organisation – has been at the forefront of addressing critical public health issues faced by
disadvantaged communities in India. Since its establishment in 1979, IHMP has positively impacted
over seven million people, focusing on maternal and neonatal health, child health, sexual and
reproductive health, family planning, and adolescent health and development.

A major focus over the last 25 years has been on safeguarding and transforming the lives of
vulnerable adolescent girls in rural and urban slum communities.

IHMP has provided life skills education to 103,000 unmarried girls, delaying marriage age from 14.5
to 18 years, while also engaging 8,600 boys and young men to prevent child marriage and promote
gender-equitable behaviours.

The Life skills Education for adolescent girls was scaled up through a network of 7 NGOs with equally
encouraging results similar to the pilot project.

IHMP’s sexual and reproductive health interventions have reached over 127,000 married adolescent
girls, significantly increasing contraceptive use, delaying first pregnancies, and reducing maternal,
neonatal and child morbidity and mortality.

<div style="width: 70%">
    <img src="/img/2025-05-02-ihmp-strengthening-adolescent-health/I1.webp">
</div>

## Problem Statement & Intervention 1: Addressing Health Risks Among Adolescent Girls

The villages of central Maharashtra and the urban slums of Pune presented several public health
challenges:

- **High Health Risks**: Early pregnancies led to increased adolescent deaths and maternal and neonatal morbidity.
- **Limited Access to Services**: Adolescent girls and young women had limited access to sexual and
reproductive health services.
- **Behavioral Barriers**: Lack of awareness had a major influence on health seeking and utilisation
behaviours and effective use of healthcare facilities.

**IHMP’s Integrated Reproductive and Sexual Health and Family Planning Project** focused on:

- Providing life skills education with the aim of empowering adolescent girls in order to prevent
early marriages.
- Increasing family planning awareness

- Improving access to contraceptives to delay early pregnancy and for adequate spacing between
pregnancies
- Improving access to antenatal and home based postnatal and neonatal care services.
- Identifying girls and young women with danger signs and linking them to appropriate
secondary or tertiary health care services
- Engaging and educating boys and young men in order to prevent child marriage and influence
their attitudes and gender inequitable behaviours, including intimate partner violence.

The intervention relied on a **community-based model**, led by ASHA workers through regular home
visits, paper-based registers, and monthly micro-plans. This manual model laid a strong foundation
for scaling up.

The interventions were scaled through a network of NGOs in 120 villages in 5 of the most backward
districts of Maharashtra. The impact of the interventions were reported in The Lancet as follows:

**Efficacy of an intervention for improving the reproductive and sexual health of married adolescent
girls and addressing the adverse consequences of early motherhood**

**Findings:** 
- **Baseline comparability:**  
  Respondents from intervention and control sites were similar at the start for most key indicators.

- **Age at first birth:**  
  - Median age at first birth at intervention sites rose from **16.9 years** (2008) to **18.1 years** (2010).

- **Contraceptive use:**  
  - Intervention: **33.7%**  
  - Control: **6.4%**  
  - (OR 7.45, 95% CI 5–11)

- **Early antenatal registration:**  
  - Intervention: **78.7%**  
  - Control: **54.7%**  
  - (OR 2.93, 95% CI 2.11–4.06)

- **Minimum standard antenatal care received:**  
  - Intervention: **56.1%**  
  - Control: **24.3%**  
  - (OR 3.89, 95% CI 2.78–5.48)

- **Treatment for antenatal complications:**  
  - Intervention: **87.6%**  
  - Control: **77.1%**  
  - (OR 2.18, 95% CI 1.21–3.12)

- **Treatment for postnatal/neonatal complications:**  
  - Intervention: **78.8%**  
  - Control: **62.0%**  
  - (p = 0.07; marginal significance)

- **Treatment for reproductive tract/sexually transmitted infections (RTI/STI):**  
  - Intervention: **60.4%**  
  - Control: **28.9%**  
  - (OR 3.76, 95% CI 2.34–6.05)

- **HIV testing:**  
  - Intervention sites: Increased from **11.7%** (2008) to **58.7%** (2010)  
  - Control sites: Increased from **1.8%** (2008) to **15.9%** (2010)

**Interpretation:** Focused, community based interventions, implemented by frontline health workers
result in a rapid and significant improvement in utilization and coverage with reproductive health
services among married adolescent girls. The interventions were implemented primarily through
community health workers and auxiliary nurse midwives. With more than 900 000 community health
workers and 140 000 auxiliary nurse midwives providing primary level care in India, replication of
this strategy seems imminently feasible.

Eventually the intervention was successfully scaled up through 7 primary health centres, in one
block, exclusively through the Government health delivery system

## Problem Statement & Intervention 2: Improving Efficiency in Healthcare Delivery Through Digital Tools

Despite successful interventions, service delivery inefficiencies emerged:

- **Manual Paperwork**: Led to frequent human errors, missed visits, and delayed interventions.
- **Frontline Worker Burden**: Excessive paperwork left less time for community engagement and service provision.

To overcome these, IHMP adopted the **Avni platform**, digitizing healthcare delivery across urban slums and rural villages.

Key features of the Avni app:

- **Census and target population listing**: leads to denominator based strategic
planning
- **Monthly Visit Scheduling and Micro-Planning**: Automated schedules based on real-time health assessments, prioritizing high-risk cases.
- **Real-time Monitoring**: Supervisors track field activities instantly, identifying and addressing gaps.
- **Job Aid for ASHAs**: The app supports symptom assessments and action guidance during visits.
- **Counseling**: It facilitates real-time need specific behaviour change
communication, counselling and motivation.
- **Referrals**: The App facilitates timely identification of danger signs and morbidity
leading to efficient referral, and supports effective linkage to health services.

<div style="width: 70%">
    <img src="/img/2025-05-02-ihmp-strengthening-adolescent-health/I2.webp">
</div>

## Impact and Outcomes

The digital intervention led to significant improvements:

- **Behavioral Changes**: Increased maternal service utilization and contraceptive use.
- **Performance of health workers**: Frontline workers demonstrated effective use
of the digital App. There was a measurable improvement in the performance of
frontline health workers
- **Quantitative Gains**: From 2021–2024, YMW (young married women) monthly visit coverage rose by 21.4 percentage points.
- **Health Status changes**: There was a significant reduction in the burden of
morbidity and maternal complications.
- **Efficiency Gains**: ASHA workers reported higher job satisfaction, reduced paperwork, and better income through performance-based incentives.
- **Monitoring and Coverage**: Real-time data allowed timely corrective actions, improving service coverage.

<h2>📹Case Study: IHMP | Digitising Health Programs for Adolescent Girls</h2>

<p>
  <a href="https://www.youtube.com/watch?v=l8MKie7cSms&list=PLEy8ff0CKDBkFhqQ95itFuEJMf38HwLBx" target="_blank" rel="noopener noreferrer">
     Click here to watch the video!
  </a>
</p>


<div style="width: 70%">
    <img src="/img/2025-05-02-ihmp-strengthening-adolescent-health/I4.webp">
</div>

## Conclusion

IHMP’s work in Maharashtra’s Marathwada region and Pune’s urban slums shows how digital tools like the Avni app can strengthen public health interventions. By enabling early identification of health needs, real-time monitoring, and effective counselling, the project has improved health outcomes for adolescent girls and young women in vulnerable communities.

The model IHMP has developed is highly replicable and scalable—both in terms of its community-based strategy and the digital infrastructure powered by Avni.

If you're interested in adopting a similar approach or want to learn more about how the Avni platform can support your initiatives:

<p>
👉 <a href="https://calendly.com/avnisupport-samanvayfoundation/product-demo-and-discussion?embed_domain=avniproject.org&embed_type=PopupText" target="_blank" rel="noopener noreferrer">
Schedule a call with us
</a>
</p>

<p>
📬 <a href="https://avniproject.us17.list-manage.com/subscribe?u=5f3876f49a7603817af2856b9&id=c9fdedc9e7" target="_blank" rel="noopener noreferrer">
Subscribe to our newsletter to stay updated on new case studies, features, and implementation stories.
</a>
</p>

Let’s work together to scale impactful solutions for better health outcomes.

# File: ./case-studies/2025-05-28-bridging-the-nutrition-gap-apf-odisha.md

---
templateKey: case-study 
title: Bridging the Nutrition Gap - APF Odisha’s Data-Driven Maternal and Child Health Program Using Avni 
date: 2025-05-28T10:00:00.000Z 
author: Anjali Bhagabati 
description: >-  
featuredpost: false 
featuredimage:
tags:
- Health
---

<div style="width: 30%; margin: auto; ">
    <img src="/img/2025-05-28-bridging-the-nutrition-gap-apf-odisha/why-child-nutrition-matters.png">
</div>

Child nutrition is a vital indicator of a nation’s health and development. While India has made significant strides in
improving maternal and child health over the last decade, there is still a pressing need to address persistent gaps,
especially in underserved rural communities.

One of the most [impactful periods in a child’s life is the first **1,000
days.**](https://azimpremjifoundation.org/what-we-do/health/creche-initiative/) Nutrition during this window plays a
pivotal role in shaping the child’s cognitive development, immunity, and long-term health outcomes.

<div style="background-color: #f9f9f9; border-left: 4px solid #007acc; padding: 16px; margin: 24px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
  <h2 style="margin: 0 0 8px 0; font-size: 1.25rem;">
    🎥 Video Case Study: Azim Premji Foundation | Community Nutrition Program (CNP)
  </h2>
  <a href="https://www.youtube.com/watch?v=sfB9QyFoWW8&list=PLEy8ff0CKDBkFhqQ95itFuEJMf38HwLBx" 
     target="_blank" 
     rel="noopener noreferrer"
     style="color: #007acc; text-decoration: underline;">
    Watch on YouTube
  </a>
</div>

### APF Odisha Nutrition Initiative: Focused Care from Pregnancy to Early Childhood

The **Azim Premji Foundation’s Odisha Nutrition Initiative** addresses these challenges with a focused intervention that
spans from pregnancy through the first five years of a child's life. The initiative targets maternal and child nutrition
through community-level engagement, regular monitoring, and technology-driven support systems.

<div style="width: 30%; ">
    <img src="/img/2025-05-28-bridging-the-nutrition-gap-apf-odisha/program-overview.png">
</div>

### Why Technology Was Essential

Frontline health workers in rural and tribal areas often operate under challenging conditions, including:

* Inconsistent or no internet connectivity
* Limited access to timely health data
* Manual, paper-based reporting systems

The solution required a digital platform that could:

* Be usable offline in remote areas with poor connectivity.
* Customizable for local health workflows.
* Supporting real-time data collection and reporting.
* Be **easy to use** for health workers with a very basic level of training.

### The Solution: Avni – Open-Source Technology for Social Impact

[**Avni**](https://avniproject.org/) is a powerful, open-source platform for field service delivery. It is designed to
enable digital data collection, decision support, and real-time reporting for community health programs. With offline
functionality and modular workflows,it is ideal for nonprofits, government partners, and social enterprises aiming for
deep impact.

Built and maintained by the [**Samanvay Foundation**,](https://www.samanvayfoundation.org/) Avni is currently being
actively used by multiple NGO across India.

### How APF Odisha Is Using Avni

[The Azim Premji Foundation integrated Avni](https://www.youtube.com/watch?v=sfB9QyFoWW8&list=PLEy8ff0CKDBkFhqQ95itFuEJMf38HwLBx&index=5)
into its Pregnancy and Child Program in Odisha, particularly in underserved rural communities. The deployment focuses on
improving early identification of at-risk cases, enhancing field supervision, and enabling data-driven program
management.

#### 1\. Pregnancy Program: Proactive Maternal Care

* Registration & Lifecycle Tracking: Every pregnant woman is registered in the Avni app and monitored through antenatal,
  delivery, and postnatal stages.

* Risk Identification: The app flags high-risk pregnancies, triggering rapid follow-up by Poshan Sathi and Quick
  Response Team (QRT) personnel.

* Timely Reminders: Health workers and supervisors receive automated alerts for critical visits (ANC and PNC), ensuring
  no woman misses essential care.

#### 2\. Child Program: Nutrition Surveillance and Support

* Growth Monitoring: Children under five are tracked monthly for weight, height, and developmental milestones, using WHO
  growth charts.

* Malnutrition Detection: Children identified with Severe Acute Malnutrition (SAM) or Moderate Acute Malnutrition (MAM)
  are prioritized for intervention.

* NRC Referrals & Follow-up: Severely affected children are referred to Nutrition Rehabilitation Centres (NRCs) directly
  through the app. Their recovery and follow-up are digitally tracked post-discharge.

#### 3\. TIMS: Training and Information Management System

The Training and Information Management System (TIMS) is a custom-built module within Avni for APF Odisha. It allows:

* Field staff to request training support based on real-time challenges

* Program leads to track training needs and conduct targeted upskilling

#### 4\. Supervisor Monitoring

Supervisors log visits to Anganwadi Centres and Village Health Nutrition Days (VSHNDs) within Avni. This ensures
real-time visibility for program managers into field operations and quality checks.

#### 5\. Comprehensive Reporting

Avni offers dashboards and downloadable reports to help APF and its partners evaluate program impact, identify issues,
and make data-driven decisions. Reports are built on an innovative BI tool \- Superset

<div style="width: 30%; float: left">
      <img src="/img/2025-05-28-bridging-the-nutrition-gap-apf-odisha/offline-dashboard.gif">
</div>
<div style="width: 30%; float: left">
      <img src="/img/2025-05-28-bridging-the-nutrition-gap-apf-odisha/individual-dashboard-child.gif">
</div>
<div style="width: 30%; float: left">
      <img src="/img/2025-05-28-bridging-the-nutrition-gap-apf-odisha/individual-dashboard.gif">
</div>
<div style="clear: both"></div>
<div style="width: 90%">
    <img src="/img/2025-05-28-bridging-the-nutrition-gap-apf-odisha/reports.png">
</div>  


## **Program Reach and Impact**

Through the Avni platform, the Odisha Nutrition Initiative has achieved significant scale:

* **300** frontline workers actively using the app

* **79,000** children tracked

* **22,000** pregnant women enrolled

* **7,357** households counselled on dietary diversity and Infant and Young Child Feeding (IYCF) practices

* **1,275** children with low Weight-for-Height (WFH) referred to CMAM

* **3,793** high-risk pregnancies linked to institutional deliveries and timely ANC

The APF-Avni collaboration in Odisha shows how **simple, scalable tech** can strengthen public health systems by
empowering field workers, improving data quality, and ensuring that no high-risk case is missed. This approach sets a
benchmark for sustainable, tech-driven healthcare delivery in rural India.

<br>
<i>“Avni plays a pivotal role in strengthening the Community Nutrition Program by bridging the gap between field-level data
collection and real-time decision-making. Its offline-first design is especially effective in remote tribal areas with
limited connectivity. By enabling frontline workers to capture key data on maternal and child health and service
delivery during home visits, growth monitoring sessions, and VHSNDs, AVNI facilitates the timely identification and
follow-up of High-Risk Pregnancies (HRP) and undernourished children.” </i> \- **Ramesh Sahu, Program Manager**


If you're interested in adopting a similar approach or want to learn more about how the Avni platform can support your initiatives:

<p>
👉 <a href="https://calendly.com/avnisupport-samanvayfoundation/product-demo-and-discussion?embed_domain=avniproject.org&embed_type=PopupText" target="_blank" rel="noopener noreferrer">
Schedule a call with us
</a>
</p>

<p>
📬 <a href="https://avniproject.us17.list-manage.com/subscribe?u=5f3876f49a7603817af2856b9&id=c9fdedc9e7" target="_blank" rel="noopener noreferrer">
Subscribe to our newsletter to stay updated on new case studies, features, and implementation stories.
</a>
</p>

Let’s work together to scale impactful solutions for better health outcomes.


# File: ./case-studies/2025-07-31-scoring-for-equality.md

---
templateKey: case-study 
title: Scoring for Equality- How Maitrayana Uses Avni to Measure Impact Through Sports
date: 2025-07-31T10:00:00.000Z 
author: Parth Halani
description: 
featuredpost: false 
featuredimage:
tags:
- Sports
- Skill Development
---
 

Gender equality is not just a vision for Maitrayana—it’s a journey made up of sessions, skills, and stories.

From netball drills to digital safety, from career guidance to life skills education, Maitrayana’s sports-based programs equip adolescent girls across India’s cities with tools to lead empowered lives.

But when that journey spans multiple programs, hundreds of sessions, and thousands of girls in Mumbai, Bangalore, and Delhi, managing it on spreadsheets is not enough.

To ensure no girl gets left behind, Maitrayana uses the **Avni platform** to digitise how participants, sessions, and progress are tracked on the ground.

That’s where Avni steps in.

## A Structured Program Built on Batches, Sessions, and Outcomes

At the heart of Maitrayana’s model is a well-defined structure:

- Participants are enrolled into batches, each linked to a donor-funded programme.
- Each programme comprises multiple sessions focusing on:
  - ✅ Life skills (e.g., leadership, communication, goal setting)
  - 🏐 Sports-based training (e.g., netball techniques, teamwork)
  - 👥 Gender and social awareness
  - 🧠 Health and wellbeing

Every session is designed to follow a specific theme, ensuring consistency and measurable learning for each participant.

With Avni, Maitrayana tracks:

- **Individual-level details**: Participant profiles, batch enrolments, and session attendance  
- **Batch-level progress**: Completion status of sessions across batches  
- **Program-level analytics**: Total reach, attendance trends, and donor-linked metrics  

## A Visual Look at the Workflow

Here’s how Maitrayana’s process flows using Avni:

> The process begins with registering participants, followed by batch creation and program enrollment (e.g., EJP, Vriddhi, YPI Pragati). Field teams then use a Session Encounter Form to mark both the activity and attendance, with a dynamic list of participants per batch auto-populated.

<div style="width: 80%; margin: auto; ">
    <img src="/img/2025-07-31-scoring-for-equality/1.webp">
</div>

## A Glimpse into the App

Below are a few screenshots from the Avni app that bring this workflow to life:

- **Batch Profile View**: Displays batch details along with a list of enrolled participants. It also links to all programs the batch is enrolled in, making it easy to view program-wise progress.  
- **Program Overview within a Batch**: Shows session history and enrollment details for each program the batch is a part of—be it EJP, Vriddhi, or YPI Pragati.  
- **Session Attendance Form Summary**: Allows facilitators to quickly mark attendance and record activity details. The dynamic participant list ensures accuracy and saves time on the field.

<div style="width: 80%; margin: auto; ">
    <img src="/img/2025-07-31-scoring-for-equality/2.webp">
</div>

> *(For illustration purposes only. Names shown are fictitious and do not represent real individuals.)*

These structured linkages—from Participant → Batch → Program → Session Form—enable Maitrayana to monitor individual participation across multiple programs.

> Whether tracking a girl’s attendance in life skills sessions under YPI Pragati or her progress across digital, career readiness, and workplace rights sessions under the Economic Justice Program (EJP), this connected data flow allows for deeper insights into engagement and outcomes.

## Monitoring and Evaluation in Action

Maitrayana’s use of Avni doesn’t stop at field data capture—it’s actively used to drive **real-time monitoring and donor reporting**. For example:

- **Attendance Summary Reports**: Maitrayana tracks attendance trends across batches, sessions, and programs. A session-wise breakdown of attendance allows them to quickly identify drop-offs or engagement gaps.

<div style="width: 80%; margin: auto; ">
    <img src="/img/2025-07-31-scoring-for-equality/3.webp">
</div>

- **Active Participant Dashboards**: Donor-wise participant engagement can be easily viewed using dashboards. This helps Maitrayana present granular data on how many girls are actively participating in each program funded by each donor.

<div style="width: 80%; margin: auto; ">
    <img src="/img/2025-07-31-scoring-for-equality/4.webp">
</div>

These visual reports empower the team to:

- Monitor outreach and attendance in near real-time  
- Ensure batch-wise accountability linked to funders  
- Take quick corrective actions when needed  
- Share transparent updates with stakeholders  

With **Avni and Metabase combined**, Maitrayana has built a monitoring and evaluation framework that’s **scalable, transparent, and responsive** to the dynamic needs of a field-based gender equity program.

## A Replicable Model for Social Impact Organisations

Maitrayana’s approach offers a replicable blueprint for other organisations running **training, education, or empowerment programs**—especially those with decentralised teams and session-based engagement.

Their use of Avni illustrates how the right digital tools can:

- 🔍 Bring structure to complex field operations  
- 📊 Enable data-driven decisions and course corrections  
- 🤝 Build transparency and accountability with donors and stakeholders

# File: ./case-studies/2025-08-01-empowering-waste-pickers.md

---
templateKey: case-study 
title: Empowering Waste Pickers Through Tech- How Hasiru Dala Scaled Impact Using Avni
date: 2025-08-01T10:00:00.000Z 
author: Anjali Bhagabati
description: 
featuredpost: false 
featuredimage:
tags:
- Waste Management
---
 

In the bustling streets of Indian cities, waste often seems invisible. But behind every clean neighbourhood is a group of people whose labour remains largely unrecognised—the waste pickers.

Established in Bangalore, India, **Hasiru Dala** (meaning “green force” in Kannada) is changing that. The organisation empowers waste pickers by recognising their contributions, securing their rights, and integrating them into formal waste management systems.

---

<div style="width: 80%; margin: auto; ">
    <img src="/img/2025-08-01-empowering-waste-pickers/123.png">
</div>

## 🧩 The Challenge: Paper-Based Chaos

Despite strong grassroots engagement, the Hasiru Dala team faced growing operational hurdles as its programs expanded:

- Records kept on paper were prone to being misplaced or having spelling mistakes.
- Follow-ups were inefficient, requiring teams to carry bulky folders and sift through files to access individual records and service histories.
- Generating reports was delayed, as field staff had to manually enter data into spreadsheets after returning from the field.

This slowed down operations, increased the chance of errors, and made real-time decision-making difficult.

---

## 🚀 The Turning Point: Going Digital with Avni

To overcome these operational hurdles, Hasiru Dala adopted **Avni**, an open-source platform tailored for fieldwork data collection and management. This move allowed them to transition from fragmented paper systems to a centralised, real-time, and error-resistant digital workflow.

---

## 💡 How Hasiru Dala Uses Avni

The organisation implemented Avni across multiple projects to:

- Register waste pickers and maintain detailed digital profiles  
- Track access to services such as KYC completion, enrolment in government schemes, and benefits received  
- Monitor training needs and delivery, including programs like Leadership Development, Solid Waste Management, and Entrepreneurship Training  
- Ensure tailored interventions using data-driven insights to deliver support based on each individual’s needs  

---

## 🌟 Impact After Using Avni

The adoption of Avni has brought significant improvements across Hasiru Dala’s operations:

- 📱 **Fully Mobile Operations**: Field staff now capture all data on the go, even without internet connectivity.  
- ✅ **Improved Data Accuracy**: Built-in validations have minimised errors. Data verification accuracy increased by **90%**, enabling more reliable service delivery.  
- 📊 **Faster, Data-Driven Decisions**: Real-time data access has reduced reporting time from **10 days to just 2 days**.  
- 🎯 **Offline Dashboard Cards**: Teams can view field status at a glance within the Avni mobile app.  
- 📥 **Efficient Reporting**: Longitudinal data exports and Superset dashboards simplify progress tracking.  
- ⚡ **Increased Field Efficiency**: Registration speed doubled—from **3 to 6 individuals per hour**, enabling greater outreach.  
- 👩‍💻 **Easy to Use**: Even field staff with limited digital literacy quickly adapted and now confidently use the app daily.  

---

<div style="width: 80%; margin: auto; ">
    <img src="/img/2025-08-01-empowering-waste-pickers/234.png">
</div>

## 🗣️ Testimonial from the Field

> "Hasiru Dala has been using Avni for many years. We have come across many features that have proven to be useful for us — especially in the enumeration and profiling of waste pickers, tracking beneficiaries, and maintaining KYC and related details in one place.
> 
> Thanks to Avni, reporting, data quality checks, analysis, and many other processes have become much easier for us. The approach to problem-solving, fulfilling requirements, and providing technical support is excellent.
> 
> I sincerely thank the Samanvay Foundation for understanding the challenges faced by field facilitators and others who handle large volumes of data.
> 
> Avni is user-friendly and loaded with features."
> 
> — **Charan Kumar**, Avni Admin, Data Supervisor, Hasiru Dala

---

## 🎥 Video Testimonials  
*Coming soon*

---

## 🌍 Why It Matters

Waste pickers are among the most marginalised urban workers in India, often facing systemic exclusion and deep-rooted social stigma. Providing them with identity, access to essential services, and pathways to formal employment not only transforms individual lives but also contributes to Sustainable Development Goals (SDGs) such as:

- **Decent Work and Economic Growth**
- **Reduced Inequalities**
- **Sustainable Cities and Communities**

Digital tools like Avni empower Hasiru Dala to deliver these interventions more effectively—by improving visibility, streamlining coordination, and ensuring that support reaches those who need it most.

The result is a model that enhances both **dignity** and **impact** for waste pickers.

---

## 🤝 Can Avni Benefit You?

If you are part of an NGO or a community-focused organisation working on projects such as **waterbody restoration, health, education,** or **social welfare**, Avni can help you:

- ✅ Ensure hassle-free and timely data collection  
- 📈 Improve transparency and accountability in your projects  
- 📊 Make informed decisions based on reliable data  
- 🚀 Scale your operations with ease, even in remote or underserved areas  

Join the growing number of organisations that are using Avni to make a difference in communities across India.

Whether you are working on waterbody rejuvenation, improving access to health services, or addressing social security issues, Avni can help you achieve your goals more efficiently.

---

👉 **[Schedule a call with us](#)**  
📬 **[Subscribe to our newsletter](#)** to stay updated on new case studies, features, and implementation stories.

---


# File: ./case-studies/avni-for-sickle-cell-disease-screening-and-treatment.md

---
templateKey: case-study
title: Avni for sickle cell disease screening and treatment
date: 2020-01-06T12:56:54.094Z
description: >-
  Sickle cell disease affects a huge percentage of tribal population in India
  because of its genetic/hereditary nature. The effects of the disease are
  severe. There is no prevention. Jan Swasthya Sahyog is working in
  collaboration with M.P. state government in Annupur district which has a high
  tribal population. The goal of the project is to screen all members of tribal
  families which has a pregnant woman. Anyone found with sickle cell disease is
  provided treatment. Avni field app was used by the entire team to manage all
  their client's data. This allowed them to coordinate their efforts amongst
  each other. Avni field ensured that the end to end steps are completed for
  each person. Avni helped improve the effectiveness of the team on the ground
  in executing the program.
tags:
  - Health
  - Government
  - Case Study
---
Sickle cell disease (common type being sickle cell anaemia) affects a huge percentage of tribal population in India because of its genetic/hereditary nature. A person can simply be a carrier which is harmless to oneself. But when a child is born from two parents who are both carriers then the child gets this disease. The effects of the disease are severe and more can be read about it here (https://en.wikipedia.org/wiki/Sickle_cell_disease). The carriers are anywhere between 10-20% in many tribal populations. The public health imperative is to reduce the number of couples where both parents are carriers and treat those who have the disease. There is no prevention.

[Jan Swasthya Sahyog](http://jssbilaspur.org/) is working in collaboration with M.P. state government in [Annupur district](https://en.wikipedia.org/wiki/Anuppur_district) which has a high tribal population. The goal of the first phase of the project is to screen all members of tribal families which has a pregnant woman. Anyone found with sickle cell disease is provided treatment*. The broad activities involved are:

* Register pregnant women at their home
* Collect their blood sample and send them for tests to the partner lab
* In the lab perform the tests
* Register and similarly test rest of family members if the woman is found to have the disease
* Start treatment for woman and other family members if they are also found with the disease
* Follow up on the treatment regularly

It is important to note that these activities are happening in parallel for many people across the district, in the village, lab and clinic. 11000 such families and 25000 total individuals were screened as part of this project. This was done by a team of 19 people, working with the ANMs in the district. Managing all these distributed activities, in parallel is a really difficult job because there are dozens of points at which the ball can get dropped. e.g. The sample could be sent to the lab, but the lab misplaces it. Or the test is done but the result is never looked at.

Avni field app was used by the entire team to manage all their client's data while they are in the village, lab or clinic. This allowed them to coordinate their efforts amongst each other. Avni field dashboard provided the users with visibility into scheduled/pending activities which is key to ensuring that the end to end steps are completed for each person who is registered into the system. The picture below where ANM is tagging samples and data entry person adding the same to Avni. "The ability to see what work is pending by the lab/clinic/in-village helped reduce the stress of the field team and made them productive" - paraphrasing the words of program lead.

![Lab sample collection and data entry in Avni](/img/jss-sickle-sample-collection.jpeg "Lab sample collection and data entry in Avni")

You can get a quick preview of how Avni provides the support for managing one's work via [a dashboard](/static/my-dashboard-c451a7d685b594c31242992322fa774a.gif), [scheduling of visits](/static/encounter-scheduling-1-9a09be849131e6a0618df65cd9a90a02.png) and [performing these scheduled visits](/static/encounter-scheduling-2-5dd0fa14255c3f893ad8284b52f88b60.png). This program now is being designed for scale-up to extend services to all tribals not just to families with pregnant woman - including extending it to other tribal districts in MP.

\*_Apart from these JSS is working with doctors and lab technicians to improve diagnosis, and with state government to improve blood availability required for blood transfusion in SCD. It also includes awareness among patients about their right to treatments via creating of patient support groups._


# File: ./case-studies/calcutta-kids-—-avni-implemented-for-maternal-and-child-health-program.md

---
templateKey: case-study
title: Calcutta Kids — Avni for maternal and child health program
date: 2019-11-06T08:46:23.019Z
description: >-
  Avni replaced an existing custom solution as Calcutta Kids. Avni empowered the
  community health workers in providing the women, maternal and child health
  services for the slum residents.
tags:
  - Health
  - Case Study
---
[Calcutta Kids](https://calcuttakids.org) is a public health organization providing health services to the underserved women and young children in the Kolkata slum area of Fakir Bagan. They provide preventive services, complemented by effective curative care when required. These services are provided primarily by trained Community Health Workers (CHW). Calcutta Kids (CK) provides a whole range of services for women health, pregnancy and child health — which has been very well detailed <a href="https://calcuttakids.org/programs/" target="_blank" rel="noopener noreferrer">here</a>. CK runs a comprehensive program where **continuous service** is provided to their clients.

Until two years back CK was using a data management system (MIS) for the services delivered. This MIS was also used to - generate the schedule of work for CHWs, derive program insights and prepare impact/activity reports.

The MIS in use was a custom solution, i.e. developed specifically for CK. The system required ongoing changes to adapt to the health program. This required CK to arrange for funds to continuously upkeep the system. This was expensive. Apart from this, there was another major issue — the system was not accessible to the CHWs in the field.

![](/img/ck-case-study.png "Health workers servicing child and pregnant women")

- - -

Avni implementation as a replacement of existing MIS was envisioned to empower the CHWs when they were servicing the beneficiaires and CK moving to a platform managed by Samanvay at much lower costs.

Some of the key aspects of this implementation of Avni were:

**Modelling CK programs onto Avni**\
In Avni, one can define multiple programs. Three programs were defined — pregnancy, child and mother. A woman can be moved between mother and pregnancy program depending on whether they were pregnant or not. A child can be enrolled in the child program at birth or if they come newly into Fakir Bagan (program area). The flexible data model offered by Avni allowed for exactly translating the programs as they exist in the real world. (Avni in fact has been designed to achieve this for all field programs).

**App available in the field instead of printouts, registers and forms**\
CHWs at CK, completely did away with the paper forms. This allows for program designers to ensure that each CHW interaction with the beneficiary can be modelled into the app — to standardise service quality. In Avni — the CHW’s interaction with beneficiary is supported via a designed form flow that brings up only the right questions, right counselling topics, displays necessary computed information (e.g. referral advice based on complete data), and highlights data input mistakes.

<br/>

<p align='center'>Counselling guidance for health worker</p>

<img src="/img/screenshot-2019-12-12-at-6.44.01-pm.png" alt="Counselling guidance for health worker" height="432" width="306" align='middle'>

<br/>

<p align='center'>Visit scheduled for health worker</p>

<img src="/img/ck-visit-scheduling.png" alt="Visit scheduled automatically for the health worker" height="432" width="306" align='middle'>

<br/>

**Bringing data from old system into new one**\
Bringing on all the data from older system to a new one can be quite challenging. Such data migration in simple scenarios involves providing data to the new system in the format that it can accept. But for large data sets that has been in use for years, it is difficult to prepare data in the expected format manually, because the data-formats of the new system is quite different from the old system. Avni uses a unique approach that makes it possible to map two complex data formats in an excel file - instead of transforming the input format.

**Generic product like Avni over a custom solution**\
Avni reduces the software development cost to the minimum, for its customer - because the product, its hosting infrastructure are shared resources. Avni is funded via philanthropy - allowing funders to contribute a product to the ecosystem. Customers of Avni paying only for implementation of their own configurations.

- - -

**Credits for icons**
icon made by — www.flaticon.com/authors/freepik and www.flaticon.com/authors/monkik — from www.flaticon.com


# File: ./case-studies/classroom-observation-tool-for-andhra-pradesh.md

---
templateKey: case-study
title: Case Study - Classroom Observation Tool for Andhra Pradesh
date: 2024-05-13T07:24:00.000Z
description: >-
  
author: Vinay Venu
tags:
  - Education
  - Government
  - Case Study
---

![](/img/classroom-observation-tool-for-andhra-pradesh/classroom.jpg)


### Introduction
The [Teach](https://www.worldbank.org/en/topic/education/brief/teach-related-blogs) tool, developed by the World Bank, serves as an observation tool aimed at measuring the quality of teaching practices. It is a key component of the [Supporting Andhra's Learning Transformation (SALT) program](https://schooledu.ap.gov.in/samagrashiksha/?page_id=209). [Leadership for Equity](https://www.leadershipforequity.org) is the technical partner in the project in charge of observing teachers and implementing need-based learning courses for teachers (among other things). 

The project involved usage of the Teach tool among around 10,000 observers, each of whom will observe around 15 teachers once in two months. Observations happen in a classroom setting where they are scored on multiple criteria. There are a total of around 250 questions around classroom culture, instruction effectiveness and socioemotional skills. The project covers all government schools in Andhra Pradesh. Below are a few images of how the Teach tool was implemented in Avni. 

![](/img/classroom-observation-tool-for-andhra-pradesh/app_images.png)


The implementation of the Teach AP program marked several significant milestones for Avni. Notably, it necessitated the development of a whitelabeled app tailored specifically for classroom observations in Andhra Pradesh, accompanied by dedicated infrastructure and rigorous third-party security testing. Furthermore, transitioning the app to government infrastructure posed additional challenges, requiring careful consideration and strategic adaptations.


### Building Trust

Ensuring trust and reliability in the Teach AP app was paramount, particularly given its distribution to a wide user base through the PlayStore. To instill confidence among users, meticulous attention was paid to the app's name, description, and logo, aligning them closely with the program's objectives. Leveraging Avni's capability to swiftly create [whitelabeled apps](https://avni.readme.io/docs/flavouring-avni) helped, resulting in an app listing that resonated with its intended purpose of classroom observations.

![](/img/classroom-observation-tool-for-andhra-pradesh/whitelabeled_avni_apps.jpeg "Different flavors of Avni")

### Knowledge and Training

Central to the success of the Teach AP program was the rigorous training and assessment of observers. By standardizing benchmarks and providing comprehensive training material, Avni facilitated uniformity in evaluation criteria and equipped observers with the necessary resources to carry out their tasks effectively. The [Documentation feature](https://avni.readme.io/docs/documentation) in Avni proved invaluable, offering quick access to training materials and reference guides, ensuring consistency and competence among observers.


### Operational Support

To run a program of this size requires several pieces to come together. Technology can help in some of them.

- Regular reports provide information to people running the program on both the regularity of the program as well as the quality of data coming in. This helps them make any necessary corrections at the right time.

![](/img/classroom-observation-tool-for-andhra-pradesh/reports.png)

- [Offline reports and custom dashboards](https://avni.readme.io/docs/offline-reports) on the Android app allow observers to understand their own work and ensure they are performing observations at the right time.

![](/img/classroom-observation-tool-for-andhra-pradesh/offline_dashboard.png)

- Bulk uploads of observers and teachers help quickly add data into the system to scale up as needed. Administrators of the system use the csv upload functionality to add new observers and teachers. 

- Support channels are required to assist users in case of any trouble on the ground. Avni can help in two different ways. First, the Application Menu allows addition of [custom links](https://avni.readme.io/docs/application-menu). This has been used in many implementations to connect to a Google Form or a Whatsapp channel where support can be provided. In another implementation, users are automatically added to a Whatsapp chatbot through Glific. This provides some support for regular questions and allows administrators to contact them when human support is required.


### Government Handover

Handing over to the government requires the ability to deploy Avni in a data center that is not AWS. This means we need to move out of all infrastructure that is dependent on AWS. There are two components of Avni that are being used in the Avni SaaS cloud - Cognito (for identity management) and S3 (for media/documents).

Cognito can be swapped with [Keycloak](https://www.keycloak.org/), a popular open source identify management system. Avni supports both out of the box. Similarly, there is a drop-in replacement for S3 - [Minio](https://min.io/).

Additionally, since a government deployment will be for a specific use case, features of Avni that are not used for this use case needed to be disabled.

After swapping out the different systems, a security audit was performed before handing over the system. 

### Future Outlook

The Teach implementation for AP and subsequent deployment at a govermnent data center has helped unearth and solve problems that show up only at this scale and complexity. Many enhancements in the product would not have been possible without this implementation. While many of the existing features proved invaluable to quickly start running observations, the new features that were built because of this implementation left Avni a much more mature product from where it started. This is a testament to the power of open source technology and its ability to use existing technology for a quick start, building over it to solve a unique problem and enriching the entire ecosystem in the process. 

Other state governments have expressed interest in implementing similar programs. At the time of this writing, Nagaland has completed a pilot and is on its way to a complete rollout. We hope the work done in Andhra Pradesh will benefit many others in the days to come.


# File: ./case-studies/dam-and-water-bodies-desilting-work-monitoring-1.md

---
templateKey: case-study
title: Dam and water bodies desilting work monitoring
date: 2020-02-20T07:24:00.000Z
description: >-
  Sedimentation is a problem faced by dams and water catchments, whereby the
  flowing sediments settle to the bottom of the dam because of stoppage of water
  flow. This impacts the dams negatively. On the other hand, the silt present in
  these sediments, are quite useful to improve the fertility of the farmland.
  This presents an opportunity for creating a win-win situation. Avni was used
  as data collection and project activity monitoring tool.
tags:
  - Water
  - Government
  - Case Study
---
Sedimentation is a problem faced by dams and water catchments, whereby the flowing sediments settle to the bottom of the dam because of stoppage of water flow. This impacts the dams negatively. On the other hand, the silt present in these sediments, are quite useful to improve the fertility of the farmland. This presents an opportunity for creating a win-win situation.

Maharashtra state has thousands of small to large dams. Maharashtra government initiated the implementation of <a href="https://www.thehindubusinessline.com/news/national/maharashtra-to-desilt-dams-water-bodies/article9691614.ece" target="_blank" rel="noopener noreferrer">its policy decision on desilting of dams and water bodies</a>. This implementation is happening in partnership with the NGOs. The idea was that farmers will bring their tractors and collect the free silt extracted.

Given the large distributed scale of the activity, monitoring of work is difficult without technology. In order to monitor the process and progress of the desilting and distribution of silt - the project a field-based data collection and a monitoring system was conceptualised. Avni because of its flexible data model and robust offline support, was chosen as the tool for collecting data from across the state from the site of work.

The data collection involved registering each dam/water-body and then collecting various types of information like - baseline status, work details of vehicle's (JCBs) used, fuel consumed, issues faced, the beneficiary details and end-line. This data is collected in the field during the complete process of desilting and distribution of silt. The collected data allowed for monitoring, spotting gaps in reporting, and anomalies in data. The monitoring team could contact the ground team to understand the reasons.

`youtube: uwwyzrOHOwI`

<p align="center"><b>Dashboard for the monitoring team</b></p>

``

`youtube: tqR226jt8Oo`

<p align="center"><b>Demo of the field app</b></p>

- - -

**Using Avni field app from the field**

Apart from the common data collection facilities, there are certain specific features of Avni that helped in the monitoring of the groundwork. The user was expected to provide their location when they are filling the data to ensure that they were at the site of work. Also, the users could record a video or take photos of the desilting work. Avni makes is possible to do all of these along with regular data collection work completely offline. Internet connectivity is only required when one wants to submit the data.

**Flexible user-defined data model**

Unlike most other implementations of Avni, the subject of data collected was not a human being (i.e. beneficiary, child, mother, patient etc), rather it is a non-living object - a dam. Avni supports such use cases in the same way. It is important to mention here, that Avni considers everything as subject and supports multiple of them - within the same implementation. For example - Avni can support a village health program that requires managing data of villagers (beneficiaries), self-help groups and water wells.


# File: ./case-studies/mahapeconet-use-of-avni-in-covid-relief.md

---
templateKey: case-study
title: "Maha PECOnet - Use of Avni in Covid relief"
date: 2021-12-06T17:00:00.00Z
description: >-
  Avni is used as a survey tool, and then as an MIS to keep tabs of Covid relief 
  activities.
featuredstudy: false
author: Vinay Venu
tags:
  - Survey
  - Case Study
---

_In 3 words , Avni MIS has been versatile , impactful and qualitative._ - **Shilpa Mirashi Director, Indian Institute of Youth Welfare Nagpur**

Summary
-------
Maha PECOnet is a UNICEF Mumbai-facilitated network of volunteers, corporates, government bodies, and over 75+ civil society organizations formed to streamline the efforts and services offered by them amid lockdown and unlock frenzy. Its members have been working to provide many services for COVID relief including emergency relief, vaccine awareness and assistance. Relief and awareness activities reach more than 5 million people in Maharashtra. While UNICEF was funding activities, RISE Infinity and YUVA were coordinating with NGOs in different districts. See their <a href="https://mahac19peconet.org" target="_blank" rel="noopener noreferrer">website</a> for more details. 

Avni is used for Maha PECOnet as an overall MIS for the programme. While individual NGOs maintain their own data for their operations, it was hard to get a summary of the entire programme without significant effort. Avni filled this gap by providing coded forms to fill in data. All data collected would then be collated and displayed in a public dashboard. 


Phases
-------
Avni for Maha PECOnet was implemented in two distinct phases. 
In the first phase, Avni was a survey collection system. Users surveyed different areas of Maharashtra to identify current levels of covid awareness, opinions on vaccination and WASH practices. This would then be used to determine the right kind of intervention. 

Based on the surveys conducted, the right kind of intervention was introduced to each area. Interventions include awareness campaigns (mics, pamphlets, online awareness activities etc), relief supplies (ration, medical equipment, masks etc), training and WASH activities (tap installation, soap distribution etc). Recording the activities performed and developing the dashboard was part of the second phase. 


Special needs
-------------
Being a combination of multiple organisations, Maha PECOnet requires coordination across multiple organisations. This means seamless data flow both from individual organisations to the coordination centre, and easy dissemination of data from the coordination centre to each organisation. It was also important to ensure data quality. To achieve this, we had to
1. Ensure data collected by field workers are validated/approved. The approval feature of Avni was used here. 
2. A public dashboard was used to ensure basic data is available for all (both participating organisations and the general public)
3. Access controls were implemented so that users are able to do only activities that they are responsible for. This greatly streamlines the user interface of each user. For example, a person handling a VHHD can only enter data for VHHD days conducted. 


The final app
-------------
**Home Screen**
![](/img/covid-mis-case-study/home.png)

**Dashboards**
![](/img/covid-mis-case-study/dashboard-1.png)

![](/img/covid-mis-case-study/dashboard-2.png)


**Showcase video**

`video: https://www.youtube.com/watch?v=emaGhtJfpuA`

New features
------------
Being an open-source project, features usually get into Avni either through grants, or projects that have new requirements. 
Maha PECOnet project funded the introduction of the Home Screen feature in Avni. The Home Screen feature is a mechanism through which you can add a custom splash screen to the Avni field app. This can be written in html, and uploaded through the App Designer. 
See documentation ![here](https://avni.readme.io/docs/extension-points)

**Splash Screen for Maha PECO net**
![](/img/covid-mis-case-study/splash.png)



Testimonial
------------
![](/img/covid-mis-case-study/shilpa_mirashi.jpg)**Shilpa Mirashi
Director, Indian Institute of Youth Welfare
Nagpur**


_The MIS and dashboard of Co-MARG MAHA peconet programme was successfully launched and was effective in data compilation, collation and final outcomes.( Nagpur rural). IIYW has used the Avni App and MIS after a focused training from project holders and IIYW found the Avni MIS very user friendly and qualitative.
IIYW could use MIS daily and the team who handled the trainings were most skilled and extremely supportive. The MIS and dashboard brought more professionalism in handling the data and mainly to reproduce its impacts.
The Avni MIS truly helped IIYW in quick compilations, approvals of data collected from remote villages and its outcomes. MIS and dashboard, in true sense, is a most efficient platform and is educative too.
The **RISE Infinity Foundation** and **YUVA** has accelerated the Co-MARG project through Avni App and MIS and  it has helped everyone create wide visibility of work._

_Working with Avni MIS is so encouraging for volunteers too and it’s effective format captures all work details.
In 3 words , Avni MIS has been **versatile , impactful and qualitative.**
Thank you._


# File: ./case-studies/use-of-avni-in-jnpct-malnutrition-project-case-study.md

---
templateKey: case-study
title: Case Study - Use of Mobile Technology (Avni App) in Malnutrition Project at JNPCT
date: 2021-02-08T07:24:00.000Z
description: >-
  
author: Dr Dhiren Modi
tags:
  - Health
  - Case Study
---
If you prefer watching over reading, do check out the [Avni webinar of January](https://youtu.be/4_nZ8Q4RKYA?t=833) where we shared this case study. Otherwise read on.


### About the organisation
Jashoda Narottam Public Charity Trust ( JNPCT) is a non-profit organization working in the two tribal blocks of Valsad District (Gujarat) since the last 20 years. JNPCT mainly undertakes activities in the following areas: Health, Education, Soil and Water Conservation and income generation activity with farmers. 

![](/img/jnpct_case_study/jnpct_scenic_surrounding.jpg "")
![](/img/jnpct_case_study/jnpct_cutoff_monsoon.jpg "")

Geographically the area in which JNPCT works is hilly and a few parts get isolated from the rest of the land during monsoon season.

The area is also called Cherrapunji of Gujarat!

### About the Malnutrition Project
The project this case study focuses on is called 'The malnutrition project'. It's objective is to provide safe and healthy motherhood, reduce the percentage of malnutrition among the children with 0-5 years of age and to minimize the Maternal mortality rate and Infant mortality rate. The various activities done under the project are
 
Antenatal care
- Early registration.
- Facilitate for hospital checkup.
- 4 antenatal home visits.
- Tracking and identification of high-risk pregnancy.
- Counselling about Iron tablet, immunization, nutrition.
- Promote hospital delivery.
- Preparation for delivery (make clothes ready, documentation, money, vehicle, blood  etc.)


Postnatal care
- Early home visit of newborn and mother as per protocol ie. (0, 3, 7, 14, 21, 28, 35, 42, 60 days).
- Examination of the newborn as per Integrated Management of Neonatal and Childhood Illness (IMNCI) guideline, morbidity identification and management.
- Counselling about newborn care and high-risk symptoms.
- If a child is low birth weight then provide a Kangaroo Mother Care (KMC) bag and demonstrate.
- Focus on exclusive breastfeeding and its scientific method for up to 6 months.
- Ensure Immunization as per age.

Child Care
- Visits of the child as per their nutritional status
- Examination of children as per IMNCI guideline, morbidity identification and management.
- Counselling about high-risk symptoms to family members.
- Counselling about weaning food practices.
- Growth monitoring by keeping records of height, weight & MUAC.
- Identification, counselling, management and referral at CMTC centres of SAM children.
- Ensure their nutritional status and immunization within time.

The work is conducted in 62 villages by about 361 workers comprising field workers, supervisors, cluster in-charges and other supportive roles. 


![](/img/jnpct_case_study/jnpct_project_achievement.jpg "Achievements of the project")

### Paper-based System
Like most organisations, we also started with a paper-based system comprising pre-designed formats for data collection. These were useful to some extent in ensuring consistency in information. 

![](/img/jnpct_case_study/jnpct_paper_format_1.jpg "")
![](/img/jnpct_case_study/jnpct_paper_format_2.jpg "")
![](/img/jnpct_case_study/jnpct_paper_format_3.jpg "")



#### Issues with the system
The data from such individual records were recorded in a concise form into registers by supervisors. However deriving insights from these registers like identifying high risk was a very tedious exercise. 

![](/img/jnpct_case_study/jnpct_tracking_hrp.jpg "Tracking high risk pregnancy in paper registers")

Apart from this, there were many other issues faced.
- In our work daily planning of field visit of supervisors was an issue 
- Took almost 2-3 days in a month to plan an exact visit as per malnutrition status of children
- Compilation of daily data was cumbersome and time-consuming
- For program manager and doctors, it was time-consuming to identify their monitoring visits
- We could see the progress report only after a month once data entered and the report generated manually

### Moving to digital system

The next logical step was to move to a digital system to address these pain points. We decided to move to Avni. 

#### Why we adopted Avni App in JNPCT 
We adopted Avni and cloud hosting from [Samanvay Foundation](http://samanvayfoundation.org/) because of the following reasons

- [SEWA Rural](https://sewarural.org/), our partner organisation, had used it for the last 4 years
- Offline capability in Android app to be able to work without an internet connection
- Ability to create customised App and Reports
- Cost-effective
- During the trial, our staff found it very useful
- Good feedback mechanism and prompt resolution on technical issues from the Samanvay support team
- Ready to update the application as per our demand even after stabilizing it

#### Development and Output
Samanvay developed the app and reports for us as per our requirements. We did testing of the app, provided feedback and changes got incorporated. We then started using the system.
 
Below are some of the screenshots from the app

![](/img/jnpct_case_study/jnpct_app_screenshot_1.png "App Screenshots 1")

![](/img/jnpct_case_study/jnpct_app_screenshot_2.png "App Screenshots 2")

We have numerous reports created in the system so that we don’t have to do data crunching when information or insights are needed

![](/img/jnpct_case_study/jnpct_reports.png "Reports")


#### Benefits as we are seeing it

Below are the advantages users are seeing as they are using the application

Supervisor level
1. Planning - The app generates the plan as per the protocol so no additional time is required for planning.
2. Easy to get a list of remaining visits and outstanding services, so no beneficiary is deprived of services
3. Saves a lot of paperwork
4. History (details) of each beneficiary is found with one click
5. Diagnosis of illness (risks) is found automatically
6. Risk advice is received through mobile
7. No need to work hard to manually calculate fields like Estimated Date of Delivery (EDD) as per Last Menstrual Period (LMP), Body Mass Index (BMI) for adults and Nutritional status for children as per Weight and Height and Grade of anaemia as per haemoglobin. These are auto-calculated.
8. Every question has to be filled compulsorily due to which the beneficiary is thoroughly investigated

Cluster in-charge level
1. Planning - The app keeps on generating the plan as per the protocol so no additional time is required for planning.
2. Supervisor monitoring - Due, overdue and cancelled visits can be monitored easily
3. Risk alerts are received
4. All PHC data can be found with one click
5. High risk beneficiaries are visited on time

Coordinator level
1. One click reports make complete and latest project information easily accessible
2. Data Quality check is easier - Misinformation can be tracked
3. Data correction - Changing the information of any beneficiary through the web app can be done easily 
4. Based on data, easier to identify where to focus on the project
5. Know the task of each supervisor/cluster in-charge
6. Location is tracked to know which supervisor was in which village on which day

Thus, we are seeing a good return on investment from using a digital system based on Avni in our Malnutrition project.

### About the Author
Dr Dhiren Modi is a Public Health Specialist working with SEWA Rural since last 14 years. He has done MBBS and MD from M.P. Shah Medical College, Jamnagar and recently finished Global Health Fellowship from UCSF Sanfrancisco. He has keen interest in public health, biostatistics, administration and handles several important responsibilites at SEWA Rural. He works as a consultant for JNPCT.



# File: ./faqs/compare-with-commcare.md

**Avni**

**Type**: Open-source field service & data collection platform (formerly OpenCHS).

**License**: AGPL v3.

**Hosting**: Self-host or cloud.

**Offline Support**: Fully offline-first; Android app works without internet, reliable sync when back online.

**Customization**: High flexibility for workflows across health, water, education, sanitation, and other sectors.

**Features**: Form designer, case management, dashboards, work diaries.

**Community**: Smaller, focused community.

**Evidence/Reach**: ~30 projects, 21,000 users, 3.2M beneficiaries (as of 2023).

**Best For**: NGOs and governments needing custom, self-managed solutions across multiple sectors.

**CommCare** (by Dimagi)

**Type**: Open-source mobile platform for data collection, case management, and decision support.

**License**: CommCare Mobile (Apache 2.0), CommCareHQ (BSD).

**Hosting**: Primarily cloud (self-hosting possible but complex).

**Offline Support**: Offline data collection with sync when internet is available.

**Customization**: No-code app builder with multimedia (images, audio, video), GPS, SMS.

**Features**: Case management, workflows, decision support, behavior-change communication.

**Community**: Large, globally active ecosystem.

**Evidence/Reach**: Used in 130+ countries, 3,000+ projects, hundreds of millions of users. Validated through RCTs and published studies.

**Best For**: Organizations wanting a proven, globally recognized platform with robust case management and large support network.

| Feature              | Avni                                              | CommCare                                              |
| -------------------- | ------------------------------------------------- | ----------------------------------------------------- |
| License              | AGPL v3                                           | Apache 2.0 / BSD                                      |
| Hosting              | Cloud or self-host (easy)                         | Cloud preferred, self-hosting harder                  |
| Offline Support      | Offline-first, reliable sync                      | Offline data collection, sync on reconnect            |
| Workflow Flexibility | Highly customizable, sector-agnostic              | Strong case management, health-focused but extensible |
| Features             | Forms, enrolments, rules, dashboards, diaries     | Forms, cases, multimedia, GPS, SMS, decision support  |
| Evidence Base        | Regional implementations, growing adoption        | Extensive global use, validated in RCTs               |
| Community            | Smaller, focused                                  | Large, global                                         |
| Use Cases            | NGOs & govts across health, education, sanitation | Primarily global health, also education, agriculture  |


# File: ./faqs/compare-with-excel.md

# Avni vs. Excel for Field Data Collection

| Feature                | Avni                                                                                 | Excel / Google Sheets                                                           |
|-------------------------|--------------------------------------------------------------------------------------|---------------------------------------------------------------------------------|
| **Purpose**            | Purpose-built field data collection & case management tool                           | General-purpose spreadsheet for tabular data entry                              |
| **Offline Support**    | Offline-first Android app; syncs automatically when internet available                | Limited offline support; depends on local file or Google Sheets offline mode    |
| **Ease of Use in Field** | Mobile-friendly, guided forms, validations, skip logic, multilingual support         | Not optimized for fieldwork; manual entry prone to errors                      |
| **Data Validation**    | In-app rules, constraints, dropdowns, required fields, cross-form logic               | Basic validations (data types, dropdowns), but weak enforcement                 |
| **Workflow Management** | Tracks beneficiaries, follow-ups, program enrolments, scheduling, case management     | No workflow support; manual tracking required                                   |
| **Collaboration**      | Multiple field users, centralized server sync, role-based access                      | Possible via shared spreadsheets, but version conflicts & access issues common  |
| **Reporting**          | Dashboards, indicators, monitoring built-in                                           | Pivot tables, charts, formulas (requires manual setup)                         |
| **Scalability**        | Handles large-scale projects with many users and millions of records                  | Struggles with large datasets; performance issues as rows/columns increase      |
| **Security**           | Role-based access, audit logs, encrypted data                                         | Basic file protection; limited audit trails                                    |
| **Best For**           | NGOs & programs needing structured, reliable, field-ready data collection             | Small-scale projects or teams needing quick, ad-hoc tabular data entry          |


# File: ./faqs/compare-with-kobo.md

# Avni vs. KoboToolbox (KoBo)

| Feature                | Avni                                                                                   | KoboToolbox (KoBo)                                                           |
|-------------------------|----------------------------------------------------------------------------------------|-------------------------------------------------------------------------------|
| **Purpose**            | Open-source field service & case management platform (multi-sector)                    | Open-source survey/data collection tool focused on humanitarian/emergency use |
| **License**            | AGPL v3                                                                                | GPL v3                                                                        |
| **Hosting**            | Self-host or managed cloud                                                             | Free public server (hosted by Harvard/UN), self-hosting also possible         |
| **Offline Support**    | Offline-first Android app with reliable sync                                           | Offline data collection on Android; syncs when internet available             |
| **Ease of Use in Field** | Mobile-friendly, supports workflows, follow-ups, multilingual                         | Mobile forms for one-time surveys; simple and lightweight                     |
| **Data Validation**    | Strong: skip logic, rules, constraints, required fields, cross-form logic              | Supports skip logic and constraints, but limited for longitudinal tracking    |
| **Workflow Management** | Full case management: enrolments, follow-ups, visit scheduling, program tracking       | No case management; survey-based only                                         |
| **Collaboration**      | Role-based access, multiple field users, centralized sync                              | Data sharing via accounts or CSV export; simpler collaboration                |
| **Reporting**          | Built-in dashboards, indicators, monitoring tools                                      | Basic charts, maps, and exports; advanced analysis requires external tools    |
| **Scalability**        | Used in multi-year projects with millions of records and large teams                   | Best for small/medium surveys; struggles with long-term, large-scale programs |
| **Community**          | Smaller but focused community (health, development, governance)                        | Large humanitarian and academic user base                                     |
| **Best For**           | NGOs/governments needing structured, long-term program data & workflows                | Quick, survey-based data collection in humanitarian or research contexts      |


# File: ./faqs/compare-with-odk.md

How does Avni compare with other tools?

# File: ./faqs/compare-with-surveycto.md

# Avni vs. SurveyCTO

| Feature                | Avni                                                                                  | SurveyCTO                                                                       |
|------------------------|----------------------------------------------------------------------------------------|----------------------------------------------------------------------------------|
| **Purpose**            | Open-source offline-first platform for field service and case management across sectors | Secure, enterprise-grade platform for complex survey workflows and data quality |
| **License**            | AGPL v3                                                                                 | Proprietary subscription-based                                                    |
| **Hosting**            | Self-host or cloud                                                                      | Managed cloud with high reliability                                               |
| **Offline Support**    | Fully offline-first mobile app with reliable sync                                       | Advanced offline capabilities: dataset publishing, offline case transfers         |
| **Workflow Flexibility** | Custom workflows with case management, enrollments, visit schedules                  | Drag-and-drop workflows with dataset linking and offline dataset publishing       |
| **Data Validation**    | In-app rules, validations, skip logic                                                   | Built-in quality checks, outlier detection, logic, and testing tools              |
| **Collaboration**      | Multi-user support with role-based access and syncing                                   | Secure, multi-user environment with role permissions, SSO, and encryption         |
| **Reporting & Monitoring** | Dashboards and monitoring tools built-in                                           | Data Explorer, API integrations, and real-time visualizations                     |
| **Security**           | Open-source security depending on deployment                                           | Enterprise-grade: encryption, GDPR, SOC 2, SSO, dedicated hosting                 |
| **Community & Support**| Smaller, project-focused community                                                      | Large professional support with extensive documentation and 24×7 support           |
| **Best For**           | NGOs/Governments needing self-managed, customizable field data workflows                | Organizations needing highly secure, enterprise-grade survey solutions            |


# File: ./faqs/how-can-i-get-access-to-metabase.md



# File: ./faqs/how-can-i-get-access-to-superset.md



# File: ./faqs/how-do-i-get-data-out.md



# File: ./prompts.md


51. How do I use rules to calculate household totals?  
52. Can I access previous encounter data in a rule?  
53. How do I check if a field value has changed in a rule?  
54. How do I create a rule that prevents duplicate registration?  
55. How can I trigger a follow-up form automatically?  
56. Can I write a rule to calculate gestational age?  
57. How do I enforce minimum and maximum age limits?  
58. How do I use rules for referral workflows?  
59. How do I debug a failing rule in Avni?  
60. Can I export all my rules for review?  
61. How do I sync my data when internet is slow?  
62. Can I use Avni offline for a whole week?  
63. How do I change the app language?  
64. How do I search for a subject in the field app?  
65. Can I update a subject’s information after registration?  
66. How do I record a missed visit?  
67. What happens if I accidentally delete a record?  
68. How do I know if my data is synced?  
69. Can I see my past encounters for a subject?  
70. How do I mark a subject as inactive?  
71. How do I transfer a subject to another worker?  
72. Can I edit a submitted form?  
73. How do I log out and log back in without losing data?  
74. How do I capture GPS when offline?  
75. What should I do if the app crashes?  
76. How do I handle duplicate subjects in the app?  
77. How do I record multiple services in a single visit?  
78. Can I use Avni on multiple devices?  
79. How do I install Avni updates?  
80. What should I check before starting field data collection?  
81. How do I export data from Avni to Excel?  
82. Can I schedule automatic data exports?  
83. How do I connect Avni to DHIS2?  
84. How do I use Avni APIs to fetch subject data?  
85. Can I integrate Avni with Power BI?  
86. How do I authenticate with Avni APIs?  
87. What’s the API endpoint for encounters?  
88. Can I import subjects from an external database?  
89. How do I set up data backups?  
90. Can I generate PDF reports from Avni?  
91. How do I get aggregated data by location?  
92. Can I query Avni directly with SQL?  
93. How do I filter data exports by date?  
94. Can Avni sync with ODK or Kobo data?  
95. How do I schedule custom reports?  
96. How do I connect Avni to a local dashboard?  
97. What is the structure of Avni’s database?  
98. How do I migrate data from another system into Avni?  
99. Can I integrate Avni with SMS or WhatsApp alerts?  
100. How do I monitor API usage and limits?  
101. How do I create a dropdown field with predefined options?  
102. Can I configure cascading dropdowns (state → district → village)?  
103. How do I copy a question from one form to another?  
104. Can I hide a field from data collectors but keep it for admins?  
105. How do I configure default language for a form?  
106. Can I restrict date fields to future dates only?  
107. How do I enable GPS capture in registration forms?  
108. Can I create a calculated field based on two numeric inputs?  
109. How do I make a field appear only during subject registration?  
110. How can I reorder questions in a form?  
111. Can I create a checkbox list where multiple options are allowed?  
112. How do I configure a lookup field from another form?  
113. Can I make a field read-only after first entry?  
114. How do I enforce that one field must be filled if another is empty?  
115. Can I configure a field to store multiple phone numbers?  
116. How do I configure a program with optional encounters?  
117. Can I use QR codes for subject IDs in Avni?  
118. How do I configure automatic case closure after 6 months?  
119. Can I configure a form to appear only once per program stage?  
120. How do I make a yes/no field mandatory?  
121. Can I pre-fill subject information from previous visits?  
122. How do I add an image upload field?  
123. Can I create dynamic labels based on other field values?  
124. How do I enable conditional skip logic across sections?  
125. Can I configure reminders for upcoming encounters?  
126. How do I configure a repeatable group of fields?  
127. Can I set a numeric field to allow decimals only?  
128. How do I configure a program where only supervisors can enroll subjects?  
129. Can I create a read-only dashboard for workers in Avni?  
130. How do I configure a field that stores household GPS plus notes?  
131. Can I configure gender-specific forms in Avni?  
132. How do I set default answers for checkboxes?  
133. How do I configure case assignment based on location?  
134. How do I model a program for chronic disease management?  
135. Can I design workflows for both subjects and facilities?  
136. How do I create a workflow for nutrition tracking?  
137. Can I model relationships like teacher → student → guardian?  
138. How do I configure parallel workflows in the same program?  
139. Can I assign a subject to multiple programs at once?  
140. How do I create a workflow for tracking immunizations?  
141. Can I design a program that ends after a specific milestone?  
142. How do I model referrals between organizations using Avni?  
143. Can I track household-level interventions as well as individuals?  
144. How do I configure seasonal visits (e.g., annual surveys)?  
145. Can I link subjects across different user groups?  
146. How do I model temporary migration of subjects?  
147. How do I configure encounter frequency based on subject category?  
148. Can I track dropout cases and reasons?  
149. How do I create workflows with flexible timelines?  
150. Can I design workflows that include supervisor approvals?  
151. How do I configure different visit schedules for children and adults?  
152. How can I model data for disaster relief beneficiaries?  
153. Can I set up workflows that branch based on eligibility?  
154. How do I manage subjects who belong to multiple households?  
155. Can I configure Avni to track both individuals and groups?  
156. How do I model a workflow for financial inclusion programs?  
157. Can I create a single program with multiple enrollment points?  
158. How do I manage subjects who transfer between facilities?  
159. Can I model a workflow where only some encounters are mandatory?  
160. How do I configure workflows for counseling services?  
161. Can I design a workflow where subjects graduate after training?  
162. How do I configure Avni for randomized trial workflows?  
163. Can I link program outcomes to subject closure rules?  
164. How do I configure workflows for child growth monitoring?  
165. Can I model a workflow where visits reduce over time?  
166. How do I track group sessions along with individual sessions?  
167. How do I check if my app has the latest forms?  
168. Can I work in two different programs at the same time?  
169. How do I find all subjects assigned to me?  
170. Can I register a new subject without network?  
171. How do I sync partially completed forms?  
172. What happens if two users register the same subject?  
173. How do I mark a subject as deceased?  
174. Can I view my assigned workload for the week?  
175. How do I reset my password in the field app?  
176. How do I identify subjects with overdue visits?  
177. Can I use voice input to fill forms in Avni?  
178. How do I update subject address information?  
179. Can I work offline for multiple programs simultaneously?  
180. How do I capture signatures in the Avni app?  
181. Can I search for subjects by multiple fields (name + phone)?  
182. How do I report an error from the field app?  
183. Can I update my app without losing offline data?  
184. How do I check which data has not yet synced?  
185. Can I pause form filling and return later?  
186. How do I use Avni with multiple languages at once?  
187. Can I hide sensitive information from field workers?  
188. How do I ensure GPS accuracy during data collection?  
189. Can I undo the last change in a filled form?  
190. How do I record multiple household members in one visit?  
191. Can I merge duplicate subjects from the app?  
192. How do I verify that sync was successful?  
193. Can I see upcoming visits in a calendar view?  
194. How do I log service delivery outside of scheduled visits?  
195. Can I use Avni on low-end Android phones?  
196. How do I check available storage before syncing?  
197. Can I filter my subject list by program status?  
198. How do I troubleshoot when sync fails?  
199. Can I capture both structured data and free text notes?  
200. How do I train new workers quickly to use Avni?  


