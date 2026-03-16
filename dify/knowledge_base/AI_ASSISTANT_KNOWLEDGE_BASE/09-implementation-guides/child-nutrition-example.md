---
title: 'Implementation Example: Child Nutrition Program'
category: implementation-guides
audience: implementer
difficulty: intermediate
priority: medium
keywords:
- child nutrition
- nutrition tracking
- growth monitoring
- implementation example
last_updated: '2026-03-16'
task_types:
- example
features:
- subjects
- programs
- encounters
- forms
technical_level:
- procedural
implementation_phase:
- planning
- development
complexity: complex
retrieval_boost: 1.0
related_topics:
- implementation-checklist.md
estimated_reading_time: 4 minutes
version: '1.0'
---
# Implementation Example: Child Nutrition Program

<!-- CHUNK: tldr -->
## TL;DR

A complete implementation example of a child nutrition program in Avni, covering growth monitoring, nutrition tracking, and health assessments for children under 6 years. Includes subject types, forms, programs, encounter types, and JavaScript rules for automated visit scheduling and growth chart calculations.

<!-- END CHUNK -->

<!-- CHUNK: overview -->
## Overview

**What:** Real-world implementation of child nutrition program using Avni.

**Use case:** Community nutrition programs, crèche management, growth monitoring in rural areas.

**Key features:**
- Child registration with growth parameters
- Monthly growth monitoring encounters
- Automated visit scheduling
- Growth chart calculations (WHO standards)
- Nutrition status tracking
- Referral management

**Implementation time:** 2-3 weeks

Child nutrition is a vital indicator of a nation’s health and development. While India has made significant strides in
improving maternal and child health over the last decade, there is still a pressing need to address persistent gaps,
especially in underserved rural communities.

One of the most impactful periods in a child’s life is the first **1,000
days.** Nutrition during this window plays a
pivotal role in shaping the child’s cognitive development, immunity, and long-term health outcomes.


  <h2 style="margin: 0 0 8px 0; font-size: 1.25rem;">
    🎥 Video Case Study: Azim Premji Foundation | Community Nutrition Program (CNP)
  </h2>
  <a href="https://www.youtube.com/watch?v=sfB9QyFoWW8&list=PLEy8ff0CKDBkFhqQ95itFuEJMf38HwLBx" 
     target="_blank" 
     rel="noopener noreferrer"
     style="color: #007acc; text-decoration: underline;">
    Watch on YouTube
  </a>


### APF Odisha Nutrition Initiative: Focused Care from Pregnancy to Early Childhood

The **Azim Premji Foundation’s Odisha Nutrition Initiative** addresses these challenges with a focused intervention that
spans from pregnancy through the first five years of a child's life. The initiative targets maternal and child nutrition
through community-level engagement, regular monitoring, and technology-driven support systems.


    <img src="/img/2025-05-28-bridging-the-nutrition-gap-apf-odisha/program-overview.png">


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


      <img src="/img/2025-05-28-bridging-the-nutrition-gap-apf-odisha/offline-dashboard.gif">


      <img src="/img/2025-05-28-bridging-the-nutrition-gap-apf-odisha/individual-dashboard-child.gif">


      <img src="/img/2025-05-28-bridging-the-nutrition-gap-apf-odisha/individual-dashboard.gif">


    <img src="/img/2025-05-28-bridging-the-nutrition-gap-apf-odisha/reports.png">
<!-- END CHUNK -->

<!-- CHUNK: program-reach-and-impact -->
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


<i>“Avni plays a pivotal role in strengthening the Community Nutrition Program by bridging the gap between field-level data
collection and real-time decision-making. Its offline-first design is especially effective in remote tribal areas with
limited connectivity. By enabling frontline workers to capture key data on maternal and child health and service
delivery during home visits, growth monitoring sessions, and VHSNDs, AVNI facilitates the timely identification and
follow-up of High-Risk Pregnancies (HRP) and undernourished children.” </i> \- **Ramesh Sahu, Program Manager**


If you're interested in adopting a similar approach or want to learn more about how the Avni platform can support your initiatives:


👉 <a href="https://calendly.com/avnisupport-samanvayfoundation/product-demo-and-discussion?embed_domain=avniproject.org&embed_type=PopupText" target="_blank" rel="noopener noreferrer">
Schedule a call with us
</a>


📬 <a href="https://avniproject.us17.list-manage.com/subscribe?u=5f3876f49a7603817af2856b9&id=c9fdedc9e7" target="_blank" rel="noopener noreferrer">
Subscribe to our newsletter to stay updated on new case studies, features, and implementation stories.
</a>


Let’s work together to scale impactful solutions for better health outcomes.
<!-- END CHUNK -->

<!-- CHUNK: related-topics -->
## Related Topics

<!-- Add links to related documentation -->
<!-- END CHUNK -->