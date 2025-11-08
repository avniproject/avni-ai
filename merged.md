

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

# File: ./readme/End User Guide/data-entry-app.md

title: Data Entry App
excerpt: ''
The Data Entry App, as the name suggests, is used to view and enter data directly without relying on mobile syncing. It can be accessed by clicking on the 'Data Entry app' tile in the home page.

<Image align="center" width="10000px" src="https://files.readme.io/be9c75e10c6f8e1eb905f84e0714b46475192e039bac88837f38b62c87cabf91-Screenshot_2025-08-25_at_7.10.40_PM.png" />

### Advantages:

* **Instant access**: When you are on a computer with internet access, you can view and enter data without downloading or syncing data like in the mobile app.
* **Larger data coverage**: On the mobile app, the maximum number of catchment locations that can be synced is 65,535. If you need to view data across more locations, the Data Entry App can be used.

### Features not supported in Data Entry App:

**Rules related limitations:**

* [Edit form rule](https://avni.readme.io/docs/writing-rules#17-edit-form-rule)
* [Member addition eligibility check rule](https://avni.readme.io/docs/writing-rules#16-member-addition-eligibility-check-rule)
* [Manual programs eligibility check rule](https://avni.readme.io/docs/writing-rules#15-manual-programs-eligibility-check-rule)
* [Rules that use service methods to filter across subjects](https://avni.readme.io/docs/writing-rules#using-service-methods-in-the-rules)

<br />

**Other unsupported features:**

* [User subject type](https://avni.readme.io/docs/user-subject-types)
* [Dashboards and report cards](https://avni.readme.io/docs/offline-reports)
* [Drafts](https://avni.readme.io/docs/draft-save)
* [Approval workflows](https://avni.readme.io/docs/approval-workflow)
* [Vaccination checklist](https://avni.readme.io/docs/upload-checklist)
* [Growth chart](https://avni.readme.io/docs/child-growth-charts)
* Details on who performed a registration, enrolment or visit
* Viewing of data outside of a user's catchment and configured sync attribute cannot be restricted. Only editing can be restricted.


# File: ./readme/End User Guide/how-to-guide-setting-up-locations-via-csv-upload.md

title: 'How to guide: Setting up Locations via CSV Upload'
excerpt: For bulk location upload after Release 10.0
## Definitions

Below is a list of definitions that are essential for understanding this document.

* **Locations:** These can be names of Villages, Schools or Dams, or other such  places which correspond to Geographical locations in the real world.  
* **Location Types:** As its name suggests, Location Types are used to classify Locations into different categories. Ex: Karnataka and Maharashtra are 2 locations that could be classified into a single Location Type called “State”. Additional caveats related to the Location Type are as follows:  
  * You may associate a “Parent” Location Type for it, which would be instrumental in coming up with Location Type Hierarchy  
  * Each location type also has an additional field called “Level” associated with it. This is a Floating point number used to indicate relative position of a Location type in-comparison to others.   
  * There can be more than one location type with the same “Level” value in an organisation.  
  * The value for “Level” should less than the “Parent” Location Type’s “Level” field value  
* **Location Type Hierarchy:** Location types using the “Parent” field can construct a hierarchy of sorts. Ex:  State(3) \-\> District(2) \-\> City(1)\
  A single organisation can have **any** number of Location Type Hierarchies within it. Note that the example is a single hierarchy.  
* **Lineage:** Location Type hierarchy, are in-turn used to come up with Location lineage. Ex: Given a “Location Type Hierarchy” of State(3) \-\> District(2) \-\> City(1) being present, we could correspondingly create Location “Lineage” of the kind “Karnataka, Hassan, Girinagara”, where-in “Karnataka” corresponds to “State” Location-type, “Hassan” to “District” and “Girinagara” to “City”.

## Overview

In Avni, Locations refer to geographical entities which could be a State, Village, Schools, Hospital, etc.. where an organisation provides services. It plays an important role in identifying the “Where” aspect of the data being captured / service that was provided. Locations are also used to group together Avni entities (Subjects, Encounters, GroupSubjects) based on their Geographical proximity, using the Catchments. This simplifies the assignment of Avni entities in the Geographical area of influence of a Field-Worker to him/her as a single composite entity rather than individually allocating each entity to the User.

Avni **“Upload\- Locations”** functionality, allows Avni Admin Users to perform following actions in **bulk**

* Create new locations   
* Update name, GPS coordinates and other properties for existing locations  
* Modify the parent location for an existing location and there-after reflect the change in lineage for it and all its children

This is achieved by means of uploading a CSV(Comma-separated Values) file of a specific format. Please read through the rest of the document to learn more about initializing Location Types and setting up large amounts of Locations for each of those types for specific Location Type Hierarchy.

## Steps to create Location Types Hierarchy

### Navigation to the Bulk Uploads screen

* Login to Avni Web Console 

![](https://files.readme.io/35932d9141d5744753f1730b6b5a4aa04a4b755a9fd18c25586ca98b58639177-image.png)

* Go to **Admin** app

![](https://files.readme.io/b51402bda3d8cf3a6aefd515b8e19cecc2c0200c5c557ae973cb38d3fa4e172e-image.png)

* Click on the **“Location Types”** section

![](https://files.readme.io/b846e3e44e146727fc20ad58b6c881cb8d2a96ac3dcdac90ae90f84b1fc81d2f-image.png)

### Create Location Types Hierarchy

When we start with creation of Location types, we do so from the highest Location type to the lowest in descending order of its level within the Location Hierarchy.

For example, to set up a Location Hierarchy of State(3) \-\> District(2) \-\> City(1), you would repeat the below process 3 times, first for “State”, then “District” and finally for “City”.

#### Create Location Type

1. Click on “CREATE” button on the top right corner, in “Location Types” screen  
2. Initialize “Name” field, to an appropriate String value starting with Upper-case Alphabet  
3. Initialize the “Level” field to appropriate Numeric value, which would be lower than its “Parent” Location Type’s “Level” value. Ex: “2.0”, “3”, “4.5”  
4. Associate “Parent” Location Type, as long as this isn’t the Highest Location type in its hierarchy  
5. Save the Location type, by clicking on the “SAVE” button

![](https://files.readme.io/2c1cb4ff350002b55cb86e570dc8f22baf8f5c5a1738bf1575def95eb6a7e1a3-image.png)

#### About Multiple Location Type Hierarchies within a single organization

Avni allows for an organization to have more than one Location hierarchy. The hierarchies could be linked at a specific location type or otherwise.

##### Example for Multiple Hierarchy joined at a common location type

![](https://files.readme.io/785775716ea75efb92621f34ebf17f014cb5f1b5a478a2c4e7d1ffff90e26b2a-image.png)

##### Example for Multiple Hierarchies not linked with each other

![](https://files.readme.io/4c530ae55ff631715c497aef020ef6591e2189c5df01b3bc034a34797acc6bc4-image.png)

### Review Location Types Hierarchy

Do a quick review of the Location Types Hierarchy, to ensure that its created as per requirement.

![](https://files.readme.io/6fccd280624ae8da4252f2bf7b3bb2bdb4950fabd5f7132f2820cc4849d6b628-image.png)

## Steps to create Form of type Locations (Optional)

For your organization, if there is a need to specify additional details as part of each Location, then Avni allows you to configure a “Location” type Form, which can be configured to store those additional details as Observations for each Location. This is an optional feature to be done only if such need arises.

* Navigate to the App Designer app

  ![](https://files.readme.io/45b6cf059a148183cb5597b2e09a93dc6d705c9af4eb09f99df0c9cdbd246050-image.png)
* Click on Forms in the left side tab, to open up the Forms section.  
* Create a new Form of type “Locations” by clicking on the “CREATE” button on the Top-Right corner of the screen.  

  ![](https://files.readme.io/2ad5b18293dfb28f217f3a87bd633dccb766d962a56c68f2c3fdb4b1611e6237-image.png)
* Setup the Locations type Form in the same way as you do for any other Avni Entity Data collection Forms. See below sample screenshot for reference.

  ![](https://files.readme.io/b5c2e8c75e8660ff5eaa3fba63826e1b2898aab32cf942beeec47d8cba11dd19-image.png)

## Steps to create Locations via CSV upload

### Prerequisites

* **Ensure Location Types Hierarchy already exists**\
  In order to start with the locations upload in the Avni app, organisation needs to have Location Types created in the requisite hierarchical order.  
* **Ensure Location Form if needed, has already been configured**\
  If your organisation needs additional properties to be set during Location creation, then ensure that you have configured a form of type “Locations” in the aforementioned manner 

### Navigation to the Bulk Uploads screen

* Login to Avni Web Console

![](https://files.readme.io/93db597e0607f374895d82942c940eca42ff9954f008e28fb2933b459a2bc280-image.png)

* Go to **Admin** app

![](https://files.readme.io/a0bfd4fcaa19d3275985307bdc624b89237c508ee94eb2a9f6a992c0f3d30348-image.png)

* Click on the **“Upload”** section

![](https://files.readme.io/81b9a7ec02dcba7ee588ceb2c4a6a508e9346610ef43e9b29c2c30ba0fb6b8fa-image.png)

### Download sample CSV file

In the Avni “Admin” app, “Upload” section, we provide the users with an option to download a sample file, which would give you a rough example for coming up with the required “Locations” upload CSV file.

The locations upload file format is different for the “Create” and “Edit” modes, therefore choose the appropriate mode and apply the same, when uploading the file later as well.

If your organization has multiple Location hierarchies, then you would have to select the specific location hierarchy for which you need the sample file. This is applicable only for “Create” mode.\
Finally, click on the “Download Sample” button, to get the sample file.

![](https://files.readme.io/31cbacad108b87cdd4a90ad196fbd4b879761676b333fe0cdfbd7baa6814f30c-image.png)

#### Sample Locations upload csv file screenshot

As part of the sample Locations csv file downloaded, you’ll have following information available to you for quick reference:

* All Headers configurable for the selected Mode and Location hierarchy  
* Descriptor row with guidance and examples on what values should be specified for each of the columns

1. **Create** mode

   ![](https://files.readme.io/00dc42970a69fea2eac1a114935cb3b2cbefe588aa540a5147cd51e7bdc930bc-image.png)
2. **Edit** mode

   ![](https://files.readme.io/42250968ba2ed5feec3e8da58e4c0521e1aa8bbe1418530de90a3f61a4eaf71f-image.png)

### Compose Locations upload CSV file

1. ### "Create" Mode

#### Headers Row

The first row of your upload file should contain Location types, arranged in descending order of their Level, in the selected Location Hierarchy from Left to Right, as comma-separated values.\
Refer Sample Locations Upload documents available [here](https://docs.google.com/spreadsheets/d/1R3l_tRUKZ7_WoZa4QIRctecFqJZoB2jdltyKUPMSD0Q/edit?usp=sharing) for Location Hierarchy of: Block(3) \-\> GP(2) \-\> Village/Hamlet(1). This is followed by “GPS Coordinates” and other Location properties name as column names.

![](https://files.readme.io/1a1dff92a0cb11f31704ee8f6d87ac78013ae49e56e8b878dc8657bb96762ece-image.png)

#### Descriptor Row

The second row of your upload file can optionally be a descriptor row, retained as is from the sample location upload file downloaded earlier. Avni would ignore the row, if its starting text matches the Sample file Descriptor row content’s starting text.

#### Data Rows

Entries provided in each of the address-level-type columns would be created as individual locations. (For example, the “Jawhar” block, “Sarsun” GP, and “Dehere” village will be created as a unique location with the appropriate location lineage, as specified during upload.)\
If the Parent locations already exists during a new location creation, then they are not re-created and are just used as is to build the location lineage.

#### GPS Coordinates

In-case, user would like to set the GPS Coordinates for locations during upload, then they would need to additionally specify values in the "GPS coordinates" column. The value for this column should be of the Format “\<Decimal number\>,\<Decimal number\>”.\
Ex: “123.456789,234.567890”, “12.34,45.67”, “13,77”

#### Additional Location Properties

Avni allows an organisation to configure Forms of Type “FormType.Location” for enabling inclusion of additional properties for each Location. These Forms are made up of the same building blocks of Pages and Questions like Forms of other types.

In-order to configure Location properties, you would need to specify the Concept “name” as the Column Header and specify the value for each of the locations in the corresponding columnar position.

![](https://files.readme.io/d779bbd3674a887c54b1f320d9e7cceb881b841f3360697f9d450c0bbf2795d1-image.png)

2. ### “Edit” Mode

This mode is to be used to perform bulk updates to locations. The type of updates allowed are as follows:

* Update name of existing locations  
* Update GPS coordinates and other properties for existing locations  
* Modify the parent location for an existing location and there-after reflect the change in lineage for it and all its children

#### Headers Row

The first row of your upload file, would usually contain following data as columns headers:

1. Location with full hierarchy  
2. New location name  
3. Parent location with full hierarchy  
4. GPS coordinates  
5. Multiple Location Properties name  

Refer Sample Locations Upload documents available [here](https://docs.google.com/spreadsheets/d/1EFpeMuQe-BEGvghUAeQWsLumfJ88B2Iv8w-lVqzQX4c/edit?usp=sharing).

![](https://files.readme.io/9d903fe0c5fe2d9d8fc93622312ef7e23efbc3fd6c2d811ade340d362c37db39-image.png)

#### Data Rows

Entries provided for the columns listed below would be used as specified here:

* Location with full hierarchy (Mandatory): Used to identify the specific location to be modified  
* New location name (Optional):  Used to specify the new title value for a location  
* Parent location with full hierarchy (Optional):  Used to identify the new parent location to move this location to. Ex: Move “Vil B” to “PHC C, Sub C” from “PHC B, Sub B”  
* GPS coordinates (Optional):  Used to update the GPS coordinates. Format:  “\<Double\>,\<Double\>”. Ex: “123.456789,234.567890”  
* Values for multiple Location Properties columns that are part of the Form of type “FormType.Location”. These again are optional.

#### Edit Row validations

1. If the “Location with full hierarchy” does not exist during location updation, then the update operation fails for that row.  
2. Atleast one among the following columns should have a valid value for the updation operation to be performed successfully for that row:  
   * New location name  
   * Parent location with full hierarchy  
   * GPS coordinates  

### Upload the CSV file

Project team then downloads the sheet in the CSV format. Navigate to the “**Upload”** tab of the Admin section, and perform the following steps to upload the file:

* Select the “Type” to be “Locations”   
* Specify the file to be uploaded using the “CHOOSE FILE” option  
* Select the appropriate “Mod&#x65;**”** of CSV Upload  
  * Create: For creating new locations  
  * Edit: For updating existing location’s Name, Parent, GPS coordinates or other properties  
* Choose appropriate “Location Hierarchy” (Applicable only for “Create” mode)  
* Click on the “Upload” button

![](https://files.readme.io/225211b913de07fb56c6a7676b1b6c88a78aecc2c92f97833c646b304b8ce6c4-image.png)

## Monitoring Progress of the Upload

Avni provides users with an easy way to monitor the progress of the CSV file uploads. In the same “Upload” tab of the Admin section, the bottom-half contains a list of all uploads triggered by users of the organization.

![](https://files.readme.io/ac1a32f7738e8035e5ad076005a218693044cfc7f00348d080bdd3a3e50d2d22-image.png)The “Status” column will indicate the overall status of the specific upload activity. With other columns like “Rows/File read” , “Rows/File completed” and “Rows/File skipped” indicating the Granular row-level progress of the file processing.

The final “Failure” column, will consist of Hyperlinks to Download an Error Information file, which would be present, only upon Erroneous completion of the upload activity.

![](https://files.readme.io/f38defc143785372fa7b8963c14e555d89eaa5feebe009aa7d55a20a40445bbf-image.png)

## Verification of Uploaded content

On successful upload of a file, the Project team can verify from the Locations tab in the “Admin” application, whether the uploaded content was indeed processed successfully as per requirement. Search for the newly created Locations and click on the same to view its details, to confirm that its created with exact configuration as intended.

![](https://files.readme.io/8457449146f1308efc4d6a9e690368dd3818a1ac9d78f329004771e7422d4fb7-image.png)


# File: ./readme/End User Guide/media-viewer.md

title: Media Viewer
excerpt: ''
If you collect media (images, video, files) as part of your workflow then Avni Media Viewer will help your users to browse through, search and bulk download such media files. Media Viewer is available as an web app on the home page.

<Image alt="Media Viewer app" align="center" border={true} src="https://files.readme.io/697f439-image.png">
  Media Viewer app
</Image>

Media can be filtered by

1. Addresses
2. Subject Types
3. Programs
4. Encounter Types
5. Concepts (numeric, text and coded datatypes are supported)

Media can be downloaded as a zip file with format described [here](https://gist.github.com/vinayvenu/eabbb7c376e32f5bf665c7a0b595f524)

### Important to note

1. Media Viewer can be used only if an organisation has analytics (ETL) enabled
2. The thumbnails are generated seperately as part of AWS Lambda jobs.

### Alternative methods to access media

Other than the Media Viewer app, media can be accessed using the following mechanisms

1. Going to the specific form where the media was collected (either in the web based Data Entry Application or the Android app)
2. Using a [report](https://avni.readme.io/docs/accessing-media-in-reports) to list out a specific media files

### Thumbnails and original image

* **Thumbnails** are shown in the search/filter results. Thumbnails are generated automatically by Avni.
* When you click an image the preview of image is shown, this is the **original image** shown in a fixed size.
* When you download the image the **original image** is downloaded.
* When you click on the name the image **original image** is shown in the new tab.

### Display of non-open formats of images

`heif` and `heic` are two image format (known to Avni team) that cannot be displayed in the browser and cannot be processed by standard libraries to generate thumbnails. These image formats are known to come from some Samsung devices.

Due to this, the thumbnails are not visible in the media viewer web app. But you can only download the full size images for the same.

Currently the users can upload standard images by turning of this feature in Samsung. There are two settings that need to be changed as described in this short video.

<Embed url="https://www.youtube.com/embed/7MLuT-dVuf0?si=B3D3GwQK8_08nXX0" title="How to Fix Android Phone Shooting Picture in HEIC/HEIF Format | Samsung Mobile" favicon="https://www.youtube.com/favicon.ico" image="https://i.ytimg.com/vi/7MLuT-dVuf0/hqdefault.jpg" provider="youtube.com" href="https://www.youtube.com/embed/7MLuT-dVuf0?si=B3D3GwQK8_08nXX0" typeOfEmbed="youtube" html="%3Ciframe%20class%3D%22embedly-embed%22%20src%3D%22%2F%2Fcdn.embedly.com%2Fwidgets%2Fmedia.html%3Fsrc%3Dhttps%253A%252F%252Fwww.youtube.com%252Fembed%252F7MLuT-dVuf0%253Ffeature%253Doembed%26display_name%3DYouTube%26url%3Dhttps%253A%252F%252Fwww.youtube.com%252Fwatch%253Fv%253D7MLuT-dVuf0%26image%3Dhttps%253A%252F%252Fi.ytimg.com%252Fvi%252F7MLuT-dVuf0%252Fhqdefault.jpg%26key%3D7788cb384c9f4d5dbbdbeffd9fe4b92f%26type%3Dtext%252Fhtml%26schema%3Dyoutube%22%20width%3D%22854%22%20height%3D%22480%22%20scrolling%3D%22no%22%20title%3D%22YouTube%20embed%22%20frameborder%3D%220%22%20allow%3D%22autoplay%3B%20fullscreen%3B%20encrypted-media%3B%20picture-in-picture%3B%22%20allowfullscreen%3D%22true%22%3E%3C%2Fiframe%3E" />


# File: ./readme/End User Guide/translation-management.md

title: Translation Management
excerpt: ''
## Overview

Since Avni is widely used for Data-collection by field workers, it is most likely to have a need for the Forms to be read and filled-up in their native language. For example, field workers providing health-care services in the remote villages of Gujarat would be most comfortable performing data-collection in Gujarathi, as opposed to English or Hindi.\
For this reason, Avni supports translation of data-collections forms to native language of the user(field worker) in the Avni "client" mobile application and "Data-Entry" Web application.

## Supported Languages

Avni currently supports Translation capabilities from English to following languages:

* Hindi  
* Marathi  
* Gujarathi  
* Tamil  
* Kannada  
* Bengali  
* Telugu  
* Odia  
* Malayalam  
* Punjabi  
* Sanskrit  
* Urdu  
* Assamese

We additionally have some default translations already available for a few of the above languages, that would make it easier for an organisation to get started on its “Translations” journey. The languages that have some baked-in translations in Avni are as follows:

* Hindi  
* Marathi  
* Gujarathi  
* Tamil  
* Kannada

## Prerequisites

In-order to set up translation for any of the aforementioned languages, the organisation should have enabled the language in the Languages section of the Organisation config.

### Steps to enable Languages for the Organisation

1. Navigate to the “Admin” application

   ![](https://files.readme.io/7bf088b321b670a88c9b73d86ed5d50999afb0ea9553067a0c3483c38e53c7b8-image.png)
2. Select the “Languages” section in the left-tab  
3. Add all the languages that are to be made available to the translation framework, using the drop-down and then click on “Save” button

   ![](https://files.readme.io/0dd7d20b674af9c7257ea0b6e3566e31a8f12dc66b8372251c4e8f305210398d-image.png)

## Steps involved in the translation process

Avni allows the management of translations using the Admin web interface. Below are the steps to translate the content of the app from English to the preferred language

### Navigation to ‘Translations’ module

Login to Avni Web Console and go to the ‘Translations’ module. 

![](https://files.readme.io/ebee37b87a4225d75c86d2c0ff612fcb9bd2ca653fd70d3e95a557ddb9c0a697-image.png)

<br />

### Downloading Translation Keys from Avni

* From the “Translations Dashboard”,download the keys after choosing the desired platform. Platforms are:  
  * Web  
  * Android  
* In general, most organisations need translations only for their field users who perform data-collection using their mobile devices. In such cases, the platform of interest is “Android” (Mobile).  
* If additionally, your organisation also wants translations to be done for the Data-Entry App, then also download the keys for the “Web” platform. 

![](https://files.readme.io/9a5030ec956f7983bf2edff00650c0a2d00367fee775375ecafb49957a8e4a6c-image.png)

<br />

* For each platform selection download, the app will download a zip file containing one JSON file per language available in the organisation config.   
* The JSON file will contain keys for both the standard platform app as well as those specific to your implementation, covering all labels in the app, form fields, location names and any other concepts created in the implementation.  
* The file will also contain existing translated values, if any. This is useful when you have to update the translations after a while, as you will already have all previously uploaded translations available for retention or modifications as needed  
* IMPORTANT Note: When organisations do not want Locations to be part of translations, then they need to bundle export without locations, import those into a temporary org and export translations from that temporary organisation. This was required for one of our organisations since they had a very large number of locations (More than 100,000) and hence were in need to translate other things before locations.

### Setting up a project in Translation Management System (TMS)

* The JSON files can be edited with any tool that the implementer is comfortable with, to come up with translated values for the target language.  
* But for most use cases, we would have multiple translators involved and/or a lot of keys are to be translated. In such cases, we highly recommend using an external translation management system (TMS) like [Lokalise](https://lokalise.com/) which provides a sophisticated editor for performing translations. The TMS provides the ability to import/export JSON files and supports a variety of use cases related to translations.  
* Avni has an enterprise-free plan for Lokalise. If you would like to use Lokalise, please request the Avni team to create your account and project to get started.

#### Creating an implementation project in Lokalise

This is an optional step, required only if the implementation project does not already exist. 

1. In the Project section, a new project needs to be created as shown in the screenshot below.   

   ![](https://files.readme.io/cde8ae8c4f81316f321973918c3717b138e529eb0c1bac0e8c305f1c74e4fb98-image.png)

   ![](https://files.readme.io/46fc019a73c69cd626060e89701fba69edf2894fdad9ccb112a85fd58cb08fd3-image.png)

   <br />

2. While creating the project, provide the Project name, Base language (Which will be english always), and target language in which translations are needed.

   ![](https://files.readme.io/3b1d13d3c4ee9db1eb2f247b44fb36b44f98063d143c684a8c620aae8f1d4d96-image.png)

#### Uploading Translation keys to Lokalise

Once the project is ready in TMS and you have downloaded the translation ZIP file(s), log in to [Lokalise](https://app.lokalise.com/projects) with Samanvay's official email address, if not already done.

* Unzip the downloaded translation zip file  

* Before uploading the JSON, please make sure that null values are removed from the json files

  ![](https://files.readme.io/db2521a87f4b27a65fbac3b98fdf384aaf6024f21dd04d864bb95df03bceff93-image.png)

* In your project, navigate to the ‘Upload’ section and import the JSON file from the unzipped folder of the previously downloaded Translations zip file.

  ![](https://files.readme.io/7d26a129395f40bc2e2bbca4a770a27cf61fa0258d5129fd75a95538a51536d6-image.png)

* In the translation zip file that is downloaded, go to the local folder and select the English json file  

* Once the JSON file has been uploaded successfully, you will see the ‘Ready for Import’ message.

  ![](https://files.readme.io/6a0496a0ba800eb383d5b8f8978defe60bbaf01130868d8e2de18ab6f4324fbe-image.png)

* Go to the ‘editor’ section and verify the keys available for the translation.

  ![](https://files.readme.io/775e3003e6a87eade2045a7acf5b844ea1d1f60efac77cd4f74370fc3572c1b0-image.png)

  <br />

#### Inviting Contributors to the project

Next, Navigate to the ‘Contributors’ section to send out invites to other people

![](https://files.readme.io/0903aa35f4aa3b0b7cc8ec50506511d0e99f0dd8b624eeaf5c403d816b204d3c-image.png)

<br />

Perform below mentioned tasks to invite users to collaborate on the project

* Role should be selected as ‘Translator’   
* “Reference language” should have the base language (Usually English) and  
* “Contributable language” should have target language

![](https://files.readme.io/c3a2ff0b427c727aea29a09ff339a6c7a7219079cf034cd76a114b956f0c3ec8-image.png)

<br />

### Guide for translating keys using Lokalise

* All invitees will receive an Email invite from Lokalise with instructions to login and access the project.

  ![](https://files.readme.io/0f9fcf8ad025f5dd50c754a3736618988e51eced350063df791a20145073c8fb-image.png)

* Once logged in, available projects will be shown in the projects tab/ home screen. you can click on the project name to access the translation items.

  ![](https://files.readme.io/29a4f970e6de4969a115870182c25584f55b1fc1a65eaa09a46b2786fc9317f6-image.png)

* The project would display the editor page by default, and the list of keys should be visible at the bottom.

  ![](https://files.readme.io/e0ab4bd3396825a5df93f6cd6f2e39997d51e8a82b9d33c9ff65d10c9f9e7e25-image.png)

* You can select the Bilingual option shown in the screenshot below and search the question or required field names to be translated.

  ![](https://files.readme.io/0de7bfccf120d85d1154466d2ae52a542f12b0ef10eddf0f133b228d3e6a49cf-image.png)

* After giving the keywords in the search bar, you can see the results below which show questions and field names on the left side. against which you need to provide the Kannada translation and save the response.

  ![](https://files.readme.io/914ab3acbc6c6d25788f872ceecca5160f1420ad85d29afc3ff45d3e240d5d16-image.png)

* Additional notes  
  * Keep the required forms handy while you start the translation process, you can refer to the questions from respective and update the values in Lokalise.  
  * In case of questions, the box on the left side might show "empty" and the question would be visible above that in blue fonts. you can provide the appropriate translation against that on the right-hand side box.

#### Translating Keys with Dynamic string having placeholders

Consider the following “Android” Platform keys, which are examples for Dynamic strings with placeholders:

| numberAboveHiAbsolute | "Should be \{\{limit}}, or less than \{\{limit}}" |
| :-------------------- | :------------------------------------------------ |
| enrolmentSavedMsg     | "\{\{programName}} Enrolment Saved"               |

In-order to translate them to Hindi, you would have to specify following in the translated json file:

| numberAboveHiAbsolute | "\{\{limit}} के बराबर या \{\{limit}} से कम" |
| :-------------------- | :------------------------------------------ |
| enrolmentSavedMsg     | "\{\{programName}} एनरोलमेण्ट सेव हुआ"      |

As shown above, ensure that you retain the string placeholder content within “\{\{” and “}}” as is in native english. Ex: “\{\{limit}}”, "\{\{programName}}”

### Uploading Translations

After completing translation for all the required keys, questions and forms you can download the translated values JSON file of the target language.

* Go to the “Downloads” section of the project  

  ![](https://files.readme.io/934b5c2b87ce2127c6983e5f97739abd5aa4381c3c0c884f7d53a040f9c4d8a1-image.png)
* As seen above, select the ‘Don’t Export’ option for the “Empty Translations” field, so as to export only the translated fields.  
* Click on “Build and Download” option to download the Translated values ZIP file

  ![](https://files.readme.io/ae74952cda34852fe4c7d78933624066f83514681cf5fe52ec8d17b53e911303-image.png)
* Please note that the downloaded ZIP file would contain the JSON file of the base language (English) and targeted language JSON.

  ![](https://files.readme.io/f61d4ac05c7f32ff80ce10f556145a89b11b3ef9f0a43ee2509c4515d31c321c-image.png)
* Now the JSON file of the translation language needs to be uploaded into the Avni. Navigate to the “Translations Dashboard“. Using its “Upload Translations” functionality, upload the JSON file, after choosing an appropriate language. Be careful about choosing the target language, it should be same as the language of the translated values.

  ![](https://files.readme.io/1cc8a1416150da1c1961d5b82bb4508b387a4be7a71d4679ad68f4778ce47301-image.png)
* On successful upload of the translated values, you should see a change in the value of the “Keys with translations” column for the corresponding Language, in the “Translations Dashboard”.

## **Using the Avni client application in User’s native Language**

On the Avni client app, users would need to sync their devices in-order to get the new translations.

If the default language for the User hasn’t been set to his/her desired native language, then the user should be able to switch to it, by navigating to the “More” menu and clicking on the “Edit Settings” button at the top, and selecting the language in which he/she wants to see the app content.

<Image align="right" width="45% " src="https://files.readme.io/28964f670ac61932780ce5d1a5d3c2553a005e392960a59852aacc0c130b57b9-image.png" />

<Image align="left" width="45% " src="https://files.readme.io/aed7f494a90af456f84dc6caa5ec5c80c32e9f469b61ec7295d60a7deaa86503-image.png" />


# File: ./readme/End User Guide/use-of-media-in-forms.md

title: Use of media in forms
excerpt: ''
Avni allows for adding media like data (image and video) in the forms. It can be in form of single or multiple media files in the same question. These can be added by the user using the camera and the file system. Multiple files can be added too in one go. Please see the following table for the capabilities.

| Media Type  | Selection type | Android Version | Supported?    |
| :---------- | :------------- | :-------------- | :------------ |
| Image/Video | Single         | &lt; 13.0       | Supported     |
| Image/Video | Multiple       | &lt; 13.0       | Not Supported |
| Image/Video | Single         | &gt;= 13.0      | Supported     |
| Image/Video | Multiple       | &gt;= 13.0      | Supported     |

<br />

## Why multi-select is not supported in older versions of android

This capability has been restricted by the react native (framework) library used by us. [https://www.npmjs.com/package/react-native-image-picker](https://www.npmjs.com/package/react-native-image-picker)

## My media is in a folder that is not showing in the albums when I am using Avni

If you have images in android folders (in storage) as archive then it is possible that they are shown when you want to upload images in Avni forms. Please see the following as a way to solve this issue.

Android displays only folders which are **considered** albums. A plain folder with images may not be shown here for this reason.

### Option 1

You can setup a folder you want to upload media in Avni by making it show up as albums. You can do that by setting it as Google Photos backup folder. You can do that by:

* going to `Google Photos` app, then `Settings`, then `Choose backup device` folders option, then choose your folder.
* going to `Google Photos` app, then `Library`, then `Utilities`, then choose `Backup Device Folders`, then choose your folder.

### Option 2

Copy/move the folder which has the media to one of the folders which are picked by the Avni form.

*Please note that Google Photos have storage limits.*

We cannot find any means by which an album be added only locally, without it being backed up on Google Photos. [https://www.reddit.com/r/googlephotos/comments/x331q9/create_albums_that_dont_sync_with_the_cloud/](https://www.reddit.com/r/googlephotos/comments/x331q9/create_albums_that_dont_sync_with_the_cloud/)

## How do apps like Dropbox, Facebook, etc support multi-select and have better album support

Since these are not open source projects we can only guess. But it is likely that they have developed their own screens that uses the android file system API.

## Why does Avni not do the same as other apps

1. It is significant amount of work to develop this from scratch compared to use the android's media picker.
2. About 50% and rapidly growing number of Avni users are already on android 13 or later.

<br />

# Also see

* [Media Viewer](doc:media-viewer)

# File: ./readme/End User Guide/user-groups.md

title: 'How to guide: Creating User Groups'
excerpt: ''
### Why are User Groups needed?

Avni users can be grouped into different Users Groups based on their roles and responsibilities and different permissions can be given to them. It ensures that users have the right access levels to perform their tasks effectively while maintaining data integrity:

1. **Role-based Access Control:** User groups ensure each user gets permissions suited to their role. For example, field workers, supervisors, and administrators may need different access levels.
2. **Permission Management:**  Instead of setting permissions individually, administrators can manage them for entire groups, reducing errors and saving time.
3. **Enhanced Security:** User groups help to  define which group can access certain data or perform certain activities in the Avni app like registration, enrolments, edits, and canceling the visit. This 
4. **Customization and Flexibility:** User groups allow for tailored permissions based on specific user roles. A user can have multiple user groups assigned based on their area of work. 
5. **Scalability:** As organizations grow, user groups can adapt to changes in roles and responsibilities, keeping the app aligned with evolving needs.

### Special kind of User Groups

There are 2 User Groups that are automatically created when an Organisation is created. They are:

1. **Everyone**: Default group to which all Users of an Org will always belong to.
2. **Administrators**: A group which would always have all privileges.

### Steps to Create User Groups:

Before creating Users & Catchment, the first step is to create User Groups. Different user groups can have different permissions depending on the roles and responsibilities. Eg. in a project, there are Field Workers who would be using the Avni app, we can create a user group called “Field Workers”

1. **Login to Avni Web Console**

![](https://files.readme.io/ced1805-image4.png)

2. **Go to Admin**

![](https://files.readme.io/172d1bf-image2.png)

3. **Click on User Groups:**

![](https://files.readme.io/6575689-image6.png)

4. **Click on Create Group**\
   Enter the Group name and click on the CREATE NEW GROUP button

![](https://files.readme.io/bb4854b-image5.png)

![](https://files.readme.io/f04a374-image8.png)

5. **Configure Group Users** By clicking on the respective user group, the list of users who are part of the user group is shown along with the permissions given to the user group. User group will show the list of users who are part of this user group along with the user id and registered email.

![](https://files.readme.io/22984c4-image7.png)

6. **Configure Group Permissions:** The permissions section contains a list of permissions which are grouped by subject/entity type. When a subject/entity type is expanded, it will display permissions specific to the subject/entity type like edit, view, perform visit, schedule visit, void any visit or subject registration, cancel visit.

![](https://files.readme.io/1ca8b52-image10.png)

![](https://files.readme.io/2a71433-image9.png)

As shown in the screenshot below, “all privileges” will provide all the permissions and accesses to the entire user group.

When a user is assigned to 2 or more user groups, the union of permissions provided to the assigned user groups will be accessible. (For example, edit access permissions disabled for a form  in one user group and enabled in another user group will allow the user to edit that form)

![](https://files.readme.io/7636af7-image11.png)

7. **Configure Group Dashboards:** This section in user groups allows users to add and provide permission to access the dashboard in the mobile app. Here multiple dashboards added to the user groups will be synced as per the user groups assigned to the user. Out of the dashboards added, primary and secondary dashboards can be defined which would be shown on the user’s mobile screen immediately after logging in. (Refer to the screenshot below)

![](https://files.readme.io/0540e63-image3.png)

Refer to [Offline Report Cards and Custom Dashboards](doc:offline-reports) section for more details regarding this.

### Assign User Groups while creating Users

Once the user groups are updated with the necessary details given above, it should be used while creating users via the Admin -> Users screen.

![](https://files.readme.io/5ea372d-image1.png)


# File: ./readme/End User Guide/users-and-catchments.md

title: Users and Catchments
excerpt: ''
## How to guide: Creating Users and Catchments from the Avni web-app

To access the features of the Avni app, users need to have a unique username and password to log in to the app and perform the activities as and when required. These login credentials can be created through Avni web-app where certain permission can be provided to each unique user as per the area of work and authority to access the data generated in the app.

### Prerequisites before creating the users:

The following items must be configured in the web app before proceeding with the user creation process.

1. Location Hierarchy, Locations ([Refer to this guide \[TO BE ADDED\]]())
2. Languages
3. User Groups ([Refer to this guide](https://avni.readme.io/docs/user-groups))
4. Catchments

### Creating Catchments:

A catchment is a group of locations that are serviced by a user i.e. the locations that a user works in. Only data captured against the locations within the catchments assigned to the user are synced to the android app of the user. The following steps can be followed to create catchments in the web app:

1. Navigate to the admin console

![alt\_text](https://files.readme.io/d32ed8d-image8.png "image_tooltip")

2. Click on the catchments and create a catchment

![](https://files.readme.io/8c7e39e-image2.png)

<br />

3. Provide a unique name for the catchment in the field given below.

![](https://files.readme.io/537772e-image7.png)

<br />

4. Add the locations which are to be part of the catchment.

![](https://files.readme.io/4220102-image11.png)

<br />

### Creating Users:

Once the above-provided prerequisites have been created successfully, we can proceed with the user creation process.

1. Navigate to the admin console in the Avni web app.

![](https://files.readme.io/d32ed8d-image8.png)

<br />

2. Click on the Users section and Create button as given below.

![](https://files.readme.io/a60ebcd-image9.png)

<br />

3. Provide a unique Login ID for each user. Login ID allows to have alphanumeric values which will be followed by @ProjectName. A Login ID that is already in use cannot be re-used to create another user. **Note:** The login name is a case-sensitive field. The user needs to provide the same login ID while logging in to the Avni app.

![](https://files.readme.io/18b704a-image4.png)

<br />

4. While creating a user, the administrator can provide a custom password by clicking on the toggle button highlighted below. This would populate two additional fields to enter a custom password and verify it by giving the same password again. 

![](https://files.readme.io/ee06b59-image3.png)

<br />

5. In case the custom password toggle button is not on, the system will continue with creating the default password. The default password would have the first four letters of the username followed by the last four digits of the mobile number provided while creating the user.
6. Provide the full name of the user along with mobile number and email address. The same mobile number and email can be used multiple times to create different users.

![](https://files.readme.io/6185872-image5.png)

<br />

7. Catchment created as given in this guide can be set here while creating the user. The system doesn’t allow to assign more than one catchment per user.

![](https://files.readme.io/ef2a51f-image10.png)

<br />

8. Set user groups as per the operational roles of the user. Multiple user groups can be assigned to a user. 

![](https://files.readme.io/511929c-image6.png)

<br />

9. Further settings specific to the user can be setup to customise the user experience 

   1. Preferred Language
   2. Track location - Switches on visit location tracking on the Field App
   3. Beneficiary mode - Enables the Beneficiary mode - a limited mode that allows beneficiaries to use the Field App
   4. Disable dashboard auto refresh - Disables Auto-refresh of MyDashboard of the Field App. Use if the dashboard is slow to refresh
   5. Disable auto sync - Disables automatic background sync. Use it if you want to trigger sync only manually
   6. Register + Enrol - Adds extra quick menu items on the Register tab to register and enrol to programs in a single flow
   7. Enable Call Masking - Enables Exotel call masking for the user
   8. Identifier Prefix - Identifier prefix for ids generated for this user. See[ documentation](https://avni.readme.io/docs/creating-identifiers) for more information
   9. Date Picker Mode - Set default date picker for the Field App
   10. Time Picker Mode - Set default time picker for the Field App

   ![](https://files.readme.io/a73b680-image1.png)

   <br />


# File: ./readme/General/architecture/reporting-in-avni/getting-started-with-avni-reports.md

title: Getting Started with Avni Self-Service Reports 📊
excerpt: ''
## What This Guide Will Help You Do

This guide will help you learn how to create reports and visualize your Avni data in Metabase, even if you've never worked with data tools before! We'll walk through real examples with step-by-step instructions.

<Callout icon="💡" theme="default">
  ### **Quick Tip:** This guide focuses on practical everyday tasks. If you need information about setup or administration, please refer to the [Self-Service Reports Guide for Avni](self-service-reports-guide-for-avni). If needed, contact Avni support team for further guidance.
</Callout>

## The Basics: Understanding Metabase

### What is Metabase and why should I care?

Metabase is a simple tool that helps you look at your organisation's data in Avni, without needing technical skills. Think of it like a smart photo editor for your data - it helps you:

* See overall Avni organisation data at a glance
* Create charts and graphs easily
* Share insights with your team
* Make better decisions based on actual numbers
* Identify trends and patterns in your data

### How to Log In 🔑

1. Open your web browser and go to [https://reporting.avniproject.org/](https://reporting.avniproject.org/)
2. Enter your email address
3. Enter your password
4. Click the "Log in" button

<Image align="center" src="https://files.readme.io/95b3cfa20f75003a170accb2312b13b1ff51752a37ffbeb1130366d044e37d8f-Screenshot_2025-05-26_at_12.07.51_PM.png" />

### Help! I Can't Log In 🆘

Don't worry! Try these steps:

1. Click the "Forgot Password" link on the login page
2. Enter your email address to receive reset instructions
3. If that doesn't work, contact your Avni support team for help

### Who Can See My Reports? 👁️

Only people from your organization can see your data and reports:

* Team members in your organization
* System administrators who help manage the platform

### Where Does This Data Come From? 📱→💾

All the data you see in reports comes from information collected by field workers using:

* The Avni mobile app on phones and tablets
* The Avni web application on computers

This information is automatically organized into easy-to-use tables via the ETL service, that you can explore in Metabase.

## Understanding Your Data

### What Are Data Tables?

In Avni, your information is organized in **tables** - think of them like Excel spreadsheets or organized lists. Each table contains specific information about your program. The Avni ETL service creates special reporting-friendly tables that make it easy to build reports and visualizations.

<Image alt="Example of a data table" align="center" src="https://files.readme.io/668dae0c3299f96b27bc34928466b31a2baff73ca24c4c9c38b98c7d9c3ad01e-metabase_database_tables.png">
  Example of organisation specific tables
</Image>

### Your Main Tables Explained

Here are all the important tables you'll work with in Metabase:

#### 1. Subject Tables

These tables contain information about the main people or things you track:

* **Example:** `Individual`, `Household`, `Facility`
* Each row represents one person or entity in your program
* Contains basic information like name, ID, registration date, address details
* Table names follow the pattern: `<subjectType>`

#### 2. Encounter Tables

These tables show visits or interactions that happened outside any program:

* **Example:** `Individual_Baseline`, `Household_Annual_Visit`
* Each row represents one visit or interaction
* Contains all the information collected during that encounter
* Table names follow the pattern: `<subjectType>_<encounterType>`
* Cancelled encounters are in separate tables named: `<subjectType>_<encounterType>_cancel`

#### 3. Program Tables

These tables show which people are enrolled in which programs:

* **Example:** `Individual_Nutrition_Program`, `Individual_Pregnancy`
* Each row represents one person's enrollment in a program
* Contains enrollment details like date joined, date exited
* Table names follow the pattern: `<subjectType>_<programName>`
* Program exits are in separate tables named: `<subjectType>_<programName>_exit`

#### 4. Program Encounter Tables

These tables show visits that happened within specific programs:

* **Example:** `Individual_Nutrition_Program_Monthly_Visit`
* Each row represents one program visit
* Contains all information collected during that program visit
* Table names follow the pattern: `<subjectType>_<programName>_<encounterType>`
* Cancelled program encounters are in separate tables named: `<subjectType>_<programName>_<encounterType>_cancel`

#### 5. Supporting Tables

Additional tables that help with specific data types:

* **Address Table:** Contains detailed address information for all subjects
* **Media Table:** Stores all media files (images, documents) in your system
* **Repeatable Group Tables:** For information that can appear multiple times
  * Table names follow the pattern: `<parentTable>_<question_group_concept_name>`

### Try It Yourself: Exploring Tables

Let's explore these tables together:

1. **Open the Data Browser:**
   * Click on "Browse Data" at the top of the screen
   * Find and click on the folder labeled with your Organisation Name, Ex: "BI DEMO"

2. **Look at any of the Subject Type Table:**
   * Click on any of the Subject Type Table, Ex: "beneficiary" table
   * Notice each person has a unique ID number
   * Browse through the information like names and addresses

3. **Understand How Tables Connect:**
   * Open any ProgramEnrolment / ProgramEncounter Table,"participation" table
   * Find the "Individual ID" column
   * This ID connects to the ID numbers in the "beneficiary" table
   * Similarly, the "Program ID" connects to IDs in the program table

> **Understanding Connections:** Tables connect through ID numbers. Think of it like this: if beneficiary #123 appears in the participation table with program #456, it means that person is enrolled in that specific program.

## Finding Exactly What You Need

### Filtering: Zooming In On Specific Information

Filtering lets you focus on exactly the information you care about - like looking at beneficiaries from only certain states or programs started after a specific date.

<Image alt="Example of filtering" align="center" src="https://files.readme.io/3d93f33b5a5a65a883c866755c4e25bf7928d30d28fa70ced336140c87aa5460-Screenshot_2025-05-26_at_12.20.49_PM.png">
  Example of Filters configuration screen for a table
</Image>

### Try It Yourself: Simple Filtering

**Exercise 1: Filter by State**

1. Open any of the Subject Type Table, Ex: "beneficiary" table
2. Find any address related column, Ex: "state" column and click on it
3. Choose "Filter by this column" from the menu
4. Select a few addresses (states) you're interested in
5. Click "Add Filter" to see only people from those states

**Exercise 2: Create Custom Filters**

1. Open any of the ProgramEnrolment / ProgramEncounter Table, Ex: "participation" table
2. Look for the "Filter" button at the top right of the screen
3. Add criteria Ex: "Role equals Caregiver"
4. Click "Apply Filter" to see the results

### Saving Your Work For Later

When you create a useful report:

1. Click the "Save" button
2. Give your report a clear name (add your name to avoid confusion)
3. Choose where to save it (your personal collection or a shared folder)

> **Why Save?** Save your reports so you don't have to recreate them every time. It's like bookmarking a webpage you want to visit again!

### Creating Summaries: The Big Picture

### Creating Summary Reports: Counting and Grouping

Summarizing helps you count things by categories - like how many beneficiaries are in each state or how many people are in each program.

<Image alt="Example of a summary" align="center" src="https://files.readme.io/a2de7339d09d2e80d4e7bd3167c95b171df2c27033acc8848889fc995daa2e30-Screenshot_2025-05-26_at_12.22.33_PM.png">
  Example of Summarization of a table
</Image>

**Try It: Create Your First Summary**

1. **Start with filtering:**
   * Open any of the ProgramEnrolment / ProgramEncounter Table, Ex: "participation" table
   * Click "Filter" at the top
   * Choose "Last Visit Date" and select "Last month"
   * Click "Apply" to see only recent visits

2. **Then create a summary:**
   * Click the "Summarize" button
   * Under "Group by" select "State"
   * Watch how your data transforms into a count by state!

3. **Create a visualization:**
   * Look at the bottom left for "Visualization"
   * Click and choose "Pie Chart"
   * Click "Done" to see your beautiful chart

> **What Did We Just Do?** We created a report showing how many beneficiaries from each state had visits in the last month. This helps you see which states are most active!

### Bringing Different Information Together: Using Joins

**What is a Join?** 

A join lets you combine information from different tables. Think of it like putting two spreadsheets side by side and connecting matching rows.

For example, you might want to see beneficiary names alongside their program enrolments, even though this information is stored in separate tables.

<Image alt="Illustration of a join concept" align="center" src="https://files.readme.io/761b483d4b5dffb3867f47eed8e460645879b9819abf4572feb7032248cc4436-Screenshot_2025-05-26_at_12.24.02_PM.png">
  Illustration of a join in Metabase
</Image>

**Try It: Joining Tables Step by Step**

1. **Start with the basic table:**
   * Open any of the ProgramEnrolment / ProgramEncounter Table, Ex: "participation" table
   * Look for the button next to "Summarize" (it's labeled "View")
   * Click it to enter editing mode

2. **Select which columns you want:**
   * Keep only the columns you're interested in
   * For example: keep "Role" and "Beneficiary ID"

3. **Connect to another table:**
   * Find and click "Join Data"
   * Select the related Subject Type table, Ex: "beneficiary" table
   * Click the join button

4. **Tell Metabase how to connect the tables:**
   * Choose ProgramEnrolment / ProgramEncounter Table -> Subject Type Table, Ex: "participation" -> "beneficiary"
   * Match ProgramEnrolment / ProgramEncounter Table Reference ID column with Subject Type Table ID column, Ex: "beneficiary\_id" with "ID"
   * Click "Join these columns"

5. **Clean up your view:**
   * Remove any extra columns you don't need
   * Click "Visualize" to see your combined data

**Make It Look Nice:**

* Go to the "Visualization" section
* Click the gear icon above the table
* Rename columns to make them easier to understand
* For example, change "beneficiary\_id" to "Person ID"

> **Why This Matters:** By joining tables, you can see complete information in one view. For instance, you can see a person's name and address along with which programs they're enrolled in, even though that information comes from different tables.

### Practice Activities: Try It Yourself

Now that you've learned how to join tables, try these exercises to build your skills:

1. **Create a Summary Chart by Category:**
   * Use any joined data you've created
   * Click "Summarize"
   * Group by any category field of your choice (like Role, Gender, Age Group, etc.)
   * Switch to a bar graph visualization
   * See the distribution across your chosen category!

2. **Create a Program Enrolment Chart:**
   * Join any Program Enrolment table with its related Program table
   * Group by "Program Name" or another program attribute
   * Create a bar graph showing counts by program

3. **Build a Complete Profile View:**
   * Create a table with address fields (like "State", "District"), person details, program information, and other relevant attributes
   * Use the Sort feature to organize your data logically (e.g., by location)
   * This gives you a complete view of who is enrolled where!

## Creating Your Own Calculations

### Adding Custom Columns

Sometimes you need information that isn't directly in your data. Metabase lets you create your own calculations!

<Image alt="Example of a custom column" align="center" width="250px" src="https://files.readme.io/f51d52859d073fc002b91aa87b3a99332b880592c05e99963ebe302fc4b30c1e-Screenshot_2025-05-26_at_12.30.07_PM.png">
  Example of a custom column
</Image>

**Try It: Calculate Address Length**

Let's say you want to see how long each person's address is:

1. Open any of the Subject Type Table, Ex: "beneficiary" table
2. Click "Edit Query" (near the top of the screen)
3. Find and click the "+ Add custom column" button
4. For the formula, type: `length([Address])`
5. Name your column: "Address length"
6. Click "Done" then "Visualize" to see your new column!

### Advanced Analysis: Grouping and Averaging

**What if you want to see the average address length for each district?**

This is where grouping comes in - it's like organizing your data into buckets and then calculating something about each bucket.

**Try It: Calculate Averages by Group**

1. Start with your table that has the Address length column

2. Click "Summarize"

3. Set up your grouping:
   * Group by "State" and "District"
   * For the calculation, choose "Average of" → "Address length"

4. Add filters if needed:
   * Maybe filter where "Address is not empty"

5. Use "Sort" to organize by state and district

6. Click "Visualize" to see your results

### Visualize Your Results

**Try creating different visualizations:**

<Image align="center" src="https://files.readme.io/1e7745387046fb5bbf15f45ad3d7524914fd92b6597c7e2725f9bd85ab7681e1-Screenshot_2025-05-26_at_12.32.38_PM.png" />

1. Try a line graph for the address length data
2. Try a bar chart comparing districts
3. Try a map visualization if geographical data is available

> **Final Tip:** The best reports answer specific questions. Before creating a report, ask yourself: "What exactly do I want to know?" Then build your report to answer that question!

## Additional Information regarding behind the Scenes: How Your Data Gets generated for use in Reporting 🔧

### Why We Need Special Reports Tables

You might wonder why you're using special tables for reporting instead of the regular Avni database. Here's a simple explanation:

**The Challenge:**\
The main Avni database is designed for collecting and storing data efficiently across organizations, not for creating reports. This creates several challenges:

1. **Complex Data Structures:** Some information is stored in specialized formats that are hard to query
2. **Performance Issues:** Running reports directly on the main database would be very slow
3. **Address Complexity:** Address information has many levels (state, district, etc.) that are difficult to work with
4. **Data Volume:** Analyzing all the data at once would be overwhelming

### How Avni Solves This: The ETL Service 🔄

Avni uses a standard process (called ETL - Extract, Transform, Load) that:

1. Copies data from the main database into a separate organization-specific database
2. Reorganizes it into formats better suited for reporting
3. Updates this reporting-friendly data periodically every hour or so)

### The Special Tables Created For You

The ETL service creates several easy-to-use tables:

* **Subject Tables:** One table for each type of person or thing you track (Ex: `Individual` or `Household`)
* **Encounter Tables:** Tables that show visits or interactions (Ex: `Individual_Baseline` or `Individual_Annual_Visit`)
* **Program Tables:** Information about program enrollment (Ex: `Individual_Nutrition_Program`)
* **Program Encounter Tables:** Records of visits within programs (Ex: `Individual_Nutrition_Program_Monthly_Visit`)
* **Supporting Tables:** Special tables for addresses, images, and repeated information

<Callout icon="💡" theme="default">
  ### **Technical Note:** Table names follow patterns like `<subjectType>_<encounterType>` or `<subjectType>_<programName>_<encounterType>` to make them easy to identify.
</Callout>

### What This Means For You

* You get faster reports
* You can easily create visualizations
* Your data is organized in a way that makes sense for analysis
* Everything updates automatically every hour or so

All of this happens behind the scenes so you can focus on getting insights from your data rather than worrying about database structures!


# File: ./readme/General/architecture/reporting-in-avni/self-service-reports-guide-for-avni.md

title: Self-Service Reports Guide for Avni
excerpt: ''
## Table of Contents

* [Introduction](#introduction)
* [Prerequisites](#prerequisites)
* [Setup Process](#setup-process)
* [User Management](#user-management)
* [Navigation](#navigation)
* [Reporting Features](#reporting-features)
* [Troubleshooting](#troubleshooting)
* [Refresh Process](#refresh-process)
* [Teardown Process](#teardown-process)
* [Appendix](#appendix)

## Introduction

### What is Metabase?

Metabase is a powerful open-source analytics and visualization tool that Avni integrates to provide comprehensive reporting capabilities. It allows you to create custom dashboards, run ad-hoc queries, and share insights across your organization with simple drag-and-drop operations.

### Self-Service Reports in Avni

Self-service Reports is a feature in Avni that allows users to create and manage reports without requiring technical expertise. It provides a user-friendly interface for creating and managing reports, and allows users to schedule and distribute reports via email.\
In Avni, we make use of Metabase to power Self-Service Reports.

> **Note:** This guide provides comprehensive documentation for setup, user management, and administration of Self-Service Reports. For hands-on training with practical exercises for using Metabase on your Avni Data, please refer to the [Getting started with Avni Metabase reports](getting-started-with-avni-reports) guide.

### Benefits of Metabase

* **User-friendly interface**: Create visualizations with simple drag-and-drop operations
* **Customizable dashboards**: Build tailored views for different stakeholders
* **Automated reporting**: Schedule and distribute reports via email
* **Data exploration**: Empower users to find insights without technical expertise
* **Secure access control**: Manage permissions at granular levels

### Inbuilt Capabilities of Self-Service Reports

Self-service Reports in Avni provides the following capabilities:

1. Creates a dedicated database user with appropriate permissions
2. Establishes a connection between Metabase and your Avni database
3. Sets up user groups and permission structures
4. Create standard Questions
5. Create collection with default dashboard

## Prerequisites

* ETL has to be enabled for your organisation, contact Avni-support team for any help regarding this.
* You need to be logged-in as a user, who belongs to a UserGroup with Analytics Privilege for your organization in Avni

<Image align="center" className="border" width="420px" border={true} src="https://files.readme.io/08e4962e2a1df9c5d3b5967ca92e0c5ac18acf0ee573971b547a4562f78e1c51-Screenshot_2025-05-20_at_7.25.43_PM.png" />

## Setup Process

### 1. Enabling Self-Service Reports

Self-Service Reports is managed at the organization level in Avni:

1. Log in to your Avni webapp
2. Navigate to Reports section
3. Click on "Self-service Reports" tab
4. Click on "Setup Reports" button

![Initial Setup State](https://files.readme.io/cdaa0376b8d1b7fbe8a1d776681b23a8f4643cbbc44c290888e5fcf356b23dd4-metabase_initial_state.png)\
*Figure 2: Initial state before Self-Service Reports setup with "Setup Reports" button*

### 2. Setup Process Stages

The setup process goes through several stages:

#### Initial Setup

When you first enable Self-Service Reports, you'll see the "Setup Reports" button. Clicking this button initiates the setup process.

#### Setup in Progress

During the setup process, you'll see a loading indicator:

![Setup in Progress](https://files.readme.io/34792bee15afc7e3ddf4a88a31e62ba4c23a8131971377c52df7a81c624c599d-metabase_loading_state.png)\
*Figure 3: Setup in progress with loading spinner*

The setup process typically takes 15-30 minutes to complete and involves:

* Database connection setup
* Initial schema synchronization
* Permission configuration
* Default Collection and Dashboard creation
* Default questions creation

#### Partial Setup

Sometimes, the setup may complete partially with only some resources available:

![Partial Setup](https://files.readme.io/61242bf6bcce5582259ac4ba46363b9cd90a102be6511728d18b6623e4417ada-metabase_partial_setup.png)\
*Figure 4.a: Partial setup with only Database resource available*

In this state, you can either:

* Wait for the remaining resources to be created automatically
* Click "Setup Reports" again to retry the setup process

### 3. Verifying Setup Completion

You can verify the setup was successful by:

1. Confirming the "Explore Your Data" button is available
2. Testing access with a user that has been added to the "Metabase Users" group in Avni

<Image align="center" src="https://files.readme.io/f0c5a313f302629bfa838cfcbbc368aac06d42a079c016331de3295e7df915a0-metabase_refresh_reports.png" />

*Figure 4.b : Successfully completed setup\
(Note: Delete button only available in development environments)*

## User Management

### User Group Synchronization

Avni automatically synchronizes users between the Avni platform and Metabase. This synchronization ensures that users added to the "Metabase Users" group in Avni can access analytics in Metabase.

#### Adding Users in Avni

To grant users access to Metabase analytics:

1. Navigate to User Groups Management in Avni Admin App
2. Select the "Metabase Users" group
3. Add the user(s) you want to grant access to the group
4. Save changes
5. User added to "Metabase Users" group, will receive an email with an account activation link

Note: Removing users from the "Metabase Users" group will remove their access to Metabase analytics.

![Avni User Groups](https://files.readme.io/5c483f0cd5480029f298a23961dfb5248f633d13195022546bc8af4248cddac7-metabase_user_groups.png)*Figure 5: Avni user groups management interface showing Metabase Users group*

#### Verification in Metabase

After adding users to the Metabase Users group in Avni, you can verify their synchronization in the Metabase admin interface:

![Metabase Admin People](https://files.readme.io/cf18e6606710fc311495adec917571095ba46e793afadd92e731a17f192fdaf1-metabase_admin_people.png)*Figure 6: Metabase Admin interface showing synchronized users*

The synchronization process:

1. Creates user accounts in Metabase with the same email addresses as in Avni
2. Includes the User in Metabase Group corresponding to their organization

## Navigation

You can navigate to Self-Service Reports from the Avni Sign-in screen, by clicking on the "METABASE REPORTS" button.

![Self-Service Reports Navigation](https://files.readme.io/5ca645c93da6b8a024963b55c58b245cb12f9c628d5a5e43eafbdf542a520699-metabase_navigate_from_avni.png)\
*Figure 7: Self-Service Reports Navigation via "Self-Service Reports" button available in Avni Sign-in screen*

## Reporting Features

### Canned Reports Dashboard

The Metabase integration includes a pre-configured "Canned Reports" dashboard that provides immediate value without requiring users to build reports from scratch.

![Canned Reports Dashboard](https://files.readme.io/7d99a2dae462bb202090ac6e4e6d73e21c47ce5a00c94c4eae4d2b09eb2ed74a-metabase_canned_reports.png)\
*Figure 8: Overview dashboard with multiple report visualizations*

Key features of the Canned Reports dashboard:

* Filter controls at the top (Date Range, Location filters, etc.)
* Multiple visualizations organized by subject area
* Interactive charts that respond to filter selections
* Donut charts showing distribution of key metrics
* Empty states for sections with no data ("No results!")
* Drill-down ability by clicking on section of Donut (or of any part of different type of vizualizations)

<Image align="center" src="https://files.readme.io/0ce0bacad8d607b479963694e94bcb13656b0f1068583aa0eaa2ed8cbe3b769b-Screenshot_2025-05-22_at_11.15.58_AM.png" />

*Figure 9: Drill-down ability, by clicking on Donut chart section or on other visualizations*

### Collection Structure

Metabase organizes reports and dashboards into collections. The default collection contains various pre-built reports:

![Collection Structure](https://files.readme.io/c62b3bd102960c9bbe38b26d36cd02980dd901cec84c54bba40c96dee98e4adf-metabase_collection.png)\
*Figure 10: Default collection structure showing dashboard and reports*

The collection includes:

* Canned Reports dashboard
* Individual report views (Completed Visits, Due Visits, etc.)
* Other Fundamental Database tables and views that power the reports

### Report Visualizations

Individual reports provide detailed visualizations of specific metrics:

![Completed / Due Visits Report](https://files.readme.io/9af7f3494e2d9173f4d6b4e74acfc9fadca9e606f95684af1f788575c5beaf2b-metabase_completed_visits.png)\
*Figure 11: Detailed visualization of Completed / Due Visits by type*

Visualization features include:

* Interactive donut charts with percentage breakdowns
* Clear labeling of data categories
* Total count displayed in the center
* Color-coded segments for easy differentiation

### Database Tables and Views

Metabase connects to your Avni database and creates optimized views for reporting:

![Database Tables and Views](https://files.readme.io/da4dc45abbb0f349603f03f05b2db26ed74f925793c729aa7199d464559ee17f-metabase_database_tables.png)\
*Figure 12: Database tables and views available in Self-Service Reports*

The database structure includes:

* Base tables (individual, household, address, etc.)
* Derived views (completed\_visits\_view, due\_visits\_view, etc.)
* Relationship tables (household\_individual, etc.)

These tables and views are automatically kept in sync with your Avni database.

### Data Exploration

Metabase allows users to explore raw data through table views:

![Individual Data Table](https://files.readme.io/cfbf4ea42ab9b037e39fc0fa1e23c7f4773c9c24bf0abd7ab598ac193815b637-metabase_individual_table.png)\
*Figure 13: Individual data table showing subject records*

![Child Data Table](https://files.readme.io/37921c0981d9e7914beaa68c5237b17baae544387131caef7ab1a4090476b09b-metabase_child_table.png)\
*Figure 14: Child data table showing specific program records*

Data exploration features include:

* Sortable columns
* Record counts and pagination
* Search functionality
* Filtering options
* Direct access to raw data

## Troubleshooting

### Error Reporting

When errors occur during the Self-Service Reports setup or synchronization process, they are displayed directly in the interface:

![Error Reporting Example](https://files.readme.io/e1e4f12702c93d949a5c05e685d120a159e2a42fee31ca6555dd4464312d883a-metabase_error_example.png)

*Figure 15: Example of an error message during Self-Service Reports setup\
(Note: Delete button only available in development environments)*

The error message includes:

* A clear indication that the attempt failed
* The specific Server error that occurred
* Details about what caused the error (in this example, a missing database table)
* A "Copy error to clipboard" button for easy sharing with support

Common errors include:

* Database connection issues
* Missing tables or schemas due to ETL failure
* ETL not enabled

### Common Issues and Solutions

| Issue                                   | Possible Cause                                                   | Solution                                             |
| --------------------------------------- | ---------------------------------------------------------------- | ---------------------------------------------------- |
| Dashboard shows no data                 | Database sync incomplete, ETL process not completed successfully | Wait for sync / ETL process to complete successfully |
| User cannot access Self-Service Reports | Not in "Metabase Users" group                                    | Add user to the group in Avni                        |
| Missing tables or fields                | ETL not enabled or not completed successfully                    | Contact Support                                      |

## Refresh Process

### When to Use Refresh

The refresh process is to be used, whenever there are new Entity Types created for the organization.

### Performing a Refresh

To refresh Self-Service Reports integration:

1. In Avni admin panel, navigate to Reports section
2. Click "Self-Service Reports" tab
3. Click "Refresh Reports" button

<Image align="center" src="https://files.readme.io/5b4264a93cd8614a6e0eb42c41a84420cb99372c773554667e95ad48d1bcb214-metabase_refresh_reports.png" />

*Figure 16: Refresh Self-Service Reports setup by clicking on "REFRESH REPORTS"\
(Note: Delete button only available in development environments)*

Wait for the process to complete.

The refresh process will:

* Create missing dashboards, cards and questions

## Appendix

### Glossary of Terms

* **Collection**: A group of questions and dashboards in Metabase
* **Dashboard**: A customizable display of multiple visualizations
* **Question**: A saved query that produces a visualization or data table
* **Sync**: The process of updating Metabase's understanding of your organization's database structure
* **Card**: An individual visualization on a dashboard


# File: ./readme/General/architecture/terms-and-their-definitions.md

title: Terminology
excerpt: >-
  description: ''
---
There is some terminology that has a specific meaning within Avni listed here. Understanding this will be useful to understand some of the documentation on this site. 

## SYSTEM-WIDE Terminology:

* **Organisation** - Avni has a multi-tenant architecture where multiple organisations can share the same server. A tenant in an Avni installation is called an organisation. Under an organisation one can have users, configuration (like programs, forms, settings, etc) and data (like subjects, visits, etc). 
* **Implementation** - Technically, this means the implementation of an organisation within Avni. However, this term is usually used interchangeably with Organisation. 
* **Subject** - Users in an organisation usually record data about one or more "subject types". A subject type could be a *person*, a *building*, a *dam*, or anything against which long-term data is to be recorded. 
* **Individual** - In earlier versions of Avni, there could be only one subject type - an individual. *Subject types* were introduced to the system later so that data can be recorded not just for people, but for any entity (or Subject). You might still find the term called individual in some places in Avni. All these will be replaced by the appropriate Subject term soon. Avni is already being used in places where the Subject being monitored is not a person, but an entity - like a "dam", etc. 
* **Location** - In Avni, it is mandatory to associate a subject to a location. A location could be geographic (state, village, etc) or class-rooms, etc. Locations have hierarchy support. 
* **Catchment** - A catchment is a group of locations that are monitored by a user. If there are multiple users assigned to a single catchment, they will all have access to the same data about subjects and their information under that catchment area. 
* **Form** - All information captured during registration, encounter, program enrolment, program encounter, program encounter cancellation, program exit, etc are captured through forms defined through the admin app. 
* **Concept** - This is the underlying meaning of a question asked in a form. It can be the same as the form question but can be different as well. For example, the question asked could be "*Please enter the height of a person*", while the underlying connected concept to this question could be "*Height*". Concepts provide a level of indirection between the visual form and the underlying data model and allow for validation and reporting or aggregation.

## USERS & ENCOUNTERS Terminology

* **User** - A person who can log in to the Avni system is a user. 
* **Organisation Admin** - A high-privilege User who can log in to the Avni Administration Web App for their organisation, and perform Admin functionality. 
* **Registration** - The process of creating a new *Subject* in the system is called Registration. A subject registration is usually associated with a form that can be customized to the subject type and the implementation. 
* **Encounter** - All observations about a subject recorded at a specific point in time is called an encounter. The term is interchangeably used for visits as well. 
* **Encounter Type** - Represents the type of encounter. This helps determine the set of questions that need to be asked during an encounter. For example, there might be a *monthly* visit where some questions are asked, while different questions are asked during a *quarterly* visit. 
* **Visit** - Alias to encounter

## PROGRAM Terminology

* **Program** - Information about a subject can be structured into different programs that they can be enrolled in. eg: pregnancy program, vaccination program, etc. A program comprises a name, forms for program enrolment, encounter types and their related forms, and visits scheduling logic. 
* **Program Enrolment** - is the process by which a subject enrolls into a program. Enrolment is usually associated with a form that is used for baseline information when starting a program. 
* **Program Exit** - is the process by which a subject exits from a program. An exit is usually associated with a form. 
* **Program Encounter** - is an encounter that is related to an enrolment. 
* **Program Visit** - is the same as program encounter
* **Visit Schedule** - is usually defined for a program. It can be dynamically calculated after a program enrolment or a program encounter. Logic to define a visit schedule is usually specific to the implementation and is defined using the visit scheduling extension point. 

## DOMAIN MODEL - DIAGRAM

A nice view of the domain and usage is provided in the [Implementer's concept guide - Introduction](doc:implementers-concept-guide-introduction). Head over there for a more detailed view of the system in action.


# File: ./readme/General/avni-hosted-service.md

title: Avni Hosted Service
excerpt: ''
Avni is available as a hosted service provided by [Samanvay Foundation](https://www.samanvayfoundation.org/). More details are available at the [Avni Project website](https://avniproject.org/). 

If you are an existing user of the Avni hosted services, you can

1. Download the application from the Android Play Store [here](https://play.google.com/store/apps/details?id=com.openchsclient)
2. Login to the web-based data entry app or app designer [here](https://app.avniproject.org/#/)

If you have configured reports via Metabase, they will be available [here](https://reporting.avniproject.org/)\
If you have configured reports via Jasper Reports, they will be available [here](https://reporting-jasper.avniproject.org/jasperserver/login.html).


# File: ./readme/General/getting-started.md

title: Introduction
excerpt: A quick overview of Avni software for field data collection and reporting.
Avni is an open-source platform for on-field service delivery and data collection. Designed for the development sector, Avni strengthens field capacity for non-profits and governments across sectors - like health, water, education, and social welfare.

This documentation site is geared to introduce Avni to those who would like to implement their program workflows using this system.

**Avni consists of 4 major components which perform various functions as explained below:**

1. **Avni Field App (Mobile)** : This is an Android app designed to be used in the field for data entry and collection. It can work in offline mode and can sync data whenever it has internet connectivity.  One can install the field app easily from the Google Play Store or from an APK file.

2. **Avni Web App**: This is the **Administration** Interface where you can configure and set up the Avni server,  for example configuring master data for Locations, Hierarchies, Users, designing the Program Forms, etc. It can also be used for Data Imports, Exports, and Data-Entry. It runs in a web browser.

3. **Avni Reporting and Dashboard**: This connects to the Avni server to pull out custom reports and dashboards that can be viewed in the web browser, or exported as PDFs and emailed.

4. **Avni Hosted Service**: The central instance of the Avni server running on the cloud, which stores all the master data, configuration, and field-entered data. If you don't want to use the cloud instance, then you can set up your own local instance of Avni in your data center/server. Avni is fully Open-Source.

See [Avni Hosted Service](doc:avni-hosted-service) for details of the Avni hosted service

**See Diagram Below**

![](https://files.readme.io/feb07ae-Avni_6.png "Avni (6).png")

# Documentations

1. [Implementer's guide](doc:implementers-concept-guide-introduction)
2. [Production Environment Setup guide](doc:environment-setup-guides)
3. [Design Documentation](doc:architecture)
4. [Avni Code of Conduct](doc:avni-code-of-conduct)


# File: ./readme/General/roadmap.md

title: Avni Roadmap
excerpt: ''
An active roadmap for Avni is maintained in the [Project board](https://github.com/orgs/avniproject/projects/2/views/7).


# File: ./readme/Implementers/advanced-feature-guide/about-audit-information.md

title: About Audit Information
excerpt: ''
In Avni mobile app the user can see certain audit information. The app displays:

1. Created by user for subjects and program enrolments.
2. Filled by user for program encounters and general encounters. This is the user who filled the form. For scheduled encounters - this is the person who filled the form and not the person who was instrumental in scheduling the encounter.
3. Where ever the audit information is not available (see below), no audit information will be shown. In other words if the audit information is not shown then it will be due to the following.

### When is the audit information not shown.

1. Since this feature has been introduced only now, release 7.0, all audit information are not available for older records and it will start showing up only for the newer records.


# File: ./readme/Implementers/advanced-feature-guide/access-control.md

title: Access Control
excerpt: ''
Before the introduction of Access Control, organisation users with access to the field app could access all functions (i.e. registration, enrolments, search etc.) in the app. There was a need for some implementations to limit access to specific functions in order to reduce the number of options visible to end users and simplify the workflow for them while also providing a mechanism for access control.

Access Control is implemented via User Groups to facilitate this need. This functionality is available to Organisation admins in the Admin section of the Web app under the User Groups menu.

# Applicability

* The access control rules are applicable in the field app, data entry app, and the web app.
* Access control is not applicable to the reporting app.

# User Groups

User Groups represent a collection of users and a set of privileges allowed to these users. User with EditUserGroup and EditUserConfiguration privilege can define as many groups as they need to define the access control required for their organisation. Each group can be assigned a set of privileges (or all privileges using the switch available at the top).

Each user can be added to multiple groups.

## Privileges are Additive

If any of the groups that a user belongs to allows a particular privilege, the user will have access to that function.

## Default Groups

By default, the system creates an `Everyone` and an `Administrators` group. `Everyone` group includes all the users in the organisation. `Administrators` group grants all the privileges to allow access to all the functionality.

<Image align="center" width="500px" src="https://files.readme.io/9c003c1-Screenshot_2023-08-08_at_3.46.23_PM.png" />

Users cannot be removed from `Everyone` group but the privileges associated with this group can be modified. The has all privileges flag cannot be reset for `Administrators` group.

## Privileges

The following privileges are available in order to allow organisation admins to configure fine-grained access to functions for the org users. These privileges are configurable per entity type i.e. a group could have the 'View subject' privilege allowed for subject type 'abc' but disallowed for subject type 'xyz'.

* The Subject level privileges are configurable for each Subject Type setup in your organisation.
* The Enrolment level privileges are configurable for each program setup in your organisation.
* The Encounter level privileges are configurable for each Encounter Type (General or Program) setup in your organisation.
* The Checklist level privileges are configurable for each Program containing checklists for your organisation. 

<Table align={["left","left","left"]}>
  <thead>
    <tr>
      <th>
        Entity Type
      </th>

      <th>
        Privilege
      </th>

      <th>
        Explanation
      </th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>
        Subject
      </td>

      <td>
        View subject
      </td>

      <td>
        Controls whether field users can see subjects of a particular subject type in the app.  

        All other privileges are dependent on this privilege. If disallowed, field users cannot see or access any functionality for the specific subject type.
      </td>
    </tr>

    <tr>
      <td>
        Subject
      </td>

      <td>
        Register subject
      </td>

      <td>
        Allows field users to register new subjects.
      </td>
    </tr>

    <tr>
      <td>
        Subject
      </td>

      <td>
        Edit subject
      </td>

      <td>
        Allows field users to edit previously registered subjects.
      </td>
    </tr>

    <tr>
      <td>
        Subject
      </td>

      <td>
        Void subject
      </td>

      <td>
        Allows field users to void previously registered subjects.
      </td>
    </tr>

    <tr>
      <td>
        Subject
      </td>

      <td>
        Add member\*
      </td>

      <td>
        Allows field users to add a member to household subject.
      </td>
    </tr>

    <tr>
      <td>
        Subject
      </td>

      <td>
        Edit member\*
      </td>

      <td>
        Allows field users to edit previously added household members.
      </td>
    </tr>

    <tr>
      <td>
        Subject
      </td>

      <td>
        Remove member\*
      </td>

      <td>
        Allows field users to remove previously added household members.
      </td>
    </tr>

    <tr>
      <td>
        Enrolment
      </td>

      <td>
        Enrol subject
      </td>

      <td>
        Allows field users to enrol a subject into a program.
      </td>
    </tr>

    <tr>
      <td>
        Enrolment
      </td>

      <td>
        View enrolment details
      </td>

      <td>
        Allows field users to view the program enrolment details for a subject.
      </td>
    </tr>

    <tr>
      <td>
        Enrolment
      </td>

      <td>
        Edit enrolment details
      </td>

      <td>
        Allows field users to edit the program enrolment details for a subject.
      </td>
    </tr>

    <tr>
      <td>
        Enrolment
      </td>

      <td>
        Exit enrolment
      </td>

      <td>
        Allows field users to exit a subject from a program.
      </td>
    </tr>

    <tr>
      <td>
        Encounter
      </td>

      <td>
        View visit
      </td>

      <td>
        Allows field users to view encounters for a subject.
      </td>
    </tr>

    <tr>
      <td>
        Encounter
      </td>

      <td>
        Schedule visit
      </td>

      <td>
        Allows field users to schedule encounters for a subject.
      </td>
    </tr>

    <tr>
      <td>
        Encounter
      </td>

      <td>
        Perform visit
      </td>

      <td>
        Allows field users to perform encounters for a subject.
      </td>
    </tr>

    <tr>
      <td>
        Encounter
      </td>

      <td>
        Edit visit
      </td>

      <td>
        Allows field users to edit previously saved encounter details.
      </td>
    </tr>

    <tr>
      <td>
        Encounter
      </td>

      <td>
        Cancel visit
      </td>

      <td>
        Allows field users to cancel a previously scheduled encounter.
      </td>
    </tr>

    <tr>
      <td>
        Encounter
      </td>

      <td>
        Void visit\*\*
      </td>

      <td>
        Allows field users to void an encounter
      </td>
    </tr>

    <tr>
      <td>
        Checklist
      </td>

      <td>
        View checklist
      </td>

      <td>
        Allows field users to view checklist.
      </td>
    </tr>

    <tr>
      <td>
        Checklist
      </td>

      <td>
        Edit checklist
      </td>

      <td>
        Allows field users to edit checklist.
      </td>
    </tr>
  </tbody>
</Table>

`*` Only for 'Household' subject types

`**` Only available as part of Avni 4.0 release (not a full list)

Some of these privileges imply others. For example, allowing the 'Register Subject' privilege implies that the group will also have 'View Subject' allowed. The system handles these dependencies automatically.

## What if I have a simple setup with no separate users?

You can add all your users to the `Administrators` group.

## Is some data with no access control?

Yes some of the app designer and admin user interface (or non-operational data) is open to all users with read access. This data is not confidential in any of the implementations of Avni, hence this has been kept open for any user with login to the organisation.

## Can users update metadata using the API

No, the server also check for the access privileges of the user.

## Super admin access

Access of super admin is restricted to non-operational data of the organisations. Operational data cannot be viewed as well by super admin. This is to provide visibility to the organisations about who can view their data.


# File: ./readme/Implementers/advanced-feature-guide/app-storage-management-and-sync-disable.md

title: App Storage Configuration and Disable Sync
excerpt: ''
### Need

After an organisation has run Avni for a few years, the amount of data collected over time can be sizeable depending on the scale of the program, number of subjects registered, number of times they were visited etc. Depending on the program objectives and especially for organisations where catchment based division of data is not used or is not effective, all of this historical data may not be of use to a field user who has just joined the organisation and is starting to use Avni. This unnecessary data causes longer initial sync time, slower dashboard loads and increases the storage used by the Avni app on the user's device.

### Solution

In order to address this, implementers can now configure an SQL query which returns the subject ids of subjects which should be disabled from being synced when a sync from the android app is performed.

This configuration can be made via the 'App Designer -> [App Storage Config](https://app.avniproject.org/#/appdesigner/appStorageConfig)' menu. This query is validated to ensure it returns a single numeric column (the subject id) as output.

The query configured via this screen is picked up by a job that runs on a daily basis (configured to run at 2AM IST) which finds subjects based on this query and disables **subsequent sync to android app on user devices** for these subjects and the related entities for these subjects (visits, program visits, entity approval status, subject migration, user subject assignments, relationships, groups, checklists, comments, subject program eligibility etc).

### Example

To disable sync for subjects that were created more than 2 years ago, the query would look like:

`select i.id from public.individual i where i.created_date_time < now() - interval '2 years';`

Remember that this job runs every night so it will keep disabling sync for records that match the criteria on a continuing basis if the condition specified in the query is relative.

### Notes

1. If the subjects (and related entities) are already present on the user device (from a previous sync or via fast sync etc), they are not deleted from the device and the user will be able to view and update them. Updates made to such subjects on the android app will be updated on the server when synced. Other users with access to these subjects will however, not receive these updated records on the android app when they sync.
2. Dashboards on the android app may differ between users having the same sync settings depending on when the respective users synced.
3. DEA users will continue to see these records and will be able to update them and see the updates.
4. No impact to existing reports and exports (sync disabled records will be included).
5. There are constraints in place to prevent the sync disabled value for related entities from becoming different from the sync disabled field for the subject. In order to prevent sync errors, `sync_disabled` should never be updated via SQL query for any entity.
6. Writing a query that looks up tables from the ETL org-specific schema might not have the intended result as the ETL schema is not guaranteed to be in sync with the public schema when the job executes.


# File: ./readme/Implementers/advanced-feature-guide/application-menu.md

title: Application Menu items
excerpt: ''
The customizable "Application menu" feature helps you add a new menu item that will show up on the "More" option of the Android app. 

This new menu item can either be an http link, or a whatsapp number. Popular apps that can be used with this linking scheme are available [here](https://gist.github.com/imbudhiraja/5b0a485fb7f36fb16c9d7d5f19b6ee40)

eg: 

* To open Whatsapp for a number, you would use a url like "whatsapp\://send?text=hello\&phone=xxxxxxxxxxxxx"
* To open a link on youtube, you would use this - youtube://watch?v=dQw4w9WgXcQ
* To open the Avniproject website on the browser, you would use [https://avniproject.org](https://avniproject.org)

### Configuration

In order to set this up, add a row to the menu\_item table. 

```sql Add new menu iterm
INSERT INTO public.menu_item (organisation_id, uuid, is_voided, version, created_by_id, last_modified_by_id,
                              created_date_time, last_modified_date_time, display_key, type, menu_group, icon,
                              link_function)
VALUES (156, uuid_generate_v4(), false, 0, 1, 1, '2022-08-25 11:05:57.791 +00:00',
        now(), 'Support', 'Link', 'Support', 'whatsapp',
        '() => "whatsapp://send?phone=+919292929292"');
```

The link\_function is a function that can create a dynamic url. See [here](https://avni.readme.io/docs/writing-rules#12-hyperlink-menu-item-rule) for more information on how these functions can be written.


# File: ./readme/Implementers/advanced-feature-guide/approval-workflow.md

title: Approvals
excerpt: ''
Avni gives you the ability to review data filled by the field users using approval workflow. Data of each form can be reviewed by the supervisor and comments can be provided to correct the data. Even field users can track what all data filled by them was approved or rejected.

Approval can be configured separately for following Avni entities:

* Individual
* Encounter
* Program Enrolment
* Program Encounter
* Checklists

## Enabling approval workflow

You can enable approval workflow for your organization using the "App Designer" app. Simply go to "Forms" tab and search for the relevant form corresponding to the Entity of interest. Ex: To enable workflow for Subject Type "Demand", we would be clicking on the Gear icon for "Subject Registration" row for Subject "Demand".

<Image alt="Click on Gear Icon of the " align="center" src="https://files.readme.io/1ab51a8-Screenshot_2023-05-31_at_3.09.59_PM.png">
  Click on the "Gear Icon" of the "Subject Registration" Form
</Image>

After that toggle the  "Enable Approval" button to enable / disable the Approval workflow specific to the Entity. Avni gives you the ability to enable this feature at each form level. So if you want you can enable it for some forms and disable it for others.

<Image alt="Toggle the &#x22;Enable Approval&#x22; button" align="center" src="https://files.readme.io/a5e98cf-Screenshot_2023-05-31_at_3.07.47_PM.png">
  Toggle the "Enable Approval" button
</Image>

Apart from enabling the feature we also need to create a custom dashboard so that we can track which all forms are pending, approved, and rejected. You can also mark this dashboard as the primary dashboard from the admin app -> "user groups" -> "dashboard".

<Image title="da.png" alt={1845} align="center" src="https://files.readme.io/a72577b-da.png">
  Approval dashboard to track the forms filled by the field users. All these are standard cards and no custom query is required.
</Image>

Once the approval dashboard is ready and approval workflow is active, every time user fills a form it'll be visible under pending items in the dashboard. The supervisor/reviewing person can review these pending forms and can either approve or reject them. If rejected, the field user will see the rejected form under rejected items and can correct the entries in the form based on the rejection comment provided by the supervisor. After correction, the form will again go for approval and once it is approved it'll start showing under approved items.

<Image title="ada.png" alt={572} align="center" src="https://files.readme.io/e85a870-ada.png">
  Approval dashboard showing pending, approved, and rejected forms.
</Image>

<Image title="ar.png" alt={567} align="center" src="https://files.readme.io/71d38c6-ar.png">
  The supervisor can approve or reject a form after reviewing the details.
</Image>

<Image title="rc.png" alt={576} align="center" src="https://files.readme.io/730dc72-rc.png">
  A rejection comment can be provided to the field user using which they can correct the information.
</Image>

Please note that you can tract the forms only when the approval workflow feature is turned on. If you turn off this feature in between then all the forms filled after that will not get tracked.

### Updates to the Approval Status UI (in development)

Approval items will be grouped by Subjects and arranged in alphabetical order.

[https://github.com/avniproject/avni-client/releases/download/untagged-ccaaf92c54fc9ece8238/Screen.Recording.2023-12-12.at.3.36.38.PM.mov](https://github.com/avniproject/avni-client/releases/download/untagged-ccaaf92c54fc9ece8238/Screen.Recording.2023-12-12.at.3.36.38.PM.mov)

![]()


# File: ./readme/Implementers/advanced-feature-guide/bulk-data-upload-v2.md

title: Bulk Data Upload v2
excerpt: applicable release 13.0 onwards
## Purpose

* Prepare data in bulk, review, and upload.
* Migrating away from an existing implementation, and need to seed with existing data.
* Your organization has a separate component where data is collected outside Avni, but you still need this data to be present with field workers using Avni.

## Using the Admin app to upload data

The Admin app of the web console has an upload option. Currently, this supports the following. Essentially for each form present in you organisation there is a corresponding upload option in the dropdown, with a sample file.

* Upload subjects
* Upload program enrolment (excluding exit information and observations)
* Upload program encounters (excluding cancel information and observations)
* Upload encounters (excluding cancel information and observations)
* [Upload locations](location-and-catchment-in-avni)
* Upload users and catchments
* Upload metadata zip file downloaded from a different implementation

## Sample file

Sample files are available in the interface. Download the file, fill in values and then upload. The file is in a [CSV](https://www.howtogeek.com/348960/what-is-a-csv-file-and-how-do-i-open-it/) format.\
Sample file acts as an up-to-date documentation on the following.

* fields
* whether they are mandatory for upload
* possible values
* format of the value

> 📘 Since above has already been documented and maintain in the sample file these are not documented here again, please refer to it as a reference documentation.

## Mandatory fields in the form

The mandatory fields in the form element are not applicable when uploading the data via CSV files - since we have seen when made mandatory especially for the legacy data, the users are force to upload some junk information (this may be added in the future).

## Rules

No rules are run as part of CSV upload. This implies that:

* field values created automatically via form element rules will not get created (such columns are present in the sample hence can be uploaded manually)
* observations created by decision rules will not be created automatically (such columns are present in the sample hence can be uploaded manually)
* Validation rule is not applied
* Edit rule is not applied

> 📘 Avni currently doesn't have a robust framework to run these rules on the server side. This may be added in future, if we observe that users need these.

## Identifiers

The primary purpose of these identifiers is for the users to be able to link different CSV file types upload data to each  other - in the same way as foreign key linkages between different records. These linkages can be created using identifiers of user's choosing. Lets try to understand this via an example. Lets assume there are three forms.

* Woman Registration (Subject)
* Pregnancy Program Enrolment (Program Enrolment)
  * links to woman
* Ante Natal Visit Form (Program Encounter)
  * links to pregnancy program

<Table align={["left","left","left"]}>
  <thead>
    <tr>
      <th>
        Form
      </th>

      <th>
        Columns
      </th>

      <th>
        Description
      </th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>
        Woman Registration
      </td>

      <td>
        Id from previous system
      </td>

      <td>
        Any unique identifier that you may want to use. Note that you can make this up if you don't already have one. e.g. WOMAN-100001, WOMAN-100002
      </td>
    </tr>

    <tr>
      <td>
        Pregnancy Program Enrolment
      </td>

      <td>
        Id from previous system
      </td>

      <td>
        Any unique identifier that you may want to use. It should unique for all program enrolments. They can be same as woman registration id, but we recommend you use something like e.g. WOMAN-100001-01, WOMAN-100001-02 so that you can use multiple enrolments for the same woman.  

        It is possible that at the time of preparing this data, you are don't plan to upload woman registration via CSV and it is already present in Avni. In such a case you should use the Avni UUID value of the woman registration in this field.
      </td>
    </tr>

    <tr>
      <td>
        Pregnancy Program Enrolment
      </td>

      <td>
        Subject Id from previous system
      </td>

      <td>
        This should be used to match the pregnancy enrolment record woman registration record. Hence, for our example used so far, this field would have values like - WOMAN-100001, WOMAN-100002
      </td>
    </tr>

    <tr>
      <td>
        Ante Natal Visit Form
      </td>

      <td>
        Id from previous system
      </td>

      <td>
        You can leave this blank, if you intention is to create new records only and not edit them.
      </td>
    </tr>

    <tr>
      <td>
        Ante Natal Visit Form
      </td>

      <td>
        Program Enrolment Id
      </td>

      <td>
        This should be used to match the program ante natal visit form record with woman registration record. Hence, for our example used so far, this field would have values like - WOMAN-100001-01, WOMAN-100002-01  

        It is possible that at the time of preparing this data, you are don't plan to upload pregnancy enrolment data via CSV and it is already present in Avni. In such a case you should use the Avni UUID value of the woman registration in this field.
      </td>
    </tr>
  </tbody>
</Table>

> 📘 The identifiers used above, for Id from previous system, are saved in Avni but is not visible in Avni after uploading, it is used only for matching records during CSV upload.

## Scheduling a visit and Upload visit details

Please note that sample file for uploading visit details and scheduling a visit are different. These two options allow for  either creating a scheduled encounter/visit or completed encounter/visit. Note that scheduling a visit and then uploading the visit details for the same visit is not supported (as that is similar to edit).

<Image align="center" className="border" border={true} src="https://files.readme.io/30f7062dbe6572554955d88df13530e6e45c5a4cd5986fd81499661a294f78a2-image.png" />

## Important Notes / Gotchas

* **Limited Concept Support in CSV Upload**: Not all concepts are supported when uploading data via CSV. Specifically, the following are not supported:
  * GroupAffiliation
  * Id
  * File
* **Id Confusion**: The identifiers (used in Id from previous system) are different from Id elements in the form, if you have them.
* **Form Data Editing**: Editing previously submitted form data is not currently supported through the CSV upload process.

# Questions

### What if I have a comma in my observation value?

* Wrap your value in quotes.

### Why are decision concepts not appearing the sample file

If you are using decision concepts in the rule but not linked those concepts then this will happen.

### Is the order of values important?

* No. Columns can be in any order.

### How do I upload images?

* For images, use a url that the avni server can download. Ensure that
  * The images are a direct download link (not a redirect to a page that uses javascript to download)
  * The image urls end with the image type. eg: [https://somedomain.com/images/abc.png](https://somedomain.com/images/abc.png)


# File: ./readme/Implementers/advanced-feature-guide/call-masking.md

title: Masked Calls
excerpt: ''
When a contact number is configured in an implementation (through concept attributes), then the user gets a "Call" button on the subject's dashboard. It is used to open the dialler and make a call to the beneficiary.

With the call masking feature, an implementation can choose to convert this call button into a masked call. There is a user settings toggle to turn this on or off. Under the wraps, Avni can use the Exotel Masked Call feature to make this happen. 

To use this feature, a user needs to purchase an Exophone and configure this in Avni. Configuration is currently done by adding a row to the external\_api table. 

### User flow

* User goes to a subject's dashboard.
* User clicks on the call button
* If call masking is enabled for this user, then the call button makes a call to the server to connect their phone to the beneficiary's number. The user and the beneficiary will get a call from Exotel through which they can talk.
* The user gets a message that the call request was made successfully, and to wait for a call back.
* If call masking is not enabled for this user, then the call button makes a direct call through the dialler.


# File: ./readme/Implementers/advanced-feature-guide/child-growth-charts.md

title: Growth Charts in Avni
excerpt: ''
## Introduction to Child Growth Indicators

Growth charts are essential tools for monitoring the physical development of children. They help healthcare providers assess whether a child is growing properly according to established standards.

Refer to WHO's [child-growth-standards](https://www.who.int/tools/child-growth-standards/standards) for in-depth coverage on all indicators used to assess the growth of a child. These indicators are intended for interpretation primarily by healthcare providers to:

* Investigate causes of growth problems 
* Counsel caregivers on recovery 
* Intervene in urgent high-risk scenarios to avert permanent damage or mortality

The child's age, sex, and measurements of weight and length or height are used to calculate the following growth indicators as per WHO standards for children aged 0 to 5 years:

* **Weight-for-age (WFA)**: Helps identify underweight or overweight conditions
* **Length/height-for-age (HFA)**: Helps identify stunting (low height for age)
* **Weight-for-length/height (WFH)**: Helps identify wasting (low weight for height) or obesity

These measurements should be taken and recorded whenever an infant or child visits a healthcare provider, such as for immunization, well-baby visits, or care during illness.

## Growth Chart Features in Avni

### Supported Indicators

The Avni client application provides growth charts for the following indicators by default:

* Weight-for-age (WFA)
* Length/height-for-age (HFA)
* Weight-for-length/height (WFH)

### Automatic Enablement

In Avni, growth chart monitoring is automatically enabled when a program with the name "Child" or "Phulwari" is created for an organization.

### Manual Enablement

For any other Program, Growth Chart monitoring can be enabled by toggling the "Show Growth Chart" widget to the Program Dashboard.

<Image align="center" src="https://files.readme.io/8e5736a641553e404b24d0ef935974afe08256a0d1a549e3f4e16d22c743bbb8-Screenshot_2025-05-29_at_6.16.30_PM.png" />

### Required Configuration

It is essential for at least a few forms of the types listed below to include concepts with the names **"Weight" and "Height"**. The values recorded for these concepts are then automatically used by the Avni application to plot the Growth Charts.

* Individual   
* Program  
* Program-Encounter     
* Encounter 

## Accessing Growth Charts

Growth Charts are available only in the Avni Client application for:

* Individuals between ages 0 to 5 years AND
* Individuals enrolled in either a program named "Child" or "Phulwari" OR any other Program that has the "Show Growth Chart" widget enabled for it

For eligible children, a "Growth Chart" button will appear on the Program Dashboard.

<Image alt="Growth Chart Button on Dashboard" align="center" width="320px" src="https://files.readme.io/16d426511ff8c27feacc0843fa7a88b1d4fd04e7af7b120fc3897146acc304c1-Screenshot_2025-05-29_at_6.29.01_PM.png">
  Screenshot showing the Growth Chart button on the Program Dashboard
</Image>

Clicking the "Growth Chart" button displays the growth chart with selector buttons at the top, allowing users to choose which specific growth indicator to display for that child.

<Image alt="Weight-for-Age Chart" align="center" width="320px" src="https://files.readme.io/4c985dc341f4e6e2548e784d742da8fba12de51699cdd7487f64f48482bf18a6-Screenshot_2025-05-29_at_6.28.39_PM.png">
  Screenshot of Weight-for-Age growth chart
</Image>

<Image alt="Height-for-Age Chart" align="center" width="320px" src="https://files.readme.io/e0d418b61e5fbd95c51651467c2c3f23f086021fea95bb9ed3ee5eda5a7b3575-Screenshot_2025-05-29_at_6.28.47_PM.png">
  Screenshot of Height-for-Age growth chart
</Image>

<Image alt="Weight-for-Height Chart" align="center" width="320px" src="https://files.readme.io/70cbcdfe31ed6d76c00445dadbfa747db32e6b75af17d9c1cd07c681abbcd262-Screenshot_2025-05-29_at_6.28.51_PM.png">
  Screenshot of Weight-for-Height growth chart
</Image>

## Understanding Growth Charts

### Chart Components

* **Reference Lines**: Standard deviation lines (typically -3SD, -2SD, -1SD, Median, +1SD, +2SD, +3SD) showing expected growth ranges based on WHO standards
* **Data Points**: Plotted points representing the individual's measurements at different ages
* **Connecting Line**: Line connecting the individual's data points to show growth trajectory
* **X-Axis**: Typically represents age in months/years
* **Y-Axis**: Represents the measurement value (weight, height, etc.)

### Color Indicators

Growth Charts use color coding to help quickly identify growth status:

* **Red Zone**: Indicates measurements below -3SD (severe malnutrition or growth faltering)
* **Yellow/Orange Zone**: Indicates measurements between -2SD and -3SD (moderate malnutrition)
* **Green Zone**: Indicates measurements above -2SD (normal/healthy ranges)

## Interpreting Growth Charts

When viewing a growth chart in Avni:

### Weight-for-Age (WFA)

* Measures overall growth and can identify underweight children
* Below -2SD: Moderately underweight
* Below -3SD: Severely underweight
* Current Status: The position of the most recent data point relative to reference lines indicates current nutritional status

### Height-for-Age (HFA)

* Measures linear growth and can identify stunting
* Below -2SD: Moderately stunted
* Below -3SD: Severely stunted
* Growth Trajectory: The direction of the connecting line shows if height growth is improving, maintaining, or declining

### Weight-for-Height (WFH)

* Measures body weight relative to height and can identify wasting
* Below -2SD: Moderate wasting
* Below -3SD: Severe wasting
* Above +2SD: Overweight
* Above +3SD: Obese
* Pattern Recognition: Multiple data points help identify patterns like wasting or weight gain relative to height

## Using Growth Chart Data for Interventions

Based on the growth chart visualization, field workers can:

1. **Identify Growth Patterns**:
   * Normal growth: Data points consistently follow a growth channel
   * Growth faltering: Flattening or downward trajectory of the curve
   * Catch-up growth: Upward trajectory after a period of growth faltering

2. **Take Appropriate Actions**:
   * Normal Growth: Continue regular monitoring and standard care
   * Moderate Concerns (between -2SD and -3SD): Implement nutritional counseling and follow-up monitoring
   * Severe Concerns (below -3SD): Refer for specialized care, nutritional interventions, or further assessment

## Technical Implementation Details

* Growth charts are dynamically rendered based on recorded encounter data
* Charts require accurate recording of birth date and measurement values
* Reference data follows WHO Child Growth Standards
* Charts are available offline once data is synced to the device
* The implementation follows Avni's offline-first architecture, ensuring charts are available even without internet connectivity
* Data points are automatically plotted based on encounter data containing Weight and Height measurements
* Growth charts interface adapts to different screen sizes on mobile devices

## Troubleshooting

If growth charts are not displaying correctly:

1. Verify that concepts named exactly "Weight" and "Height" are included in encounter forms
2. Ensure measurements are recorded in the correct units (kg for weight, cm for height)
3. Confirm the child's date of birth is recorded accurately. Current implementation supports display of Growth Chart only for children aged 0-5 years
4. Check that multiple encounters with measurements exist for proper trend visualization
5. Sync your device to ensure you have the latest program configuration
6. Verify that the program name is either "Child" or "Phulwari" to enable Growth Chart functionality automatically. For other programs, Growth Chart functionality can be enabled by toggling the "Show Growth Chart" widget to the Program Dashboard

## Summary

Avni's Growth Chart functionality provides a powerful tool for field workers to monitor and assess child growth in accordance with WHO standards. The offline-first implementation ensures that these critical assessment tools are available even in areas with limited connectivity, aligning with Avni's core mission of supporting field workers in remote areas.

By following the simple configuration requirements and understanding how to interpret the charts, organizations can effectively track child growth and development, enabling timely interventions when needed.


# File: ./readme/Implementers/advanced-feature-guide/comment-workflow.md

title: Comment workflow
excerpt: ''
This is an issue resolution mechanism provided by Avni which helps to fix the mistakes in the record. Comment workflow helps to pinpoint the exact subject for which data correction is required. This saves a lot of time the user spends searching for that subject.

## Enabling comment workflow

Comment workflow can be enabled from the admin app. Simply go to organisation details and switch on "enable comments" option.

<Image title="comment.png" alt={1848} src="https://files.readme.io/548038c-comment.png">
  Enable comments option in the admin app
</Image>

Once this feature is enabled users will start seeing the comment icon on the subject dashboard. They can click on the icon to open all the comment threads of the subject. They can perform the following operations on the comment screen.

* Open a comment thread and read all the comments on that thread.
* Reply to a comment thread.
* Mark a comment thread as resolved, if the issue is resolved.
* Open a new comment thread by pressing add icon.

<Image title="comment screen.png" alt={574} src="https://files.readme.io/f1a3a13-comment_screen.png">
  Comment screen showing one open thread. Users can see all the comments in a thread by clicking on that thread.
</Image>

**Useful tips** 

* When comment workflow is enabled, ensure that a standard report card of type "comments" is added to the dashboard. This will help users to see only the comments threads which are open and they need to work on.


# File: ./readme/Implementers/advanced-feature-guide/creating-identifiers.md

title: Autogenerated Ids
excerpt: ''
    - type: basic
      slug: upload-checklist
      title: Upload checklist
---
### Identifiers

Identifiers are unique strings generated by the system, which can be used to identify a beneficiary. Usually, these have special patterns - prefixes, suffixes, special numbering patterns etc, which aid users in understanding a beneficiary. 

### ID Generation in Avni

In usual systems, identifiers are generated from a central place because we need them to be unique. However, the Avni Android app is expected to work offline. Offline ID generation is possible, but is done differently. IDs in Avni are generated in batches and sent to a user. 

There is a special form element type called ID. If you configure a form element to be of ID type, then the Avni android app will automatically retrieve the next ID from this batch and assign it as the value. 

*Advanced* - It is also possible to create rules that modify the final ID that is stored for the beneficiary. For example, if there is the need of adding a date to the final ID being generated, you would write a ViewFilter rule that will use the generated ID and append a date to it. 

### Identifier sources

It is possible to have multiple IDs being generated at the same time. Each ID type is called an identifier source. An identifier source will have a certain type (discussed later), prefix (optional), minimum and maximum lengths and can be assigned to a  catchment.\
The type of an identifier source determines the strategy used to generate IDS of that source. There are currently two types available. The only difference between them is the place where the prefix is stored. 

1. User pool based identifier generation - Here, a pool of users within a catchment share the same prefix. The prefix is stored within the identifier source within options. Every user asking for ids is provided with a set of ids prefixed with this value. 
2. User based identifier generation - Here, the prefix is stored in the "idPrefix" value of the user's settings.

### Rules

1. User pool based identifier generation - overlaps in ID for the same identifier source not allowed.
2. User based identifier generation - Two users in the same organisation cannot have same prefix. This check is case in-sensitive.

Queries to analyse existing data is available here - [https://github.com/avniproject/avni-webapp/issues/1022#issuecomment-1693064436](https://github.com/avniproject/avni-webapp/issues/1022#issuecomment-1693064436)

### Tutorial

#### 1. Create Identifier Source from admin section:

1. Give name
2. Choose type - User pool based identifier generator or User based identifier generator. Difference between the two is explained above.
3. Choose catchment
4. Choose batch generation size. This is the number of identifiers that will be generated at once and be sent to client app on sync. If your field users can not sync for a long time then you should estimate how many identifiers they may need.
5. Choose minimum balance. This is useful to make sure that your users get a warning to sync before they run out of identifiers.
6. Choose Min length and max length. This specifies the min and max length of the generated identifiers.
7. You will get an option to add Prefix if you chose User Pool Based Identifier Generator in the Type field(1.2). This prefix will be shared by all identifiers generated for users sharing the same identifier source.

#### 2. Create Identifier User Assignment from admin section:

1. Choose User. The user that you select will start getting auto-generated ids  once they Sync.
2. Choose Identifier Source. This is the resource that you created in Step 1 above(Create Identifier Source from admin section).
3. Enter initial identifier to be generated for this user. It should also include the prefix. E.g. if you had set the prefix to be ANC and min length to be 3, and you want the identifiers to start from 100 then the value of this field could ANC100.
4. Enter last identifier to be generated for this user. System will not generate any identifiers beyond this. E.g. If your prefix is ANC, max length is 4 and you want identifiers only till 2000 then this could be ANC2000.

#### 3. Create a question in the form with concept type Id

1. In the form where you want the auto generated identifier, do create a question with concept type Id and select the identifier source.


# File: ./readme/Implementers/advanced-feature-guide/custom-fields-in-search-results.md

title: Custom fields in search results
excerpt: ''
Avni app has the capability to setup [custom search filters](https://avni.readme.io/docs/my-dashboard-and-search-filters), but the results do not show any of these fields. Using this feature one can add additional fields to the search result.

## Setting up custom fields in search results

1. In the app designer go to Search Result Fields and select the subject type for which you want to setup the custom search result fields.
2. Next From the dropdown choose the concept name.
3. You can reorder the custom search fields by drag and drop and finally save the changes.
4. Sync the mobile app and you should see the newly added concept in the search result field.

![1031](https://files.readme.io/8c14b56-custom-search-result-fields2.gif "custom-search-result-fields(2).gif")

**Note**: Only concepts in the registration form are supported.\
**Supported data types**: Text, Id, coded, numeric, and date.


# File: ./readme/Implementers/advanced-feature-guide/documentation.md

title: Form Documentation
excerpt: ''
Custom documentation can be created in Avni. Documentation supports rich text and can be written in different\
languages supported by an organization. Right now you can also link particular documentation to a form element and it'll show up in the mobile app. This is useful where more context is required for any question.

## Steps to configure and link documentation

The below GIF displays how documentation can be created and linked to a form element.

<Image title="Documentation-linking.gif" alt={1851} src="https://files.readme.io/d2a237f-Documentation-linking.gif">
  Configuring and linking documentation
</Image>

Once documentation is linked to the form element, it'll start appearing in the mobile app. Users can expand and close the documentation while filling out the form.

<Image title="form-element-documentation.png" alt={568} src="https://files.readme.io/542e811-form-element-documentation.png">
  Documentation on the mobile app.
</Image>


# File: ./readme/Implementers/advanced-feature-guide/draft-save.md

title: Draft save
excerpt: ''
Sometimes we have huge forms and all the information is not available when you start capturing the data of such forms. Avni gives you the facility to save the half-filled form as a draft. These draft forms are not synced to the server, and once you fill the form completely draft is automatically deleted.

## Enabling Draft save

You can enable draft to save for your organization using the admin app. Simply go to "organisation Details" and enable "Draft save".

![](https://files.readme.io/d824dc2-draft_save.png "draft save.png")

Once the "draft save" feature is enabled you can see the half-filled forms in the registration tab in the field app. Please note that these drafts will get if the draft is left untouched for more than 30 days.

It gets converted into a regular Subject or Encounter on pressing Save button during modification of a draft.

![](https://files.readme.io/8386271-d.png "d.png")

## Key points

* **Applicability:** Currently, this feature works only for the registration and encounter forms. So Program enrolment and program encounter forms won't get saved as a draft if left in middle.
* **Display:** Registration drafts are displayed on the Register screen. Encounter drafts are displayed under the on the 'General' tab on the Subject Dashboard. Unscheduled encounter drafts are displayed under the 'Drafts' section and scheduled encounter drafts are accessible by tapping 'Do' on encounters under the 'Visits Planned' section.
* **Save Checkpoint:** A draft save action is performed on clicking "Next" or "Previous" buttons while filling in a form, therefore, if User fills in a page but does not click on "Next" or "Previous" buttons, then the Draft saved would have content only till the previous page (On which "Next" button was clicked)
* **Exiting a form:** To exit from a form in-between, user may click on the "Header" "Back" button or click on "Footer" "Home" buttons\*\*
* **Stale Drafts clean-up:** Usually drafts get deleted once you perform a final save operation to convert it to an actual entity. Along with that we have a periodic drafts clean-up which gets executed once a day, to delete drafts that were last updated more than 30 days ago.


# File: ./readme/Implementers/advanced-feature-guide/encryption-of-data-on-the-android-app.md

title: Encryption of data on the Android app
excerpt: ''
Some implementations require a higher level of security, which includes encryption of the database on Android. 

### How to enable encryption:

To have all the users field app database encrypted, the option for encryption need to be enabled under `Organisation Details`  as shown in the image below. Users would be in need to sync the app, to reflect the encryption setting change.

<Image align="center" src="https://files.readme.io/e132e70-Screenshot_2023-08-14_at_4.24.22_PM.png" />

### Side-effects of using the feature:

* As shown in the warning message in the image above, enabling this feature will not permit the user to use [fast sync](https://avni.readme.io/docs/fast-sync) and upload db feature from the Menu options on the field app.
* After the option is enabled, it can be disabled anytime on change of mind. 

### Developer debug notes:

* To see the data of encrypted realm db, print out the commented out line that calculates `hexEncodedKey` in the `EncryptionService`. And use the printed value to open the realm db when it asks for the encryption key as shown in the image below.

<Image align="center" src="https://files.readme.io/e79ad32-Screenshot_2023-08-09_at_4.41.56_PM.png" />


# File: ./readme/Implementers/advanced-feature-guide/etl-schema-and-reporting.md

title: ETL schema, reporting and management
excerpt: ''
The public datamodel is not suited for easy reporting because of a few reasons. 

1. jsonb fields 
   1. Cannot be indexed because GIN index and RLS do not work well with each other
   2. Cannot be easily explored because of the way it is setup
2. Analytic queries typically require full table scans, and reducing the data to just one organisation makes it easier
3. Address fields are hierarchical, and are not easy to handle for reports. Especially when we need grouping by different levels of address
4. Many times, pre-created rollups might help make reports easier

### The ETL service

The Avni ETL service fixes the above problems by moving data to a denormalized database that is suited for reporting. It creates tables of the form

* For all subject types, a table called \<subjectType\>
* For all general encounters, a table called \<subjectType\>\_\<encounterType\> and \<subjectType\>\_\<encounterType>\_cancel
* For all programs, a table called \<subjectType\>\_\<programName\> and \<subjectType\>\_\<programName\>\_exit
* For all program encounters, a table called \<subjectType\>\_\<programName\>\_\<encounterType\> and \<subjectType\>\_\<programName\>\_\<encounterType\>\_cancel
* An address table for all addresses
* A media table for all media
* For every Repeatable Question Group present for an entity(Subject, Encounter, ProgramEnrolment or ProgramEncounter), we'll have a separate secondary table called  \<parentTable\>\_\<question\_group\_concept\_name\>

#### Other details of the service

* Data is moved from the public schema to a schema defined by the schemaName of the organisation
* Data is moved incrementally every hour
* Analytics needs to be enabled for an organisation in order for it to work (from the Organisation edit screen of Admin)

### Management of ETL process for an organisation

ETL management for an organisation is only available for support users and not to the users of the organisation itself including administrators. You require super admin login to perform these activities.

* ETL can be enabled or disabled from the organisation edit screen.
* In organisation listing the enable disable status is displayed. One can also open an organisation to check the status. Note: that in listing the status is sometimes shown as blank. This is a defect but we have not been able to fix it. In such a case please check organisation show screen.
* If you want to run the ETL process immediately for an organisation (for which it is already enabled) - then you need to disable and enable. The rescheduling of the job will cause it to run after 10 seconds of enabling.

### Checking error of ETL job of an organisation

GET `{{origin}}/etl/job/{{orgUUID}}` with `auth-token` in header for super admin user.

e.g. [https://app.avniproject.org/etl/job/392bcc3e-0b04-495c-861a-64589d2692b4](https://app.avniproject.org/etl/job/392bcc3e-0b04-495c-861a-64589d2692b4)

You can find replace \\n\\t with newline to get a clearer stack trace.


# File: ./readme/Implementers/advanced-feature-guide/extension-points.md

title: Extensions
excerpt: ''
Extensions are points in Avni where custom html can be used to enhance functionality. There are a few such predefined points where custom html can be inserted. 

In Data Entry App

* Subject Dashboard
* Subject Dashboard for a specific program
* Search Results page

In the Field-App

* Splash Screen

## Creating Extensions

### Creating the extension

In order to create an extension, first you need to create a web app. For each extension point, there will be parameters that you will receive that can be used for custom behaviour. Data can be fetched from the database using the Avni API.

Parameters

* Subject Dashboard - subjectUUIDs (subject's uuid), token (auth token)
* Search Results page - subjectUUIDs (Comma separated list of subjects that have been selected), token
* Splash screen - nothing

The token field must be added as a header AUTH-TOKEN in case you need to use the public API to interact with the Avni server.

### Adding the extension on the App Designer

Extensions can now be added to Avni through the app designer ([https://app.avniproject.org/#/appdesigner/extensions](https://app.avniproject.org/#/appdesigner/extensions)).\
All your extensions must be zipped and uploaded on this screen. You can enter the name of the extension, the file name in the zip file that must be rendered (use relative paths if your HTML file is within a directory), and the type of extension (called Extension Scope). 

![](https://files.readme.io/e772f7d-Screenshot_2021-10-27_at_10.58.02_AM.png "Screenshot 2021-10-27 at 10.58.02 AM.png")


# File: ./readme/Implementers/advanced-feature-guide/fast-sync.md

title: Fast sync
excerpt: ''
When setting up Avni freshly on an android device the first-time sync can take a lot of time, especially if you have a lot of transactional data for the catchment. To make this process faster Avni provides an option to set up fast sync for a catchment.

The performance of syncing data from the server to the local mobile database is dependent on the volume of data - hence cannot be improved significantly. Hence fast sync depends on using the already synced mobile database file as the starting database for other users. This significantly improves the sync duration to less than 5 minutes in most cases.

There are few things to note before we start setting up fast sync.

* Fast sync is set up for a catchment, so if there is a new user in a catchment called "a" then any existing user of the catchment "a" should set up the fast sync from their device.
* Fast sync does not update automatically, which means if the user has set up fast sync one month earlier, then all the data filled after that will get downloaded by the regular sync. So it is recommended to update the fast sync whenever any user is freshly setting up the Avni on their device.
* Fast sync is triggered only when the user is syncing for the first time. So if the user has not logged in for a long time, then it is recommended to delete all the app data and log in again to use the fast sync.

## Setting up fast sync

.Setting up fast sync is very easy and it requires an active internet connection. Existing users can go to "More -> Setup fast sync" and then click "Yes". This will take a while depending on the data in the device. This uploads the database file from the user's device to Avni storage as fast sync file for this catchment.

<Image title="fast sync.png" alt={568} align="center" src="https://files.readme.io/125e0b2-fast_sync.png">
  Fast sync setup option.
</Image>

Once it is done, the new user from the same catchment will get an option to use the fast sync when he logs in for the first time.

<br />

## Verification of Existence of Fast-Sync file

Steps to follow:

1. Figure out Catchment UUID corresponding to the User facing the issue
2. Login into AWS and open up the S3 Console 
3. Navigate to "s3/buckets/\<env\>-user-media/\<org\_media\_bucket\_name\>"
4. There the FastSync files will have prefix of "MobileDbBackup-" followed by Catchment UUID Ex: "MobileDbBackup-b9103c96-7ed7-4798-a866-89419103d361"
5. Download the file and unzip if needed to check size / content

<br />

<Image align="center" src="https://files.readme.io/f6786a7c51e3bdc43bdb24a7960bc74cd7b38af163ec88dc8685f7fe46c395f2-Screenshot_2025-04-03_at_1.14.45_PM.png" />

<br />

## Perils of Fast Sync

"Fast sync" speed up the initial sync and improves new user onboarding experience. But the flip-side of setting up "Fast Sync" are as follows:

* "Fast Sync", if setup using a newer version of app, prevent fresh logins from older version of the app
* "Fast Sync", is setup per Catchment basis, so, if there are restrictions due to Sync-Concept-Values or UserGroup Privileges for one set of users and they have the FastSync Setup for them, then the other set of Users with conflicting Sync-Concept-Values or UserGroup Privileges might end up receiving invalid data / missing data during sync
* "Fast Sync", when setup, assumes that the Catchment constituent Locations are fixed, any change to the catchment results in a "Reset Sync" being created for all users which are associated with that catchment. But new users who get assigned to that Catchment, will not have the "Reset Sync" configured appropriately in all cases, this could result in missed / extraneous data sync happening to the new users.
* "Fast Sync" data cannot be modularly distributed to users of different catchment with overlapping location boundaries. You would have to spearately setup Fast sync for each catchment.
* There is no easy way for Organisation users to remove a "Fast Sync" setup for a Catchment, he should either over-write it with a new "Fast Sync" file, or contact Support team for deletion of old one. To be able to overcome the Sync failure error, you would need to do:
  * Either do "Fresh login" after that(Deletion / overwrite of FastSync file)
  * Or continue and "Perform Slow Sync"

<Image alt="Fast Sync Failure due to Version mismatch" align="center" width="450px" src="https://files.readme.io/a2bce3187fea665854c9d179dc43c9597a0dfff81f3eec23b77626bb5af2aacd-Screenshot_20250410_184143.jpg">
  Fast Sync Failure due to Version mismatch
</Image>


# File: ./readme/Implementers/advanced-feature-guide/flavouring-avni.md

title: Rollout your own Avni App from Play store
excerpt: Branding options available in Avni, and how to proceed
There are can be several reasons for rolling out your own app from the play store.

* You have a different deployment of Avni
* You want your own branding (icons, logos, etc)

You can change the following

1. App logo
2. App name
3. Splash screen (Splash screen is done through [extensions](doc:extension-points))

You may be required to change the following, if your hosting is not managed by Samanvay or not planned to be managed by Samanvay in future.

1. Firebase configuration
2. Bugsnag configuration
   1. Create an account in Bugsnag and create a project of type React Native.
   2. Get the Notifier API key from the project settings

A new app is called a flavor of the app (terminology from [Android flavors](https://developer.android.com/build/build-variants)). There are a few flavors already configured today. This configuration is done in the [avni-client](https://github.com/avniproject/avni-client) repository.

## Steps:

1. [Create new flavor in android-client](https://avni.readme.io/docs/flavouring-avni#steps-to-create-a-new-flavor-in-client)
2. [Configure to get build from circle-ci](https://avni.readme.io/docs/flavouring-avni#steps-to-do-in-to-get-build-via-circle-ci)
3. [Steps to follow in google playstore](https://avni.readme.io/docs/flavouring-avni#steps-to-do-in-google-play-store)

### Steps to create a new flavor in client:

* Under `packages/openchs-android/android/app/src`, create a folder with the flavor name.
  * Flavor naming conventions:
    * Use camelCase for flavor name, since it is used in the android [docs](https://developer.android.com/build/build-variants).  This is also inline with the folder names generated during the build process.
    * The flavor name, need not have org name, just app name will suffice. 
    * Eg: for `Teach Nagaland` app from LFE, the flavor name can be `teachNagaland` and not `teach_nagaland` or `lfeTeachNagaland`.
  * Under `assets` folder add `logo.png`. The file needs to be in `png` format for the animation in the screensaver to work and for the logo to appear in the Login page.
    * To resize the logo to a reasonable size, `Preview` app can be used. Open the file and go to `Tools -> Adjust Size`.
    * To convert the logo from say, jpg to png format, open the file, then go to `File -> Export -> Change the format to png -> Save`.
  * Under `res` folder, create folders for each resolution. This images in this folder is used to display launcher icon in android app. This [website](https://icon.kitchen/) can be used to generate circle and square icons for each resolution.
  * To integrate with firebase analytics, copy `google-services.json` from [firebase console](https://console.firebase.google.com/u/0/) by creating a project specific to the flavor or an app within an existing project as per need. To view data of an app within a project, you can : Add comparison > Dimension = "Stream name" > Match Type = "exactly matches" > Value: select your app via checkbox
  * When some resources are common across flavors, add it under `packages/openchs-android/android/app/src/main` folder (instruction for Avni product team only)
  * Add a flavor specific privacy policy under `docs` to be linked to from the play store app listing using the Avni privacy policy as a reference and make changes specific to the flavor such as app name.
* Changes to be made in `build.gradle`
  * Add the `signingConfig` for the new flavor. To create keystore, check [here](https://developer.android.com/studio/publish/app-signing#generate-key) or use the following command.
    * `keytool -genkey -v -keystore <flavor>-release-key.keystore -storepass <keystorepassword> -alias <alias> -keypass <keypassword> -keyalg RSA -keysize 2048 -validity 10000`
  * In `packages/openchs-android/android/app/build.gradle`, under `productFlavors` add the key value pairs for the new flavor. 
    * For applicationId, use the format, `com.openchsclient.{client_name}.{region_name}`, where `region_name` need to be given if different flavors of the app exists for different regions.
    * create new bugsnag app, and add its API key.
  * Using `sourceSets` config in the `build.gradle`, modules specific to flavors can be configured.
* In `flavor_config.json` add the config for the new flavor. The values here are used by make tasks.
  * super admin password of the server url need to be mentioned as value for `prod_admin_password_env_var_name` .

### Steps to do to get build via circle-ci:

* Update `.circleci/config.yml` to add flavor to enum of valid `flavors`.
* Add environment variables.
  * Go to `Project Settings -> Environment variables` in circleci.
  * Add values for key password (`<flavor>_KEY_PASSWORD`), key store password (`<flavor>_KEYSTORE_PASSWORD`), key alias (`<flavor>_KEY_ALIAS`), bugsnag api key.
* Refer this [link](https://avni.readme.io/docs/release-process-for-the-cloud#circleci-build) to know how to generate apks and aab from circle-ci for specific flavor.

### Steps to do in google play store:

* Create app on google play console.
* Under `Grow -> Store Presence -> Main store listing` and enter the details. For phone and tablet screenshots, same screenshots can be uploaded.
* Under `Grow -> Store settings`, enter the details similar to other app.
* Go to `Publishing overview` and finish the steps mentioned to be able to publish for review.
  * For privacy policy, make sure the privacy policy mentions the name of the app instead of `Avni`.
  * To complete the steps take the help of already filled values of other apps. For that refer, `Policy and programmes -> App content -> Actioned` 
* Create release. 
  * As per this [link](https://stackoverflow.com/questions/73132752/i-dont-use-ads-in-my-flutter-app-then-why-this-message-is-showing-in-my-play-co), seems like Firebase Analytics plugin needs permission `com.google.android.gms.permission.AD_ID`. Hence click `Yes` for `AD_ID` permissions and check `Analytics` for usage.
  * Upload the bundle downloaded from the playstore.
* Send the changes made above for review.

### How to use a specific flavor:

By default, generic flavor without organisation branding will be picked up . When need to run make tasks for specific flavor, pass the flavor variable to the make task.

Eg: ` make run_app_staging flavor='apf'`

### Other branding changes in Avni that are relevant

There are other places where icons/colours can be configured. Below is a table that summarizes the changes that are possible. All changes can be performed through the App Designer.

| Type   | Item              | Specifications                                                                                                |
| :----- | :---------------- | :------------------------------------------------------------------------------------------------------------ |
| Icon   | Subject Type Icon | jpg/png square images 75 \* 75 px                                                                             |
| Icon   | Report card       | jpg/png square images 75 \* 75 px                                                                             |
| Icon   | Menu Item         | Material Community Icon from [https://pictogrammers.com/library/mdi/](https://pictogrammers.com/library/mdi/) |
| Colour | Program           | RGB                                                                                                           |
| Colour | Report Card       | RGB                                                                                                           |
| Colour | Form Header       | RGB                                                                                                           |


# File: ./readme/Implementers/advanced-feature-guide/importing-excel-data.md

title: Excel-based migration [Deprecated]
excerpt: ''
> ❗️ Avni does not support Excel based import any longer, please refer to Admin App based approach to upload data [Bulk Data Upload page](https://avni.readme.io/docs/upload-data#is-the-order-of-values-important)

> 🚧 Introduction
>
> Read [https://avni.readme.io/v2.0/docs/structure-import-metadata-excel-excel](https://avni.readme.io/v2.0/docs/structure-import-metadata-excel-excel)

**Note: dates get parsed incorrectly sometimes while converting from CSV to XLSX in Google Sheets (Eg. 12-01-2018 (dd-mm-yyyy) gets parsed as 01/12/2018) which may not be easy to spot. One solution is to download the CSV file and convert to XLSX in LibreOffice.**

[An example of Metadata.xlsx file](https://docs.google.com/spreadsheets/d/1M0QvcgZ7TagcHvMnTSo3qt-sZHwUDHEiN0T2hlKTn9Y/edit?usp=sharing)\
[An example of Data.xlsx file](https://docs.google.com/spreadsheets/d/19aCEIlODNvJMR68_mGl4Q-Kx6n3qI0Dk4hL0aQ8dwAo/edit?usp=sharing)


# File: ./readme/Implementers/advanced-feature-guide/integration-service-operations.md

title: Integration Service Operations
excerpt: ''
Please refer to the [Integration design and developer guide](doc:integration-developer-guide) for - how to develop integration code. This guide describes how to operate and support the integration service

### Managing Metadata Mapping

When new fields or sometimes entity types come up in the system or incorrect mapping needs to be fixed, then the one can use the Metadata Mapping tab to do so. For all entities and fields in Avni name/title is used. For other system it could be UUID or some other identifier. When providing the field mapping one should provide the parent entity type of the field.

### Integration job monitoring

* Background jobs can be monitored via [https://healthchecks.io/](https://healthchecks.io/). The failure here indicates that the background job didn't complete in time. It could be because the job didn't run, or it hung, or it failed with error. A ticket can be raised or product team support can be taken when this happens.
  * If it failed for error then the error can be checked in Bugsnag. The stack trace and link to the error can be put in the ticket. Usually these should be urgent tickets.

### Business Error monitoring

The integration module is coded to handle business errors. These are also called classified errors. The errors can be viewed from the Error tab in the admin app. The operations team should ignore these errors when the system is handed over to the customer. The customer is responsible for looking at classified errors and fixing them by fixing the data.

The classified errors are due to data in Avni or the integrated system - never in the integration service module. If this is not the case then product team should be informed.

For each classified error the required action must be available in the document as to how to rectify them.

In most integration systems, these errors are frequent - hence no specific monitoring has been put up for this. But it can be if required.

### Frequency of scheduled job

Each module has two scheduled jobs - for regular and error processing. The regular job performs synchronising in both directions (if applicable). These jobs can be run more or less frequently via the system environment variable of the integration service.


# File: ./readme/Implementers/advanced-feature-guide/my-dashboard-and-search-filters.md

title: My Dashboard and Search Filters
excerpt: ''
    - type: basic
      slug: translation-management
      title: Translation Management
---
Avni allows the display of custom filter in **Search** and **My Dashboard filter** page. These settings are available within App designer. Filter settings are stored in organisation\_config table.  You can define filters for different subject types. Please refer to the table below for various options.

# Filter Types

<Table align={["left","left","left"]}>
  <thead>
    <tr>
      <th style={{ textAlign: "left" }}>
        Type
      </th>

      <th style={{ textAlign: "left" }}>
        Applies on Field
      </th>

      <th style={{ textAlign: "left" }}>
        Widget Types
      </th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td style={{ textAlign: "left" }}>
        Name
      </td>

      <td style={{ textAlign: "left" }}>
        Name of the subject
      </td>

      <td style={{ textAlign: "left" }}>
        Default (Text)
      </td>
    </tr>

    <tr>
      <td style={{ textAlign: "left" }}>
        Age
      </td>

      <td style={{ textAlign: "left" }}>
        Age of the subject
      </td>

      <td style={{ textAlign: "left" }}>
        Default : Numeric field. Fetches result matching records with values +/- 4.
      </td>
    </tr>

    <tr>
      <td style={{ textAlign: "left" }}>
        Gender
      </td>

      <td style={{ textAlign: "left" }}>
        Gender of the subject
      </td>

      <td style={{ textAlign: "left" }}>
        Default : Multiselect with configured gender options.
      </td>
    </tr>

    <tr>
      <td style={{ textAlign: "left" }}>
        Address
      </td>

      <td style={{ textAlign: "left" }}>
        Address of the subject
      </td>

      <td style={{ textAlign: "left" }}>
        Default : Multiselect option to choose the address of the subject. Nested options appear if multiple levels of address are present. e.g. District -> Taluka -> Village.
      </td>
    </tr>

    <tr>
      <td style={{ textAlign: "left" }}>
        Registration Date
      </td>

      <td style={{ textAlign: "left" }}>
        Date of Registration of the subject
      </td>

      <td style={{ textAlign: "left" }}>
        Default : Fixed date\
        Range : Options to choose Start date and End date
      </td>
    </tr>

    <tr>
      <td style={{ textAlign: "left" }}>
        Enrolment Date
      </td>

      <td style={{ textAlign: "left" }}>
        Date of Enrolment in any program
      </td>

      <td style={{ textAlign: "left" }}>
        Default : Fixed date\
        Range : Options to choose Start date and End date
      </td>
    </tr>

    <tr>
      <td style={{ textAlign: "left" }}>
        Encounter Date
      </td>

      <td style={{ textAlign: "left" }}>
        Date of Encounter in any Encounter
      </td>

      <td style={{ textAlign: "left" }}>
        Default : Fixed date\
        Range : Options to choose Start date and End date
      </td>
    </tr>

    <tr>
      <td style={{ textAlign: "left" }}>
        Program Encounter Date
      </td>

      <td style={{ textAlign: "left" }}>
        Date of Program Encounter in any Program Encounter
      </td>

      <td style={{ textAlign: "left" }}>
        Default : Fixed date\
        Range : Options to choose Start date and End date
      </td>
    </tr>

    <tr>
      <td style={{ textAlign: "left" }}>
        Search All
      </td>

      <td style={{ textAlign: "left" }}>
        Text fields in all the core fields and observations in Registration and Program enrolment
      </td>

      <td style={{ textAlign: "left" }}>
        Default : Text Field
      </td>
    </tr>
  </tbody>
</Table>

#### Limitation: Right now we cannot have multiple scopes for a filter, i.e. we cannot search a concept in program encounter and encounter with the same filter.

# Users need to sync the app for getting any of the above changes.


# File: ./readme/Implementers/advanced-feature-guide/new-longitudinal-export.md

title: New Longitudinal export
excerpt: Guide for New Longitudinal Export
## Introduction

The “New Longitudinal export” feature allows for an Implementation Admin user to extract data in Longitudinal format for a specific Subject Type. All invoked requests are listed at the bottom of the “New Longitudinal export” screen, which also includes Status information. The export requests are processed asynchronously in the backend and upon completion they are uploaded to cloud and are available for download in the same screen in-line with the request status details.

New longitudinal export fixes the following issues with old export.

* Inability to fetch data across different forms for the same subject. eg: Fetch data from two different encounter types on the same program
* Inability to fetch group/household information
* Inability to fetch only selected fields from different forms

### Limitations

* There is a limit of maximum of 10,000 Individuals data that could be exported at once, as part of a single Longitudinal export request

## Presupposition

In-order for an Implementation admin user to be able to successfully invoke a “New Longitudinal export” request, he / she would need to have the following:

* Basic understanding of JSON syntax
* Understanding of Avni Entity Types and their inter-relationships

## Preparation

Implementation Admin would need to come up with a list of UUIDs corresponding to Entity Types and Concepts whose data should be included in the exported file.

In-order to fetch this, the most accessible approach is the Avni Webapp. The concept uuid is shown in the address bar, where-as the Entity type (Individual) UUIDs are available on inspecting the network response, as shown in the screenshot below.

![Reference Screen-shot for fetching UUID for Subject type](https://files.readme.io/487a1fa-Screenshot_2023-05-30_at_6.43.42_PM.png)

For Avni Internal team members, they can connect to the DB and invoke appropriate SQL queries to fetcht the UUID information.

```Text SQL
#Query to fetch concept names and UUIDs
set role <org_db_user>;
select
    f.name  as FormName
    -- ,fm.entity_id
    -- ,fm.observations_type_entity_id
    -- ,fm.organisation_id
        ,
    feg.name,
    fe.name as "Form Element",
    c2.name as "Concept"
from form f
         inner join form_element_group feg on feg.form_id = f.id
         inner join form_element fe on fe.form_element_group_id = feg.id
         inner join concept c2 on fe.concept_id = c2.id
order by
    f.name
       , feg.display_order asc
       , fe.display_order asc;
```

## Request Payload Format

```sql JSON
{
  "individual": {
    "uuid": "<Specify Subject Type's UUID>",
    "fields": [
      "id",
      "uuid",
      "firstName",
      "registrationDate",
      "gender",
      "dateOfBirth"
    ],
    "filters": {
      "addressLevelIds": [],
      "date": {
        "from": "2020-01-12",
        "to": "2022-05-04"
      }
    },
    "encounters": [
      {
        "uuid": "<Specify Encounter type's UUID>",
        "fields": [
          "id",
          "encounterDateTime",
          "cancelDateTime",
          "uuid",
          "name",
          "voided",
          "<Specify Encounter's Concept UUID>"
        ],
        "filters": {
          "includeVoided": true,
          "date": {
            "from": "2020-01-12",
            "to": "2022-05-04"
          }
        }
      }
    ],
    "groups": [
      {
        "uuid": "<Specify Group Subject Type's UUID>",
        "fields": [
          "id",
          "uuid",
          "firstName"
        ],
        "encounters": [
          {
            "uuid": "<Specify Group Subject's Encounter Type UUID>",
            "fields": [
              "id"
            ]
          }
        ]
      }
    ],
    "programs": [
      {
        "uuid": "<Specify Program's UUID>",
        "fields": [
          "id",
          "uuid",
          "enrolmentDateTime"
        ],
        "encounters": [
          {
            "uuid": "<Specify Program Encounter's UUID>",
            "fields": [
              "id",
              "uuid",
              "name",
              "encounterDateTime",
              "cancelDateTime",
              "voided",
              "<Specify Program Encounter's Concept 1 UUID>",
              "<Specify Program Encounter's Concept 2 UUID>"
            ],
            "filters": {
              "includeVoided": true
            }
          }
        ]
      }
    ]
  },
  "timezone": "Asia/Calcutta"
}

```

## Description of elements that can be used to compose a Export request

```c <ROOT> (The root JSON element)
- "individual" : "<Specify Subject Type request details>"
- "timezone" : "<Specify timezone to adhere while displaying date fields>"
```

```c "individual” (Request details of the Subject Type for which data has to be extracted)
- "uuid" : "<Specify Subject Type's UUID>"
- "fields" : "<Specify fields on subjects to be included in the export>"
- "filters" : "<Specify filters applicable on subjects to be included in the export>"
- "encounters" : "<Specify General Encounter Types request details>"
  -- "uuid" : "<Specify Encounter Type's UUID>"
  -- "fields" : "<Specify fields on Encounters to be included in the export>"
  -- "filters" : "<Specify filters applicable on Encounters to be included in the export>"
  -- "maxCount" : "<Specify maximum count of Encounters to be included in the export>"
- "groups" : "<Specify Group Subject request details>"
  -- "uuid" : "<Specify Group Subject’s UUID>"
  -- "fields" : "<Specify fields on Group Subject’s to be included in the export>"
  -- "filters" : "<Specify filters applicable on Group Subject to be included in the export>"
  -- "maxCount" : "<Specify maximum count of Group to be included in the export>"
  -- "encounters" : "<Specify Group Subject Encounter Type’s request details>"
- "programs" : "<Specify Program request details>"
  -- "uuid" : "<Specify Program's UUID>"
  -- "fields" : "<Specify fields on Program Enrolment’s to be included in the export>"
  -- "filters" : "<Specify filters applicable on Program Enrolments to be included in the export>"
  -- "maxCount" : "<Specify maximum count of Program Enrolment to be included in the export>"
  -- "encounters" : "<Specify Program Encounter Types request details>"
```

### Allowed list of Individual fields that could be included in the export file ("fields" within “individual” or "groups" element )​

```c Fields
"id"  
"uuid"  
"firstName"  
"middleName"  
"lastName"
"dateOfBirth"  
"registrationDate"  
"gender"  
"createdBy"  
"createdDateTime"  
"lastModifiedBy"  
"lastModifiedDateTime"  
"voided"  
"registrationDate"  
"registrationLocation"
"gender"  
"dateOfBirth"  
"concept_uuid" : "<Specify Individual’s Concept UUID>"
```

### Allowed list of filters that could be applied to an entity ( "filters" within any entity “individual”, “encounters”, “groups”, “programs”)

```c Filters
"addressLevelIds" : "<Specify Array of Address Level Ids>"  
"date" : "<Specify date range to filter data>"  
"includeVoided" : "<Specify whether voided fields should be included, Allowed values are a. true and b.false >"
```

### Allowed fields with-in "date" element nested inside other entities(Used to restrict the data fetch to have registrationDate or encounterDateTime within the range specified)

```c Date
"from" : Format => "yyyy-MM-dd" Ex: "2020-01-12" (Mandatory)  
"to" : Format => "yyyy-MM-dd" Ex: "2020-01-12" (Mandatory)
```

### Allowed list of Encounter fields that could be included in the export file  ("fields" within "encounters", "program encounters" and  "group subject encounters" element)

```c Fields
"id"  
"uuid"  
"name"  
"earliestVisitDateTime"  
"maxVisitDateTime" 
"encounterDateTime"  
"encounterLocation"
"cancelLocation"
"cancelDateTime"
"createdBy"  
"createdDateTime"  
"lastModifiedBy"  
"lastModifiedDateTime"  
"Voided"
"concept_uuid" : "<Specify Encounter’s Concept UUID>"
```

### Allowed list of enrolment fields that could be included in the export file ("fields" within "enrolment" element )

```c Fields
"id"  
"uuid"  
"name"  
"enrolmentDateTime"  
"programExitDateTime"
"enrolmentLocation"
"exitLocation"
"createdBy"  
"createdDateTime"  
"lastModifiedBy"  
"lastModifiedDateTime"  
"Voided"
"concept_uuid" : "<Specify Enrolment’s Concept UUID>"
```

## Sample Payload

```c JSON
{
   "individual": {
       "uuid": "d22027ff-e019-4d1c-9352-bd740efccc38",
       "fields": ["id", "uuid", "firstName", "registrationDate", "gender", "dateOfBirth"],
       "filters": {
           "addressLevelIds": [],
           "date": {
               "from": "2020-01-12",
               "to": "2022-05-04"
           }
       },
       "encounters": [
           {
               "uuid": "16a3be1b-18a1-45e9-bfc8-f7915898abef",
               "fields": ["id", "encounterDateTime", "cancelDateTime", "uuid", "name", "voided",
                               "1f51e7f7-6db0-41ea-a372-e7b553ccb857",
                               "a6a6d4c0-4339-4ef0-b152-6d1c23eaf7c2",
                               "a44678fd-ee6d-4dc5-b103-f5534eb0f338",
                               "ab095140-b090-4f59-98ac-89b6479df471"],
               "filters": {
                           "includeVoided": true,
                           "date": {
                               "from": "2020-01-12",
                               "to": "2022-05-04"
                           }
                       }
           }
       ],
       "groups": [
           {
               "uuid": "e524b328-c0ad-4232-9fcb-2cf8c126a2c6",
               "fields": ["id", "uuid", "firstName"],
               "encounters": [
                   {
                       "uuid": "0c823f64-b2ec-420b-9e28-5e953b66b6d1",
                       "fields": ["id"]
                   }
               ]
           }
       ],
       "programs": [
           {
               "uuid": "9d6cd285-fb85-48f0-badc-6f004b9024d8",
               "fields": ["id", "uuid", "enrolmentDateTime"],
               "encounters": [
                   {
                       "uuid": "b2f419dc-209a-4285-b74c-29d93f2a628e",
                       "fields": ["id", "uuid", "name","encounterDateTime", "cancelDateTime","voided",
                           "45f02196-217b-4772-8085-3d17c41244da",
                           "d1774f83-ee28-41b8-9cb8-309098ee0f16",
                           "82efa85a-46a9-4c75-8c53-c488b8c48c54",
                           "84a99b8c-f9bb-4436-9d83-d79a60a0b450",
                           "74745370-ee9e-4f58-b25e-57ebac69d75d",
                           "2da75202-7f70-4a76-a8eb-cd9b289cdf8a",
                           "d9f8ee0c-960f-43d7-9b02-aa2557a9aa10",
                           "3e092c91-8e32-42b1-ac26-045b846e3893",
                           "80d88c23-1e44-423a-96bf-5ddaf105042e",
                           "e9190320-3211-4d9f-a72c-288f42cf830c",
                           "1cae9bd0-0dba-4479-954a-2d569c58d711",
                           "ac4d5664-0b5f-467f-a3c9-c0e4c8c221b7",
                           "8f67d53a-07bf-4652-b7ad-f2f6ef6bdfa2",
                           "44a608f8-54d3-4a8b-96b8-7175c65e1d01",
                           "a9f45a38-99a7-4fd8-8e28-1291434eace0",
                           "dfdc75c1-5a47-4aae-887c-3ee9f050d75e",
                           "c78e883a-60de-4629-8d85-8e4512cd13d5",
                           "0fc3b733-0ee0-4554-b316-e5e29c1978d2",
                           "83f01615-04b1-4115-84a5-48e89c9aff54",
                           "5e4d8a9d-28a5-49ec-a4c9-cd9cfd4dd134",
                           "89bf3601-d8ab-4353-85a3-8070a959394e",
                           "8263f129-5851-4f9d-a909-818dacacd862",
                           "5592def2-fe5e-4234-9253-ca5fd0322e26"],
                       "filters": {
                           "includeVoided": true
                       }
                   }
               ]
           }
       ]
   },
   "timezone": "Asia/Calcutta"
}

```


# File: ./readme/Implementers/advanced-feature-guide/news-broadcast.md

title: News broadcast
excerpt: ''
Sometimes it is important to share some important information with all the field users. Avni provides this facility using the News broadcast feature. This feature helps in easy communication with the field users.

## Creating a news broadcast

Creating a news broadcast is very simple, follow the below steps.

* Go to the home page of the Avni web app and open the News Broadcast app.

<Image title="News Broadcast.png" alt={1839} align="center" src="https://files.readme.io/2623e59-News_Broadcast.png">
  Click on the news broadcast to see all the news set up in the organisation
</Image>

* Click on "Create a news broadcast".

<Image title="Create News.png" alt={1846} align="center" src="https://files.readme.io/e42cb0c-Create_News.png">
  The new broadcast can be created by clicking on Create a new broadcast
</Image>

* Provide all the details like image, title, and content and click on "Save news".

<Image title="new news.png" alt={1854} align="center" src="https://files.readme.io/e79d8b2-new_news.png">
  New broadcast screen
</Image>

* Once the news is saved, we need to publish it so that field users can see it on their device. For publishing the news click on "see details" and click on "Publish news".
* Once the news is published field user can see it on their android app.

## News option on android app

After the news is published, the field user can go to "More -> News" to see all the published news. News details can be read by pressing any of the news card.


# File: ./readme/Implementers/advanced-feature-guide/offline-reports.md

title: Offline Report Cards and Custom Dashboards
excerpt: ''
Avni allows you to create different indicator reports that are available offline to the field users. These reports help field users to derive more insights on the captured data. 

Creating an offline report is a two-step process. First, we need to create a report card that holds the actual query function. Second, we group multiple cards into to a dashboard.

## Creating a Report Card

Creating a new report card is no different than creating any other Avni entity. Open app designer and go to the report card tab. Click on the new report card and provide the details like name description, etc.

### Report Card Types

Report cards can be of 2 types - 'Standard' and 'Custom'. The logic used to display the values in 'Standard' type cards are already implemented in Avni whereas the logic needs to be written by the implementer for 'Custom' type cards.

1. Standard Report Cards, the different types of which are as follows (Entity specified in brackets indicates the type of entity listed on clicking on the card):

   * Pending approval (Entity Approval Statuses)

   * Approved (Entity Approval Statuses)

   * Rejected (Entity Approval Statuses)

   * Scheduled visits (Subjects)

   * Overdue visits (Subjects)

   * Recent registrations (Subjects)

   * Recent enrolments (Subjects)

   * Recent visits (Subjects)

   * Total (Subjects)

   * Comments (Subjects)

   * Call tasks (Tasks)

   * Open subject tasks (Tasks)

   * Due checklist (Individuals)

   <Image align="center" src="https://files.readme.io/5093034-Screenshot_2023-12-11_at_4.55.48_PM.png" />
2. Custom Report cards: Report card with configurable **Query**, which returns a list of Individuals as the response. Length of the list is shown on the card and on clicking the card, the list of Individuals returned is shown. Please note that the query function can return a list of Individuals or an object with these properties, ` { primaryValue: '20', secondaryValue: '(5%)',  lineListFunction  }`, here `lineListFunction` should always return the list of subjects.

![](https://files.readme.io/387d221-Report_card.png "Report card.png")

#### Standard Report Card Type Filters

Filters can be added at the report card level for certain standard report types. The following filters are supported:

1. Subject Type
2. Program
3. Encounter Type
4. Recent Duration

Subject Type, Program and Encounter Type filters are supported for 'Overdue Visits', 'Scheduled Visits', 'Total' and 'Recent' types ('Recent registrations', 'Recent enrolments', 'Recent visits').

![](https://files.readme.io/c2f3eb0a468c1e8e3efb808ccb831cf87e19c5da5ba92ae9ed99a0af619d528f-image.png) 

<br />

Filters can also be configured at the dashboard level (covered below). If a filter is configured both at the report card level and the dashboard level, the filter at the report card level is applied first. Hence, mixing of the same type of filter at both levels should be avoided as it could lead to the unintuitive behaviour of the field user selecting a value, say 'Household' for the subject type filter at the dashboard level but still seeing the numbers for the 'Individual' subject type which is configured at the report card level.

## Creating a Dashboard

After all the cards are done it's time to group them together using the dashboard. Offline Dashboards have the following sub-components:

* Sections : Visual Partitions used to club together cards of specific grouping type
* Offline (Custom) Report Cards : Usually Clickable blocks with count information about grouping of Individuals or EntityApprovals of specific type
* Filters : Configurable filters that get applied to all "Report Cards" count and listing

Users with access to the "App Designer" can Create, Modifiy or Delete Custom Dashboards as seen below. 

![](https://files.readme.io/824878a-image.png)

### Steps to configure a Custom Dashboard

* Click on the dashboard tab on the app designer and click on the new dashboard.
* This will take you to the new dashboard screen. Provide the name and description of the dashboard.
* You can create sections on this screen and
* Select all the cards you need to add to the section in the dashboard.
* After adding all the cards, you can re-arrange the cards in the order you want them to see in the field app.

<Image align="center" src="https://files.readme.io/b6a8b74-Screenshot_2023-12-11_at_4.45.34_PM.png" />

### Dashboard Filters

You can also create filters for a dashboard on the same screen by clicking on "Add Filter". This shows a popup as in the below screenshot where you can configure your filter and set the filter name, type, widget type and other values based on your filter type.

![](https://files.readme.io/91f1aa1-image.png)

Once all the changes are done. Save the dashboard.

#### For the filters to be applied to the cards in the dashboard, the code for the cards will need to handle the filters.

Sample Code for handling filters in report card:

```
'use strict';
({params, imports}) => {
//console.log('------>',params.ruleInput.filter( type => type.Name === "Gender" ));
//console.log("params:::", JSON.stringify(params.ruleInput));
  let individualList = params.db.objects('Individual').filtered("voided = false and subjectType.name = 'Individual'" )
     .filter( (individual) => individual.getAgeInYears() >= 18 && individual.getAgeInYears() <= 49  &&  individual.getObservationReadableValue('Is sterilisation done') === 'No');
  
  if (params.ruleInput) {

       let genderFilter = params.ruleInput.filter(rule => rule.type === "Gender");
       let genderValue = genderFilter[0].filterValue[0].name;
      
        console.log('genderFilter---------',genderFilter);
        console.log('genderValue---------',genderValue);        
        
      return individualList
     .filter( (individual) => {
     console.log("individual.gender:::", JSON.stringify(individual.gender.name));
     return individual.gender.name === genderValue;
     });
     }
     else return individualList;
};
```

### Assigning custom Dashboards to User Groups

Custom Dashboards created need to be assigned specifically to a User Group, in-order for Users to see it on the Avni-client mobile app. You may do this, by navigating to the "Admin" app -> "User Groups" -> (User\_GROUP) -> "Dashboards" tab, and assigning one or more Custom Dashboards to a User-Group.

In addition, You can also mark one of these Custom Dashboards as the Primary (Is Primary: True) dashboard from the "Admin" app -> "User Groups" -> (User\_GROUP) -> "Dashboards".

<Image align="center" src="https://files.readme.io/54b6434-Screenshot_2024-06-26_at_12.14.37_PM.png" />

## Using the Dashboard in the Field App

After saving the dashboard sync the field app, and from the bottom "More" tab click on the "Dashboards" option. It will take you to the dashboard screen and will show all the cards that are added to the dashboard.

<Image title="dashboard-field-app.png" alt="Report cards only passing List of subjects." align="center" width="400px" src="https://files.readme.io/8b37cf6-Screenshot_2024-06-26_at_12.15.37_PM.png">
  Report cards only passing List of subjects.
</Image>

<Image title="offline-dashboard.png" alt={566} align="center" width="400px" src="https://files.readme.io/548f99d-offline-dashboard.png">
  Report cards  returning `primaryValue` and `secondaryValue` object
</Image>

Clicking any card will take the user to the subject listing page, which will display all the subject names returned by the card query.

<Image align="center" width="400px" src="https://files.readme.io/18fb944-Subject-list-field-app.png" />

Users can click on any subject and navigate to their dashboard.

## Secondary Dashboard

### Web app configuration

As part of Avni release 8.0.0, a new feature of a secondary dashboard is added which can be configured at user group level to populate an additional option on the Avni mobile app bottom drawer to navigate to a secondary dashboard. This configuration has to be done in the user group in Avni web app. 

* By navigating to the dashboard section in a particular user group where dashboards can be added to user groups, the secondary dashboard can be defined apart from the home dashboard. As shown in the screenshot below, any dashboard can be selected as the secondary dashboard.

<Image align="center" width="1500px" src="https://files.readme.io/68ac5d9-Screenshot_2024-06-26_at_12.14.37_PM.png" />

<Image align="center" width="15px" src="https://files.readme.io/a5640e1-Se.png" />

### Secondary dashboard in mobile app

The configuration mentioned above would display the particular dashboard in the mobile app as given below. This would allow users to access the home and secondary dashboard from the bottom drawer of the mobile app instead of navigating to the more page. 

<Image align="center" width="400px" src="https://files.readme.io/d95166d-Screenshot_2024-06-26_at_12.17.40_PM.png" />

### Clash in Dashboards configuration across different UserGroups

In-case a User belongs to multiple UserGroups, where-in each has a different Primary and/or Secondary Dashboards, then the behaviour is undeterministic. I.e, any of the possible Primary Dashboards across the various UserGroups, would show up as the Primary on the app. Similar behaviour should be expected of the Secondary Dashboard as well.

## Report card query example

As mentioned earlier query can return a list of Individuals or an object with properties, ` { primaryValue: '20', secondaryValue: '(5%)',  lineListFunction  }`. DB instance is passed using the params and useful libraries like lodash and moment are available in the imports parameter of the function. Below are some examples of writing the `lineListFunction`.

The below function returns a list of pregnant women having any high-risk conditions.

```javascript High risk condition women
'use strict';
({params, imports}) => {
    const isHighRiskWomen = (enrolment) => {
        const weight = enrolment.findLatestObservationInEntireEnrolment('Weight');
        const hb = enrolment.findLatestObservationInEntireEnrolment('Hb');
        const numberOfLiveChildren = enrolment.findLatestObservationInEntireEnrolment('Number of live children');
        return (weight && weight.getReadableValue() < 40) || (hb && hb.getReadableValue() < 8) ||
            (numberOfLiveChildren && numberOfLiveChildren.getReadableValue() > 3)
    };
    return {
      lineListFunction: () => params.db.objects('Individual')
        .filtered(`SUBQUERY(enrolments, $enrolment, SUBQUERY($enrolment.encounters, $encounter, $encounter.encounterType.name = 'Monthly monitoring of pregnant woman' and $encounter.voided = false).@count > 0 and $enrolment.voided = false and voided = false).@count > 0`)
        .filter((individual) => individual.voided === false && _.some(individual.enrolments, (enrolment) => enrolment.program.name === 'Pregnant Woman' && isHighRiskWomen(enrolment)))
    }
};
```

It is important to write optimised query and load very less data in memory for processing. There will be the cases where query can't be written in realm and we need to load the data in memory, but remember more data we load into the memory slower will be the reports. As an example consider below two cases, in the first case we directly query realm to fetch all the individuals enrolled in Child program, but in the second case we first load all individuals into memory and then filter those cases. 

```javascript Query in Realm context (better performance)
'use strict';
({params, imports}) => ({
    lineListFunction: () => params.db.objects('Individual')
        .filtered(`SUBQUERY(enrolments, $enrolment, $enrolment.program.name = 'Child' and voided = false).@count > 0`)
});
```
```javascript Query in app context (poor performance)
'use strict';
({params, imports}) => {
    return params.db.objects('Individual')
        .filter((individual) => individual.voided === false && _.some(individual.enrolments, (enrolment) => enrolment.program.name === 'Child'))
};
```

For using the filters in the rules also check section on Dashboard Card Rule here - [Writing rules](doc:writing-rules)

## Performance of queries

The report cards requires one to return a list individuals. This can be done by:

1. Performing db.objects on Individual and filtering them down.
2. Performing db.objects on descendants of Subject (like encounter, enrolment), filter them down, then return list of Individuals from each filtered object. Example is given below.

## Implementation Patterns for writing performant queries

Please refer to [this reference for Realm Query Language](https://www.mongodb.com/docs/atlas/device-sdks/realm-query-language/).

To understand difference between filter and filtered that is referred below, please see, [https://avni.readme.io/docs/writing-rules#difference-between-filter-and-filtered](https://avni.readme.io/docs/writing-rules#difference-between-filter-and-filtered)

Please also get in touch with platform team if you identify a new pattern and a new type of requirement where none of the following fits.

1. Filter based on chronological data
   1. The matching has to be done on specific chronological descendant entity. e.g. `first` encounter of a specific type, `recent` encounter of specific type.
   2. In this case performing `db.objects` on Individual will lead to either very complex queries or will demand performing filtering in memory using JS.
   3. In this case one can do `db.objects` on descendant entity and then use something like `.filtered('TRUEPREDICATE sort(programEnrolment.individual.uuid asc , encounterDateTime desc) Distinct(programEnrolment.individual.uuid)')` to get the chronological relevant entity at the top in each group. Distinct keyword picks only the first entity in the sorted group.
   4. After performing `filtered`, one can return Subjects by performing `list.map(enc => enc.programEnrolment.individual)`
2. Filter based exact observation value
   1. Matching observations by loading them in memory and calling JS functions will lead to slower reports.
   2. A combination of `subquery` and realm query based match will have much better performance. For example: matching observation that has a specific value - `SUBQUERY(observations, $observation, $observation.concept.name = 'Phone number' and $observation.valueJSON CONTAINS '7555795537'`
3. Filter based on exact specific coded observation value
   1. Matching coded value using its name will require one to load data in memory and perform the match. But this could result in sub-optimal performance. Hence the readability of the report should be sacrificed here for performance.
   2. The query will be like `SUBQUERY(observations, $observation, $observation.concept.uuid = 'Marital Status' and $observation.valueJSON CONTAINS 'fb1080b4-d1ec-4c87-a10d-3838ba9abc5b'`
   3. Please note here that multiple observations can be matched here using OR, AND etc.
4. Filter based on a custom observation value expression.
   1. Instead of matching against a single value match using numeric expression. e.g. match BMI greater than 20.0.
   2. This kind of match cannot be done using realm query and implementing them in JS may result in poor performance.
   3. In such cases we should find out the significance of magic number 20.0. Usually we also have a coded decision observation associated that has meaning behind 20.0, like malnutrition status, BMI Status etc. If there is one then we should match against that using pattern 3 above. If such observation is not present then consider adding them to decisions.
   4. In requirements where such associated coded observation are not present and cannot be added, the performance will depend on the number of observations and entities being matched. If this number is large the performance is expected to be slow, it is better to avoid making reports, or move such reports to their own dashboard - so that they don't impact the usability of other reports.

### Detailed examples

#### DEPRECATED: Avoid using generic functions:

* The following is deprecated cause we should use `Filter based on chronological data` pattern from above.
* To find observation of a concept avoid using the function `findLatestObservationInEntireEnrolment` unless absolutely necessary since it searches for the observation in all encounters and enrolment observations. Use specific functions.
* Eg: To find observation in enrolment can use the function `enrolment.findObservation` or to find observations in specific encounter type can get the encounters using `enrolment.lastFulfilledEncounter(...encounterTypeNames)` and then find observation. Refer code examples for the below 3 usecases.
* ```text Usecase 1
  Find children with birth weight less than 2. Birth weight is captured in enrolment
  ```
  ```javascript Recommended way
  'use strict';
  ({params, imports}) => {
      const isLowBirthWeight = (enrolment) => {
          const obs = enrolment.findObservation('Birth Weight');
          return obs ? obs.getReadableValue() <= 2 : false;
      };
      return params.db.objects('Individual')
          .filtered(`voided = false and SUBQUERY(enrolments, $enrolment, $enrolment.program.name = 'Child' and $enrolment.programExitDateTime = null and $enrolment.voided = false).@count > 0`)
          .filter((individual) => _.some(individual.enrolments, enrolment => enrolment.program.name === 'Child' && _.isNil(enrolment.programExitDateTime) && !enrolment.voided && isLowBirthWeight(enrolment)))
  };
  ```
  ```javascript Not recommended way
  'use strict';
  ({params, imports}) => {
      const isLowBirthWeight = (enrolment) => {
          const obs = enrolment.findLatestObservationInEntireEnrolment('Birth Weight');
          return obs ? obs.getReadableValue() <= 2 : false;
      };
      return params.db.objects('Individual')
          .filtered(`SUBQUERY(enrolments, $enrolment, $enrolment.program.name = 'Child' and $enrolment.programExitDateTime = null and $enrolment.voided = false and SUBQUERY($enrolment.observations, $observation, $observation.concept.uuid = 'c82cd1c8-d0a9-4237-b791-8d64e52b6c4a').@count > 0 and voided = false).@count > 0`)
          .filter((individual) => individual.voided === false && _.some(individual.enrolments, enrolment => enrolment.program.name === 'Child' && isLowBirthWeight(enrolment)))
  };
  ```
  ```Text How optimized
  do voided check first in realm instead of JS - helps in filtering ahead
  Check for concept where it is used - no need to check in all encounters and enrolment
  ```
  ```Text Usecase 2
  Find MAM status from value of Nutritional status concept captured in Child Followup encounter
  ```
  ```javascript Recommended way
  // While this example is illustrating the right JS function to use, but it may be better to filter(ed)
  // encounter schema than to start with Individual
  // i.e. someting like db.objects("ProgramEncounter").filtered("programEnrolment.individual.voided = false AND programEnrolment.voided = false AND ...")
  // then return Individuals using .map(enc => enc.programEnrolment.individual) after filtering all program encounters
  'use strict';
  ({params, imports}) => {
      const isUndernourished = (enrolment) => {
          const encounter = enrolment.lastFulfilledEncounter('Child Followup'); 
          if(_.isNil(encounter)) return false; 
         
         const obs = encounter.findObservation("Nutritional status of child");
         return (!_.isNil(obs) && _.isEqual(obs.getValueWrapper().getValue(), "MAM"));
      };
      
      return params.db.objects('Individual')
          .filtered(`voided = false and SUBQUERY(enrolments, $enrolment,$enrolment.program.name = 'Child' and $enrolment.programExitDateTime = null and $enrolment.voided = false and SUBQUERY($enrolment.encounters, $encounter, $encounter.encounterType.name = 'Child Followup' and $encounter.voided = false).@count > 0).@count > 0`)
          .filter((individual) => individual.getAgeInMonths() > 6 && _.some(individual.enrolments, enrolment => enrolment.program.name === 'Child' && _.isNil(enrolment.programExitDateTime) && !enrolment.voided && isUndernourished(enrolment)))
  };
  ```
  ```javascript Not recommended way
  'use strict';
  ({params, imports}) => {
      const isUndernourished = (enrolment) => {
          const obs = enrolment.findLatestObservationInEntireEnrolment('Nutritional status of child');
          return obs ? _.includes(['MAM'], obs.getReadableValue()) : false;
      };
      return params.db.objects('Individual')
          .filtered(`SUBQUERY(enrolments, $enrolment, $enrolment.program.name = 'Child' and $enrolment.programExitDateTime = null and $enrolment.voided = false and SUBQUERY($enrolment.encounters, $encounter, $encounter.encounterType.name = 'Child Followup' and $encounter.voided = false and SUBQUERY($encounter.observations, $observation, $observation.concept.uuid = '3fb85722-fd53-43db-9e8b-d34767af9f7e').@count > 0).@count > 0 and voided = false).@count > 0`)
          .filter((individual) => individual.voided === false && individual.getAgeInMonths() > 6 && _.some(individual.enrolments, enrolment => enrolment.program.name === 'Child' && isUndernourished(enrolment)))
  };
  ```
  ```Text How optimized
  Check only in specific encounter type
  ```
  ```Text Usecase 3
  Find sick children using the presence of value for concept 'Refer to the hospital for' which is not a mandatory concept
  ```
  ```javascript Recommended way
  // also see comments in Recommended way for use case 2
  'use strict';
  ({params, imports}) => {
      const isChildSick = (enrolment) => {
        const encounter = enrolment.lastFulfilledEncounter('Child Followup', 'Child PNC'); 
        if(_.isNil(encounter)) return false; 
         
        const obs = encounter.findObservation('Refer to the hospital for');
        return !_.isNil(obs);
      };
      
      return params.db.objects('Individual')
          .filtered(`voided = false and SUBQUERY(enrolments, $enrolment, $enrolment.program.name = 'Child' and $enrolment.programExitDateTime = null and $enrolment.voided = false).@count > 0`)
          .filter(individual => _.some(individual.enrolments, enrolment => enrolment.program.name === 'Child' && _.isNil(enrolment.programExitDateTime) && !enrolment.voided && isChildSick(enrolment)))
  };
  ```
  ```javascript Not recommended way
  'use strict';
  ({params, imports}) => {
      const isChildSick = (enrolment) => {
           const obs = enrolment.findLatestObservationFromEncounters('Refer to the hospital for');    
           return obs ? obs.getReadableValue() != undefined : false;
      };
      
      return params.db.objects('Individual')
          .filtered(`SUBQUERY(enrolments, $enrolment, $enrolment.program.name = 'Child' and $enrolment.programExitDateTime = null and $enrolment.voided = false).@count > 0`)
          .filter((individual) => individual.voided === false && (_.some(individual.enrolments, enrolment => enrolment.program.name === 'Child' && isChildSick(enrolment))) )
  };
  ```
  ```Text How optimized
  Check only in last encounter, not all encounters since the concept is not a mandatory concept. 
  Using findLatestObservationFromEncounters will check in all encounters and mark child has sick even if the concept value had represented sick in any of the previous encounters, resulting in bug, since the concept is not a mandatory concept.
  ```

#### Based on the use case decide whether to write the logic using realm query or JS.

* Not always achieving the purpose using realm queries might be efficient/possible. 

  * **DEPRECATED** cause we should use `Filter based on chronological data` pattern from above. Eg: consider a use case where a mandatory concept is used in a program encounter. Now to check the latest value of the concept, its sufficient to check the last encounter and need not iterate all encounters. Since realm subquery doesn't support searching only in the last encounter, for such usecases, using realm queries not only becomes slow and also sometimes inappropriate depending on the usecase. So in such cases, using JS code for the logic, is more efficient. (refer the below code example)

    * ```Text Usecase
      Find dead children using concept value captured in encounter cancel or program exit form.
      ```
      ```javascript Recommended way
      'use strict';
      ({params, imports}) => { 
         const moment = imports.moment;

         const isChildDead = (enrolment) => {
            const exitObservation = enrolment.findExitObservation('29238876-fbd8-4f39-b749-edb66024e25e');
            if(!_.isNil(exitObservation) && _.isEqual(exitObservation.getValueWrapper().getValue(), "cbb0969c-c7fe-4ce4-b8a2-670c4e3c5039"))
              return true;
            
            const encounters = enrolment.getEncounters(false);
            const sortedEncounters = _.sortBy(encounters, (encounter) => {
            return _.isNil(encounter.cancelDateTime)? moment().diff(encounter.encounterDateTime) : 
            moment().diff(encounter.cancelDateTime)}); 
            const latestEncounter = _.head(sortedEncounters);
            if(_.isNil(latestEncounter)) return false; 
             
            const cancelObservation = latestEncounter.findCancelEncounterObservation('0066a0f7-c087-40f4-ae44-a3e931967767');
            if(_.isNil(cancelObservation)) return false;
            return _.isEqual(cancelObservation.getValueWrapper().getValue(), "cbb0969c-c7fe-4ce4-b8a2-670c4e3c5039")
          };

      return params.db.objects('Individual')
              .filtered(`voided = false`)
              .filter(individual => _.some(individual.enrolments, enrolment => enrolment.program.name === 'Child' && isChildDead(enrolment)));
      }
      ```
      ```javascript Not recommended way
      'use strict';
      ({params, imports}) => {

      return params.db.objects('Individual')
              .filtered(`subquery(enrolments, $enrolment, $enrolment.program.name == "Child" and subquery(programExitObservations, $exitObservation, $exitObservation.concept.uuid ==  "29238876-fbd8-4f39-b749-edb66024e25e" and ( $exitObservation.valueJSON ==  '{"answer":"cbb0969c-c7fe-4ce4-b8a2-670c4e3c5039"}')  ).@count > 0 ).@count > 0 OR subquery(enrolments.encounters, $encounter, $encounter.voided == false and subquery(cancelObservations, $cancelObservation, $cancelObservation.concept.uuid ==  "0066a0f7-c087-40f4-ae44-a3e931967767" and ( $cancelObservation.valueJSON ==  '{"answer":"cbb0969c-c7fe-4ce4-b8a2-670c4e3c5039"}')  ).@count > 0 ).@count > 0`)
              .filter(ind => ind.voided == false)
      };
      ```
      ```Text How optimized
      Moving to JS since realm query iterates through all encounters which can be avoided in JS
      In this cases since the intention is to find if child is dead, hence it can be assumed to be captured in the last encounter or in program exit form based on the domain knowledge

      ```
  * Please also refer to `Filter based on a custom observation value expression` pattern above, before using this. Consider another use case, where observations of numeric concepts need to be compared. This is not possible to achieve via realm query since the solution would involve the need for JSON parsing of the stored observation. Hence JS logic is appropriate here. (refer below code example)
    * ```Text Usecase
      Find children with birth weight less than 2. Birth weight is captured in enrolment
      ```
      ```javascript Recommended way
      'use strict';
      ({params, imports}) => {
          const isLowBirthWeight = (enrolment) => {
              const obs = enrolment.findObservation('Birth Weight');
              return obs ? obs.getReadableValue() <= 2 : false;
          };
          return params.db.objects('Individual')
              .filtered(`voided = false and SUBQUERY(enrolments, $enrolment, $enrolment.program.name = 'Child' and $enrolment.programExitDateTime = null and $enrolment.voided = false).@count > 0`)
              .filter((individual) => _.some(individual.enrolments, enrolment => enrolment.program.name === 'Child' && _.isNil(enrolment.programExitDateTime) && !enrolment.voided && isLowBirthWeight(enrolment)))
      };
      ```
      ```javascript Not recommended way
      'use strict';
      ({params, imports}) => {
          const isLowBirthWeight = (enrolment) => {
              const obs = enrolment.findLatestObservationInEntireEnrolment('Birth Weight');
              return obs ? obs.getReadableValue() <= 2 : false;
          };
          return params.db.objects('Individual')
              .filtered(`SUBQUERY(enrolments, $enrolment, $enrolment.program.name = 'Child' and $enrolment.programExitDateTime = null and $enrolment.voided = false and SUBQUERY($enrolment.observations, $observation, $observation.concept.uuid = 'c82cd1c8-d0a9-4237-b791-8d64e52b6c4a').@count > 0 and voided = false).@count > 0`)
              .filter((individual) => individual.voided === false && _.some(individual.enrolments, enrolment => enrolment.program.name === 'Child' && isLowBirthWeight(enrolment)))
      };
      ```
      ```Text How optimized
      Moving to realm query for checking birth weight was not possible. If it were a equals comparison it can be achieved using 'CONTAINS' in realm
      ```
* But in cases where time complexity is the same for both cases, writing realm queries would be efficient to achieve the purpose. (refer below code example). Also refer to `Filter based on a custom observation value expression` pattern above.

  * ```Text Usecase
    Find 13 months children who are completely immunised
    ```
    ```javascript Recommended way
    'use strict';
    ({params, imports}) => {        
       return params.db.objects('Individual')
            .filtered(`voided = false and SUBQUERY(enrolments, $enrolment, $enrolment.program.name = 'Child' and $enrolment.programExitDateTime = null and $enrolment.voided = false and SUBQUERY(checklists, $checklist, SUBQUERY(items, $item, ($item.detail.concept.name = 'BCG' OR $item.detail.concept.name = 'Polio 0' OR $item.detail.concept.name = 'Polio 1' OR $item.detail.concept.name = 'Polio 2' OR $item.detail.concept.name = 'Polio 3' OR $item.detail.concept.name = 'Pentavalent 1' OR $item.detail.concept.name = 'Pentavalent 2' OR $item.detail.concept.name = 'Pentavalent 3' OR $item.detail.concept.name = 'Measles 1' OR $item.detail.concept.name = 'Measles 2' OR $item.detail.concept.name = 'FIPV 1' OR $item.detail.concept.name = 'FIPV 2' OR $item.detail.concept.name = 'Rota 1' OR $item.detail.concept.name = 'Rota 2') and $item.completionDate <> nil).@count = 14).@count > 0).@count > 0`)
            .filter(individual => individual.getAgeInMonths() >= 13)     
    };
    ```
    ```javascript Not recommended way
    'use strict';
    ({params, imports}) => {
        const isChildGettingImmunised = (enrolment) => {
            if (enrolment.hasChecklist) {
                const vaccineToCheck = ['BCG', 'Polio 0', 'Polio 1', 'Polio 2', 'Polio 3', 'Pentavalent 1', 'Pentavalent 2', 'Pentavalent 3', 'Measles 1', 'Measles 2', 'FIPV 1', 'FIPV 2', 'Rota 1', 'Rota 2'];
                const checklist = _.head(enrolment.getChecklists());
                return _.chain(checklist.items)
                    .filter(({detail}) => _.includes(vaccineToCheck, detail.concept.name))
                    .every(({completionDate}) => !_.isNil(completionDate))
                    .value();
            }
            return false;
        };

        return params.db.objects('Individual')
            .filtered(`SUBQUERY(enrolments, $enrolment, $enrolment.program.name = 'Child' and $enrolment.programExitDateTime = null and $enrolment.voided = false).@count > 0`)
            .filter((individual) => individual.voided === false && individual.getAgeInMonths() >= 13 && _.some(individual.enrolments, enrolment => enrolment.program.name === 'Child' && isChildGettingImmunised(enrolment)))
    };
    ```
    ```Text How optimized
    Moving to realm query since no of children with age < 13 months were less
    ```
* In most cases, filtering as much as possible using realm queries (for cases like voided checks) and then doing JS filtering on top of it if needed, would be appropriate. (refer the below code example)

  * ```Text Usecase
    Find dead children using concept value captured in encounter cancel or program exit form.
    ```
    ```javascript Recommended way
    'use strict';
    ({params, imports}) => { 
       const moment = imports.moment;

       const isChildDead = (enrolment) => {
          const exitObservation = enrolment.findExitObservation('29238876-fbd8-4f39-b749-edb66024e25e');
          if(!_.isNil(exitObservation) && _.isEqual(exitObservation.getValueWrapper().getValue(), "cbb0969c-c7fe-4ce4-b8a2-670c4e3c5039"))
            return true;
          
          const encounters = enrolment.getEncounters(false);
          const sortedEncounters = _.sortBy(encounters, (encounter) => {
          return _.isNil(encounter.cancelDateTime)? moment().diff(encounter.encounterDateTime) : 
          moment().diff(encounter.cancelDateTime)}); 
          const latestEncounter = _.head(sortedEncounters);
          if(_.isNil(latestEncounter)) return false; 
           
          const cancelObservation = latestEncounter.findCancelEncounterObservation('0066a0f7-c087-40f4-ae44-a3e931967767');
          if(_.isNil(cancelObservation)) return false;
          return _.isEqual(cancelObservation.getValueWrapper().getValue(), "cbb0969c-c7fe-4ce4-b8a2-670c4e3c5039")
        };

    return params.db.objects('Individual')
            .filtered(`voided = false`)
            .filter(individual => _.some(individual.enrolments, enrolment => enrolment.program.name === 'Child' && isChildDead(enrolment)));
    }
    ```
    ```javascript Not recommended way
    'use strict';
    ({params, imports}) => {

    return params.db.objects('Individual')
            .filtered(`subquery(enrolments, $enrolment, $enrolment.program.name == "Child" and subquery(programExitObservations, $exitObservation, $exitObservation.concept.uuid ==  "29238876-fbd8-4f39-b749-edb66024e25e" and ( $exitObservation.valueJSON ==  '{"answer":"cbb0969c-c7fe-4ce4-b8a2-670c4e3c5039"}')  ).@count > 0 ).@count > 0 OR subquery(enrolments.encounters, $encounter, $encounter.voided == false and subquery(cancelObservations, $cancelObservation, $cancelObservation.concept.uuid ==  "0066a0f7-c087-40f4-ae44-a3e931967767" and ( $cancelObservation.valueJSON ==  '{"answer":"cbb0969c-c7fe-4ce4-b8a2-670c4e3c5039"}')  ).@count > 0 ).@count > 0`)
            .filter(ind => ind.voided == false);
    };
    ```
    ```Text How optimized
    Moving to JS since realm query iterates through all encounters which can be avoided in JS
    In this cases since the intention is to find if child is dead it can be assumed to be captured in the last encounter or in program exit form based on the domain knowledge

    ```

Also check - [https://avni.readme.io/docs/writing-rules#using-paramsdb-object-when-writing-rules](https://avni.readme.io/docs/writing-rules#using-paramsdb-object-when-writing-rules)

#### DEPRECATED. Use Concept UUIDs instead of their names for comparison

Please check - `Filter based on a custom observation value expression` pattern above.

Though not much performance improvement, using concept uuids(for comparing with concept answers), instead of getting its readable values did provide minor improvement(in seconds) when need to iterate through thousands of rows. (refer below code example)

* ```Text Usecase
  Find children with congential abnormality based on values of certain concepts
  ```
  ```javascript Recommended way
  'use strict';
  ({params, imports}) => {
      const isChildCongenitalAnamoly = (enrolment) => {
         const _ = imports.lodash;
      
         const encounter = enrolment.lastFulfilledEncounter('Child PNC'); 
         if(_.isNil(encounter)) return false; 
         
         const obs1 = encounter.findObservation("Is the infant's mouth cleft pallet seen?");
         const condition2 = obs1 ? obs1.getValueWrapper().getValue() === '3a9fe9a1-a866-47ed-b75c-c0071ea22d97' : false;
           
         const obs2 = encounter.findObservation('Is there visible tumor on back or on head of infant?');
         const condition3 = obs2 ? obs2.getValueWrapper().getValue() === '3a9fe9a1-a866-47ed-b75c-c0071ea22d97' : false;
           
         const obs3 = encounter.findObservation("Is foam coming from infant's mouth continuously?");
         const condition4 = obs3 ? obs3.getValueWrapper().getValue() === '3a9fe9a1-a866-47ed-b75c-c0071ea22d97' : false;
                    
           return condition2 || condition3 || condition4;
      };
      
      const isChildCongenitalAnamolyReg = (individual) => {
           const obs = individual.findObservation('Has any congenital abnormality?');
           return obs ? obs.getValueWrapper().getValue() === '3a9fe9a1-a866-47ed-b75c-c0071ea22d97' : false;
      };
      
      return params.db.objects('Individual')
          .filtered(`voided = false and SUBQUERY(enrolments, $enrolment, $enrolment.program.name = 'Child' and $enrolment.programExitDateTime = null and $enrolment.voided = false).@count > 0`)
          .filter((individual) => (isChildCongenitalAnamolyReg(individual) || 
              _.some(individual.enrolments, enrolment => enrolment.program.name === 'Child' && _.isNil(enrolment.programExitDateTime) && !enrolment.voided && isChildCongenitalAnamoly(enrolment) )) )
  };
  ```
  ```javascript Not recommended way
  'use strict';
  ({params, imports}) => {
      const isChildCongenitalAnamoly = (enrolment) => {
           
           const obs1 = enrolment.findLatestObservationInEntireEnrolment("Is the infant's mouth cleft pallet seen?");
           const condition2 = obs1 ? obs1.getReadableValue() === 'Yes' : false;
           
       const obs2 = enrolment.findLatestObservationInEntireEnrolment('Is there visible tumor on back or on head of infant?');
           const condition3 = obs2 ? obs2.getReadableValue() === 'Yes' : false;
           
           const obs3 = enrolment.findLatestObservationInEntireEnrolment("Is foam coming from infant's mouth continuously?");
           const condition4 = obs3 ? obs3.getReadableValue() === 'Yes' : false;
                    
           return condition2 || condition3 || condition4;
      };
      
      const isChildCongenitalAnamolyReg = (individual) => {
           const obs = individual.getObservationReadableValue('Has any congenital abnormality?');
           return obs ? obs === 'Yes' : false;
      };
      
      return params.db.objects('Individual')
          .filtered(`SUBQUERY(enrolments, $enrolment, $enrolment.program.name = 'Child' and $enrolment.programExitDateTime = null and $enrolment.voided = false).@count > 0`)
          .filter((individual) => individual.voided === false && (isChildCongenitalAnamolyReg(individual) || 
              _.some(individual.enrolments, enrolment => enrolment.program.name === 'Child' && isChildCongenitalAnamoly(enrolment) )) )
  };
  ```
  ```Text How optimized
  Use concept uuid instead of readableValue to compare and check for value only in specific encounter type where the concept was used
  ```

## Nested Report Cards

Frequently there are cases where across report cards very similar logic is used and only a value used for comparison, changes. Eg: in one of our partner organisations, we load 'Total SAM children' and 'Total MAM children'. For rendering each takes around 20-30s. And hence the dashboard nos doesn't load until both the report card results are calculated and it makes the user to wait for a minute. If the logic is combined, we can render the results in 30s since it would need only retrieval from db and iterating once.\
The above kind of scenarios also lead to code duplication across report cards and when some requirement changes, then the change needs to be done in both.

In-order to handle such scenarios, we recommend using the Nested Report Card. This is a non-standard report card, which has the ability to show upto a maximum of **9** report cards, based on a single Query's response.

The query can return an object with "reportCards" property, which holds within it an array of objets with properties, ` { cardName: 'nested-i', cardColor: '#123456', textColor: '#654321', primaryValue: '20', secondaryValue: '(5%)',  lineListFunction: () => {/*Do something*/} }`. DB instance is passed using the params and useful libraries like lodash and moment are available in the imports parameter of the function. 

```javascript Nested Report Card Query Format
'use strict';
({params, imports}) => {
    /*
    Business logic
    */
    return {reportCards: \[
        {
            cardName: 'nested-i',
            cardColor: '#123456',
            textColor: '#654321',
            primaryValue: '20',
            secondaryValue: '(5%)',
            lineListFunction: () => {
                /*Do something*/
            }
        },
        {
            cardName: 'nested-i+1',
            cardColor: '#123456',
            textColor: '#654321',
            primaryValue: '20',
            secondaryValue: '(5%)',
            lineListFunction: () => {
                /*Do something*/
            }
        }
    ]
	}
};
```
```Text Mandatory Fields
- primaryValue
- secondaryValue
- lineListFunction
```
```Text Optional fields
- cardName
- cardColor
- textColor
```

```javascript Sample Nested Report card Query
// Documentation - https://docs.mongodb.com/realm-legacy/docs/javascript/latest/index.html#queries

'use strict';
({params, imports}) => {
const _ = imports.lodash;
const moment = imports.moment;

const substanceUseDue = (enrolment) => {
    const substanceUseEnc = enrolment.scheduledEncountersOfType('Record Substance use details');
    
    const substanceUse = substanceUseEnc
    .filter((e) => moment().isSameOrAfter(moment(e.earliestVisitDateTime)) && e.cancelDateTime === null && e.encounterDateTime === null );
    
    return substanceUse.length > 0 ? true : false;
    
    };
const indList = params.db.objects('Individual')
        .filtered(`SUBQUERY(enrolments, $enrolment, $enrolment.program.name = 'Substance use' and $enrolment.programExitDateTime = null and $enrolment.voided = false and SUBQUERY($enrolment.encounters, $encounter, $encounter.encounterType.name = 'Record Substance use details' and $encounter.voided = false ).@count > 0 and voided = false).@count > 0`)
        .filter((individual) => _.some(individual.enrolments, enrolment => substanceUseDue(enrolment)
        )); 
        
const includingVoidedLength = indList.length;
const excludingVoidedLength = 6;  
const llf1 = () => { return params.db.objects('Individual')
        .filtered(`SUBQUERY(enrolments, $enrolment, $enrolment.program.name = 'Substance use' and $enrolment.programExitDateTime = null and $enrolment.voided = false and SUBQUERY($enrolment.encounters, $encounter, $encounter.encounterType.name = 'Record Substance use details' and $encounter.voided = false ).@count > 0 and voided = false).@count > 0`)
        .filter((individual) => _.some(individual.enrolments, enrolment => substanceUseDue(enrolment)
        ));    
        };
           

return {reportCards: [{
      cardName: 'nested 1',
      textColor: '#bb34ff',
      primaryValue: includingVoidedLength,   
      secondaryValue: null,
      lineListFunction: llf1
  },
  {
      cardName: 'nested 2',
      cardColor: '#ff34ff',
      primaryValue: excludingVoidedLength,   
      secondaryValue: null,
      lineListFunction: () => {return params.db.objects('Individual')
        .filtered(`SUBQUERY(enrolments, $enrolment, $enrolment.program.name = 'Substance use' and $enrolment.programExitDateTime = null and $enrolment.voided = false and SUBQUERY($enrolment.encounters, $encounter, $encounter.encounterType.name = 'Record Substance use details' and $encounter.voided = false ).@count > 0 and voided = false).@count > 0`)
        .filter((individual) => individual.voided === false  && _.some(individual.enrolments, enrolment => substanceUseDue(enrolment)
        ));}
  }]}
};
```

### Screenshot of Nested Custom Dashboard Report Card Edit screen on Avni Webapp

<Image align="center" src="https://files.readme.io/ecdd996-Screenshot_2024-01-25_at_5.15.20_PM.png" />

### Screenshot of Nested Report Cards in Custom Dashboard in Avni Client

<Image align="center" width="576px" src="https://files.readme.io/dca68e5-Screenshot_2024-01-25_at_5.19.04_PM.png" />

![]()

Note: If there is a mismatch between the count of nested report cards configured and the length of reportCards property returned by the query response, then we show an appropriate error message on all Nested Report Cards corresponding to the Custom Report Card.

<Image align="center" width="576px" src="https://files.readme.io/82d8ca0-Screenshot_2024-01-25_at_5.23.56_PM.png" />

<br />

## Default Dashboard and Report Cards

Starting in release 10.0, any newly created organisation will have a default dashboard created with the following sections, standard cards and filters.

Default Dashboard (Filters: 'Subject Type' and 'As On Date')

1. Visit Details Section
   1. Scheduled Visits Card
   2. Overdue Visits Card
2. Recent Statistics Section
   1. Recent Registrations Card (Recent duration filter configured as - 1 day)
   2. Recent Enrolments Card (Recent duration filter configured as - 1 day)
   3. Recent Visits Card (Recent duration filter configured as - 1 day)
3. Registration Overview Section
   1. Total Card

This default dashboard will also be assigned as Primary dashboard on the 'Everyone' user group. 

## Reference screen-shots of Avni-Client Custom Dashboard with Approvals ReportCards and Location filter

<Image alt="Default state of Approvals Report Cards without any filter applied" align="center" border={true} src="https://files.readme.io/e35888a-Screenshot_2023-12-12_at_12.46.46_PM.png">
  Default state of Approvals Report Cards without any filter applied
</Image>

***

<Image alt="Custom Dashboards filter page" align="center" border={true} src="https://files.readme.io/576efec-Screenshot_2023-12-12_at_12.47.01_PM.png">
  Custom Dashboards filter page
</Image>

***

<Image alt="State of Approvals Report Cards after the Location filter was applied" align="center" border={true} src="https://files.readme.io/c5ac6f6-Screenshot_2023-12-12_at_12.47.25_PM.png">
  State of Approvals Report Cards after the Location filter was applied
</Image>

***


# File: ./readme/Implementers/advanced-feature-guide/organisation-group.md

title: How and when to use organisation group
excerpt: ''
If an organisation works with other sub-organisations performing same activity and if it wants each sub-organisation to be able to view/manage only their data - then one can check organisation group feature to solve for:

* Same app definition shared across partner organisations
* Each partner organisation get their own dashboard and reports without being able to see data from other partner organisations.
* Super organisation to be able to have a dashboard where they can view all sub-organisation data.

> 🚧 Should not be used when the number of partner organisations can grow a large number over time.

### Organisation and organisation groups

1. Mainline Organisation - for maintaining the trunk of source bundle
2. Release Organisation - for maintaining the released branch of source bundle
3. One production organisation for each partner organisation. One production organisation group.
4. Two UAT organisations. One organisation group consisting of these two organisations)
   1. Two organisations allow us to replicate the organisation group.

### Testing Deployment

Active development take places on mainline organisation.

### Release Deployment

1. The bundle from mainline organisation is released to release organisation and sanity testing can be done on this.
2. The bundle from release organisation is uploaded to each production organisation.

### Managing locations

There are two options.

1. There is one location set that is used by all partner organisations. These locations are to be imported in each organisation.
2. Each organisation has their own locations. In this case if the same logical location is used by multiple organisations, then Location should suffixed like Location1 (Org 1), Location2 (Org 1) when uploading. See the filters section below for the trade-off.

### Reporting

Metabase is not right tool for such setup and SuperSet should be used.

#### How to create separation between different partner organisations so that they do not see each other's data.

1. All reports should connect using the organisation group db\_user to the database. ETL should be enabled for only organisation group.
2. Setup row level security and roles for each organisation (feature of Superset).
3. Assign correct role to the user when provisioning users from any partner organisation
4. For users who can see the reports for all organisations no role level security role is required.

### Filters

1. Filters like dates and hardcoded values there is nothing different to be done.

2. (Assumes row-level security works for filter queries as well) Filters that display drop downs like any concept's coded values, location types query with distinct clause should be used. Distinct clause is required for super organisation users, other wise they will see repeated values from each organisation.
   1. In query match against the concept, location type name and not ID or UUID.

3. (Assumes row-level security works for filter queries as well) Filters displaying location
   1. If approach 2 has been taken the users will be required to select all locations for same logical location.

## Access control

1. App Designer, Location Types - Recommended that these edit access is not provided for these to the customer.
2. Location - In Approach 1 (in Managing Locations), the access should not be given to the customer. In approach 2 one can do that with some training on naming if required.
3. User Groups - If access has to be given to customers then the tradeoff is in giving up on centralised source bundle management and it should excluded from bundles every time.

## Activities to consider when creating multiple organisations

1. Setup of organisations as described above
2. Release is more complex than for regular organisation
3. Each partner addition will require release activities like org setup, bundle upload, location setup and administrator training, row-level security / roles creation in superset, higher support required due to lack of access control that can be provided to the customers.


# File: ./readme/Implementers/advanced-feature-guide/program.md

title: Enrol to same program multiple times
excerpt: ''
Each subject type can have multiple programs within them. If these programs are defined, the user can enroll subjects of these subject types into these programs.

Number of enrolments per subject

* Typically and hence by default, a subject can have only one active enrolment for a program. This implies that for a subject to be enrolled again the previous enrolment must be exited. e.g. Pregnancy program. Sometimes for chronic diseases, a person may remain in a program forever like diabetes. In such cases, the subject is never exited.
* Starting release 3.37, Avni also supports multiple active enrolments in a program. This can be done by switching on this per program. When this is switched on the above condition is relaxed by Avni.

<Image align="center" className="border" width="300px" border={true} src="https://files.readme.io/62b1f10-image.png" />


# File: ./readme/Implementers/advanced-feature-guide/quick-form-edit-and-jump-to-summary.md

title: Quick form edit and jump to summary
excerpt: ''
This feature allows users to jump directly to any page in the form and then quickly save the form skipping the middle questions. This will save a lot of time as now users don't have to go through all the pages.\
There is no configuration required for the quick form edit feature however, one need to enable jump to summary feature

## Enabling jump to summary

In the admin app go to "Organisation Details" and enable the "Show summary button" option. 

<Image title="Jump to summary.png" alt={1832} src="https://files.readme.io/19f3021-Jump_to_summary.png">
  Enabling Jump to summary feature
</Image>

After enabling the "jump to summary feature", sync the field app. The user will see the Summary button at the top right corner in the form.

<Image title="quick-form-edit(1).gif" alt={176} src="https://files.readme.io/aea853d-quick-form-edit1.gif">
  Quick form edit in action
</Image>

**Note**: This feature is only supported in the mobile application.


# File: ./readme/Implementers/advanced-feature-guide/repeatable-question-group.md

title: Repeatable question group
excerpt: ''
A repeatable question group is an extension of the question group form element. A Question group is like any other data type in Avni. The only difference is it allows implementers to group similar fields together and show those questions like a group. Now there are cases where you want to repeat the same set of questions(group) multiple times. This can be easily done by just marking the question group as repeatable.

## Steps to configure repeatable Question group

1. Create a form element having a question group concept.
2. This will allow you to add multiple questions inside the question group.
3. Once all the questions are added, mark it repeatable and finally save the form.

<Image title="Repeaable-question-group.png" alt={1495} align="center" src="https://files.readme.io/ae26aab-Repeaable-question-group.png">
  Notice how the question group is marked repeatable.
</Image>

<Image title="repeatable-question.gif" alt={585} align="center" src="https://files.readme.io/61bee14-repeatable-question.gif">
  Repeatable questions in mobile app
</Image>

### Limitations

At this time, the following elements that are part of the forms are not yet supported. 

* Nested Groups
* Encounter form element
* Id form element
* Subject form element with the "Show all members" option (Regular subject form elements are supported)

  * To get this working within a Question-Group/ Repeatable-Question-Group, for a Non "Group" Subject Type, please select the **"Search Option"** in the Subject FormElement while configuring the Form inside **App Designer**

  <Image align="center" src="https://files.readme.io/c5c15ae-Screenshot_2024-06-10_at_2.35.04_PM.png" />


# File: ./readme/Implementers/advanced-feature-guide/reporting-views.md

title: Reporting Views [Deprecated]
excerpt: ''
Avni has a generic data model to support the dynamic creation of forms. For new implementers wanting to write custom reports, this can be overwhelming and complex.\
To ease the creation of reports, Avni generates simplified database views with one view corresponding to each form.

## Creating / Refreshing Reporting Views

You can create views for reporting by going to the `Reporting Views` option in the app designer and clicking on `create/refresh view`. For each form, one view is created with all the questions as the columns in the view. 

<Image title="Screen Shot 2020-09-04 at 9.28.47 AM.png" alt={3356} src="https://files.readme.io/f47db05-Screen_Shot_2020-09-04_at_9.28.47_AM.png">
  App Designer Reporting Views Screen
</Image>

You can see the view definition by clicking on the expand button, and delete the view by clicking on the delete button.

The views would be accessible in Metabase or any other reporting tool the implementation may be using.

## Naming convention

As PostgreSQL doesn't allow identifiers of length more than 63 bytes, we follow these naming conventions as long as the view name is below 63 characters.

<Table align={["left","left"]}>
  <thead>
    <tr>
      <th>
        Form type
      </th>

      <th>
        View name
      </th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>
        Registration
      </td>

      <td>
        `{UsernameSuffix}_{SubjectTypeName}`
      </td>
    </tr>

    <tr>
      <td>
        Encounter
      </td>

      <td>
        `{UsernameSuffix}_{SubjectTypeName}_{encounterTypeName}`
      </td>
    </tr>

    <tr>
      <td>
        Encounter Cancellation
      </td>

      <td>
        `{UsernameSuffix}_{SubjectTypeName}_{encounterTypeName}_cancel`
      </td>
    </tr>

    <tr>
      <td>
        Program Enrolment
      </td>

      <td>
        `{UsernameSuffix}_{SubjectTypeName}_{ProgramName}`
      </td>
    </tr>

    <tr>
      <td>
        Program Exit
      </td>

      <td>
        `{UsernameSuffix}_{SubjectTypeName}_{ProgramName}_exit`
      </td>
    </tr>

    <tr>
      <td>
        Program Encounter
      </td>

      <td>
        `{UsernameSuffix}_{SubjectTypeName}_{ProgramName}_{EncounterTypeName}`
      </td>
    </tr>

    <tr>
      <td>
        Program Encounter Cancellation
      </td>

      <td>
        `{UsernameSuffix}_{SubjectTypeName}_{ProgramName}_{EncounterTypeName}_cancel`
      </td>
    </tr>
  </tbody>
</Table>

If the view name exceeds 63 characters we trim some parts from different entity type names to keep it below 63 characters. For trimming, we follow the below rule.

*\{UsernameSuffix}*\{First 6 characters of SubjectTypeName}*\{First 6 characters of ProgramName}\_\{First 20 characters of EncounterTypeName}*

Some view names exceed the character limit even after the above optimisation. In such a case we take away the last few characters and replace them with the hashcode of the full name. Hashcode is used so that the name remains unique.


# File: ./readme/Implementers/advanced-feature-guide/structure-import-metadata-excel-excel.md

title: Introduction to excel based import [Deprecated]
excerpt: >-
next:
  description: ''
  pages:
    - type: basic
      slug: importing-excel-data
      title: Importing Excel data
---
> ❗️ Avni does not support Excel based import any longer, please refer to Admin App based approach to upload data [Bulk Data Upload page](https://avni.readme.io/docs/upload-data#is-the-order-of-values-important)

<br />

We can Import transactional data from excel files. Data can be Subject Registration, Enrolment, Encounters, relationships between Subjects, Vaccinations, etc. The data file, ideally, should have columns like RegistrationDate, FirstName, LastName, DOB, .. in case of Registration, and SubjectUUID, DateOfEnrolment, Program, .. in case of Enrolment, and SubjectUUID, EnrolmentUUID, EncounterType, Name, .. for Encounters. Along with these default fields, all the observations specific to the implementation should be present in the data file.

The definition of those forms cannot be imported this way. Only the data recorded against those forms can be imported this way.

We need a metaData.xlsx file that would work as an adapter between the data.xlsx file and the avni system.  
The data.xlsx file will be provided by the org-admin which should have consistent and tabular data. The metaData.xlsx file defines the relationship between each column and its corresponding field in the avni system/implementation.

## Structure of metaData.xlsx file:

The following are the various spreadsheets within a metaData.xlsx file.

### Sheets

Sheets represent a logical sheet of data. A physical sheet of data can be mapped to multiple logical sheets of data.

<table>
<thead>
<tr>
  <th>Column</th>
  <th>Description</th>
</tr>
</thead>
<tbody>
<tr>
  <td><p>File Name</p></td>
  <td><p>The data migration service is used by supplying the metadata excel file, a data excel file, and a fileName (since the server reads the data excel file via a stream it doesn&#39;t know the name of the file originally uploaded hence it needs to be explicitly provided).  </p>
<p>Only the sheets which have the file name matching the fileName via the API would be imported.</p></td>
</tr>
<tr>
  <td><p>User File Type</p></td>
  <td><p>This is the unique name given to the file of specific types. There can be more than one physical file of the same type, in which case the user file type will be the same but file names will be different.</p></td>
</tr>
<tr>
  <td><p>Sheet Name</p></td>
  <td><p>This is the name of the actual sheet in the data file uploaded where the data should be read.</p></td>
</tr>
<tr>
  <td><p>Entity Type, Program Name and Visit Type, Address</p></td>
  <td><p>Core but optional data to be provided depending on the type of data being imported</p></td>
</tr>
<tr>
  <td><p>Active</p></td>
  <td><p>During data migration, it is possible that there are a lot of files and mapping metadata definition for those files may not be complete. Active flag (Yes or No) can be used to disable sheets that need not be considered for migration when uploaded.</p></td>
</tr>
<tr>
  <td><p>Name of fields</p></td>
  <td><p>One can add multiple columns after this such that it matches the name of a System Field and provides the default value for the entire virtual sheet.</p></td>
</tr>
</tbody>
</table>

#### Sample

| File Name                          | User File Type | Sheet Name | Entity Type      | Program Name | Visit Type | Active | Date of Birth Verified | SubjectTypeUUID                          | Registration Date | Enrolment Date |
| ---------------------------------- | -------------- | ---------- | ---------------- | ------------ | ---------- | ------ | ---------------------- | ---------------------------------------- | ----------------- | -------------- |
| master\_data\_district\_wise\.xlsx | Registration   | AhmedNagar | Individual       |              |            | No     |                        | 8a9b0ef8\-325b\-4f75\-8453\-daeaf59df29d | YYYY\-MM\-DD      |                |
| master\_data\_district\_wise\.xlsx | Enrolment      | AhmedNagar | ProgramEnrolment | GDGS 2019    |            | No     |                        |                                          |                   | YYYY\-MM\-DD   |

### Fields

The mapping for non-calculated fields

<table>
<thead>
<tr>
  <th>Column</th>
  <th>Description</th>
</tr>
</thead>
<tbody>
<tr>
  <td><p>User File Type</p></td>
  <td><p>This is the same as in Sheets.</p></td>
</tr>
<tr>
  <td><p>Form Type</p></td>
  <td><p>[IndividualProfile, Encounter, ProgramEncounter, ProgramEnrolment, ProgramExit, ProgramEncounterCancellation, ChecklistItem, IndividualRelationship]</p></td>
</tr>
<tr>
  <td><p>System Field</p></td>
  <td><p>The concept name is specified in the form.<br/>Or Default field (this can be seen in different importers, See below ).</p></td>
</tr>
<tr>
  <td><p>User Field</p></td>
  <td><p>Name of the column from data.xlsx file</p></td>
</tr>
</tbody>
</table>

#### Default fields for each entity as of Dec 2019

| Subject Registration   | Encounter          | Enrolment       | ProgramEncounter | Checklist       | Relationship     |
| ---------------------- | ------------------ | --------------- | ---------------- | --------------- | ---------------- |
| First Name             | Individual UUID    | Enrolment UUID  | Enrolment UUID   | Enrolment UUID  | EnterDateTime    |
| Last Name              | UUID               | Individual UUID | UUID             | Base Date       | ExitDateTime     |
| Age                    | Visit Type         | Enrolment Date  | Visit Type       | Checklist Name  | IndividualAUUID  |
| Date of Birth          | Encounter DateTime | Address         | Visit Name       | Item Name       | IndividualBUUID  |
| Date of Birth Verified | User               | Exit Date       | Earliest Date    | Completion Date | RelationshipType |
| Gender                 | Voided             | User            | Actual Date      | User            | User             |
| Registration Date      |                    | Voided          | Max Date         | Voided          | Voided           |
| Address Level          |                    |                 | Address          |                 |                  |
| AddressUUID            |                    |                 | Cancel Date      |                 |                  |
| Individual UUID        |                    |                 | User             |                 |                  |
| Catchment UUID         |                    |                 | Voided           |                 |                  |
| SubjectTypeUUID        |                    |                 |                  |                 |                  |
| User                   |                    |                 |                  |                 |                  |
| Voided                 |                    |                 |                  |                 |                  |

Along with these, the implementation-specific observations are also to be mapped.

#### Sample

| User File Type | Form Type         | System Field                         | User Field                     |
| -------------- | ----------------- | ------------------------------------ | ------------------------------ |
| Registration   | IndividualProfile | Individual UUID                      | SiteUUID                       |
| Registration   | IndividualProfile | First Name                           | Site                           |
| Registration   | IndividualProfile | AddressUUID                          | VillageUUID                    |
| Registration   | IndividualProfile | Type of waterbody                    | Type                           |
| Registration   | IndividualProfile | Concerned Govt\. Dept\.              | Concerned Govt\. Dept\.        |
| Enrolment      | ProgramEnrolment  | Silt Estimation as per the work plan | Estimated quantity of Silt cum |
| Enrolment      | ProgramEnrolment  | Individual UUID                      | SiteUUID                       |
| Enrolment      | ProgramEnrolment  | Enrolment UUID                       | EnrolmentUUID                  |

[An example of Metadata.xlsx file](https://docs.google.com/spreadsheets/d/1M0QvcgZ7TagcHvMnTSo3qt-sZHwUDHEiN0T2hlKTn9Y/edit?usp=sharing)  
[An example of Data.xlsx file](https://docs.google.com/spreadsheets/d/19aCEIlODNvJMR68_mGl4Q-Kx6n3qI0Dk4hL0aQ8dwAo/edit?usp=sharing)

> 🚧 UUIDs in Data.xlsx file
> 
> Note that
> 
> - Individual UUID (aka Subject UUID, in this example called SiteUUID), EnrolmentUUID, or any `<Transactional-data UUID>` will have to be manually assigned by the developer before import.
>   - Use tools like uuid: `npm i -g uuid`.
>   - `for n in {1..100}; do uuidgen -r; done` `#to get 100 uuids from CLI`
> - AddressUUID (or Village UUID) will not be available when the data file is provided by the Implmentation. And has to be determined from the `Full Address details` (see example Data.xlsx).
>   - For this get all locations and it's uuid into a `Ref Sheet` in data.xlsx file
>   - do vlookup for uuid by `full address details`

### Google Drive Files

For uploading files (images/documents) you can put the URL of the file. Please follow the following steps:

- Ensure the drive file is shared without any restrictions
- Copy the file link and use this website to get the link that can be put into the excel file to be uploaded - [https://sites.google.com/site/gdocs2direct/?pli=1](https://sites.google.com/site/gdocs2direct/?pli=1)
- Copy the link generated by the above website for your file and put it in the excel/CSV cell.

**Technical link for Avni Team**

_The above website uses the following http request behind the scenes_

`curl 'https://www.google-analytics.com/g/collect?v=2&tid=G-KV5S9LK4WB&gtm=2oe1a1&_p=437198370&gdid=dZWRiYj&cid=1650660276.1673947139&ul=en-gb&sr=1440x900&uaa=x86&uab=64&uafvl=Not%253FA_Brand%3B8.0.0.0%7CChromium%3B108.0.5359.124%7CGoogle%2520Chrome%3B108.0.5359.124&uamb=0&uam=&uap=macOS&uapv=10.14.6&uaw=0&_s=1&sid=1673947138&sct=1&seg=1&dl=https%3A%2F%2Fsites.google.com%2Fsite%2Fgdocs2direct%2F%3Fpli%3D1&dr=https%3A%2F%2Fwww.google.com%2F&dt=Google%20Drive%20Direct%20Link%20Generator&en=page_view&_ee=1' 
  -X 'POST' 
  -H 'authority: www.google-analytics.com' 
  -H 'accept: _/_' 
  -H 'accept-language: en-GB,en;q=0.9,hi-IN;q=0.8,hi;q=0.7,en-US;q=0.6,de;q=0.5' 
  -H 'content-length: 0' 
  -H 'dnt: 1' 
  -H 'origin: https://sites.google.com' 
  -H 'referer: https://sites.google.com/' 
  -H 'sec-ch-ua: "Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"' 
  -H 'sec-ch-ua-mobile: ?0' 
  -H 'sec-ch-ua-platform: "macOS"' 
  -H 'sec-fetch-dest: empty' 
  -H 'sec-fetch-mode: no-cors' 
  -H 'sec-fetch-site: cross-site' 
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36' 
  --compressed`

# File: ./readme/Implementers/advanced-feature-guide/styling-the-name-of-the-page.md

title: Colourful forms
excerpt: ''
Implementers can provide the custom background color and text color to the page header(form element group). Although the implementer can choose from any color present in the color palette, we suggest choosing the contrast colors for the background and text so that the page header is visible properly.

Background and text color can be chosen from the option available at the bottom of each page. Once the colors are chosen and the form is saved, it'll be visible in the observation table in the subject dashboard and also while filling the form.

![585](https://files.readme.io/54b0c74-colourful-groups.gif "colourful-groups.gif")


# File: ./readme/Implementers/advanced-feature-guide/sync-capabilities.md

title: Sync capabilities
excerpt: ''
## Offline

Avni works completely in offline mode except during login and sync. The first time sync runs just after login.

## About Sync

* Download - Get data meant for the user from the server onto the device. It is incremental after first sync after login.
* Upload - Uploads any new data created by the user.

| Sync Initiation | Function         | Frequency      |
| :-------------- | :--------------- | :------------- |
| Login           | Download, Upload | NA             |
| Manual Sync     | Download, Upload | NA             |
| Auto Sync       | Upload           | Every hour     |
| Auto Sync       | Download         | Every 12 hours |

<br/>

## More about Auto Sync

Auto sync needs to run in the background when the user is not using the app for data integrity and app availability to the user.

* Battery usage - Upload sync should have minimal device resource usage as it will do anything only if the user has captured any new data. Download sync will run twice in a day and the duration for which it runs depends on Internet quality and amount of incremental data it has to get from the server. Also, if the internet quality is poor the device is mostly be CPU idle during the sync.
  * The users may report unusual battery usage using the Battery Usage in the settings for a period of time > 1 day.

# File: ./readme/Implementers/advanced-feature-guide/tasks.md

title: Tasks
excerpt: ''
Most activities in Avni are modeled as encounters with subjects, sometimes linked to a program. However, there are other kinds of data collection that happens in field work that is not related to any subject.\
eg: A list of contacts that need to be contacted first before creating subjects etc.  

To handle such flows, Avni now has a new mechanism called tasks. Tasks can currently be created only through the external API. They can be assigned to people, who can change the status of a task. 

## Task Configuration

Task configuration is handled currently through SQL inserts since there are no mechanisms on the App Designer. Given below are the new concepts introduced in the task configuration. 

### Task types

A task can have a type. There are currently two kinds of task types - Call and Open Subject. A Call type task helps the user call the user, while the open subject task allows the user to navigate to the subject assigned to the task. 

### Task status

A number of statuses can be configured for a task. This helps in moving these calls into buckets. Some of these cards can be marked as "terminal" tasks. A terminal task indicates that the task is complete. 

### Task search fields

If you configure a list of concepts as task search fields, they are available in the Assignment screen for filtering. This is configured per task type

### Task metadata

Some metadata (concept:value array) can be set on a task when creating it. This will help users get more information on a task before taking actions on them. 

### Task observations

Task observations are filled in when completing a task. A new form type called "Task" is configured for this purpose. The user will be given the option to fill in the form when completing a task. 

### Standard report cards for task

There is a standard report card that can be configured for tasks. This is currently the only way tasks will be visible on the Avni android app. 

## Task assignment

The web application provides a new option - "Assignment" to assign users to a task. Only one user can be assigned to a task at this time. If you assign a new user, the old user is unassigned. 

### Caveats

* Task type configuration does not have an interface on the App Designer. 
* Tasks can only be created through the external API
* Tasks can be assigned through the Assignment feature on the web application
* Tasks are not currently supported on the Data Entry App


# File: ./readme/Implementers/advanced-feature-guide/timed-questions.md

title: Timed questions
excerpt: ''
Questions can be timed in Avni. If you want the user to fill some set of questions after a particular time then you can mark the page as a timed page and specify the time when the questions on the page should be visible. You also set the stay time which forces user to fill all those questions in the mentioned time frame.

## Steps to configure timed questions

Any page can be marked as timed. It is important that you specify the start time and stay time for the timed pages. The start time indicates that the page should start at the provided time and the stay time will keep the question visible till the specified time. Once the stay time is over screen automatically moves to the next page.

<Image title="timed_page.png" alt={1809} src="https://files.readme.io/cf86f77-timed_page.png">
  Example of the timed page in the form
</Image>

There are some assumptions that must be followed to make timed questions work properly.

1. Questions inside the timed page should not be mandatory.
2. If any page is marked as timed then it should not have any visibility rule to hide the entire page. The visibility rule might get ignored.
3. Timer only runs for the first time when filling up the form. Once users have filled in all the timed questions they can go back and edit the entries. Also, the edit flow does not show any timer for the timed questions.
4. If multiple pages are timed and are placed one after the other then the same timer is used for all the pages. Only when there is at least one non-timed page in between two timed page app asks the user to start the timer again.


# File: ./readme/Implementers/advanced-feature-guide/translation-management-old.md

title: Translations
excerpt: ''
    - type: basic
      slug: creating-identifiers
      title: Creating identifiers
---
Avni allows the management of translations using the Admin web interface. Below are the steps to manage translations.

## 1. Add Languages to Organisation Config

First languages have to be added to organisation config. Only the languages that are added in the organisation config are made available to the translation framework

## 2. Download Keys

From the translations page of the Avni Admin app, download the keys after choosing the platform. For the mobile app choose 'Android'. This will download a zip file containing one JSON file per language available in the organisation config. The JSON file will contain keys for both platforms as well as implementation covering all labels in the app, form fields, and any other concepts created in the implementation. The file will contain values for any existing translations. 

## 3. Updating files with translations

The JSON files can be edited with any tool that the implementer is comfortable with. For use cases, where multiple translators are involved or a lot of keys are to be translated we recommend using an external translation management system (TMS) like [Lokalise](https://lokalise.com) which provides a sophisticated editor for performing translations. The TMS provides the ability to import/export JSON files and support a variety of use cases related to translations. Avni has an enterprise-free plan of Lokalise. If you would like to use Lokalise, please request the Avni team to create your account and project to get started.

## 4. Uploading Translations

When downloading translations to a JSON file in Lokalise, under `Advanced settings`, select `Don't export` as value for `Empty translations` field. Once the JSON files are available with updated translations, upload the file in the Avni admin interface by choosing an appropriate language. Be careful about choosing the correct language.

![](https://files.readme.io/d92456b-Screen_Shot_2019-10-21_at_5.58.47_PM.png "Screen Shot 2019-10-21 at 5.58.47 PM.png")

## Translation Dashboard

Once the translations have been uploaded, the translations dashboard will reflect the status. 

The users need to sync their devices to get the new translations.


# File: ./readme/Implementers/advanced-feature-guide/upload-checklist.md

title: Vaccination checklist
excerpt: ''
    - type: basic
      slug: upload-data
      title: Upload data
---
Avni allows you to upload checklist items from web interface. Before uploading checklist make sure you have already created checklist Item form and checklist rule is already in place. As other forms in Avni, each checklist item need to be a concept and should be uploaded/created before uploading checklist json. A sample concept file for vaccination item looks like [this](https://github.com/avniproject/avni-health-modules/blob/master/src/health_modules/child/metadata/vaccinationConcepts.json). You can directly upload these concepts using metadata upload UI.

Once all the dependencies required by checklist are deployed, you can create a checklist json in the UI editor and upload it. A sample Vaccination checklist looks like [this](https://raw.githubusercontent.com/avniproject/calcutta-kids/master/child/checklist.json).

Click [here](https://docs.google.com/spreadsheets/d/e/2PACX-1vS1Xq4cVi1pDn8B78g_BEdQOcqr5p2hTCeuyhXtpZGKGMHCyba7enJop29zYJy9UyEVYeg523lIutQC/pubhtml#) to see more examples.

### Structure of Checklist json file

```json
{
    "name": "Vaccination",
    "uuid": "uuid of this checklist. We support only single checklist in the system right now so don't change this uuid after you save the file for the first time",
    "items": [
        `<item-object>`
    ]
}
```

### Structure of item-object

```json
{
    //uuid of checklist item
    "uuid": "uuid of checklist item",
    //uuid of a form used to mark the vaccine as completed
    "formUUID": "uuid of a form used to mark the vaccine as completed",
    //uuid of a dependency. This item will get due only after the dependency is marked as completed
    "dependentOn": "uuid",
    //Set this when the dependency can expire and you want this item to be scheduled even then
    "scheduleOnExpiryOfDependency": `<boolean>`,
    //Number of days from base date of checklist after which the item becomes due. Put this only if you are also making this item dependent on another item.
    "minDaysFromStartDate": `<integer>`,
    //Number of days from completion date of dependency after which the item becomes due. Put this only if you are also making this item dependent on another item.
    "minDaysFromDependent": `<integer>`,
    //If an item can expire then you can use this to specify it. It's relative from the base date of the checklist.
    "expiresAfter": `<integer>`,
    //Array of status objects. We use this to specify different phases an item can be in. E.g. You may want to define that it's Due from day 2 to day 30, Critical from Day 30 to 60, and Overdue after day 60. 
    "status": "array of `<status-object>`",
    "concept": `<concept-object>`
}
```

### Structure of status-object

```json
{
  //Looks like an unused field right now. Set it in increasing order for now inside status array
  "displayOrder": 1,
  //Days after which this state should be active
  "start": 270,
  //Days after which this state will not be active
  "end": 291,
  //Name of state
  "state": "Due",
  //Color that the item is displayed in when this state is active
  "color": "#FBF9DA"
}   
```

### Strucuture of concept-object

```json
{
  "uuid": "uuid of the concept that should be used for this item",
  "comment": "Put the name of the concept here for readability"
}
```

### Overview

You can use checklist json file to build the checklist. You can do add list of items and for each item define a state like Due, Critical, Overdue. You can also set depedencies between vaccines so the depedent will get scheduled only after dependency is marked as completed.

## Important Questions:

#### How to test?

Change the device date in future. Don't edit date of birth in profile of the subject.

#### How to add a new item?

Add an item-object in items array

#### How to remove an existing item?

Add voided attribute to an item with value true.

#### How do you add a depedency?

Add dependentOn field

#### How is due date calculated when there is a depedency?

A dependent item goes into it's first state after completion date of it's depedency + specified value of minDaysFromDependent. But there can also be a necessity that an item has to be scheduled only after minimum number of days from base date of the checklist. In the case where we have specified both minDaysFromDependent and minDaysFromStartDate then we compute the **max** of both start dates.

```Text Example
max(dependentCompletionDate + minDaysFromDependent + item.start, 
dependentCompletionDate + minDaysFromStartDate + item.start), 
and move the item to it's first state on that date.
```

#### What will happen if my computed due date is after the expiry date.?

An item's due date based on computations of dependent's completion\_date, minDaysFromDependent and item.start, if exceeds the "expiresAfter" value, then we give priority to "expiresAfter" and mark it as expired.

### Flowchart for determining the Vaccination state:

<Image align="center" src="https://files.readme.io/815c13987e5ad6616202a18db078663bae5ec8000d94680642a418ff4e2ca2f3-Flowcharts_2.png" />

### <span style={{ color: "blue" }}>TODOS:</span>

* [ ] It is not clear if there is any default ordering in displaying status groups and is it possible to change it. E.g. we may want to show all due items in first row, all critical in second, overdue in third, expired in fourth and completed in fifth.

# File: ./readme/Implementers/advanced-feature-guide/upload-data.md

title: Bulk Data Upload
excerpt: ''
    - type: basic
      slug: writing-rules
      title: Writing rules
---
### Purpose

* Prepare data in bulk, review, and upload.
* Migrating away from an existing implementation, and need to seed with existing data.
* Your organization has a separate component where data is collected outside Avni, but you still need this data to be present with field workers using Avni.

### Using the Admin app to upload data

The Admin app of the web console has an upload option. Currently, this supports

* Upload subjects
* Upload program enrolment (excluding exit information and observations)
* Upload program encounters (excluding cancel information and observations)
* Upload encounters (excluding cancel information and observations)
* [Upload locations](location-and-catchment-in-avni)
* Upload users and catchments
* Upload metadata zip file downloaded from a different implementation

Sample files are available in the interface. Download the file, fill in values and then upload. The file is in a [CSV](https://www.howtogeek.com/348960/what-is-a-csv-file-and-how-do-i-open-it/) format.

### Form validations and rules

* All the entries in CSV are validated before saving to the database. Suppose a field is marked mandatory in the form and value is not provided in the CSV then upload fails giving the error that the mandatory field cannot be empty. 
* All form element and form element group rules are run during CSV upload, so if there is a value for any form element which is hidden then that value is ignored. This behaves similarly to how data entry is done from the web or mobile app.
* New visits get saved based on the visit schedule logic.
* Decisions are saved along with the observations based on the decision rule logic.

### Questions and Answers

#### What is the Id field in every file?

* The Id is an identifier for the row you are uploading. This is important to ensure that if you upload the same file twice, we do not create duplicate records. For import, this usually should map to the id from your previous system. For updates, you can specify the value for the Id field as the id from your previous system or the uuid generated by Avni when creating the record. If you have two different individuals or encounters to be uploaded, please ensure they are uploaded using different ids. If not, they will be overwritten. The Id can be any string. 

#### What if I have a comma in my observation?

* Wrap your observation in quotes. 

##### What if I need to upload an observation whose concept is not specified in the sample file?

* It is possible you have a computed value that is not part of the form that needs to be uploaded. Just add the concept name in the header, and it will be added to the observations. 

##### Is the order of values important?

* No. Columns can be in any order. 

##### What if I have a concept called "Id"? This will mean there are two headers in the same file with the same name.

* Unfortunately, the upload process does not support this scenario. You can potentially change the name of the concept for a little while until the upload is complete, and then change it back (if you are doing an initial import, this makes sense). If not, try changing the name of the concept (we do an exact case-sensitive string match, so you can change the concept name to something like "ID", and it should work fine).

#### How to upload data for the grouped form elements?

* Columns for the grouped form elements are labeled as "Parent|Child". One can fill in the values for all the child form elements and it'll get saved as grouped observation.

#### How do I upload images?

* For images, use a url that the avni server can download. Ensure that
  * The images are a direct download link (not a redirect to a page that uses javascript to download)
  * The image urls end with the image type. eg: [https://somedomain.com/images/abc.png](https://somedomain.com/images/abc.png)


# File: ./readme/Implementers/advanced-feature-guide/user-subject-types.md

title: User Subject Types
excerpt: ''
A user subject type is a type that can be used to manage information about users of the system. Each user will have one subject created based on a User type SubjectType. This subject and any data collected against it's encounters and enrolments correspond only to that particular user.

## Special Characteristics

* **Subject Type Create / Edit**: Once a User type SubjectType is created, Avni doesnot allow Administrators to modify the basic configurations of the SubjectType. Ensure that you configure the Subject as needed at the outset. Contact Avni Support if you need any modifications to be done for the User type SubjectType.

  * Registration Date for the subject will be same as User Creation DateTime
  * Toggle of 'Allow empty location' is disabled and is always set to true
  * User's username is inserted as Subject's Firstname
* **Subject Type Create / Edit**: You may only edit the below shown properties post SubjectType creation.

<Image align="center" width="600px" src="https://files.readme.io/ba11a11-Screenshot_2024-05-17_at_3.40.56_PM.png" />

* **Sync**: By default, User type Subjects follow their own Sync strategy, which is currently, to sync a User type Subject only to its corresponding User
* **Subject Creation**: On creation of a "User" type SubjectType, we **automatically** create User type subjects :
  * for every new User created thereafter via the "Webapp" 
  * for new Users created via "CSV Uploads", by triggering a Background Job
  * for all existing Users, by triggering a Background Job
* **Ability to Disable Registration of User type SubjectTypes on Client**: Currently, Avni allows an Organisation Administrator to disable User's ability to create any new User Subject Type Subjects on client, by following the below steps:

  1. Navigate to "App Designer", Forms Section

     <Image align="center" src="https://files.readme.io/af7a60f-Screenshot_2024-05-17_at_3.51.29_PM.png" />
  2. Click on the "Gear Wheel" icon, to load the Form-Mapping Edit view

     <Image align="center" src="https://files.readme.io/2c4cffc-Screenshot_2024-05-17_at_3.52.44_PM.png" />
  3. Click on the "Bin (Delete)" icon to Void the Form to Subject type association (Form Mapping)
* **Access to User type Subject on the client**: Users cannot make use of "Subject Search" capability to access the User type Subject on the Client. They would always have to make use of "Filter" button on "My Dashboard" to select the User type Subject, as shown below.

<Image alt="Select User type in the Subject Filter" align="center" width="500px" border={true} src="https://files.readme.io/f265252-Screenshot_2024-05-17_at_4.23.24_PM.png">
  Select User type in the Subject Filter
</Image>

For organisations that use a Custom Dashboard as the Primary Dashboard, they can easily configure a Offline Report card to provide access to User type Subject.

* **Actions allowed on the User type Subject**: Avni allows organisation to configure a User type Subject similar to the way they would configure a "Person" / "Individual" type Subject types. i.e. they are free to setup Program, Encounter, VisitScheduleRules and so on. They can also configure Privileges in-order to restrict these actions across different UserGroups. A sample screen recording of the client, which has full access to a User type Subject is attached below for reference.

<Image align="center" className="border" width="500px" border={true} src="https://files.readme.io/d966e6d-output.gif" />


# File: ./readme/Implementers/advanced-feature-guide/whatsapp-integration.md

title: Whatsapp integration
excerpt: Talk to your beneficiaries through Whatsapp
## Purpose

Being able to communicate to your beneficiaries through Whatsapp is very powerful in many scenarios of field work. It can be used to provide reminders for important events or your field-worker's visit. You can provide nudges for those who need to be follow a routine. 

#### Use cases

1. Remind everyone in a village about an upcoming Village Health and Nutrition Day (VHND)
2. Remind pregnant mothers about an upcoming ANC visit
3. Send motivational videos to all users enrolled into a de addiction programme
4. Inform a student about an upcoming interview
5. Remind a teacher and their principal about an observation session the next day
6. Remind field-workers to submit their monthly reports

## How it works

<Image align="center" width="350px" src="https://files.readme.io/5faa756-Screenshot_2023-10-13_at_1.28.13_PM.png" />

Avni uses [Glific](https://glific.org/) to send Whatsapp messages to beneficiaries and users. Glific is not just a way to connect to Whatsapp. It also provides rich communication between beneficiaries through chatbots. Glific also provides a neat way for two-way communication between beneficiaries. 

If an organisation uses Avni, a lot of information about the user is available in Avni. More importantly, Avni also understands when an important event has either happened, or is about to happen. Due to this reason, Avni is well-placed to provide reminders and nudges where they are necessary. Avni-Glific integration has three pieces. 

1. Sending of a message on a trigger. Triggers can be registration of a user, enrolment into a program or completion of a visit. When such a trigger happens, Avni can send a message to Glific at a scheduled time. 
2. Bulk send of messages for a group of users. Sometimes, the organisation needs to share a piece of information to their entire set of beneficiaries, or a sub-group within it. This can be done through a web-based mechanism
3. Sending of messages to an individual and viewing sent messages on the Avni field-app

**PS**: Interested organisations must create an account in Glific and configure Glific in Avni in order to use this functionality

### Sending messages on a trigger

In the application designer, there is an option within subject types, programs and encounter types to provide 

1. A schedule rule that specifies the time in which the message needs to be sent (once the event is triggered)
2. A message rule that helps figure out the parameters required for the message

The messages are scheduled when the event is synced to the server (or at save if you are using the Data Entry Application). 

#### Setup

First, you need to enable messaging in the Organisation Settings on the Admin page

![](https://files.readme.io/69637ed-image.png)

Next, provide details to connect to Glific into the external\_api table. This currently does not have a UI. Entries need to be made in the format. 

`insert into external_system_config(organisation_id, version, created_by_id, last_modified_by_id, created_date_time, last_modified_date_time, system_name, config)
values (2, 1, 1, 1, now(), now(), 'Glific', '{"baseUrl": "API URI field value from password manager", "phone": "Login for API field value from password manager", "password": "Password field value from password manager", "avniSystemUser": "maha@test"}'::jsonb);`

Ensure that atleast one of your form fields is marked as a phone number. This can be done by going to a **Text** or **PhoneNumber** concept, and marking its "contact\_number" value to "yes". Use this concept in the form to register the subject. It is to the value of this field, that the whatsapp message will be sent.

<Image align="center" className="border" border={true} src="https://files.readme.io/4f4f325-Screenshot_2022-11-14_at_7.07.26_PM.png" />

Once this configuration is complete, go over to the App Designer and create rules to send messages. 

There are 2 rules to be configured here. The first (Schedule rule) determines the time when the message needs to be sent. The second (Message rule) gives the parameters on the message. These parameters can be fetched from any part of the entity. The message rule should return the computed array of parameters for this entity. 

You can choose to send the message to either the subject/beneficiary or the user who made the entry. 

You can also have multiple rules defined for the same trigger. In this case, you can have a message to be sent immediately, and another to be sent after a week.

You also have the ability to not schedule a message if required by setting the `shouldSend` parameter in the response of the Schedule Rule to false. If this parameter is not set, it defaults to true i.e. the message will be scheduled.

![](https://files.readme.io/cbed815-image.png)For sending messages, for the entities(subject/encounter/enrolment) created in mobile app, the created data in mobile app should have been synced to the server.

### Bulk send of messages for a group of users

![](https://files.readme.io/958a89d-image.png)

Under Broadcast section of the Avni web application, you will now see a new option - WhatsApp. This can be used to send messages to beneficiaries, users or groups. 

Check [this](https://drive.google.com/file/d/1J2qt1s2ltJoOjQoWXdmq1GZA171usPsq/view?usp=share_link) video out, to know how to manage groups and send messages to groups.

Currently only name of the subject/user is supported as dynamic parameter. To use this, enter `@name` in the parameter input field.

### Limitations

Currently, only HSM messages is in scope of this integration. Eventually, the integration will also include triggering workflows in Glific.

### Viewing messages for a Subject, User or a Group

Currently, through the web-app, we are able to look at the Sent and Scheduled messages for a Subject, User or a Group, with a caveat that only the latest 100 messages are fetched. This is due to performance constraints in Avni-Glific data fetch.

### Debugging

* To understand the db design for debugging, checkout [this](https://avni.readme.io/docs/understanding-whatsapp-integration-tables#to-understand-the-status-of-automatic-messages) and [this](https://dbdiagram.io/d/63bb840e7d39e42284e9a83d) link.
* To view the logs printed when executing message rule or schedule rule execute the following after ssh-ing into the server machine:

  ```
  sudo su - rules-server-user
  pm2 logs --lines 1000
  ```
* If expected message not delivered, can check in the glific webapp (credentials in keeweb) to see if any error displayed beside the message in the chat. Sometimes say, when the phone no is invalid or the expected no of parameters not mentioned, an error message stating the reason for inability to deliver the message gets displayed in the chat.
* The background job that runs for sending messages from message\_request\_queue table is currently configured to run once in 5 mins.
* In order to handle scenarios where either system is unavailable, the background job retries messages that were not successfully sent. Messages older than a certain period are not retried. Default: 4 (days); Configuration: `AVNI_SEND_MESSAGES_SCHEDULED_SINCE_DAYS`


# File: ./readme/Implementers/advanced-feature-guide/when-to-use-translations.md

title: When to use Translations
excerpt: ''
Since the issue of change in concept name has come up a few times - in terms of what impact it would have on rules. Also, we use uuid for concept as the name can change - but this reduces readbility of the rule.\
Here is a mental model to think about this.

Concept name, form element name should be considered programming keywords - representing an idea.\
e.g. Mother's name\
When we name a concept/element in app designer we are defining a name for it in the programming realm not in the user realm.

How this idea is presented to user is using an English translation or another language translation.\
What does English translation represent?\
It represents a mapping from the idea to a view for the user.

So two realms - programming and user.\
What is the benefit of this?

As long the the core idea doesn't change, there is no need to change the name of the concept/element.\
e.g. if the customer says we want to call it - Name of mother - then it is a change only in the user's realm not programming realm.

So we can simply change/add a translation for it based on the user/customer's preference. The translation feature offers a decoupling between programming and user realm.

Following from this, there is no need to use UUID of the concept in the rule. Why? Because once the concept/element name is defined, there is no need to change it based on what user/customer wants it to be named.

Concept/element should be renamed only if there is a semantic change in the idea behind it - this happens very rarely.

If there a typo in the name, then you can change it, but remember there is cost to it - which may or may not be worth paying - depending on how deep you have been in the cycle of the project.\
Avni has been designed such that almost everything can be shown to the user in their own language.\
But what also follows from this is - everything is also defined separately in the programmer and user realms.


# File: ./readme/Implementers/basic-feature-guide/avnis-domain-model-of-field-based-work.md

title: Avni's domain model of field based work
excerpt: ''
    resulting in a working application specific to your
    organisation/implementation.
  pages:
    - type: basic
      slug: key-system-and-data-flows
      title: Key system and data flows concepts
---
To understand how Avni works lets first understand the domain model of field-based work. Any field-based work can be broadly subdivided into three components.

1. **Service delivery organisation** - The organisation, with providers and the geographical area where they work.
2. **Services (or schema of data to be collected)** - The actual set of services provided by the above organisation to the people (or data to be collected about something in a said geographical area).
3. **Service encounter** - Each service is broken down into a discrete set of type of encounters that providers of the organisation have with the people.

Now lets further explore each one of the above one by one and how Avni models it into the software system.

# 1.  The architecture of the service delivery organisation

Avni allows for modelling of the work geography of the organisation and mapping of service providers to their geographical units. In avni, one can set up the complete geographical area into multiple levels and locations at the same level.

Lets first identify the key domain concepts with their names. A service delivery organisation consists of the following:

* An **organisation** (e.g. NGO, or government department, university), the entity that provides the service or collects some data.
* In order to provide this service or collect data, this organisation employs, hires or engages service providers. They can be called field workers, frontline worker, health worker, etc - we will simply call them **provider or user**.
* The service provided by the organisation via the providers is received by *beneficiaries, citizens, patients, students, children* so on. In the case where the work is data collection, the provider may be additionally or only collecting data for non-living objects like *water body, school, health centre*, etc. Since Avni is a generic platform, let's call of them by a rather imaginative name **subject**.
* In most Avni use cases, the subjects may be spread across a geographical area such that one provider cannot service (or collect data from) all subjects. Hence each provider is assigned a specific area that is called **catchment** in Avni. A catchment could be a block, a cluster of slums, etc.
* Each catchment may have one or more geographical units which are called **location**s in Avni. A location could a village, slum, subcenter area so on.

Each user **must** to be associated with at least one catchment.

![1918](https://files.readme.io/4343bff-Screenshot_2019-11-15_at_5.17.05_PM.png "Screenshot 2019-11-15 at 5.17.05 PM.png")

<Image title="Screenshot 2020-11-16 at 11.50.38 AM.png" alt={2372} src="https://files.readme.io/514028d-Screenshot_2020-11-16_at_11.50.38_AM.png">
  An example of service delivery organisation
</Image>

In Avni system, the organisation, provider, catchment and location are setup via web application by the implementer, IT or program administrator. When a subject is created/registered in the system, they are assigned a location. This is usually done by the field user using their mobile device

# 2.  Modelling the services provided into Avni

Avni allows for modelling of the services provided (or data collected) via a three-level configurable data structure. Avni allows for setting up subjects, enrolment of subjects in programs, and defining encounters for enrolments/subjects. There can be multiple programs per subject type and multiple encounter types per program.

* An organisation may have one or more **subject types** to which they provide service (or collect data for).
* To each subject type, the organisation may be providing one or more service types (or have the purpose of data collection). In Avni, each service type is called a **program**.
* Each service type may involve one or more types of interactions which are called **encounter type**s. Avni also allows one to avoid the service type completely and define encounter types directly for the subject types - allowing for modelling of interactions which are not required to be grouped under services.

![2084](https://files.readme.io/b63d3c9-Screenshot_2019-11-15_at_5.26.15_PM.png "Screenshot 2019-11-15 at 5.26.15 PM.png")

![1942](https://files.readme.io/93a551a-Screenshot_2019-11-15_at_5.27.48_PM.png "Screenshot 2019-11-15 at 5.27.48 PM.png")

![1906](https://files.readme.io/3ca82d4-Screenshot_2020-09-23_at_6.00.45_PM.png "Screenshot 2020-09-23 at 6.00.45 PM.png")

# 3. Groups and relationships

Avni allows for creating groups of subjects and more specifically a special type of group called household or family whereby another subject types (created to represent people) can be members of the household. These members can also be linked to each other via relationships. Do note though that in Avni we have modelled group and households via attributes on subject types. The subjects of such types can be linked as child elements of the parent subject. Please the diagrams below. Avni application behaves differently for groups and households.

<Image title="Screenshot 2020-04-28 at 11.20.04 AM.png" alt={2374} src="https://files.readme.io/a5fd36e-Screenshot_2020-04-28_at_11.20.04_AM.png">
  Group also can behave like subjects also, along with being a group of subjects.
</Image>

<Image title="Screenshot 2020-04-28 at 11.16.09 AM.png" alt={2750} src="https://files.readme.io/740185f-Screenshot_2020-04-28_at_11.16.09_AM.png">
  Household is a special type of group, which has persons as members. The persons can be related to each other via human relationship types.
</Image>

# 4.  Design of a service encounter

Service encounter is an encapsulation of a type of interaction between the service provider and the beneficiary - as explained above. Each service encounter consists of the following:

* observation made by the service provider (field workers)
* answer is given by the beneficiary for a question asked by the provider
* information/suggestion/recommendation made by provider
* computed or preset information provided by the avni app to the provider
* photos/videos taken by the provider

Avni allows you to arrange these sequentially and including based on conditions set by you. It also allows to schedule next service encounters based on a rule set by you. This is modelled using form, rules and content. Each service encounter can be defined in this way.

<Image title="Screenshot 2019-11-15 at 5.30.31 PM.png" alt={2040} src="https://files.readme.io/d7f0b31-Screenshot_2019-11-15_at_5.30.31_PM.png">
  Anatomy of an encounter type (or a subject registration form)
</Image>

<Image title="Screenshot 2019-11-15 at 1.53.16 PM.png" alt={1814} border={true} src="https://files.readme.io/5fdb3eb-Screenshot_2019-11-15_at_1.53.16_PM.png">
  Example of a few form element groups.
</Image>

<Image title="Screenshot 2019-11-15 at 1.55.34 PM.png" alt={2180} border={true} src="https://files.readme.io/2c87d92-Screenshot_2019-11-15_at_1.55.34_PM.png">
  Example of form elements within a form element group.
</Image>


# File: ./readme/Implementers/basic-feature-guide/concepts.md

title: Concepts
excerpt: Learn about the different types of concepts and their nuances
    - type: basic
      slug: rules-concept-guide
      title: Rules concept guide
---
**Concepts** define the different pieces of information that you collect as part of your service delivery.  

For example, if you collect the blood pressure of a subject in a form, then "*Blood Pressure*" should be defined as a concept. You would notice that every question in a form requires a concept.  

The *datatype* of a concept determines the kind of data can be stored against a concept, and therefor against the form question or form element. Using concepts with datatypes ensures incorrect answers are not captured in a form question, and is helpful for eventually data aggregation, validation and reporting.

## Supported DataTypes in Concepts

The following datatypes are supported while defining concepts to be used in forms:

<Table align={["left","left"]}>
  <thead>
    <tr>
      <th>
        Concept DataType
      </th>

      <th>
        Description
      </th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>
        * Numeric\_ **concepts** 
      </td>

      <td>
        Numeric concepts are used to capture numbers. When creating a numeric concept, you can define normal ranges and absolute ranges. In the field application, if an observation for a concept collected goes beyond the normal range, then it is highlighted in red. Values above the absolute range are not allowed.  For instance for concept: Blood Pressure (Systolic), you can choose a Numeric concept with ranges.
      </td>
    </tr>

    <tr>
      <td>
        **Coded concepts (and NA concepts)** 
      </td>

      <td>
        Coded concepts are those that have a fixed set of answers. For instance for Blood Group you would choose a coded concept with values: A+, B+, AB+, etc.  

        These answers are also defined as concepts of NA datatype.
      </td>
    </tr>

    <tr>
      <td>
        **ID datatype** 
      </td>

      <td>
        A concept of Id datatype is used to store autogenerated ids. See [Creating identifiers](doc:creating-identifiers) for more information on creating autogenerated ids.  For instance PatientIDs, TestIDs, etc.
      </td>
    </tr>

    <tr>
      <td>
        **Media concepts (Image, Video and Audio)**
      </td>

      <td>
        Images and videos can be captured using Image and Video concept datatypes. For audio recording, Audio datatype can be used.
      </td>
    </tr>

    <tr>
      <td>
        **Text (and Notes) concepts** 
      </td>

      <td>
        The *Text* data type helps capture one-line text while the *Notes* datatype is used to capture longer **form** text.
      </td>
    </tr>

    <tr>
      <td>
        **Date and time concepts**
      </td>

      <td>
        There are different datatypes that can be used to capture date and time.  

        * \*Date\*\* - A simple date with no time  
        * \*Time\*\* - Just the time of day, with no date  
        * \*DateTime\*\* - To store both date and time in a single observation  
        * \*Duration\*\* - To capture durations such as 4 weeks, 2 days etc.
      </td>
    </tr>

    <tr>
      <td>
        **Location concepts**
      </td>

      <td>
        * Location\_ concepts can be used to capture locations based on the location types configured in your implementation.  

        Location concepts have 3 attributes:  

        1. Within Catchment - Denotes whether the location to be captured would be within the catchment already assigned to your field workers. This attribute defaults to true and is mandatory.

        2. Lowest Level(s) - Denotes the lowest location type(s) you intend to capture via form elements using this concept. This attribute is mandatory.

        3. Highest Level - Denotes the highest location type that you would like to capture via form elements using this concept. This attribute is optional.
      </td>
    </tr>

    <tr>
      <td>
        **Subject concepts**
      </td>

      <td>
        * Subject\_ concepts can be used to link to other subjects.  

        Each Subject concept can map to a single subject type.  

        Any form element using this concept can capture one or multiple subjects of the specified subject type.
      </td>
    </tr>

    <tr>
      <td>
        **Phone Number concepts**
      </td>

      <td>
        For capturing the phone number. It comes with a 10 digit validation. OTP verification can be enabled by turning on the "Switch on Verification" option. Avni uses msg91 for OTP messages, so msg91 `Auth key` and `Template` need to be step up using the admin app.
      </td>
    </tr>

    <tr>
      <td>
        **Group Affiliation concepts** 
      </td>

      <td>
        Whenever automatic addition of a subject to a group is required  Group Affiliation concept can be used. It provides the list of all the group subjects in the form and choosing any group will add that subject to that group when the form is saved.
      </td>
    </tr>

    <tr>
      <td>
        **Encounter** 
      </td>

      <td>
        * Encounter\_ concepts can be used to link an encounter to any form.  

        Each Encounter concept can map to a single encounter type.  It should also provide the scope to search that encounter. Also, name identifiers can be constructed by specifying the concepts used in the encounter form.  

        Any form element using this concept can capture one or multiple encounters of the specified encounter type.
      </td>
    </tr>
  </tbody>
</Table>

<br />

## Showing counselling points in Forms

For showing counselling points in a form, always create a Form Element, using below coded Concept:

* Concept UUID: b4e5a662-97bf-4846-b9b7-9baeab4d89c4
* Concept Name: Placeholder for counselling form element
* Answers: \<None, no answers, to avoid showing them any options>

Specify counselling point as the Form Element Name, add numbering if needed.

Note: **You can reuse the same "Placeholder for counselling form element" multiple times in a single form**, without worrying about uniqueness constraint breach concerns.


# File: ./readme/Implementers/basic-feature-guide/draft-simplification-of-reports/avni-metabase-reporting-standards-best-practices.md

title: 'Avni Metabase Reporting : Standards & Best Practices'
excerpt: >-

#### **Three-Tier Dashboard Layout:**

```
Row 1: Summary & Description
├── Dashboard title and purpose description
├── Explanation of Filters available
└── Key metrics overview

Row 2: Total Count Cards  
├── Aggregate metrics from base query
└── Apply Conditional filters only where appropriate

Row 3+: Filtered Linelists
├── Detailed records for each count card
└── Conditional filters applied
```

#### **Implementation Guidelines:**

* **Base Query Foundation**: All dashboard elements derive from a single, well-defined base query
* **Hierarchical Information Flow**: Summary → Aggregates → Details
* **Consistent Filtering**: Apply same filter logic across all dashboard components
* **User Journey**: Enable logical progression from high-level insights to detailed records

### **2. Dashboard Purity Principle**

#### **Primary Table Focus:**

* **Single Source of Truth**: Each dashboard should have one primary table as its foundation
* **Controlled Joins**: Join additional tables only for supplementary information, not core metrics
* **Avoid Data Mixing**: Don't combine unrelated data sources in a single dashboard

#### **When to Split Dashboards:**

```
❌ Bad: Combined Dashboard
- Subject registrations + Program enrollments + Encounter data
- Multiple unrelated KPIs in one view
- Mixed time periods and contexts

✅ Good: Separate Dashboards  
- Subject Registration Dashboard (primary: beneficiary table)
- Program Performance Dashboard (primary: beneficiary_pregnancy table)
- Service Delivery Dashboard (primary: beneficiary_pregnancy_anc tables)
```

#### **Benefits of Pure Dashboards:**

* **Performance**: Faster query execution
* **Maintainability**: Easier to debug and modify
* **User Experience**: Clear, focused insights
* **Data Integrity**: Reduced risk of incorrect joins

### **3. Complex Query Management via PostETLSync**

#### **PostETLSync Overview**

PostETLSync enables custom data transformations after standard ETL completion through configurable SQL transformations. This feature supports incremental processing, ordered execution, and organization-specific configurations while ensuring data integrity through transaction management.

#### **When to Use PostETLSync:**

* **Views Persisted Across ETL Schema Recreates**: Maintain custom views and derived tables that survive ETL schema rebuilds
* **Derived Tables**: Create complex aggregated views from multiple source tables
* **Custom Business Logic**: Implement organization-specific calculations and transformations
* **Performance Optimization**: Pre-compute complex queries for faster dashboard loading
* **Incremental Updates**: Process only changed data since last sync using timestamp filtering

#### **Configuration Structure:**

PostETLSync uses JSON configuration files (`post-etl-sync-processing-config.json`) with two main sections:

* **DDL Operations**: Create tables, indexes, and database objects (executed first)
* **DML Operations**: Insert and update data with ordered execution and parameter substitution

#### **Key Features:**

* **Automatic Parameter Substitution**: `:previousCutoffDateTime` and `:newCutoffDateTime` for incremental processing
* **Schema-Qualified Operations**: All table references must include schema names for proper permissions
* **Timestamp Filtering**: Built-in support for processing only modified records
* **Transaction Safety**: Ensures data consistency during transformation processes

#### **Best Practices:**

* Always use both timestamp parameters in data modification queries
* Include `is_voided = false` checks when applicable
* Use descriptive prefixes for SQL script naming
* Apply timestamp filters to all subqueries and CTEs
* Begin DDL scripts with appropriate role setting for permissions

This approach transforms complex reporting requirements into maintainable, performant solutions that integrate seamlessly with Avni's ETL pipeline while providing the flexibility needed for organization-specific reporting needs.

### **4. Implementation Best Practices**

#### **Base Query Design:**

```sql
-- Standard base query structure
SELECT 
    -- Primary identifiers
    subject.uuid,
    subject.first_name,
    subject.last_name,
    
    -- Core metrics
    program.name as program_name,
    enrolment.enrolment_date_time,
    
    -- Derived fields for filtering
    CASE WHEN enrolment.program_exit_date_time IS NULL 
         THEN 'Active' ELSE 'Exited' END as enrollment_status,
    
    -- Location hierarchy for geographic filtering
    village.title as village,
    block.title as block,
    district.title as district

FROM beneficiary subject
JOIN beneficiary_pregnancy enrolment ON subject.id = enrolment.individual_id
JOIN program ON enrolment.program_id = program.id
-- Add location joins as needed
WHERE subject.is_voided = false 
  AND enrolment.is_voided = false
```

#### **Dashboard Card Organization:**

1. **Summary Card**: Dashboard description and key insights
2. **Count Cards**: Total enrollments, active cases, completed visits
3. **Linelist Cards**: Detailed records filtered by each count metric

#### **Filter Strategy:**

* **Consistent Parameters**: Same date ranges, locations, programs across all cards
* **Cascading Filters**: Location hierarchy (State → District → Block → Village)
* **User-Friendly Defaults**: Reasonable default values for common use cases

### **5. Quality Assurance Guidelines**

#### **Dashboard Review Checklist:**

* [ ] Single primary table identified
* [ ] All cards use same base query logic
* [ ] Filters work consistently across all cards
* [ ] Performance acceptable (\< 30 seconds load time)
* [ ] Data accuracy verified against source systems
* [ ] User permissions properly configured

#### **Documentation Requirements:**

* Dashboard purpose and target audience
* Base query explanation and assumptions
* Filter definitions and expected behaviors

### **6. Reference Implementation**

Following the <Anchor label="Avni reporting simplification guidelines" target="_blank" href="https://avni.readme.io/docs/draft-simplification-of-reports">Avni reporting simplification guidelines</Anchor>, these principles ensure:

* **Scalable Architecture**: Reports that perform well as data grows
* **Maintainable Codebase**: Clear separation of concerns
* **User-Centric Design**: Intuitive navigation from summary to detail
* **Data Governance**: Consistent metrics across the organization

This structured approach transforms complex organisational data into actionable insights while maintaining system performance and user experience quality.


# File: ./readme/Implementers/basic-feature-guide/encounter-type.md

title: Encounter types
excerpt: ''
    - type: basic
      slug: concepts
      title: Concepts
---
Encounter Types (also called Visit Types) are used to determine the kinds of encounters/visits that can be performed. An encounter can be scheduled for a specific encounter type using rules. Here, we define that encounter type and the forms associated with the encounter type.

An encounter type is either associated directly with a Subject type or is associated with a Program type, which in-turn would be associated with a subject type. It need not always be associated with programs (you can perform an annual survey of a population using encounter types not associated with programs, and use this information to enrol subjects into a program).

## Immutable encounter type

The encounter type can be made immutable by switching on the immutable flag on the encounter type create/edit screen. If the encounter type is marked as immutable then data from the last encounter is copied to the next encounter. Since the encounter is immutable, the edit is not allowed on these encounters.


# File: ./readme/Implementers/basic-feature-guide/internal-details-of-avni-sync.md

title: Sync internals
excerpt: ''
Synchronization (sync) of data from the Avni server to the client is a complex procedure. This document tries to explain it in detail. 

Note that this is an advanced topic that can be skipped for those who are not very familiar with Avni. 

### The primary assumptions related to data collection in Avni

A single User effects a change in data stored on the server for a particular Individual at any given point of time. After this all clients subscribing to that Individual's data are supposed to fetch the latest information from the server and only then perform any other actions related to that Individual. This is implemented through means of providing Idempotent POST Apis for all major entity types in Avni.

This is done, so that, there are no concurrent conflicting changes applied for the same Individual by different users, which would results in indeterminate state for the Individual's data.

### The different objectives of sync

During sync, the primary objective is to push all local changes to the server, and fetch all changes from the server to the device. However, there are a few other side-effects that take place during the sync. 

* #### Handling of change of permissions

When there is a change in the permissions of a user, new entities may need to be synced, or existing entities may need to be deleted from the device. This is handled on the fly during the sync. 

* #### Migration of beneficiaries

Sometimes beneficiaries are migrated from one catchment to another. To handle this, we might either have to retrieve all records of a beneficiary that moved in, or remove all records of a beneficiary that moved out. This is handled through a subject\_migration sync mechanism

**It is highly recommended that any correction to an Individual or its related entities "SyncConcept observations" be made using Individual (POST/PUT/PATCH) External API calls**, so that we perform a holistic update of the Individual and all its related entities( Enrolments, Encounters, Program-encounters, Checklists, EntityApprovalStatus, IndividualRelationships, etc..). We would also be creating the SubjectMigration entities, which are essential in removing the beneficiary records from Users who should no longer have the entity.

* #### Reset of sync

If the catchment of a beneficiary changes (either via change of a user's catchment, or a change in the catchment itself), the existing database becomes invalid and needs a complete resync to ensure the right beneficiaries are present. This is called a sync reset. 

There are partial resets that happen due to change of sync attributes of a particular subject type. This is also handled through smaller sync resets. 

* #### Fast sync

When a user is syncing for the first time, some implementations create an existing Realm database for that catchment that has been synced upto a certain point. The app downloads this pre-created database and syncs everything since that point. This is useful when there are multiple users sharing a catchment, or when a user wants to login from another device. 

### Sync specific data storage

Each app maintains its status of sync through three tables - EntityQueue (for push), EntitySyncStatus (for pull) and SyncTelemetry (for telemetry). 

* #### EntityQueue

There are actually 2 tables that are maintained in Avni for entities that have been either created or changed. These are 

* EntityQueue
* MediaQueue

Before syncing media, observations are stored with the name of the media file. During sync, it is assumed that internet is present. 

During this time, the sync service does the following

1. For each of the media queue items:
   1. It pushes the media to S3 and
   2. On Success, replaces the corresponding observation with the S3 url
   3. Otherwise, for failures, it creates a "Media '$\{Entity}' Error" entry in the EntitySyncStatus, to highlight issues during upload of Media content. These entries get cleaned up only when those exact Media content get synced successfully to the server. If in-case the media gets deleted from the device or did not exist even before the first sync attempt, then those "Media '$\{Entity}' Error" entries remain as is till User does a fresh sync 
2. Only if all Media are uploaded successfully, do the modified Avni entities (with observations having the S3 url) get pushed to the server

At the end of sync, a sync telemetry entries are pushed to the server. 

* #### EntitySyncStatus

The EntitySyncStatus table keeps a pointer of each kind of entity to be synced and the last time it was synced. This helps the sync process to start from where it left off last time. Rows will contain the entity type (Subject, Encounter etc), the specific entity type (Individual, Household, ANC etc. essentially the subject type, program or encounter type) and the last sync time. 

The server api provides a paginated service to pull from the last sync time. The table is updated on each page synced. 

* #### EntityMetadata

This is maintained in code, and provides the following for each kind of entity

* Name of the entity
* url to fetch the entity from the server
* Type of entity - entity can be divided into metadata and transactional data
* Order of sync - The sync is dependent on a specific order. Subjects need to be synced before program encounters etc. 

Sync uses EntityMetadata in conjunction with EntitySyncStatus (for pull) or EntityQueue (for push) to identify the exact order in which entities need to be synced. 

* #### Sync Telemetry

Sync Telemetry notes down the details of each sync - the kind of sync, start time, end time, number of entities synced, app details etc and pushes it to the server for analysis. 

### Detailed sync steps

The sync process can be broadly divided into two activities

1. Data Server sync
2. Media sync\
   In the Data Server sync, all data except media is synced to the server. This is a 2-way sync\
   In the Media sync, media observations are taken from the MediaQueue and uploaded. Observations are modified to match the new S3 urls. 

In our current sync process, if there is media, we do a media sync first and then a data server sync. If there is no media, then we do a single data server sync. 

Once the data server sync and media sync is complete, sync telemetry is uploaded to the server. 

#### Data Server Sync

Here are the steps for a data server sync

1. Retrieve /syncDetails. This sends the existing EntityMetadata to the server to identify all the entities that have changed since the last sync. Only relevant entities are then synced to the client. 
2. Upload all entities marked in the EntityQueue
3. Verify if a data reset is required. If it is, then perform necessary resets
4. Get all reference data
5. Update database to account for new privileges if any (privileges are part of reference data)
6. Get all transactional data
7. Perform any migrations necessary (migration data is part of transactional data. New subjects are downloaded in one-shot with all transactions of a subject retrieved using the /subject/$\{subjectUUID}/allEntities endpoint)
8. Download images linked to news broadcasts
9. Download extensions if any
10. Download icon images of subject types

#### Media server sync

Media content are taken from the MediaQueue and uploaded to S3. Once this is done, these observations are modified to have the S3 url as part of the observation instead of the local file name. The next data server sync syncs these new entities back to the server. 

### Automated sync

Since release 3.36, there is now an automated sync mechanism. With this, entities are synced automatically on a timed basis. This happens once every hour, only if a sync was not run within the last half an hour. Normally, this only includes uploading entities that have been changed on the client. If it has been more than 12 hours since we have had a full sync, then the app does a full sync instead. From release 4.0.0, automated sync can be disabled from user settings in both field app and  webapp.

### Sync from a server's perspective

#### Sync strategy

While the app does not worry too much about the data that is being downloaded, the server ensures that only the right data is being sent to the app. Each subject is synced to the app of a user based on a few conditions

1. If the catchment of the subject matches the catchment of the user
2. If the sync attributes on the registration form of the subject matches the sync attributes of a user
3. If the subject is assigned to the user

The exact sync strategy is defined in a subject type. 

You can read more about the different Sync strategies supported in Avni [here](https://avni.readme.io/docs/sync-strategies).

#### Other tidbits

All transactional data except entity approval status is synced based on catchment. From release 3.38, entity approval status is also synced based on catchment. All reference data except locations is completely synced to the app. Locations are filtered by catchment of the user. 

The /syncDetails call is used to ensure that only relevant entities are requested by the app for a sync. This greatly reduces the number of calls on unchanged entities (there could be about 100 different entities present for an implementation, and only about less than 10 change frequently). 

Only data that has been in the server for more than 10 seconds from the time of the start of sync is provided to the app. This is to prevent in-process transactions from being missed out, and ensures that partial transactions that happen during the sync do not cause any errors


# File: ./readme/Implementers/basic-feature-guide/key-system-and-data-flows.md

title: Key system and data flows concepts
excerpt: ''
    - type: basic
      slug: subject-types
      title: Subject types
---
Now that we understand the [three key components of fieldwork](doc:avnis-domain-model-of-field-based-work) i.e. Organisation, Services and Service Encounter - let's try to understand how Avni works and achieves various functions.

# How implementation-specific mobile application is created?

Avni is a generic platform that allows any organisation doing field-based work to use it for their specific purpose. The diagram below explains the steps involved in creating an organisation-specific application from a generic platform.

<Image title="Screenshot 2019-11-15 at 5.33.27 PM.png" alt={1440} align="center" src="https://files.readme.io/8932d2e-Screenshot_2019-11-15_at_5.33.27_PM.png">
  Data flow of organisation, services and service encounter definition.
</Image>

# How does avni field user gets all the subject data on his/her device?

As we saw earlier, given the organisation work physically consists of catchments and locations. The subjects are living or located at these locations.

<Image title="Screenshot 2019-11-15 at 5.35.21 PM.png" alt={1726} align="center" src="https://files.readme.io/0f59c92-Screenshot_2019-11-15_at_5.35.21_PM.png">
  During organisation setup the implementer or customer IT person sets up catchments with locations and assigns them to the provider (field user)
</Image>

The diagram below shows how the subjects and the subjects's complete data, which is required by the field user (and only those subjects) are made available.

<Image title="Screenshot 2019-11-15 at 6.07.48 PM.png" alt={1580} align="center" src="https://files.readme.io/8e8be68-Screenshot_2019-11-15_at_6.07.48_PM.png">
  Subjects belonging to the catchment of the user downloaded to their device
</Image>

# How Avni works in an offline mode

Avni maintains a database on the mobile device. All the data downloaded from the server is kept on this device. When the user is using the application, all the data is served from this device to the user and all the new data created by the user is stored in the mobile database. When the synchronisation happens this new data is sent to the server.

# How does the generic avni mobile application behave as if it has been developed for a specific organisation?

The diagram below explains how avni app customises itself based on the complete organisational setup (explained earlier).

<Image title="Screenshot 2019-11-15 at 5.52.34 PM.png" alt={1792} align="center" src="https://files.readme.io/8033619-Screenshot_2019-11-15_at_5.52.34_PM.png">
  Avni app customises itself based on the organisation data setup present in the mobile database on the device
</Image>


# File: ./readme/Implementers/basic-feature-guide/performance-expectations.md

title: Performance expectations
excerpt: ''
In the table below different performance items have been listed with the rough expectations of how long they should take. If during your testing you see response times not inline with the following table, please get it verified by the platform team or technical leads in your team, if indeed the response time is OK.

### Implementation

<Table align={["left","left","left"]}>
  <thead>
    <tr>
      <th style={{ textAlign: "left" }}>
        Performance Item
      </th>

      <th style={{ textAlign: "left" }}>
        General Expectation
      </th>

      <th style={{ textAlign: "left" }}>
        Raise red flag
      </th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td style={{ textAlign: "left" }}>
        **SuperSet/Metabase Dashboard**
        (with or without filters)
      </td>

      <td style={{ textAlign: "left" }}>
        \< 10 seconds
      </td>

      <td style={{ textAlign: "left" }}>
        > 20 seconds
      </td>
    </tr>

    <tr>
      <td style={{ textAlign: "left" }}>
        **SuperSet/Metabase Line list download**
      </td>

      <td style={{ textAlign: "left" }}>
        \< 60 seconds
      </td>

      <td style={{ textAlign: "left" }}>
        > 3 minutes
      </td>
    </tr>

    <tr>
      <td style={{ textAlign: "left" }}>
        **Offline mobile dashboard**\
        (with or without filter values,\
        for any catchment size; on any device)
      </td>

      <td style={{ textAlign: "left" }}>
        \<= 2 seconds
      </td>

      <td style={{ textAlign: "left" }}>
        > 5 seconds
      </td>
    </tr>

    <tr>
      <td style={{ textAlign: "left" }}>
        * \*Summary and Recommendations\
          Screen\*\* (mobile app; on any device)
      </td>

      <td style={{ textAlign: "left" }}>
        \<= 2 seconds
      </td>

      <td style={{ textAlign: "left" }}>
        > 5 seconds
      </td>
    </tr>
  </tbody>
</Table>

### Platform

These are platform issues, but may have been caused by some specific configuration of the organisation, hence may not be a known issue. So please feel free to report them.

<Table align={["left","left","left"]}>
  <thead>
    <tr>
      <th>
        Performance Item
      </th>

      <th>
        General Expectation
      </th>

      <th>
        Raise red flag
      </th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>
        **Incremental sync**
        (on wifi network; on any device)
      </td>

      <td>
        \< 20 seconds
      </td>

      <td>
        > 1 minute
      </td>
    </tr>

    <tr>
      <td>
        * \*Subject search\*\* (mobile app; on any device)
      </td>

      <td>
        \<= 3 seconds
      </td>

      <td>
        > 5 seconds
      </td>
    </tr>

    <tr>
      <td>
        * \*DEA subject search\*\* (after release 10)\
          with/without filters
      </td>

      <td>
        \<= 5 seconds
      </td>

      <td>
        > 10 seconds
      </td>
    </tr>

    <tr>
      <td>
        **All admin / app designer screens**\
        (Except CSV, bundle uploads)
      </td>

      <td>
        \<= 5 seconds
      </td>

      <td>
        > 10 seconds
      </td>
    </tr>
  </tbody>
</Table>


# File: ./readme/Implementers/basic-feature-guide/rules-concept-guide.md

title: Rules concept guide
excerpt: ''
Avni uses rules, or more accurately snippets of code (functions are written in JavaScript) in multiple places to provide flexibility to the implementers/developers to customise what Avni can do for the users. One can think of the rule system of Avni as a set of hooks that can be used by the rule authors to plug their own data/behaviour/logic to the app when it is used in the field and in the data entry application.

The rules are simple JavaScript functions that receive all the data via function parameters and they should return to the platform what it wants to get done. There is no state that needs to be maintained by JavaScript functions across invocations.

## Why are rules needed in Avni?

Since Avni is a general-purpose platform it doesn't know certain details about your problem domain. Wherever Avni doesn't know this - it leaves a hook for the implementer to provide the missing functionality.

## Overview of various rules

Complete programmatic reference is provided in the [Writing rules](doc:writing-rules), the following diagram explains how most of the rules are used. It displays navigation between the different screens and shows the rules that are triggered in the yellow boxes.

<Image align="center" className="border" width="80%" border={true} src="https://files.readme.io/37b4a00-Screenshot_2024-02-21_at_8.51.57_PM.png" />

In most rules, the rule has access to all the data of the subject and any data that is logically linked to the subject. e.g. In an encounter form level rule, one can access its subject form data, subject's relatives data, subject's relatives encounter data and so on.

#### Validation Rule

Validate the entire form. Last page of the form wizard. One per form.

#### Decision Rule

Add additional system generated observations. Last page of the form wizard. One per form.

#### Visit (Encounter) Schedule Rule

Create scheduled encounters with only due dates and no data.

#### Worklist Updation Rule

To display next forms on completion of one form.

#### Subject/Enrolment Summary

Display chosen information to summarise subject/enrolment on Subject dashboard screen.

#### Encounter/Enrolment Eligibility Check Rule

Before displaying list of forms that the user can fill check and filter out forms.

#### Manual Enrolment Eligibility Check Rule

If this rule is present, a custom form is shown to the user when the user starts enrolment. Based on the data filled and other subject data the rule decides which programs to display.

#### Edit Form Rule

If defined it can disallow editing of any form based on the rule. This rule is applied after access control is checked. This is available for: Registration, Enrolment, Enrolment Exit, Program Encounter, Program Encounter Cancel, General Encounter, General Encounter Cancel, Group Subject Registration, Form Element Group Edit and Checklist Item. It is not available/applicable for:

* Location
* Task (as there is no edit screen for it)
* SubjectEnrolmentEligibility, ManualProgramEnrolmentEligibility (these are unused features as of now)
* Encounter Drafts, Scheduled Encounters - should always be editable/fillable unless controlled by access control.


# File: ./readme/Implementers/basic-feature-guide/setting-up-your-data-model.md

title: Setting up your data model
excerpt: ''
    - type: basic
      slug: my-dashboard-and-search-filters
      title: My Dashboard and Search Filters
---
As explained in [Implementer's concept guide - Introduction](doc:implementers-concept-guide-introduction) - subject, program and encounter are the three key building blocks you have - using which you can model almost all field-based work. Groups (households) that are a special type of subject will be treated as the fourth building block.

In the web application, you would see three menus which map to above - subject types, programs and encounter types. You must be assigned an organisation admin role to be able to do this. If you are, then you can see these options under the Admin section. Each one of the following is linked to their respective forms which you can navigate from the user interface.

![](https://files.readme.io/f4090d7-Screenshot_2020-04-28_at_11.30.58_AM.png "Screenshot 2020-04-28 at 11.30.58 AM.png")

When setting up your model you will be defining the concepts and forms. The diagram below explains the relationship between entities above, form and concepts. Currently, in the application, you may need to go to the concept's view to edit it fully. Soon we would provide seamless editability of the underlying concept via form editing.

![](https://files.readme.io/f678cdd-Screenshot_2020-04-28_at_6.44.23_PM.png "Screenshot 2020-04-28 at 6.44.23 PM.png")

An example form below of name "Child Enrolment", with one form element group called "Child Enrolment Basic Details". This form element group has 6 form elements.

![](https://files.readme.io/eb3a4bf-Screenshot_2020-04-28_at_7.13.21_PM.png "Screenshot 2020-04-28 at 7.13.21 PM.png")

One of the form element is displayed below with all the details. The concept used by the form element is also displayed like allow data range values. From this screen, as of now, it is not editable you need to go to the concepts tab to edit it.

![](https://files.readme.io/f968766-Screenshot_2020-04-28_at_7.17.04_PM.png "Screenshot 2020-04-28 at 7.17.04 PM.png")

You can specify the skip logic for under the rule tab within the form element. This currently is done only using JavaScript, but in future, one would be able to do it using the UI directly. For more on rules please see the [Writing rules](doc:writing-rules).

![](https://files.readme.io/661ab7b-Screenshot_2020-05-19_at_4.49.43_PM.png "Screenshot 2020-05-19 at 4.49.43 PM.png")


# File: ./readme/Implementers/basic-feature-guide/subject-types.md

title: Subject types
excerpt: ''
    - type: basic
      slug: encounter-type
      title: Encounter types
---
Subject Types define the subjects that you collect information on. Eg: Individual, Tractor, Water source, Classroom session. Service Providers in an organisation could be 

* taking action "Against" or "For" beneficiaries, citizens, patients, students, children, etc.
* collecting data for non-living objects like Water-body, School, Health Centre, etc.

## Different types of Subject in Avni

Avni allows for creating multiple Subject Types, each of which can be of any one of the following kind: 

* **Group** - Used for representing an entity which constitutes a group of another subject type. Ex: A group of Interns enrolled for a specific Program for the Year 2023
* **Household** - Special kind of Group, which usually refers to a Household of beneficiaries living in a single postal address location. Ex: A household consisting of a family of Father, Mother and children. Additionally, has a feature to assign one of the members as Head of the Household.
* **Individual** - Generic type of Subject to represent a Place, Person, Thing, Action. etc.. Ex: School, Student, Pocelain Machine, Distribution of Materials, etc.
* **Person** - Special kind of Individual, to specifically indicate a Human Being. Additionally has in-built capability to save First and Last Names, Gender and Date of Birth.
* **User** - A type of Subject used to provide self-refer to the Service Providers in Avni. Read more about [User Subject Types](doc:user-subject-types)


# File: ./readme/Implementers/basic-feature-guide/sync-strategies.md

title: Sync strategies
excerpt: ''
Sync strategies define the way a subject should sync to the user's device. Sync strategies can be defined for each subject type. Each subject type can have different/same sync strategies based on the use case.\
Setting up a sync strategy is a two-step process.

* Defining sync strategy for a subject type.
* Assigning the value of the defined strategy to the user.

## Defining sync strategy for a subject type

For defining sync strategy edit the subject type and under the advance settings configure the sync settings. Below are the different sync strategies available.

| Sync strategy               | Description                                                                                                                                                     |
| :-------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Sync by location            | This is the default strategy and the subject is synced by their registered location.                                                                            |
| Sync by direct assignment   | When this is enabled only subjects assigned to the user will get synced to the user's device.                                                                   |
| Sync registration concept 1 | Any mandatory form element's concept from the registration form can be selected. Subjects get synced based on the values assigned to the user for this concept. |
| Sync registration concept 2 | Similar to `Sync registration concept 1`, this is to support once more concept for the same subject type.                                                       |

![](https://files.readme.io/ad013a1-sync-settings.png "sync-settings.png")

## Assigning the value of the defined strategy to the user

Once the sync strategy is defined for a subject type, values can be assigned to the user so that only those values get synced to the user's device. This can be done by editing an existing user or while creating a new user.

| Sync strategy               | Supported values                   |
| :-------------------------- | :--------------------------------- |
| Sync by location            | Catchment                          |
| Sync by direct assignment   | Already registered subjects        |
| Sync registration concept 1 | Concept values (Code/Text/Numeric) |
| Sync registration concept 2 | Concept values (Code/Text/Numeric) |

![](https://files.readme.io/f215814-Sync_settings.png "Sync settings.png")

**Note** 

* In case of any catchment changes/direct assignment changes user needs to delete the old data and sync as per the newly assigned values.

## Handling on Data Entry App (DEA)

Starting August 2024 ([v9.3.0](https://github.com/avniproject/avni-product/releases/tag/v9.3.0)), sync strategy is also respected for updates made via DEA. DEA users will be able to search for and view all data but will be restricted from creating new / updating existing entities that do not match their sync settings.

If the update the DEA user is making involves changing the value of the attribute controlling sync, the user will be blocked from doing so unless the sync setting allows the user access to both the original value as well as the changed value. i.e. if the DEA user is updating the address of a subject from 'Delhi' to 'Mumbai', the catchment for the DEA user needs to contain both 'Delhi' and 'Mumbai' 

### Override to ignore sync registration concepts

A user-level setting is available to ignore the user's sync registration concept settings for updates made via DEA. Location and Assignment strategies will continue to be respected. In the Avni admin app, navigate to Users -> Search for / Select the user to be modified -> Edit -> Toggle the setting 'Ignore below listed sync settings in the Data Entry app'

![](https://files.readme.io/2f475037479d5e87ded6067331bc01566e0a94bac10d7e896d6725043ea1e44f-image.png)


# File: ./readme/Implementers/basic-feature-guide/sync.md

title: Sync Scheduling
excerpt: >-
  description: ''
---
## Sync data between Avni Client and Server

Sync between Avni Client and Server is initiated by the Client and could be of following types:

### Manual Sync(User triggered, upload and fetch data)

> 📘
>
> As part of manual sync, we'll first replace the "background-sync" job with a "dummy sync" job, perform manual-sync and then, replace the "dummy sync" job again with "background-sync" job.\
> In react-native-background-worker, when we schedule a job with same jobKey(Name) as an existing job, it replaces the old one with new one. Therefore, above specified steps are supposed to fulfill our need to NOT run background-sync in parallel with manual-sync.\
> This is done, as we do not have a way to cancel jobs by name directly in react-native-background-worker. We could only cancel by id, but we do not want to store job id in db.\
> ![](https://files.readme.io/2dcc00c-ManualAndDummySync.png)

### Automatic Sync

1. Complete Sync (Both upload and fetch data)
2. Partial Sync (Only upload of data)\
   ![](https://files.readme.io/d567681-Screenshot_2023-10-30_at_12.08.26_PM.png)


# File: ./readme/Implementers/basic-feature-guide/writing-rules.md

title: Writing rules
excerpt: ''
    - type: basic
      slug: access-control
      title: Access Control
---
> 🚧 Important Update on Rules Execution
> 
> Please be informed that all existing rules stored in the rules table will become obsolete by the end of this year, 2024. This means that starting January 1, 2025, these rules will no longer be executed.
> 
> However, any rules added through the App Designer and avni-health-modules will continue to work as expected.
> 
> If you have any questions or need assistance with migrating your rules, please contact our support team.

# Contents:

[Introduction](/docs/writing-rules#introduction)  
[Rule types](/docs/writing-rules#rule-types)  
[Using service methods in the rules](/docs/writing-rules#using-service-methods-in-the-rules)  
[Using other group/household individuals' information in the rules](/docs/writing-rules#using-other-grouphousehold-individuals-information-in-the-rules)  
[Types of rules and their support/availability in Data Entry App](/docs/writing-rules#types-of-rules-and-their-supportavailability-in-data-entry-app)  
[Types of rules and their support/availability in transaction data upload](/docs/writing-rules#types-of-rules-and-their-supportavailability-in-transaction-data-upload)

## Introduction:

Rules are just normal JavaScript functions that take some input and returns something. You can use the full power of JavaScript in these functions. We also provide you with some helper libraries that make it easier to write rules. We will introduce you to these libraries in the examples below.

All rule functions get passed an object as a parameter. The parameter object has two properties: 1. imports 2. params. The imports object is used to pass down common libraries. The params object is used to pass rule-specific parameters. In params object, we pass the relevant entity on which rule is being executed e.g. if a rule is invoked when a program encounter is being performed then we pass the ProgramEncounter object. The entities that we pass are an instance of classes defined in [avni-models](https://github.com/avniproject/avni-models)

### Shape of common imports object:

```javascript
{
  rulesConfig: {}, //It exposes everything exported by rules-config library. https://github.com/avniproject/rules-config/blob/master/rules.js.
  common: {}, // Library we have for common functions https://github.com/avniproject/avni-client/blob/master/packages/openchs-health-modules/health_modules/common.js
  lodash: {}, // lodash library
  moment: {}, // momentjs library
  motherCalculations: {}, //mother program calculations https://github.com/avniproject/avni-health-modules/blob/master/src/health_modules/mother/calculations.js
  log: {} //console.log object
}
```

### Shape of common parameters in all params object

Note there are other elements in params object which are specific to the rule hence have been described below.

```javascript
{    
  user, //Current User's UserInfo object  
  myUserGroups //List of Group objects, to which the User is assigned to 
}
```

User: [https://github.com/avniproject/avni-models/blob/master/src/UserInfo.js](https://github.com/avniproject/avni-models/blob/master/src/UserInfo.js)

Group: [https://github.com/avniproject/avni-models/blob/master/src/Groups.js](https://github.com/avniproject/avni-models/blob/master/src/Groups.js)

#### Entities passed to the rule

All rule receives an entity from the `params` object. Depending on the rule type an entity can be one of [Individual](https://github.com/avniproject/avni-models/blob/master/src/Individual.ts), [ProgramEncounter](https://github.com/avniproject/avni-models/blob/master/src/ProgramEncounter.js), [ProgramEnrolment](https://github.com/avniproject/avni-models/blob/master/src/ProgramEnrolment.js), [Encounter](https://github.com/avniproject/avni-models/blob/master/src/Encounter.js), or [ChecklistItem](https://github.com/avniproject/avni-models/blob/master/src/ChecklistItem.js). The shape of the entity object and the supported methods can be viewed from the above links on each entity.

## Rule types

1. [Enrolment summary rule](/docs/writing-rules#1-enrolment-summary-rule)
2. [Form element rule](/docs/writing-rules#2-form-element-rule)
3. [Form element group rule](/docs/writing-rules#3-form-element-group-rule)
4. [Visit schedule rule](/docs/writing-rules#4-visit-schedule-rule)
5. [Decision rule](/docs/writing-rules#5-decision-rule)
6. [Validation rule](/docs/writing-rules#6-validation-rule)
7. [Enrolment eligibility check rule](/docs/writing-rules#7-enrolment-eligibility-check-rule)
8. [Encounter eligibility check rule](/docs/writing-rules#8-encounter-eligibility-check-rule)
9. [Checklists rule](/docs/writing-rules#9-checklists-rule)
10. [Work list updation rule](/docs/writing-rules#10-work-list-updation-rule)
11. [Subject summary rule](/docs/writing-rules#11-subject-summary-rule)
12. [Hyperlink menu item rule](/docs/writing-rules#12-hyperlink-menu-item-rule)
13. [Message rule](https://avni.readme.io/docs/writing-rules#13-message-rule)
14. [Dashboard Card rule](https://avni.readme.io/docs/writing-rules#14-dashboard-card-rule)
15. [Manual Programs Eligibility Check Rule](https://avni.readme.io/docs/writing-rules#15-manual-programs-eligibility-check-rule)
16. [Member Addition Eligibility Check Rule](https://avni.readme.io/docs/writing-rules#16-member-addition-eligibility-check-rule)
17. [Edit Form Rule](https://avni.readme.io/docs/writing-rules#17-edit-form-rule)
18. [Global reusable code rule](https://avni.readme.io/docs/writing-rules#18-global-reusable-code-rule-alpha)

<br />
![Invocation of different rule types](https://files.readme.io/2284f79-Screenshot_2020-07-03_at_9.33.55_AM.png)

<br />
![](https://files.readme.io/baad794-Screenshot_2020-07-03_at_9.59.42_AM.png)

<br/><hr/>

## 1. Enrolment summary rule

- Logical scope = Program Enrolment
- Trigger = Before the opening of a subject dashboard with default program selection. On program change of subject dashboard.
- In designer = Program (Enrolment Summary Rule)
- When to use = Display important information in the subject dashboard for a program

You can use this rule to highlight important information about the program on the Subject Dashboard in table format. It can pull data from all the encounters of enrolment and the enrolment itself. You can use this when the information you want to show is not entered by the user in any of the forms and is also not required for any reporting purposes (hence you wouldn't also generate this data via decision rule).

### Shape of params object:

```javascript
{ 
  summaries: [],
  programEnrolment: {}, // ProgramEnrolment model
	services,
  user, //Current User's UserInfo object  
  myUserGroups //List of Group objects  
}
```

You need to return an array of summary objects from this function.

### Shape of the summary object:

```
{
  "name": "name of the summary concept",
  "value": <text> | <number> | <date> | <datetime> | <concept list in case of Coded question>
}
```

### Example:

```
({params, imports}) =>  {
    const summaries = [];
    const programEnrolment = params.programEnrolment;
    const birthWeight = programEnrolment.findObservationInEntireEnrolment('Birth Weight');
    if (birthWeight) {
      summaries.push({name: 'Birth Weight', value: birthWeight.getValue()});
    }
    return summaries;
};
```
![](https://files.readme.io/4f29afe-Screenshot_2020-05-19_at_3.09.44_PM.png)

<br />
![](https://files.readme.io/6fdb1f3-4bf85d9-encounter-scheduling-2.png)

<br/><hr/>

## 2. Form element rule

- Logical scope = Form Element
- Trigger = Before display of form element in the form wizard and on any change done by the user in on that page
- In designer = Form Element (RULES tab)
- When to use = 
  - Hide/show a form element
  - auto calculate the value of a form element
  - reset value of a form element

### Shape of params object:

```javascript
{
  entity: {}, //it could be one of Individual, ProgramEncounter, ProgramEnrolment, Encounter and ChecklistItem depending on what type of form is this rule attached to
  formElement: {}, //form element to which this rule is attached to
  questionGroupIndex,
  services,
  entityContext,
  user, //Current User's UserInfo object  
  myUserGroups //List of Group objects  
}
```

This function should return an instance of [FormElementStatus](https://github.com/avniproject/avni-models/blob/master/src/application/FormElementStatus.js) to show/hide the element, show validation error, set its value, reset a value, or skip answers.

To reset a value, you can use FormElementStatus.\_resetIfValueIsNull() method.  
You can either use FormElementStatusBuilder or use normal JavaScript to build the return value. FormElementStatusBuilder is a helper class provided by Avni that helps writing rules in a declarative way.

### Examples using FormElementStatusBuilder.

```javascript Registration Form
'use strict';
({params, imports}) => {
  const individual = params.entity;
  const formElement = params.formElement;
  const statusBuilder = new imports.rulesConfig.FormElementStatusBuilder({individual, formElement});
  statusBuilder.show().when.valueInRegistration("Number of hywas required").is.greaterThan(0);
  return statusBuilder.build();
};
```
```javascript Program Enrolment Form 1
({params, imports}) => {
  const programEnrolment = params.entity;
  const formElement = params.formElement;
  const statusBuilder = new imports.rulesConfig.FormElementStatusBuilder({programEnrolment, formElement});
  statusBuilder.show().when.valueInEnrolment('Is child getting registered at Birth').containsAnswerConceptName("No");
  return statusBuilder.build();//this method returns FormElementStatus object with visibility true if the conditions given above matches
};
```
```javascript Program Enrolment Form 2
({params, imports}) => {
    const gravidaBreakup = [
        'Number of miscarriages',
        'Number of abortions',
        'Number of stillbirths',
        'Number of child deaths',
        'Number of living children'
    ];
    const computeGravida = (programEnrolment) => gravidaBreakup
        .map((cn) => programEnrolment.getObservationValue(cn))
        .filter(Number.isFinite)
        .reduce((a, b) => a + b, 1);
    
    const [formElement, programEnrolment] = params.programEnrolment;
    const firstPregnancy = programEnrolment.getObservationReadableValue('Is this your first pregnancy?');
    const value = firstPregnancy === 'Yes' ? 1 : firstPregnancy === 'No' ? computeGravida(programEnrolment) : undefined;
    return new FormElementStatus(formElement.uuid, true, value);
};
```
```javascript Program Encounter Form
'use strict';
({params, imports}) => {
  const programEncounter = params.entity;
  const formElement = params.formElement;
  const statusBuilder = new imports.rulesConfig.FormElementStatusBuilder({programEncounter, formElement});
  const value = programEncounter.findLatestObservationInEntireEnrolment('Have you received first dose of TT');
  statusBuilder.show().whenItem( value.getReadableValue() == 'No').is.truthy;
  return statusBuilder.build();
};
```
```javascript Encounter Form
'use strict';
({params, imports}) => {
  const encounter = params.entity;
  const formElement = params.formElement;
  const statusBuilder = new imports.rulesConfig.FormElementStatusBuilder({encounter, formElement});
  statusBuilder.show().when.valueInEncounter("Are machine start and end hour readings recorded").is.yes;
  return statusBuilder.build();
};
```
```Text AffiliatedGroups
//In-order to fetch affiliatedGroups set as part of GroupAffiliation Concept in the same form,
//one needs to access params.entityContext.affiliatedGroups variable.

// Old Rule snippet
// const phulwariName = _.get(_.find(programEnrolment.individual.affiliatedGroups, ({voided}) => !voided), ['groupSubject', 'firstName'], '');

// New Rule snippet
const phulwariName = _.get(_.find(params.entityContext.affiliatedGroups, ({voided}) => !voided), ['groupSubject', 'firstName'], '');

```
![](https://files.readme.io/ece1355-Screenshot_2020-07-02_at_6.21.43_PM.png)
<br />
![](https://files.readme.io/abb6bcf-4692c21-SkipLogic.gif)

Please note that form element rules are not transitive and cannot depend on the result of another form element's form element rule. The rule logic for a particular element will need to cater to this. 

i.e. If rule C on element C depends on value of element B and rule B depends on value of element A, updating A will only update B's value and not C's value. 

<br/><hr/>

## 3. Form element group rule

- Scope = Form Element Group
- Trigger = Before display of form element group to the user (including previous or next)
- In designer = Form Element Group (RULES tab)
- When to use = Hide/show a form element group

Sometimes we want to hide the entire form element group based on some conditions. This can be done using a form element group (FEG) rule. There is a rules tab on each FEG where this type of rule can be written. Note that this rule gets executed before form element rule so if the form element is hidden by this rule then the _form element rule_ will not get executed.

### Shape of params object:

```javascript
{
  entity: {}, //it could be one of Individual, ProgramEncounter, ProgramEnrolment, Encounter and ChecklistItem depending on what type of form is this rule attached to
  formElementGroup: {}, //form element group to which this rule is attached to
  services,
  entityContext,
  user, //Current User's UserInfo object
  myUserGroups //List of Group objects
}
```

This function should return an array of  [FormElementStatus](https://github.com/avniproject/avni-models/blob/master/src/application/FormElementStatus.js)

### Example:

```
({params, imports}) => {
    const formElementGroup = params.formElementGroup;
    return formElementGroup.formElements.map(({uuid}) => {
        return new imports.rulesConfig.FormElementStatus(uuid, false, null);
    });
};
```

<br/><hr/>

## 4. Visit schedule rule

- Logical scope = Encounter (aka Visit), Subject, or Program Enrolment
- Trigger = On completion of an form wizard before final screen is displayed
- In designer = Form (RULES tab)
- When to use = For scheduling one or more encounters in the future

### Shape of params object:

```javascript
{
  entity: {}, //it could be one of ProgramEncounter, ProgramEnrolment, Encounter depending on what type of form is this rule attached to.
  visitSchedule: []// Array of already scheduled visits.
  entityContext
  services,
  user, //Current User's UserInfo object  
  myUserGroups //List of Group objects  
}
```

You need to return an array of visit schedules from this function.

### Shape of the return value

```
[
  <visit schedule object>
  ...
]
```

### visit schedule object

```
{
	name: "visit name", 
	encounterType: "encounter type name", 
	earliestDate: <date>, 
	maxDate: <date>,
	visitCreationStrategy: "Optional. One of default|createNew",
	programEnrolment: "<Optional. Used if you want to create a visit in a different program enrolment. If the program enrolment is tied to another subject, the visit will be schedule for that subject. Do not pass this parameter if you want to schedule a general encounter.>",
	subjectUUID: "<Optional UUID string. Used if you want to create a general visit for another subject.>"
}
```

### Example

```
({ params, imports }) => {
  const programEnrolment = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({
    programEnrolment
  });
  scheduleBuilder
    .add({
      name: "First Birth Registration Visit",
      encounterType: "Birth Registration",
      earliestDate: programEnrolment.enrolmentDateTime,
      maxDate: programEnrolment.enrolmentDateTime
    })
    .whenItem(programEnrolment.getEncounters(true).length)
    .equals(0);
  return scheduleBuilder.getAll();
};
```

### Example 2 - Schedule a general visit on a household when a member completes a program enrolment

```
.
.
  scheduleBuilder.add({
      name: "TB Family Screening Form",
      encounterType: "TB Family Screening Form",
      earliestDate: imports.moment(programEnrolment.encounterDateTime).toDate(),
      maxDate: imports.moment(programEnrolment.encounterDateTime).add(15, 'days').toDate(),
      subjectUUID: programEnrolment.individual.groups[0].groupSubject.uuid
  });
.
.
```
![](https://files.readme.io/42b7d6b-Screenshot_2020-05-19_at_7.04.19_PM.png)

<br />
![](https://files.readme.io/cbaef6a-4fff50b-encounter-scheduling-1.png)

### Strategies that Avni uses.

For all the visit schedules that are returned, Avni evaluates how to create a visit. Assume you provide the default visitCreationStrategy (this is the default behaviour). Avni checks if there is already a scheduled visit for the given encounter type. If it is there, then it is updated with the incoming scheduled visit's name and other parameters. This strategy works well in most cases. 

- Remember that the VisitSchedule rule gets called whether you create a visit, or edit it. 
- Remember not to send multiple visit schedule objects for the same encounter type. If you do, the last one will overwrite the previous objects. 

### Using the "createNew" visit strategy

Do this only if you know what you are doing. If you add visitCreationStrategy of "createNew", then a new visit will be created no matter what. 

You need to be careful while using this strategy because, in edit scenarios, we might end up creating the same kind of visits multiple times. 

### Using the VisitScheduleBuilder.getAllUniqueVisits

VisitSchedulBuilder class has a getAllUniqueVisits method that provides some shortcuts to reduce the cruft you might have to do while creating scheduled visits. It mostly does the right thing, so you don't have to worry about its logic. However, if you think it is doing something you didn't intend, then you can replace it with your own implementation. Look up the [code](https://github.com/avniproject/rules-config/blob/master/src/rules/builder/VisitScheduleBuilder.js) for more details. 

<br/><hr/>

## 5. Decision rule

- Logical scope = Encounter (aka Visit), Subject, or Program Enrolment
- Trigger = On completion of an form wizard before final screen is displayed
- In designer = Form (RULES tab)
- When to use = To create any additional observations based on all the data filled by the user in the form

Used to add decisions/recommendations to the form. The decisions are displayed on the last page of the form and are also saved in the form's observations.

### Shape of params object:

```javascript
{
	entity: {}, //it could be ProgramEncounter, ProgramEnrolment or Encounter depending on what type of form is this rule attached to.
 	entityContext,
  services,
  user, //Current User's UserInfo object  
  myUserGroups, //List of Group objects  
  decisions: {
     	"enrolmentDecisions": [],
    	"encounterDecisions": [],
      "registrationDecisions": []
  } // Decisions object on which you need to add decisions. 
}
```

### Shape of decisions parameter:

```javascript
{
  "enrolmentDecisions": [],
  "encounterDecisions": [],
  "registrationDecisions": []
}
```

You need to add `<decision object>` to decisions parameter's appropriate field and return it back.  
Inside the function, you will build decisions using ComplicationsBuilder and push the decisions to the decisions parameter's appropriate field. The return value will be the modified decisions parameter. You can also choose to not use ComplicationsBuilder and directly construct the return value as per the contract shown below:

### Shape of the return value

```
{
  "enrolmentDecisions": [<decision object>, ...],
  "encounterDecisions": [<decision object>, ...],
  "registrationDecisions": [<decision object>, ...]
}
The shape of <decision object>
{
  "name": "name of the decision concept",
  "value": <text> | <number> | <date> | <datetime> | <name of anwer concepts in case of Coded question>
}
```

### Example

```
({params, imports}) => {
    const programEncounter = params.entity;
    const decisions = params.decisions;
    const complicationsBuilder = new imports.rulesConfig.complicationsBuilder({
        programEncounter: programEncounter,
        complicationsConcept: "Birth status"
    });
    complicationsBuilder
        .addComplication("Baby is over weight")
        .when.valueInEncounter("Birth Weight")
        .is.greaterThanOrEqualTo(8);
    complicationsBuilder
        .addComplication("Baby is under weight")
        .when.valueInEncounter("Birth Weight")
        .is.lessThanOrEqualTo(5);
    complicationsBuilder
        .addComplication("Baby is normal")
        .when.valueInEncounter("Birth Weight")
        .is.lessThan(8)
        .and.when.valueInEncounter("Birth Weight")
        .is.greaterThan(5);
    decisions.encounterDecisions.push(complicationsBuilder.getComplications());
    return decisions;
};
```
![](https://files.readme.io/f0f898a-Screenshot_2020-05-19_at_7.09.58_PM.png)

<br />
![](https://files.readme.io/4b488cc-4fff50b-encounter-scheduling-1.png)

<br/><hr/>

## 6. Validation rule

- Logical scope = Encounter (aka Visit), Subject, or Program Enrolment
- Trigger = On completion of an form wizard before final screen is displayed
- In designer = Form (RULES tab)
- When to use = To provide validation error(s) to the user that are not specific to one form element but involved data in multiple form elements.

Used to stop users from filling invalid data

### Shape of params object:

```
{
  entity: {}, //it could be ProgramEncounter, ProgramEnrolment or Encounter depending on what type of form is this rule attached to.
  entityContext,
  services,
  user, //Current User's UserInfo object  
  myUserGroups //List of Group objects  
}
```

The return value of this function is an array with validation errors.

### Example:

```
({params, imports}) => {
  const validationResults = [];
  if(programEncounter.getObservationReadableValue('Parity') > programEncounter.getObservationReadableValue('Gravida')) {
    validationResults.push(imports.common.createValidationError('Para Cannot be greater than Gravida'));
  }
  return validationResults;
};
```
![](https://files.readme.io/fb8e5df-Screenshot_2020-05-19_at_7.14.05_PM.png)

<br/><hr/>

## 7. Enrolment Eligibility Check Rule

- Logical scope = Subject
- Trigger = On launch of program list when user enrols a subject into program
- In designer = Program page
- When to use = To restrict the programs which are available for enrolment based on subject's data (e.g. not allowing males to enrol in pregnancy programs)

### Shape of params object:

```
{
  entity: {}//Subject will be passed here.
  program,
  services,
  user, //Current User's UserInfo object  
  myUserGroups //List of Group objects  
}
```

### Shape of the return value

The return value of this function should be a boolean.

### Example:

```
({params, imports}) => {
  const individual = params.entity;
  return individual.isFemale() && individual.getAgeInYears() > 5;
};
```

**Notes**: The eligibility check is triggered only when someone tries to create a visit manually. Form stitching rules can override this default behaviour. 
![](https://files.readme.io/bc76050-Screenshot_2020-05-20_at_3.57.52_PM.png)

<br />
![](https://files.readme.io/ba63cb1-cbe944e-Screenshot_2019-11-20_at_6.51.40_PM.png)

<br/><hr/>

## 8. Encounter Eligibility Check Rule

- Logical scope = Subject or Program Enrolment
- Trigger = On launch of new visit (encounter) list
- In designer = Encounter page
- When to use = To restrict the encounters which are available based on subject's full data (e.g. not showing postnatal care form if the delivery form has not been filed yet)

Used to hide some visit types depending on some data. If there existed scheduled encounters for that subject or program enrolment, clicking on an ineligible visit type, will fill up the scheduled encounter. 

### Shape of params object:

```javascript
{
  entity: {}//Subject will be passed here.
  services,
  user, //Current User's UserInfo object  
  myUserGroups //List of Group objects  
}
```

### Shape of the return value

The return value of this function should be a boolean.

### Example:

```
({params, imports}) => {
  const individual = params.entity;
  const visitCount = individual.enrolments[0].encounters.filter(e => e.encounterType.uuid === 'a30afe96-cdbb-42d9-bf30-6cf4b07354d1').length;
  let visibility = true;
  if (_.isEqual(visitCount, 1)) visibility = false;
  return visibility;
};
```

**Notes**: The eligibility check is triggered only when someone tries to create a visit manually. Form stitching rules can override this default behaviour. 
![](https://files.readme.io/0d034b9-Screenshot_2020-05-20_at_4.02.24_PM.png)

<br/><hr/>

## 9. Checklists rule

Used to add a checklist to an enrolment

### Shape of params object:

```javascript
{
  entity: {} //ProgramEnrolment
  checklistDetails: [] // Array of ChecklistDetail
  services,
  user, //Current User's UserInfo object  
  myUserGroups //List of Group objects  
}
```

### Example

```
({params, imports}) => {
  let vaccination = params.checklistDetails.find(cd => cd.name === 'Vaccination');
  if (vaccination === undefined) return [];
  const vaccinationList = {
    baseDate: params.entity.individual.dateOfBirth,
    detail: {uuid: vaccination.uuid},
    items: vaccination.items.map(vi => ({
      detail: {uuid: vi.uuid}
    }))
  };
  return [vaccinationList];
};
```

<br/><hr/>

## 10. Work List Updation rule

- Logical scope = Subject, Program Enrolment, or Encounters
- Trigger = On display of system recommendation's page in form wizard
- In designer = Main Menu
- When to use = Stitch together multiple forms which can be filled back to back

The System Recommendations screen of Avni can be configured to direct a user to go to the next task to be done. Typically, if a new encounter is scheduled for a person on the same day, then the system automatically prompts the user to perform that encounter.  
This is performed using worklists. A worklist is an array of [work items](https://github.com/avniproject/avni-models/blob/master/src/application/WorkItem.js). 

The WorkListUpdation rule is used to customize this flow. The WorkLists object is passed on to this rule just before showing the System Recommendations screen. Any modification in the worklists is applied immediately to the flow. 

You can add a new WorkItem anywhere after the currentWorkList.currentItem. 

### Shape of params object:

```javascript
{
  worklists: {},
  context: {},
  services,
  user, //Current User's UserInfo object  
  myUserGroups //List of Group objects  
}
```

### Example

[https://gist.github.com/hithacker/d0fe89107b974797fbb11ced1feda146](https://gist.github.com/hithacker/d0fe89107b974797fbb11ced1feda146)
![](https://files.readme.io/ef3535d-Screenshot_2020-05-21_at_3.25.33_PM.png)


<br/><hr/>

## 11. Subject summary rule

- Logical scope = Subject registration
- Trigger = Before the opening of the subject dashboard profile tab.
- In designer = Subject (Subject Summary Rule)
- When to use = Display important information in the subject's profile. It can be used to show the summary if there are no programs.

This rule is very similar to the Enrolment summary rule. Except its scope is the Subject's registration.

### Shape of params object:

```
{ 
  individual: {}, // Subject model,
  user, //Current User's UserInfo object  
  myUserGroups //List of Group objects  
}
```

You need to return an array of summary objects from this function.

### Shape of the summary object:

```
{
  "name": "name of the summary concept",
  "value": <text> | <number> | <date> | <datetime> | <concept list in case of Coded question>
}
```

### Example:

```
({params, imports}) =>  {
    const summaries = [];
    const individual = params.individual;
    const mobileNumber = individual.findObservation('Mobile Number'); 
    if(mobileNumber) {
      summaries.push({name: 'Mobile Number', value: mobileNumber.getValueWrapper()});
    }
    return summaries;
};
```

<br/><hr/>

## 12. Hyperlink menu item rule

- Logical scope = User
- Trigger = When More navigation is opened in the mobile app
- In designer = Coming very soon...
- When to use = When a dynamic link has to be provided to the user (these links cannot be specific to subjects)

### Shape of params object:

```
{
  user: {}, // User
  moment: {}, // moment. note other parameters are not supported yet,
  token, //Auth-token of the logged-in user
  myUserGroups //List of Group objects  
}
```

User: [https://github.com/avniproject/avni-models/blob/master/src/UserInfo.js](https://github.com/avniproject/avni-models/blob/master/src/UserInfo.js)

You need to return a string that is the full URL that can be opened in a browser.

### Example:

```
({params}) => {return `https://reporting.avniproject.org/public/question/11265388-5909-438e-9d9a-6faaa0c5863f?username=${encodeURIComponent(user.username)}&name=${encodeURIComponent(user.name)}&month=${imports.moment().month() + 1}&year=${imports.moment().year()}`;}
```

<br/><hr/>

## 13. Message rule

- When to use =  To configure sending Glific messages
- Logical scope = User, Subject, General and Program Encounter, Program Enrolment
- Trigger = 
  - For User : Only on creation of an User . 
  - For Subject, General and Program Encounter, Program Enrolment : On every save (create / update)
- In designer = "User Messaging Config", "Subject Type" , "Encounter type" and "Programs" page

Message Rule can be configured only when 'Messaging' is enabled for the organisation. Its configuration constitutes specifying following details:

- **Name** identifier name for the Message Rule
- **Template** Used to indicate the Skeleton of the message with placeholders for parameters
- **Receiver Type** Used to indicate the target audience for the Glific Whatsap message
- **Schedule** date and time configuration should return the time to send the message.
- **Message** content configuration should return the parameters to be filled in the Glific message template selected under 'Select Template' dropdown.

 Any number of message Rules can be configured.

### Example configuration:

Say, 'common_otp' Glific message template is 'Your OTP for `{{1}}` is `{{2}}`. This is valid for `{{3}}`.' If we want to send a OTP message that says 'Your OTP for receiving books is 1458. This is valid for 2 hours.' to a student after 1 day of their registration, then we need to configure for student subject type as shown in the below image (Note the shape of the return objects): 
![](https://files.readme.io/2e3e442-Screenshot_2023-12-27_at_6.15.54_PM.png)

```Text Schedule
'use strict';  
({params, imports}) => ({  
  scheduledDateTime: new Date("2023-01-05T10:10:00.000+05:30")  
});
```
```text Message
'use strict';  
({params, imports}) => {  
  const individual = params.entity;  
  return {  
    parameters: ['Verify user phone number', '0123', '1 day']  
  }  
};
```

### Shape of params object:

```
{
  entity: {}, //it could be one of User, Individual, General Encounter, ProgramEncounter or Program Enrolment depending on the type of form this rule is attached to
  user, //Current User's UserInfo object  
  myUserGroups //List of Group objects  
}
```

## 14. Dashboard Card Rule

The shape of dashboard card rule

```javascript
{
  db: "the realm db instance",
  user,
  myUserGroups,
  // ruleInput object can be null
  ruleInput: {
    type: "string. see 14.1 below",
    dataType: "values can be Default or Range",
    subjectType: "SubjectType model object. The subject type of the subjects to query and display to the user",
    groupSubjectTypeFilter: {
      subjectType: "SubjectType. The group subject type to filter by"
    },
    observationBasedFilter: {
      scope: "string. See 14.2 below",
      concept: "Concept. the observation value being referred to by the filter value",
      programs: {
         "UUID of the program": "Program model object"
      },
      encounterTypes: {
         "UUID of the encounter type": "Encounter Type model object"
      }
    },
    // filterValue can be null or empty array when there are no filters chosen by the user
    filterValue: "value chosen by the user. the type of data depends on the type of the filter"
  }
}
```

### Filter Value Shapes

**Address Filter**

```json
{
  "uuid":"924674dc-d32b-4276-b7b5-fb782f5511f2",
  "name":"Kerala",
  "level":4,
  "type":"State",
  "parentUuid":null,
}
```

<br />

14.1) [https://github.com/avniproject/avni-models/blob/8613b53edbf88e9b19150eda9e13da573e2a59ba/src/CustomFilter.js#L2](https://github.com/avniproject/avni-models/blob/8613b53edbf88e9b19150eda9e13da573e2a59ba/src/CustomFilter.js#L2)

14.2) [https://github.com/avniproject/avni-models/blob/8613b53edbf88e9b19150eda9e13da573e2a59ba/src/CustomFilter.js#L30](https://github.com/avniproject/avni-models/blob/8613b53edbf88e9b19150eda9e13da573e2a59ba/src/CustomFilter.js#L30)

<br/><hr/>

### 15. Manual Programs Eligibility Check Rule

This rule is used when the user fills a form based on which the eligibility of given program is determined by this rule.

#### Shape of Input Object

```javascript
params: {
  entity: typeof SubjectProgramEligibility,
  subject: typeof Individual,
  program: typeof Program,
  services,
  user, //Current User's UserInfo object  
  myUserGroups //List of Group objects  
},
imports: {}
```

#### Return

_boolean_

### 16. Member Addition Eligibility Check Rule

This rule is used to determine whether an **existing** member can be added to a group or household. The rule is configured at the subject type level and is executed when a user attempts to add an existing member to a group/household.

- Logical scope = Group/Household and Individual
- Trigger = On attempt to add a member to a group/household
- In designer = Subject Type (Member Addition Eligibility Check Rule)
- When to use = To validate if an **existing** individual can be added as a member to a specific group/household based on custom business rules

#### Shape of Input Object

```javascript
params: {
  member: typeof Individual, // The individual being added as a member
  group: typeof Individual, // The group/household to which the member is being added
  context: Object, // The execution context
  services,
  user, // Current User's UserInfo object  
  myUserGroups // List of Group objects  
},
imports: {}
```

#### Return

This rule should return an object that follows the ActionEligibilityResponse format, with the following structure:

```javascript
// For allowing addition
{
  eligible: {
    value: true
  }
}

// For disallowing addition with a reason
{
  eligible: {
    value: false,
    message: "Reason why the member cannot be added" //Value of message has translation support.
  }
}
```

#### Example

**Use Case:**

While adding members to a "Self-help" group, we need to validate that the person is an adult, in-which case we would come up with the following

**Member Addition Eligibility Check Rule:**

```javascript
"use strict";
({params, imports}) => {
  const member = params.member;
  const group = params.group;
  
  // Example: Only allow adding members who are above 18 years of age
  const age = member.getAgeInYears();//As on current date
  
  if (age < 18) {
    return {
      eligible: {
        value: false,
        message: "Only individuals above 18 years can be added to this group"
      }
    };
  }
  
  return {
    eligible: {
      value: true
    }
  };
};
```

**Reference Screenshot, when Member Addition Eligibility Check Rule fails:**
![](https://files.readme.io/aaa48f09aa4c5bcaebf2d9ae72f19c0777e719bd463b213b43e011796fd8db0a-Screenshot_2025-06-27_at_7.41.28_PM.png)

#### Error Handling

When a Member Addition Eligibility Check rule fails (throws an exception), the error is logged and stored in the RuleFailureTelemetry with the following information:

- source_type: 'MemberAdditionEligibilityCheck'
- source_id: UUID of the subject type
- entity_type: 'Individual'
- entity_id: UUID of the group/household to which a member is being added
- individual_uuid: UUID of the individual being added to the group/household

### 17. Edit Form Rule

This rule is used when the user tries to edit a form. If non-boolean value is returned in the value, or the rule fails, then it would be treated as true and edit will be allowed. To check the places where it is available, not available, & not applicable - [https://avni.readme.io/docs/rules-concept-guide#edit-form-rule](https://avni.readme.io/docs/rules-concept-guide#edit-form-rule).Value of message has translation support.

#### Sample Rule

```
"use strict";
({params, imports}) => {
    const {entity, form, services, entityContext, myUserGroups, userInfo} = params;

    const output = {
      eligible : {
        value: false, //return false to disallow, true to allow;
        message: 'Edit access denied: <Specify reason here>.' //optional
      } 
    }; 

    return output;
};
```

#### Shape of Input Object

```javascript
params: {entity, services, form, myUserGroups,user},
imports: {}
```

#### Shape of return object

```javascript
// Previous format (still supported)
const output = {
  editable : {
    value: true/false,
    messageKey: 'foo'
  }
};

// New format (generic for all rule based access control)
const output = {
  eligible : {
    value: true/false,
    message: 'foo'
  }
};
```

### 18. Global reusable code rule (Alpha)

This rule is intended maintaining reusable JavaScript functions across implementations. While this could also be used within implementation only but that is not the purpose of this. If you want to create reusable JavaScript code within an implementation only, please check with the product management team to get it prioritised.

> 📘 Not supported in Data entry app. Feature available from 11.0 version.

#### Shape of Input Object

```javascript
// Get handle to the reusable function
const globalFunction = imports.globalFn;
// invoke your function, two examples below.
globalFn().hello();
globalFn().sum(1,2);
```

Note that you can define the signature of your new function (like hello, sum). It is not determined by the global function.

#### How to deploy global function (TBD)

1. Use `make deploy-global-rule`.
   1. Provide the origin and token
   2. The token will determine the organisation to which it is deployed. Rerunning it will update the previous rule.
2. Run sync in the mobile app

## Accessing Address Level Properties :

Old Way is to get the address level properties and extract from the json object. In new way, get the address level and access its observation value as per location attribute form.

```Text JavaScript
'use strict';
({params, imports}) => {
  const programEncounter = params.entity;
  const moment = imports.moment;
  const formElement = params.formElement;
  const _ = imports.lodash;
  let visibility = false;
  let value = 'No';
  let answersToSkip = [];
  let validationErrors = [];
  
  const address_level = programEncounter.programEnrolment.individual.lowestAddressLevel;  
  
  const gHighRisk = address_level.getObservationReadableValue("Geographically hard to reach village");

  if(gHighRisk === "Yes"){
      value = 'Yes';
  }

  
  return new imports.rulesConfig.FormElementStatus(formElement.uuid, visibility, value, answersToSkip, validationErrors);
};
```

<br />

## Handling rule-evaluation across Mobile and Web Applications

This section provides guidelines for handling rule-evaluation across Mobile and Web Applications in Avni implementations. It includes practical examples from the Goonj implementation.

### Detecting Web Application Context

To determine if the application is running in a web context, you can check the `titleLineage` property of the lowest address level:

```javascript
const webapp = individual.lowestAddressLevel.titleLineage;
```

This pattern is used to identify if the application is running in a web context and adjust behavior accordingly.

### Handling Webapp-Specific Scenarios

When working with web applications, consider the following:

- Some validations might need to be bypassed in web context
- UI/UX might need adjustments for web vs mobile
- Performance considerations might differ between platforms

#### Basic Pattern

```javascript
function handleWebappContext(individual) {
    const webapp = individual.lowestAddressLevel.titleLineage;
    
    // Apply webapp-specific logic
    if (webapp) {
        // Webapp-specific code here
    } else {
        // Mobile-specific code here
    }
}

try {
    handleWebappContext(individual);
} catch (error) {
    console.error('Error handling webapp context:', error);
}
```

#### Examples

In the Goonj implementation, we encountered an issue where certain validations were failing in the web context but were not applicable to web users.

##### 1. Webapp Detection and Validation Bypass

```javascript
function validateForm(individual, formData) {
    const webapp = individual.lowestAddressLevel.titleLineage;
    const errors = [];
    
    // Skip webapp-specific validations for web users
    if (!webapp) {
        // Mobile-only validations go here
        if (!formData.requiredField) {
            errors.push('This field is required for mobile users');
        }
    }
    
    // Common validations for both web and mobile
    if (!formData.commonField) {
        errors.push('This field is required for all users');
    }
    
    return errors.length ? errors : null;
}
```

##### 2. Location Validation Example

```javascript
function validateLocation(individual, locationData) {
    const webapp = individual.lowestAddressLevel.titleLineage;
    
    // Skip location validation for webapp
    if (webapp) {
        return null;
    }
    
    // Mobile location validation logic
    if (!locationData || !locationData.coordinates) {
        return ['Location is required for mobile users'];
    }
    
    return null;
}
```

<br />

## Accessing audit fields when writing rules

#### When writing rules, you often need to access information about who created or modified entities, and when these actions occurred. Avni provides several audit fields that can be accessed through the entity object in your rules.

Available Audit Fields

  The following audit fields are available :

- createdByUUID
- lastModifiedByUUID
- createdBy
- lastModifiedBy
- filledBy (only for program and general encounters)
- filledByUUID (only for program and general encounters)

```coffeescript JS
//SAMPLE EDIT FORM RULE
  "use strict";
({params, imports}) => {
const {entity} = params;
console.log("params.entity.createdByUUID:", params.entity.createdByUUID);
console.log("params.entity.lastModifiedByUUID:", params.entity.lastModifiedByUUID);

console.log("params.entity.createdBy:", params.entity.createdBy);
console.log("params.entity.lastModifiedBy:", params.entity.lastModifiedBy);

console.log("params.entity.filledBy:", params.entity.filledBy);
console.log("params.entity.filledByUUID:", params.entity.filledByUUID);

return output;
};
```

<br />

## Using params.db object when writing rules

In many of the rules params db object is available to query the offline database directly. The db object is an instance of type [Realm](https://www.mongodb.com/docs/realm-sdks/js/latest/classes/Realm-1.html) on which [objects](https://www.mongodb.com/docs/realm-sdks/js/latest/classes/Realm-1.html#objects) is first method that will get called. This returns [Realm Results](https://www.mongodb.com/docs/realm-sdks/js/latest/classes/Results.html) instance, on which one may further call the [filtered](https://www.mongodb.com/docs/realm-sdks/js/latest/classes/Results.html#filtered) method one or more times each time returning realm results. Realm result a list with each item being of type (model object's schema name) originally passed in objects method.

```coffeescript JS
'use strict';
({params, imports}) => {
  //...
  
  const db = params.db;
  const farmers = db.objects("Individual").filtered(`voided = false AND subjectType.uuid = "73271784-512d-4435-8dc8-0f102b99d682"`);
  console.log('Found farmers with count', farmers && farmers.length > 0 && farmers.length);

  //...
  return new imports.rulesConfig.FormElementStatus(formElement.uuid, visibility, value, answersToSkip, validationErrors);
};
```

<br />

**Realm Query Language Reference** - [https://www.mongodb.com/docs/realm/realm-query-language](https://www.mongodb.com/docs/realm/realm-query-language)

### Difference between filter and filtered

`filtered` method is like running SQL query executed closer or in the database process and hence it orders of magnitude faster than `filter` - which is JavaScript method ran by constructing model object for each item is JS memory and then passing it through the filter function. As much as possible filtered should be used for best performance and user experience.

### Example of filtered

```javascript
({params}) => {
  const db = {params};
  return db.objects("Individual").filtered(`voided = true AND subjectType.name = "Foo"`);
}
```

## Using service methods in the rules

Often, there is the need to get the context of implementation beyond what the models themselves provide. For example, knowing other subjects in the location might be necessary to run a specific rule. For such scenarios, Avni provides querying the DB using the services passed to the rules.

The services object looks like this

```javascript
{
    individualService: '',
}
```

Right now only individual service is injected into all the rules. One method which is implemented right now returns an array of subjects in a particular location. The method looks like the following, it takes address-level object and subject type name as its parameters and returns a list of all the subjects in that location.

```javascript
getSubjectsInLocation(addressLevel, subjectTypeName) {
  const allSubjects = ....;
  return allSubjects;
}
```

Note that this function is not implemented for the data entry app and throws a "method not supported" error for all the rules when run from the data entry app.

### Service methods available are:

- [https://github.com/avniproject/avni-client/blob/master/packages/openchs-android/src/service/facade/IndividualServiceFacade.js](https://github.com/avniproject/avni-client/blob/master/packages/openchs-android/src/service/facade/IndividualServiceFacade.js)
- [https://github.com/avniproject/avni-client/blob/master/packages/openchs-android/src/service/facade/AddressLevelServiceFacade.js](https://github.com/avniproject/avni-client/blob/master/packages/openchs-android/src/service/facade/AddressLevelServiceFacade.js)

### Examples

The view-filter rule is for the subject data type concept that displays all the subjects of type 'Person' in the passed location. 

```
'use strict';
({params, imports}) => {
  const encounter = params.entity;
  const formElement = params.formElement;
  const statusBuilder = new imports.rulesConfig.FormElementStatusBuilder({encounter, formElement});
  const individualService = params.services.individualService;
  const subjects = individualService.getSubjectsInLocation(encounter.individual.lowestAddressLevel, 'Person');
  const uuids = _.map(subjects, ({uuid}) => uuid);
  statusBuilder.showAnswers(...uuids);
  return statusBuilder.build();
};
```

<br />

#### Fetch Subjects by Subject Type with Custom Filtering

For business reasons, you may need to fetch subjects of a specific type with additional filtering criteria.

##### Using IndividualServiceFacade "getSubjects" method

Use IndividualServiceFacade`getSubjects(subjectTypeName, realmFilter)` method to get subjects by type with optional filtering.

##### Method Signature

- subjectTypeName (string): The name of the subject type (e.g., 'Volunteer', 'Patient', 'Household')
- realmFilter (string, optional): Realm query filter string for additional filtering

```js

  const individualService = params.services.individualService;
  const volunteers = individualService.getSubjects('Volunteer');
  console.log('volunteers:', volunteers.length);

  const subjectsWithObservation = individualService.getSubjects(
    'Patient',
    'SUBQUERY(observations, $obs, $obs.concept.uuid == "concept-uuid-here").@count > 0'
  );
  console.log('Patients with specific observation:', subjectsWithObservation.length);

  
```

## Using other group/household individuals' information in the rules

Say, an individual belongs to a group A. Sometimes, there is a need to use data of other individuals in the group A.  For example, to auto-populate caste information in an individual's registration form (say, when navigated to individual's registration form when tried to add a member to group/household A), we might need to know the caste information of other individuals in that group/household. For such scenarios, Avni provides a way to access `group` object from `params.entityContext`.

### Example

The below rule is for the case when an individual's concept named `Caste` needs to be auto-populated based on other member's data in the same group.

```
'use strict';
({params, imports}) => {
  const individual = params.entity;
  const moment = imports.moment;
  const formElement = params.formElement;
  const _ = imports.lodash;
  let visibility = true;
  let value = null;
  let answersToSkip = [];
  let validationErrors = [];
  
  const groupSubject = params.entityContext.group;
  if(groupSubject.groupSubjects.length > 0) {
     const ind = params.entityContext.group.groupSubjects[0].memberSubject;
     const caste = ind.getObservationReadableValue('Caste');
     value = caste; 
  }
  
  return new imports.rulesConfig.FormElementStatus(formElement.uuid, visibility, value, answersToSkip, validationErrors);
};
```

## Handling special scenarios while updating value using FormElementStatus rule

### How to reset value using FormElement Rule logic

When the FormElementStatus value is set to null, by default it is treated as a No-action operation and hence we do not reset the value of the concept.

But instead, if we are trying to say that "I am not setting the value", and any previous value has to be reset, then we need to specify the resetValueIfNull argument to be **true** in the FormElementStatus constructor, used to generate response during the rule execution.

```
'use strict';
({params, imports}) => {

//Rule content
  
//FormElementStatus Constructor signature
return new imports.rulesConfig.FormElementStatus(formElementUUID, visibility, value, answersToSkip = [], validationErrors = [], answersToShow = [], resetValueIfNull = false);
}
```

<br />

### Handle set of Modifiable Select Coded Concepts

In-order to init a modifiable Select Coded Concept FormElement's Value in a form, you can specify the AnswerConcept **Name** as the value, which should be enough to set the initial value as expected.

### Handle set of Read-Only Select Coded Concepts

There were 2 issues that were preventing implementation team from reliably setting a **Read-only** SingleSelectCodeConcept's value via FormElement Rules:

1. Selection of a AnswerConcept
2. Stablizing the selected value over multiple execution of FormElement rule due to changes elsewhere in the FormElementGroup

#### Recommended solution

To resolve these issues, we only needed to make following adjustments in the FormElement Rule:

1. Selection of a AnswerConcept => Make use of AnswerConcept's UUID instead of name as value
2. Stablizing the selected value  => 
   > - Mark the SelectedCodedConcept value as ReadOnly 
   > - For Multi-select: Return a FormElementStatus object with only the difference between previous valueArray and new valueArray. If no change in value, then return empty array.
   > - For Single-select: Return a FormElementStatus object with selected value, only if previousValue was null. If not, return null.

This would toggle the answers as expected and result in only the expected value(s) being shown as selected. 

#### Example Rule for SingleSelect FormElement set via Rule

```javascript
'use strict';
({params, imports}) => {
  const individual = params.entity;
  const moment = imports.moment;
  const formElement = params.formElement;
  const _ = imports.lodash;
  let visibility = true;
  let value = null;
  let answersToSkip = [];
  let validationErrors = [];
    
    const condition11 = triue; //some visibility condition
    visibility = condition11;
     
    if (condition11) {
       //some business logic
          if(someCondition) {
             value = "conceptUUID1";
          }
          else{
             value = "conceptUUID2";
          }
       }
    }
    let que = individual.findGroupedObservation('bafb80ac-6088-4649-8ed3-0501e1296c6e')[params.questionGroupIndex];
    if(que){
      let obs = que.findObservationByConceptUUID('ef952d55-f879-4c34-99e2-722c680ed2e2');
      if(obs && obs.getValue() === value) {//i.e obs.getValue() are both same answerConcept
         return null;//Old value is retained
       }   
    }
    else {
       return new imports.rulesConfig.FormElementStatus(formElement.uuid, visibility, value, answersToSkip, validationErrors); //new value is updated
    }
};
```

### Handle Uniqueness validation for Read-Only Text field

As the value for the ReadOnly TextFormElement is set via Rule of some sort, the validation for enforcing uniqueness too has to be done during the same rule execution.

#### Example FE rule for enforcing Uniqueness validation on Read-only Text field

```Text Javascript
'use strict';
({params, imports}) => {
    const individual = params.entity;
    const moment = imports.moment;
    const _ = imports.lodash;
    const formElement = params.formElement;
    let visibility = true;
    let value = null;
    let validationErrors = [];
    let nameNotUnique = false;
    
    
   //Business logic to set value
   value = '[dummy3]as';


    //Execute some business logic to update nameNotUnique 
    nameNotUnique = (value === '[dummy3]as');
    
    if(nameNotUnique) {
       validationErrors.push('Another Work Order has same value');
    }
   
    return new imports.rulesConfig.FormElementStatus(formElement.uuid, visibility, value, null, validationErrors);
};

```

<br />

### Handle Fetch of Individuals with specific Phone Numbers for duplicates validation

For business reasons, we might need to verify that there are **No / Limited number of** duplicate Subjects with the same Phone Number. To do this, we have 2 possible approaches:

#### 1. Use IndividualServiceFacade "findAllSubjectsWithMobileNumberForType" helper method

Use IndividualServiceFacade.findAllSubjectsWithMobileNumberForType(mobileNumber, subjectTypeUUID) method to get subjects with same phone number.

**Requires the PhoneNumber concept to have, KeyValue (primary_contact : yes) or (contact_number : yes)**
![](https://files.readme.io/f48da098be8218e797e7dd841e023036199eb0b7aa696ece422a6974e0b3f56f-421821795-e7b7766d-3865-4a66-a66e-93f4ddc8b13d.png)

```js

  const individualService = params.services.individualService;
  const subjects = individualService.findAllSubjectsWithMobileNumberForType('<phone_number>', "<subject_type_uuid>");
  console.log('found subjects with number', subjects && subjects.length > 0);
  
```

#### 2. [Using params.db object to find duplicates with custom filter logic](/docs/writing-rules#using-paramsdb-object-when-writing-rules)

## Types of rules and their support/availability in Data Entry App

| Not supported                          | Supported via rules-server       | Supported in browser     |
| :------------------------------------- | :------------------------------- | :----------------------- |
| Global reusable function               | Enrolment eligibility check rule | Form Element Rule        |
| Dashboard Card rule (NA)               | Encounter eligibility check rule | Form Element GroupRule   |
| Checklists rule                        | Visit schedule rule              | Enrolment Summary Rule   |
| Work list updation rule                | Message rule                     | Hyperlink menu item rule |
| Hyperlink menu item rule               | Decision rule                    |                          |
| Validation rule                        |                                  |                          |
| Edit Form rule                         |                                  |                          |
| Member addition eligibility check rule |                                  |                          |

## Types of rules and their support/availability in transaction data upload

| Not supported | Supported via rules-server | Not Applicable                   |
| :------------ | :------------------------- | :------------------------------- |
| Message rule  | Visit schedule rule        | Hyperlink menu item rule         |
|               | Decision rule              | Enrolment Summary Rule           |
|               | Validation rule            | Form Element GroupRule           |
|               |                            | Form Element Rule                |
|               |                            | Encounter eligibility check rule |
|               |                            | Enrolment eligibility check rule |
|               |                            | Hyperlink menu item rule         |
|               |                            | Work list updation rule          |
|               |                            | Checklists rule                  |
|               |                            | Dashboard Card rule              |

# File: ./readme/Implementers/how-do-i/accessing-media-in-reports.md

title: Access media in reports
excerpt: ''
Data in Avni is stored in two different data sources. The first is the postgres database, which are easily connected to the reporting servers that are being used by hosting. The second is an S3 database where media is stored. 

In reporting tools, there is a mechanism to show data by connecting to a data source. However, S3 access is usually not provided. In case you need to expose media through reports, here is what you need to do. 

1. Provide users access to Avni. 
2. In reports, observations are usually of the form "[https://prod-user-media.s3.ap-south-1.amazonaws.com/org\_name/file\_name.png"](https://prod-user-media.s3.ap-south-1.amazonaws.com/org_name/file_name.png"). This will be stored in observations of the form. To provide a link that shows this, change it to the form " [https://app.avniproject.org/web/media?url=https://prod-user-media.s3.ap-south-1.amazonaws.com/org\_name/file\_name.png"](https://app.avniproject.org/web/media?url=https://prod-user-media.s3.ap-south-1.amazonaws.com/org_name/file_name.png"). 

Doing this will send the user to app.avniproject.org, which will redirect the user to the corresponding media once they have authenticated themselves on avniproject.


# File: ./readme/Implementers/how-do-i/choose-colours-for-offline-report-cards.md

title: Colours for Offline Report Cards
excerpt: >-
  description: ''
---
<Image align="center" src="https://files.readme.io/71e201dc45bef425cb65222621d02e8a698eeef4c2a95033664bd1a5c5d70808-Screenshot_2025-07-28_at_4.58.22_PM.png" />


# File: ./readme/Implementers/how-do-i/choosing-android-device-for-avni.md

title: Choosing android device for Avni
excerpt: ''
We are listing down some criteria which could help you in deciding which device to choose. The price range kept in this analysis is between 7000 to 10000 Indian Rupees.

**OS Version**: While Avni will work on version >= 5.0, but if you are purchasing a new device then it is better to go for a more recent version. Realistically though setting the bar too high will reduce your options. Hence we recommend version >= 11.

**RAM**: Primary memory >= 4 GB is minimum requirement for quick response during app launch or screen transitions. Recommend devices with memory >= 6GB.

**CPU Speed**: Minimum requirement is a 64-bit ARM processor, with atleast 4 cores clocked at 2.0 GHz. Recommend Octa-core devices clocked at >= 2.0 GHz.

**Storage**: >= 64 GB is required for ensuring Phone OS version and all installed app versions are up to date, while retaining enough space to store media content for extended period of time.

**SD Card**: Avni in future may allow for keeping an additional backup of the data on the SD card. This is to protect against corruption of main data on internal storage which is not completely synced up with the server. Required only if your device has less than 64GB of Storage on itself.

**Screen Size**: For users who will use the application quite often, we recommend 6 inches as ideal, also considering the ability to carry it. You can, of course, go for higher or lower based on your preference.

**Camera**: A minimum of a 8MP camera will be required for good resolution images of the field work. Higher is also fine, but keep in mind that, the higher resolution requires more network bandwidth to upload. The storage of device will also need to support.

**Network Support**: Avni just needs a network connection. It could even work on 2G connectivity, but again, given that you are buying a new device go for devices which can work with 4G networks. Devices with 5G support are also fine, if they are tuned to work with 4G networks in low network availability scenarios. 

**Battery Life**: Once you have multiple devices that you can compare, look for their mAh rating. Higher is better.


# File: ./readme/Implementers/how-do-i/complex-visit-schedule-testing.md

title: Complex Visit Schedule Testing
excerpt: ''
If we break down the visit schedule complexity into three levels simple to complex, we would notice that the testing mechanism for level 2 & 3 visit schedules are quite wasteful due to long feedback loops. The feedback loop is long mainly because the testing of visit schedule logic requires filling forms to setup data and to see the result. In development mode performing sync the second main reason the feedback loop is long.

It is important to remember that for most (may be not all) bugs the testing of all the scenarios need to be carried our all over again. After certain number iterations of such testing the testing fatigue is likely to kick-in, compromising quality as well.

This feedback loop can be shortened significantly by following age old unit testing written in the form of business specifications. This approach improve quality and reduce waste.

Business specification style will allow for customer, business analyst, developer and testers all to come on the same page about the requirements. Automation of unit tests allows for verification of production code against the specification - repeatedly.

## Business specification style tests

These are tests that are written such that they read close normal english using the language of problem domain, but they can be executed as well. It helps in understanding the basic structure of such tests which is capture in a three step process - **given, when, then**. It would be useful to quickly read about it, if you don't know about this already. One such article is [here](https://www.agilealliance.org/glossary/given-when-then/), but there are many.

### Example

This is one test for scheduling visits on edit of an ANC Visit - [https://github.com/avniproject/apf-odisha-2/blob/main/test/ANCTest.js#L117](https://github.com/avniproject/apf-odisha-2/blob/main/test/ANCTest.js#L117).

**Given** that the for beneficiary ANC-1 visit is completed and ANC-2 visit is scheduled for the next month

**When** ANC-1 is edited

**Then** PW Home or ANC visit should not be scheduled

## QA strategy

Visit schedules for which such unit tests have been written should be tested differently.

* Review the test scenarios already automated via these tests.  If any scenario is missing, request the developer to add those scenarios to the test suite.
* Pick a handful, not too many, of these to verify whether the mobile application is indeed working in the same way as well.
* **Most importantly - do not manually run all the scenarios.**

## For developers

* Jest - [https://jestjs.io/docs/api](https://jestjs.io/docs/api)
* It is important to learn about test lifecycle and setup, teardown, describe, test/it methods. [https://jestjs.io/docs/setup-teardown](https://jestjs.io/docs/setup-teardown)
* It is important the each test (test/it) runs independent of other tests, so that execution of one test doesn't have any impact on another test. To achieve this all variables should be instantiated in each test, i.e. in move all the code common instantiation code (not functions) to beforeEach. Do not instantiate anything outside beforeEach and it/test. Unit tests run super-fast so optimisation is not useful and is in fact counter-productive.


# File: ./readme/Implementers/how-do-i/get-bulk-data-out-of-avni.md

title: Get bulk data out of Avni
excerpt: ''
## Transaction data

*i.e. Subjects, Encounters, Enrolments etc.*

There are a few options available suited for different purpose.

### 1. Longitudinal Export

Use this if the purpose is to get all the data associated to a subject in a single row. Also see - [New Longitudinal export](doc:new-longitudinal-export). Note currently there is a limit of 10,000 rows in this export. One can use date ranges to get data in parts.

### 2. Download Metabase tables

Metabase automatically recognises all the tables in the data source that it is pointed to. Hence, on browsing to the implementation specific schema one can see all the ETL tables. Metabase allows the ability to download the data for each table. A few points to consider/know:

a. Although in the display Metabase has limit of 10,000 rows. There is no such limit on downloads.

b. These downloads are per-table with foreign keys to parent tables (e.g. encounter form tables will have foreign keys for program enrolment, subject ETL tables). The consumer of this data will have to join these themselves in their analytics solution.

c. Download operations currently are not metered. This may change in future, if we see performance impact on the reporting database. It is recommended that these downloads are done after hours, lets say after 6 pm - so that it doesn't impact other reporting operations.

### 3. Download custom query data (SuperSet and Metabase)

This can be used to provide custom downloads based on queries. This can get around any limitations of approach 2 above in terms of the shape of downloadable data. e.g. One can join Subject, Enrolment in encounter and provide a report that one can use to download subject, enrolment, identification data along with encounter data.

The point 2(c) applies to this as well.


# File: ./readme/Implementers/how-do-i/how-to-guide-installing-avni-field-app-and-basic-set-up-on-your-mobile-phone.md

title: 'How To Guide: Installing Avni Field App and Basic Set-Up on your Mobile Phone'
excerpt: >-
  robots: index
next:
  description: ''
---
**Step 1: Install the Avni app from Google Play Store**

1. Go to the Google Play Store on your mobile device
2. Type **Avni** on the search bar
3. Click on **Install** to download the app

<br />

<Image align="left" className="border" width="250px" border={true} src="https://files.readme.io/b2ec7c3-Playstore.JPEG" />

<Image align="left" className="border" width="250px" border={true} src="https://files.readme.io/e07f14d-Avni.JPEG" />

<br />

<Image align="center" className="border" width="250px" border={true} src="https://files.readme.io/daf3937-Install.JPEG" />

**Step 2: LOGIN**

1. LOGIN to the app by entering your User ID and Password
2. Click on the LOGIN button

Note: The User ID and Password is sent to the registered mobile number via SMS once the user is created in Avni Web Console

<br />

<Image align="center" className="border" width="300px" border={true} src="https://files.readme.io/99d67fd-LOGIN.JPEG" />

<br />

**Step 3: Basic Set - Ups**

a) **Sync**

It is important to sync the app whenever an internet connection is available for the new data to get stored and reflect in the app Dashboard. This can be done by clicking on the Sync button at the top right

<br />

<Image align="center" className="border" width="300px" border={true} src="https://files.readme.io/4f2e86b-Sync2.JPEG" />

<br />

b) **Language:**

By clicking on the Edit Settings button at the top, you can select the language in which you want to see the app content. The default language selected is English

<br />

<Image align="left" width="250px" src="https://files.readme.io/75ffcfa-Edit_Lang.JPEG" />

<Image align="center" width="250px" src="https://files.readme.io/f9de6e9-1712641958848.JPEG" />

**c) Change Password**: 

If you wish to change your password, you can do so, by clicking on the Change Password button and entering the new password details.

<br />

<Image align="left" className="border" width="250px" border={true} src="https://files.readme.io/5b1f088-Change_Pass.JPEG" />

<Image align="center" className="border" width="250px" border={true} src="https://files.readme.io/69adaa1-Password.JPEG" />

# File: ./readme/Implementers/how-do-i/migrate-location-of-subject.md

title: Migrate location of subject
excerpt: ''
# Please refer to API Doc

[https://editor.swagger.io/?url=https://raw.githubusercontent.com/avniproject/avni-server/master/avni-server-api/src/main/resources/api/external-api.yaml](https://editor.swagger.io/?url=https://raw.githubusercontent.com/avniproject/avni-server/master/avni-server-api/src/main/resources/api/external-api.yaml)

# Documentation Deprecated

Since there are multiple entities that need to be changed, the migration should not be done by making changes directly to the database using SQL commands. In order to migrate a subject use the follow API.

### Endpoint

`{{origin}}/subjectMigration/bulk`

e.g. [https://app.avniproject.org/subjectMigration/bulk](https://app.avniproject.org/subjectMigration/bulk)

### Headers

`auth-token`

### Body

* destinationAddresses is a map of source address level id and destination address level id.
* subject type ids is an array of subject types that you want migrated

```Text JSON
{
    "destinationAddresses": {
        "330785": "330856",
        "334657": "335043",
        "331106": "331466"
    },
    "subjectTypeIds": [
        672,
        671
    ]
}
```

### Also know

* if you have a lot of addresses then the request may timeout, but the server will continue to process
* Each source to destination mapping for each subject type, will be done in its own transaction. So for above example there will be 6 transactions (3 address mapping multiplied by 2 subject types).


# File: ./readme/Implementers/how-do-i/move-org-to-custom-dashboard-from-mydashboard.md

title: Move Org to Custom Dashboard from MyDashboard
excerpt: ''
1. As super admin, call `POST /api/defaultDashboard/create?orgId=[organisationId]` (`organisationId` being the id of the organisation for which you want to create the default dashboard - typically your UAT org)
2. This API will only create the default dashboard for non Prod orgs.
3. Assign the newly created dashboard to the required user groups.
4. Test and verify functionality in UAT org
5. Upload bundle from UAT org to live org.


# File: ./readme/Implementers/how-do-i/review-implementation-bundle.md

title: Review Implementation Bundle
excerpt: ''
Avni offers the ability to export the configuration and metadata from an implementation into a bundle ([App Designer -> Bundle](https://app.avniproject.org/#/appdesigner/bundle)). This bundle can then be uploaded into another implementation if it is required to have the same metadata and configuration setup ([Admin -> Upload](https://app.avniproject.org/#/admin/upload) ).

Since this a feature with widespread consequences if the wrong bundle is used on the wrong implementation, the implementer can review the changes that will be affected as a result of uploading a bundle before applying it. The option to review the changes is displayed after selecting the upload type as 'Metadata Zip' on the upload screen and uploading the bundle.

<br />

On clicking 'Review', the uploaded bundle is compared against the implementation that the user is currently logged into and a file by file list of differences is displayed on screen. The file listing categorises the changes as additions (green), modifications (orange), removals (red) or if completely new items will be created if the bundle is applied.

![](https://files.readme.io/2582a6ae1664ad643eb9421b4cd7484d0d8baa00c480a9d13c36b60e6e8d8dbb-image.png)

<br />

On selecting a file, the details of the changes in that file are shown. The implementer can use the 'Back to Upload' option to return to the upload screen after reviewing the changes to change the bundle file used or apply the bundle.

![](https://files.readme.io/312f6da0ac043d3048fc4837f167416132de631a8d193084d809e81a63988fc8-metadata-diff.webp)


# File: ./readme/Implementers/how-do-i/updating-rules-in-bulk.md

title: Update rules in bulk
excerpt: ''
```sql
set role <organisation_db_user>;

-- Subject Type
update subject_type set
    program_eligibility_check_rule = replace(program_eligibility_check_rule, 'ruleServiceLibraryInterfaceForSharingModules', 'imports'),
    last_modified_date_time = current_timestamp
    where program_eligibility_check_rule like '%ruleServiceLibraryInterfaceForSharingModules%';
update subject_type set subject_summary_rule = replace(subject_summary_rule, 'ruleServiceLibraryInterfaceForSharingModules', 'imports'),
                        last_modified_date_time = current_timestamp
    where subject_summary_rule like '%ruleServiceLibraryInterfaceForSharingModules%';

-- Encounter Type
update encounter_type set encounter_eligibility_check_rule = replace(encounter_eligibility_check_rule, 'ruleServiceLibraryInterfaceForSharingModules', 'imports'),
                          last_modified_date_time = current_timestamp
    where encounter_eligibility_check_rule like '%ruleServiceLibraryInterfaceForSharingModules%';

-- Program
update program set enrolment_summary_rule = replace(enrolment_summary_rule, 'ruleServiceLibraryInterfaceForSharingModules', 'imports'),
                          last_modified_date_time = current_timestamp
    where enrolment_summary_rule like '%ruleServiceLibraryInterfaceForSharingModules%';
update program set enrolment_eligibility_check_rule = replace(enrolment_eligibility_check_rule, 'ruleServiceLibraryInterfaceForSharingModules', 'imports'),
                          last_modified_date_time = current_timestamp
    where enrolment_eligibility_check_rule like '%ruleServiceLibraryInterfaceForSharingModules%';
update program set manual_enrolment_eligibility_check_rule = replace(manual_enrolment_eligibility_check_rule, 'ruleServiceLibraryInterfaceForSharingModules', 'imports'),
                          last_modified_date_time = current_timestamp
    where manual_enrolment_eligibility_check_rule like '%ruleServiceLibraryInterfaceForSharingModules%';

-- Form
update form set decision_rule = replace(decision_rule, 'ruleServiceLibraryInterfaceForSharingModules', 'imports'),
                   last_modified_date_time = current_timestamp
where decision_rule like '%ruleServiceLibraryInterfaceForSharingModules%';
update form set validation_rule = replace(validation_rule, 'ruleServiceLibraryInterfaceForSharingModules', 'imports'),
                   last_modified_date_time = current_timestamp
where validation_rule like '%ruleServiceLibraryInterfaceForSharingModules%';
update form set visit_schedule_rule = replace(visit_schedule_rule, 'ruleServiceLibraryInterfaceForSharingModules', 'imports'),
                   last_modified_date_time = current_timestamp
where visit_schedule_rule like '%ruleServiceLibraryInterfaceForSharingModules%';
update form set checklists_rule = replace(checklists_rule, 'ruleServiceLibraryInterfaceForSharingModules', 'imports'),
                   last_modified_date_time = current_timestamp
where checklists_rule like '%ruleServiceLibraryInterfaceForSharingModules%';
update form set task_schedule_rule = replace(task_schedule_rule, 'ruleServiceLibraryInterfaceForSharingModules', 'imports'),
                   last_modified_date_time = current_timestamp
where task_schedule_rule like '%ruleServiceLibraryInterfaceForSharingModules%';

-- Form element

update form_element set "rule" = replace("rule", 'ruleServiceLibraryInterfaceForSharingModules', 'imports'),
					last_modified_date_time = current_timestamp 
where rule like '%ruleServiceLibraryInterfaceForSharingModules%';

-- Form element group

update form_element_group set "rule" = replace("rule", 'ruleServiceLibraryInterfaceForSharingModules', 'imports'),
					last_modified_date_time = current_timestamp 
where rule like '%ruleServiceLibraryInterfaceForSharingModules%';

-- Report Card
update report_card set query = replace(query, 'ruleServiceLibraryInterfaceForSharingModules', 'imports'),
                last_modified_date_time = current_timestamp
where query like '%ruleServiceLibraryInterfaceForSharingModules%'

-- Organisation Config
update organisation_config set worklist_updation_rule = replace(worklist_updation_rule, 'ruleServiceLibraryInterfaceForSharingModules', 'imports'),
                last_modified_date_time = current_timestamp
where worklist_updation_rule like '%ruleServiceLibraryInterfaceForSharingModules%';
```

One example is illustrated here, one can change the text and replace with something else.


# File: ./readme/Implementers/how-do-i/upload-local-database.md

title: Upload local database
excerpt: ''
Many times, the local database of the Android app provides clues to an issue happening on that device. Avni provides a mechanism to send a backup of the local database to Avni so that a developer can recreate this issue and perform fixes if required. 

To upload your local database, go to the "More" section on the home page and press on the "Upload Database" menu item. 

<Image align="center" width="500px" src="https://files.readme.io/be788e5-Upload_Database.png" />


# File: ./readme/Implementers/how-do-i/validate-a-new-implementation-for-user-acceptance-test-purposes.md

title: Validate a new Implementation for User Acceptance Test Purposes
excerpt: ''
<br/>

**UAT Test Scenarios** 

**Step 1: Download the Avni App** from Playstore to proceed with the test cases given below.

![](Aspose.Words.e7a1731f-5ee8-4023-8075-158ab95af182.001.png)

**Step 2: Login :**

* **Valid User Login:** Verify that a user can successfully log in with a valid username and password. (Ex. Username: xyza\@ProjectName, Password: xyza7988)

* **Invalid User Login:** Confirm that the system handles login attempts with invalid usernames and passwords.

* Test Ex. 1:** With an invalid username and valid password (Authentication error)

  Username: xy\@ProjectName, Password: xyza7988

* Test Ex. 2: With an invalid username with space applied anywhere in the user (Error should be displayed as incorrect username)

  User name: xyza\@cini\_uat, Password: xyza7988

* Test eg 3: When the user name is incorrect, it does not exist in the system. It will give an authentication error

* ` `Username: dinesh or dineshProjectName, Password: dine7988

* Test eg 4:** With a valid username and invalid password (Authentication error)

  Username: xyza\@cini\_uat, Password: xyza798

* Test eg 5:** With a valid username and invalid password special characters (Authentication error)

  Username: xyza\@cini\_uat, Password: xyza\@7988

  ![](Aspose.Words.e7a1731f-5ee8-4023-8075-158ab95af182.002.png)

* **Password Visibility**: Ensure the password field can be shown or hidden upon using the ‘show password’ toggle.

  ![](Aspose.Words.e7a1731f-5ee8-4023-8075-158ab95af182.003.png)

* **Forgot Password:** Forgot password option on the login page allows the user to generate a new password.

* By clicking on the forgot password, user can see the page where the registered user ID needs to be submitted. On providing the correct user ID, a pop-up will be displayed ‘We have sent an OTP on your registered Mobile Number’.

  ![](Aspose.Words.e7a1731f-5ee8-4023-8075-158ab95af182.004.png)![](Aspose.Words.e7a1731f-5ee8-4023-8075-158ab95af182.005.png)

* With that, the next page will be displayed with 3 fields to enter the one-time password received on the mobile number, the old password, and the new password.

  ![](Aspose.Words.e7a1731f-5ee8-4023-8075-158ab95af182.006.png)

* By successfully submitting all the details, the user can change the password and log in with the user ID and new password.

**3. Home Page:**

* **Home Dashboard:** The home page would have a dashboard to populate the aggregate (count) of different types of data, Ex. number of registrations, number of visits due, number of visits overdue, number of enrolments in the program, etc. By clicking on any of these cards, a list of individuals or other subjects will be displayed where the user can view profiles and details submitted in the registration form of any individual.

  ![](Aspose.Words.e7a1731f-5ee8-4023-8075-158ab95af182.007.png)

* Home Dashboard can have filters to update the data as per date or any other parameter to display card’s data accordingly.

  ![](Aspose.Words.e7a1731f-5ee8-4023-8075-158ab95af182.008.png)

**Last 24 Hours Statistics:**

* **Last 24 hours registration:** The user should be able to see the count of Registered individuals and click on it to list the details               
* **Last 24 hours visits:** The user should be able to see the count of Visits and click on it to list the details   

  ![](Aspose.Words.e7a1731f-5ee8-4023-8075-158ab95af182.009.png)

**4. Sync:**

* Sync button available on top right corner of the home page, allows user to sync the registration, enrollments, visits and changes done to the existing data.

  ![](Aspose.Words.e7a1731f-5ee8-4023-8075-158ab95af182.010.png)

* By clicking on the sync button, system syncs the changes done in particular in device’s app with server. Data synced in app can be seen in the reports.

* Number shown on the sync button suggests the changes are which ready to be synced.

* A successful sync would display a pop-up as shown below and If sync isn't done popularly or it displays some error like a Fatal error or Association error we have to contact the administrator ![](Aspose.Words.e7a1731f-5ee8-4023-8075-158ab95af182.011.png)

  ![](Aspose.Words.e7a1731f-5ee8-4023-8075-158ab95af182.012.png)

* If sync fails with the reason Network request then users have to check the internet connection and try to resync.

**5. Registration:**

* The register section should allow the user to register the subjects as per the project, Ex. Individuals, Anganwadi, Camps, Patients, etc.

  ![](Aspose.Words.e7a1731f-5ee8-4023-8075-158ab95af182.013.png)

* The user should be able to save, register the registration form, and proceed to the next registration form.
* After Registering the individual/any other subject in the mobile app, sync the data and validate that the data is reflected in the web app
* Register the individual/any other subject in the mobile app. Do not sync and validate that the data is not reflected in the web app.
* Register the individual in the mobile app using without turning on the network. Turn on the network, don't sync the data, and validate that the data is automatically synced after 10 minutes.

**6. Search Page:**

* Click on the Search button
* Select the subject (i.e. individual, camp, student, etc.) under Choose type, select other filters and click on Submit.

  ![](Aspose.Words.e7a1731f-5ee8-4023-8075-158ab95af182.014.png)

* On the search page, option called included voided if the user toggles it and clicks on the search it should display all the voided and unvoided data
* The result should display the list of subjects as per the filter provided. Along with the list of subjects, ‘Total matching results will be displayed’ to populate the count of subjects as per the filter provided.

  ![](Aspose.Words.e7a1731f-5ee8-4023-8075-158ab95af182.015.png)

* Please note that user can use any combinations of filter simultaneously to populate the results as required.

**6. More Page:**

* **Edit Settings:** In the ‘More’ section, the user should be able to click on the user icon to open ‘edit settings’. The edit setting should have configuration fields of Language, Location, Dashboard, and Auto-sync as shown below.

  ![](Aspose.Words.e7a1731f-5ee8-4023-8075-158ab95af182.016.png)

* In the **Language,** select the language the app content should be displayed and the app content should be displayed in the selected language. The default language is English

* If the language is not updated as select in the ‘edit settings’, then it is a bug.

* **Track location,** if it is enabled it will ask the user for permission if the user accepts the permission then it will capture the longitude and latitude of the current location

* Track location if it is disabled or they refuse to give the permission then it should not capture the user's location

* **Dashboard Auto-Refresh,** disabling this toggle would restrict the user from seeing updated version automatically

* If the user disables the auto refresh then the dashboard should not update the data on the dashboard automatically.

* **Auto Sync,** if the user enables the auto sync then data should sync automatically for every 10 minutes

* If the user disables the auto sync then data should not be synced automatically.

  ![](Aspose.Words.e7a1731f-5ee8-4023-8075-158ab95af182.017.png)

* **Dashboard,** click on this it should display offline dashboards where aggregate cards of different visits due/overdue, registration, and enrolments are done.

  ![](Aspose.Words.e7a1731f-5ee8-4023-8075-158ab95af182.018.png)

* By opening the aggregate cards given on the dashboard, the user can see the list of individuals/subjects and their profiles which aggregates to a count in the dashboard. (Refer to point#7 Profile more details)![](Aspose.Words.e7a1731f-5ee8-4023-8075-158ab95af182.019.png)

  ![](Aspose.Words.e7a1731f-5ee8-4023-8075-158ab95af182.020.png)

* **Entity Sync Status**

* **Setup Fast Sync**

* **Change Password,** click on it directly to the password change page

* Users can enter their current password

* The user should be able to enter the new password

* Password Visibility, ensure the password field can be shown or hidden upon user selection.

* Password Visibility (Toggle): Verify that toggling the password visibility option works as intended.

* Password mismatch if the user gives the current password as invalid then it should display the incorrect password or user ID

* Forgot password, If the user doesn't remember the current password while clicking on it. It will send you the OTP using that user enters the new OTP and also a new password

* Password mismatch if the user gives the mismatch value for Enter a new password and Confirm new password then it should display an error password mismatch

  Eg: Enter a new password: din123, Confirm new password: din321

* Password successfully: if the user gives the match value for Enter new password and Confirm new password then it should display password changed successfully.

  ![](Aspose.Words.e7a1731f-5ee8-4023-8075-158ab95af182.021.png)

* **Logout** should help the user close the current session and return to the login screen. Upon clicking the logout button, the user should be able to see a pop-up to confirm to end the current session and logout.

  ![](Aspose.Words.e7a1731f-5ee8-4023-8075-158ab95af182.022.png)

**7. Profile:**

* **Subject Profile:** The profile should typically contain details submitted in various forms and will populate details of enrollment and forms that are scheduled and filled previously.
* Subject profile would typically have name, gender, age, address on top.
* Profile page would contain the list of program subject enrolled to along with the option to enroll in a new program if eligible but not enrolled yet.
* Profile page would have the summary section to display important details which are filled in different forms.
* Profile would also contain visit planned which would display the visit scheduled along with completed visits section.

  ![](Aspose.Words.e7a1731f-5ee8-4023-8075-158ab95af182.023.png)![](Aspose.Words.e7a1731f-5ee8-4023-8075-158ab95af182.024.png)

  ![](Aspose.Words.e7a1731f-5ee8-4023-8075-158ab95af182.025.png)

**Important note:**

**The changes done in the application should be synced to save these changes on the server. Sync can be done manually from the button on the home page's top right corner.**

# File: ./readme/Implementers/implementers-concept-guide-introduction.md

title: Introduction
excerpt: ''
    - type: basic
      slug: avnis-domain-model-of-field-based-work
      title: Avni's domain model of field based work
---
Implementer's concept guide is for anyone who would like to implement Avni for any field-based program. We recommend this guide to be the first one to be read by anyone wanting to understand Avni.

While internally there are many parts of the system, if you are an implementer and using the hosted instance then these are the components you will be using. Some of the functions are intended for the end-users but you will use them for testing the application.

<Image title="Avni (4).png" alt={1089} width="80%" src="https://files.readme.io/9fa4f1f-Avni_4.png">
  User/Implementer components of Avni
</Image>


# File: ./readme/Implementers/reporting-and-business-analytics/ai-in-reporting.md

title: Developing BI dashboards using AI services
excerpt: >-
  robots: index
next:
  description: ''
---
The tool used for this is Cursor which internally uses other AI services. You can download [Cursor](https://www.cursor.com/).

The source code used in this tool is available here [avni-ai-experiment](https://github.com/avniproject/avni-ai-experiment) (private repository as the CSV files used in the context may contain customer specific information). This repository will become a public repository soon. 

# Generate aggregate and line list query

### When to use

Excel or spreadsheet contain the requirements for the report all present in a single sheet. This is the input used for generating the SQL. If you do not have this file then the steps below are **not recommended** as it will not be productive approach.

### Setup

1. Open avni-ai-experiment in Cursor.
2. Download the requirement sheet as a CSV file. Copy its contents and put them in any file under `bi-reporting-spike/dataset/workspace` folder. Let's say - `requirement.csv`. An example is present in workspace folder by name `example.csv`.
3. Create one file which contains all the table definition in the `bi-reporting-spike/aggregate/workspace`  or `bi-reporting-spike/linelist/workspace` folder. Let's say - `table-def.sql`. An example is present in workspace folder by name `example-jnpct-def.sql`. This was generated from IntelliJ (select schema and generate).

### Chat

1. Open chat window in Cursor.
2. Prompt to forget everything (line 1 of `aggregate-query-prompt.md` or `linelist-query-prompt.md`)
3. Follow the steps in [https://github.com/avniproject/avni-ai-experiment/blob/main/bi-reporting-spike/aggregate/workspace/aggregate-query-prompt.md](https://github.com/avniproject/avni-ai-experiment/blob/main/bi-reporting-spike/aggregate/workspace/aggregate-query-prompt.md) or [https://github.com/avniproject/avni-ai-experiment/blob/master/bi-reporting-spike/linelist/workspace/line-list-prompt.md](https://github.com/avniproject/avni-ai-experiment/blob/master/bi-reporting-spike/linelist/workspace/line-list-prompt.md)


# File: ./readme/Implementers/reporting-and-business-analytics/form-analytics-using-metabase-x-ray-feature.md

title: Form analytics using Metabase X-Ray feature
excerpt: ''
Metabase xRay allows for generating basic analytics on click of a button from the database table. Please follow the steps below for setting up table analytics that can be used. The steps below having been provided at a logical level.

> 📘 Note: The dashboard created using this approach cannot be easily migrated to another database hence the development should be done in production database, else it will involve rework.

### Features relevant to us

* Auto generated breakup by coded fields
* Can see line list for each breakup
* Related tables can be mapped to logical names
* Internal columns can be removed
* Related table’s data can be seen from the line list (e.g. by clicking on Individual name)
* In pie-chart form also see the percentage
* Can be used with custom models feature

### Standard ETL table or Custom Model

It is possible that your requirement involves using joins with other table like location for using in filters. To achieve this use Custom Model feature and use the metabase designer to join. Using native query is not recommended - as that requires configuring the columns to make it understanding to metabase features.

In your custom model you may want to take filter out records like voided = true, or exited, cancelled etc.

### Table configuration changes

Available from Admin ->> Table Metadata tab.

Remove visibility of fields that do not concern the user. Some you can remove from **everywhere** and some only in **detail view** (line list view). Discuss with functional people in your team about the exact system fields to change.

### Generate xRay

1. Find a table from data source
2. Click xRay
3. Choose more details
4. Save the dashboard automatically created. You can also move this to the right place using move option. By default they do in the `Automatically Generated Dashboards`. Note - You cannot add filter before generating dashboards.

### Dashboard changes

* Remove any unnecessary generated filters and cards first. With fewer cards the performance of the dashboard during the design process will be better.
* Any field directly on the table/form can be added as filter.
* Only one address filter can be added per table/dashboard (note that table metadata should be changed to map too).

### Table configuration changes to make certain fields more useful

Metabase allows to map a foreign key field such that one can see a logical text instead of seeing a number. For example - individual\_id can be mapped to Individual.first\_name; address\_id can be mapped to Address.Title.

### Known Limitations

* Cannot do percentage only totals (why? - [https://avni.readme.io/docs/form-analytics-using-metabase-x-ray-feature](https://avni.readme.io/docs/form-analytics-using-metabase-x-ray-feature)) in non-pie chart form.
* Once xRay dashboard is generated subsequent addition of fields will have to be manual, otherwise the previous changes will be lost.


# File: ./readme/Implementers/reporting-and-business-analytics/guide-to-export-and-import-reports-across-different-jasper-servers.md

title: Guide To Export and Import Reports across different Jasper Servers
excerpt: ''
## Reference: [https://community.jaspersoft.com/documentation/jasperreports-server/tibco-jasperreports-server-security-guide/vv900/jasperreports-server-security-guide-\_-keymanagement-\_-import\_and\_export/#Key\_Command\_Line\_Export](https://community.jaspersoft.com/documentation/jasperreports-server/tibco-jasperreports-server-security-guide/vv900/jasperreports-server-security-guide-_-keymanagement-_-import_and_export/#Key_Command_Line_Export)

## Login into Source server

## Execute below commands to export the report

```
## Navigate to scripts dir
cd /home/ubuntu/jasperreports-server-cp-7.5.0-bin/buildomatic  
## Execute the report export script
./js-export.sh --uris /RWB_2023 --output-zip gramin_rwb_2023.zip --secret-key="\<specify_key_value>"  
## Copy the generated export file to home dir
cp gramin_rwb_2023.zip ~/  
## Exit
exit
```

## Transfer file to your system using scp

Ex: from your machine terminal

```shell Shell
scp jasper-reporting-openchs:gramin_rwb_2023.zip ./
```

## Login into Target Jasper server webapp

Import the zip file in target jasper using the "Key Value" option by specifying the key value "\<specify\_key\_value>" used during export.

<Image align="center" src="https://files.readme.io/6ca70fd-Screenshot_2024-03-15_at_4.32.26_PM.png" />


# File: ./readme/Implementers/reporting-and-business-analytics/jasper-notes.md

title: Jasper notes
excerpt: ''
### Self referential hierarchical reports

1. The contents of JRXML can be manipulated based on the url parameters. The url parameters can be coming from the same report at a higher level.
2. Each report can have filters specific to that level, which cannot be dynamically changed. So this is a blocker.

### Creating new version

This is to avoid changing the production version as it is already in use.

1. Copy can be created using export.
2. All the files are text files so these can be changed in editor and then imported after zipping.


# File: ./sample-implementations/adolescent-care.md



# File: ./sample-implementations/agro-forestry.md



# File: ./sample-implementations/eye-camp.md



# File: ./sample-implementations/mch.md



# File: ./sample-implementations/ncd.md



# File: ./sample-implementations/sickle-cell-screening.md



# File: ./sample-implementations/social-security.md



# File: ./sample-implementations/teach.md



# File: ./sample-implementations/waste-collection.md



# File: ./scripts/README.md

# README File Processing Scripts

This directory contains scripts to process markdown files in the `readme` directory by removing YAML front matter while preserving title and excerpt information.

## Scripts Overview

### 1. `process_readme_files.py` - Main Processing Script
**Purpose**: Processes all markdown files in the readme directory by removing the first 12 lines but keeping lines 2 and 3.

**What it does**:
- Keeps line 2 (title)
- Keeps line 3 (excerpt) 
- Removes lines 1, 4-12 (YAML front matter)
- Keeps all content from original line 13 onwards

**Usage**:
```bash
cd scripts
python3 process_readme_files.py
```

### 2. `backup_readme_files.py` - Backup Script
**Purpose**: Creates timestamped backups of all markdown files before processing.

**Usage**:
```bash
cd scripts
python3 backup_readme_files.py
```

### 3. `test_single_file.py` - Test Script
**Purpose**: Tests the transformation on a single file to verify the logic before running on all files.

**Usage**:
```bash
cd scripts
python3 test_single_file.py
```

## Recommended Workflow

1. **Create Backup** (recommended):
   ```bash
   python3 backup_readme_files.py
   ```

2. **Test on Single File** (optional but recommended):
   ```bash
   python3 test_single_file.py
   ```

3. **Process All Files**:
   ```bash
   python3 process_readme_files.py
   ```

## Example Transformation

**Before** (original file):
```markdown
---
title: 'How to guide: Setting up Locations via CSV Upload'
excerpt: For bulk location upload after Release 10.0
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
## Definitions

Below is a list of definitions...
```

**After** (processed file):
```markdown
title: 'How to guide: Setting up Locations via CSV Upload'
excerpt: For bulk location upload after Release 10.0
## Definitions

Below is a list of definitions...
```

## Safety Features

- **Backup Script**: Creates timestamped backups before processing
- **Test Script**: Allows testing on a single file first
- **Error Handling**: Scripts handle errors gracefully and report issues
- **File Validation**: Checks if files have enough lines before processing
- **Progress Reporting**: Shows detailed progress and results

## File Structure

```
scripts/
├── README.md                    # This file
├── process_readme_files.py      # Main processing script
├── backup_readme_files.py       # Backup creation script
├── test_single_file.py          # Single file test script
└── readme_backup_YYYYMMDD_HHMMSS/  # Backup directories (created when needed)
```

## Notes

- All scripts are designed to work from the `scripts` directory
- The scripts automatically find the `readme` directory relative to their location
- Processing is recursive - it finds all `.md` files in subdirectories
- Scripts preserve file encoding (UTF-8) and line endings
- Error reporting shows which files failed to process (if any)


# File: ./webapp-documentation/sideBarDocumentation/ApplicationMenu.md

The customizable "Application menu" feature helps you add a new menu item that will show up on the "More" option of the Android app.

[Learn about creating an entry in Application Menu.](https://avni.readme.io/docs/application-menu)


# File: ./webapp-documentation/sideBarDocumentation/Bundle.md

Configuration from an organisation can be exported and imported into another organisation. This helps migrating the implementation of a program from one organisation to another.


# File: ./webapp-documentation/sideBarDocumentation/Card.md

Card contains the actual query that gets executed. Right now query should return a list of individual object.


# File: ./webapp-documentation/sideBarDocumentation/Catchment.md

A Catchment is a group of locations. Catchments are used to segregate areas of operation of each user (or group of users).

The field app will sync only data for the catchment assigned to the logged in user. By dividing into catchments, we ensure that the user has a smaller set of information to work with.

**Uploading catchments**
Catchments can also be created along with users in bulk using the [upload screen](/#/admin/upload).

[Learn more about Avni's domain model](https://avni.readme.io/docs/avnis-domain-model-of-field-based-work)


# File: ./webapp-documentation/sideBarDocumentation/Checklist.md

Checklists are typically used to upload time-tables of things to do such as vaccination.

[Learn about uploading a checklist](https://avni.readme.io/docs/upload-checklist)


# File: ./webapp-documentation/sideBarDocumentation/Concept.md

Concepts define the different pieces of information that you collect as part of your service delivery.

For example, if you collect the blood pressure of a subject in a form, then "Blood Pressure" should be defined as a concept. You would notice that every question in a form requires a concept

- [More information about concepts](https://avni.readme.io/docs/concepts)
- [Learn more about Avni's domain model](https://avni.readme.io/docs/avnis-domain-model-of-field-based-work)


# File: ./webapp-documentation/sideBarDocumentation/Dashboard.md

`Dashboard` created here will be shown in the field app.
You can add multiple `Sections` to a dashboard.
`Sections` will be shown in the same order as added here from the app-designer.
`Sections` can have multiple `Cards`, either in `Tile` or `List` format.
Within a `Section`, `Cards` will be shown in the same order as added here.

Collapse all the `Sections` for changing their order.


# File: ./webapp-documentation/sideBarDocumentation/Documentation.md

You can create documentation for the app. Currently documentation can be attached to a form element.


# File: ./webapp-documentation/sideBarDocumentation/EncounterType.md

Encounter Types (also called Visit Types) are used to determine the kinds of encounters/visits that can be performed. An encounter can be scheduled for a specific encounter type using rules. Here, we define that encounter type and the forms associated with the encounter type.

An encounter type is associated to a subject type. It need not be associated with programs (you can perform an annual survey of a population using encounter types not associated with programs, and use this information to enrol subjects into a program).

The encounter eligibility check rule is used to determine eligibility of an encounter type for a subject at any time.

- [Learn more about Avni's domain model](https://avni.readme.io/docs/avnis-domain-model-of-field-based-work)
- [Learn more about writing rules](https://avni.readme.io/docs/rules-concept-guide)


# File: ./webapp-documentation/sideBarDocumentation/IdentifierSource.md

Create autogenerated Ids by configuring Identifier Sources, and creating Identifier user assignments

[Learn more about setting up identifiers](https://avni.readme.io/docs/creating-identifiers)


# File: ./webapp-documentation/sideBarDocumentation/IdentifierUserAssignment.md

[Learn more about setting up identifiers](https://avni.readme.io/docs/creating-identifiers)


# File: ./webapp-documentation/sideBarDocumentation/Language.md

Choose all the languages you need the app to be available in.

Users can choose the language of their choice through their settings. You should remember to provide translations for your forms in these languages through the [translations](/#/translations) section.

When creating users, you can also provide the default language for each user

[Learn more about translation management](https://avni.readme.io/docs/translation-management)


# File: ./webapp-documentation/sideBarDocumentation/Location.md

Your service area is a hierarchy of different locations (eg: district, taluka, village).

A Location is associated with a Location Type. Define Location Types from the [Location Types menu](/#/admin/addressLevelType) before you start adding Locations.

All Subjects are associated with Locations. The field app requires you to provide this location to the lowest level available in the system.

**Uploading Locations**

You can also upload locations in bulk using the [upload screen](/#/admin/upload). When using the upload screen, location types are automatically created.

[Learn more about Avni's domain model](https://avni.readme.io/docs/avnis-domain-model-of-field-based-work)


# File: ./webapp-documentation/sideBarDocumentation/LocationType.md

Your service area is a hierarchy of different locations (eg: district, taluka, village). Here, we define the different location types that are required for your program to run.

**Example**: In State -> District -> City hierarchy
<br>City is level 1, District is level 2 and parent of City, State is level 3 and parent of District.

All Subjects are associated with Locations. The field app requires you to provide this location to the lowest level available in the system.

**Uploading Locations**

You can also upload locations using the Upload screen. This option will automatically create Location Types.

[Learn more about Avni's domain model](https://avni.readme.io/docs/avnis-domain-model-of-field-based-work)


# File: ./webapp-documentation/sideBarDocumentation/MyDashboardFilter.md

MyDashboard in Avni comes with some default filters. Additional filters can be added here.

[Look up more details](https://avni.readme.io/docs/my-dashboard-and-search-filters)


# File: ./webapp-documentation/sideBarDocumentation/NewsBroadcast.md

You can create and publish news from here. Once news is published it starts showing up to the field users after sync.


# File: ./webapp-documentation/sideBarDocumentation/OrganisationDetail.md

You can delete all the data that is filled using the field app. Also if you select to delete metadata, it'll delete all the forms and concept that you had created using web application.

**Please note that DELETE ALL DATA action is irreversible, so choose the options very carefully**

Several organisation-wide changes can be enabled from here.

`Approval Workflow`: Enabling this will allow you to approve/reject all the forms filled by the field users. You'll need to create a [custom dashboard](#/appdesigner/dashboard) and also adjust the [privileges](#/admin/userGroups) accordingly.

`Draft Save`: Enabling this feature will enable saving the registration form automatically on every press of next button. All the drafts are available on the register page.

`Enable Messaging`: Enabling this will introduce the capability of sending messages through Whatsapp. Remember that there is more configuration required for this integration to work.


# File: ./webapp-documentation/sideBarDocumentation/PhoneNumberVerification.md

This configuration is used to integrate with Msg91 to perform verification of phone numbers by sending an OTP.

[Learn more about Phone Number Verification](https://avni.readme.io/docs/phone-number-verification)


# File: ./webapp-documentation/sideBarDocumentation/Prints.md

Custom web pages for the prints can be uploaded from here. All the required static files must be zipped and uploaded here. Below information is required while uploading the zip file.

`Label: Text that will appear on the subject dashboard`

`File Name: HTML file name that will be served when above label button is pressed`

Multiple `Label/FileName` can be added by clicking on `Add more extensions`


# File: ./webapp-documentation/sideBarDocumentation/Program.md

A program defines the service, or intervention that you provide to subjects.

A subject is enrolled into the program using the Enrolment Form. Routine information is collected through Encounters. A subject exits a program by filling in the Exit Form.

- [Learn more about Avni's domain model](https://avni.readme.io/docs/avnis-domain-model-of-field-based-work)
- [Learn more about writing rules](https://avni.readme.io/docs/rules-concept-guide)


# File: ./webapp-documentation/sideBarDocumentation/Relationship.md

If you plan to store relationships of individuals between each other, define these relationships here.


# File: ./webapp-documentation/sideBarDocumentation/RelationshipType.md

Relationship Types define the different kind of relationships, and their reverse relationships. For example, the reverse relationship of a relationship "Son" could be "Mother" or "Father" (or "Guardian", or "Parent" depending on how you model relationships).


# File: ./webapp-documentation/sideBarDocumentation/Report.md

Reports of different type can be generated from here.


# File: ./webapp-documentation/sideBarDocumentation/SearchFilter.md

Filters on the Search tab of the field app can be enhanced by adding filters here.

[Look up more details](https://avni.readme.io/docs/my-dashboard-and-search-filters)


# File: ./webapp-documentation/sideBarDocumentation/SearchResultFields.md

Custom search result fields can be setup for each subject type. User can choose concepts from the
registration form. If no fields are setup for a subject type default fields will show up in the search result.


# File: ./webapp-documentation/sideBarDocumentation/StorageManagementConfig.md

This feature enables configuration of a custom SQL query which is used to determine which subjects' records should be excluded from syncing to the Avni mobile app. This helps to reduce storage usage on mobile devices and the time taken to sync the records.

The SQL query should only return the IDs of subjects whose data needs to be excluded from syncing. Refer to [the documentation for this feature](https://avni.readme.io/docs/app-storage-management-and-sync-disable) for additional details.


# File: ./webapp-documentation/sideBarDocumentation/SubjectType.md

Subject Types define the subjects (or things) that you collect information on. eg: Individual, Tractor, Water source, Classroom session.

**Person**

If you use this type, you get some bonus questions for free in the registration form - first and last names, gender and date of birth.

**Individual**

Use this type when you want to record data against non-human and single entity.

**Group**

Use the group type to define groups of a certain subject type. eg: A school might decide to define "Class" as a subject type against which information can be captured. It can also contain member subjects that are can have their own information.

**Household**

A household is a special kind of group. Groups roles are predefined when you choose household type, but you can choose any of the existing Person as member subject.

**User**

A user subject type is a type that can be used to manage information about users of the system. Each user will have one subject created based on this subject type. This subject and any data collected against it will or encounters and enrolments are only for single user.

[Learn more about Avni's domain model](https://avni.readme.io/docs/avnis-domain-model-of-field-based-work)


# File: ./webapp-documentation/sideBarDocumentation/Translation.md

After adding [languages](#/admin/language) you will be able to download/upload the translation file for all the different languages.

Learn more about [translation management](https://avni.readme.io/docs/translation-management).


# File: ./webapp-documentation/sideBarDocumentation/Upload.md

You can upload users, subjects, enrolments and encounters in bulk in this screen. Metadata zip files that have been downloaded from another organisation can also be uploaded in this screen.

All files except the metadata zip are supposed to be in a [CSV](https://en.wikipedia.org/wiki/Comma-separated_values) format. If you use Microsoft Excel, it has an option to save your spreadsheet in CSV format.

Use the **Download Sample** option to download a sample file. More details about the sample file are available [here](https://avni.readme.io/docs/upload-data)


# File: ./webapp-documentation/sideBarDocumentation/User.md

Logins for Avni. Users will get their first login details on email and SMS.

Ensure that you have created catchments for your users before creating them. Users can be created either through the [Users screen](/#/admin/user) or through the [upload screen](/#/admin/upload).

Users can be created or disabled. Disabled users cannot login. In case of password issues, the field application has the capability to reset passwords.

[Learn more about Users](https://avni.readme.io/docs/access-control)


# File: ./webapp-documentation/sideBarDocumentation/UserGroup.md

User Groups can be created to finely control user access to functions in the field and data entry apps.

By default, no configuration is required here as there is already an Everyone group that has all privileges.

[Learn more about Access Control and User Groups](https://avni.readme.io/docs/access-control)


# File: ./webapp-documentation/sideBarDocumentation/UserMessagingConfig.md

Newly created users will receive a message on their "WhatsApp application registered with their mobile number", based on the configuration here.
[Refer this link to know more about how to configure.](https://avni.readme.io/docs/writing-rules#13-message-rule)


# File: ./webapp-documentation/sideBarDocumentation/Video.md

You can create video playlist from webApp. These videos will show up in field application.

**Make sure that videos are already downloaded and exists in the path "OpenCHS/movies"**


# File: ./webapp-documentation/sideBarDocumentation/View.md

The views on this page are automatically generated or refreshed on click of `Create/Refresh View` button. There is one view corresponding to each form with every form field available as a column. These views help in writing the reports easily without having to understand the generic underlying Avni schema. Once generated, the views are available in Metabase or any other reporting tool you use.

The column names are based on form fields (concepts) which can be longer than permitted by the database, in such a case the names are shortened and you can see them at the top of view definition in comments. The format is - `Field name >> Shortened column name`.

Some types of change in form definition can cause these views to become obsolete. In such a case please regenerate these views and check your reports based on these views.


# File: ./webapp-documentation/sideBarDocumentation/WorklistUpdationRule.md

Worklist updation rules help stitch together different workflows, such as registration, enrolment and completion of various forms.

[Learn more about writing rules](https://avni.readme.io/docs/rules-concept-guide)
