"""
100 Visit Schedule Rule Examples for Testing LLM Rules Generator
Generated based on analysis of existing visit_schedule_rules.csv and form types
Distribution: 17 examples each for 6 form types (ProgramEncounter, Encounter, ProgramEnrolment, ProgramEncounterCancellation, IndividualEncounterCancellation, ProgramExit) = 102 total, reduced to 100
"""

VISIT_SCHEDULE_RULE_EXAMPLES = [
    # ============== PROGRAM ENCOUNTER EXAMPLES (17) ==============
    {
        "id": 1,
        "scenario": "Schedule ANC follow-up 28 days after current ANC visit",
        "context": {
            "formType": "ProgramEncounter",
            "encounterType": "ANC",
            "encounterTypes": [
                {"name": "ANC", "program": "Maternal Health"},
                {"name": "ANC - Follow Up", "program": "Maternal Health"},
                {"name": "Delivery", "program": "Maternal Health"},
                {"name": "PNC", "program": "Maternal Health"},
            ],
            "concepts": [
                "lmp-date",
                "edd-date",
                "gestational-age",
                "high-risk-factors",
            ],
        },
        "rule_request": "Schedule ANC Follow Up visit 28 days after the current ANC encounter",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEncounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEncounter });
  
  const hasExitedProgram = (programEncounter) => programEncounter.programEnrolment.programExitDateTime;
  if(hasExitedProgram(programEncounter)) return scheduleBuilder.getAll();

  const moment = imports.moment;
  
  const earliestDate = moment(programEncounter.encounterDateTime).add(28, 'days').toDate();
  const maxDate = moment(earliestDate).add(7, 'days').toDate();
  
  scheduleBuilder.add({
    name: "ANC - Follow Up",
    encounterType: "ANC - Follow Up",
    earliestDate,
    maxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 2,
        "scenario": "Schedule Child Followup based on nutritional status",
        "context": {
            "formType": "ProgramEncounter",
            "encounterType": "Growth Monitoring",
            "encounterTypes": [
                {"name": "Growth Monitoring", "program": "Child Health"},
                {"name": "Child Followup", "program": "Child Health"},
                {"name": "NRC Admission", "program": "Child Health"},
            ],
            "concepts": ["nutritional-status", "weight", "height", "muac-measurement"],
        },
        "rule_request": "Schedule Child Followup in 7 days if nutritional status is 'SAM', in 14 days if 'MAM', and in 30 days if normal",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEncounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEncounter });
  
  const hasExitedProgram = (programEncounter) => programEncounter.programEnrolment.programExitDateTime;
  if(hasExitedProgram(programEncounter)) return scheduleBuilder.getAll();

  const moment = imports.moment;
  const nutritionalStatus = programEncounter.getObservationReadableValue('nutritional-status');
  
  let dayOffset;
  if (nutritionalStatus === 'SAM') {
    dayOffset = 7;
  } else if (nutritionalStatus === 'MAM') {
    dayOffset = 14;
  } else {
    dayOffset = 30;
  }
  
  const earliestDate = moment(programEncounter.encounterDateTime).add(dayOffset, 'days').toDate();
  const maxDate = moment(earliestDate).add(7, 'days').toDate();
  
  scheduleBuilder.add({
    name: "Child Followup",
    encounterType: "Child Followup",
    earliestDate,
    maxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 3,
        "scenario": "Schedule next ANC based on gestational age",
        "context": {
            "formType": "ProgramEncounter",
            "encounterType": "ANC",
            "encounterTypes": [
                {"name": "ANC", "program": "Maternal Health"},
                {"name": "ANC - Follow Up", "program": "Maternal Health"},
                {"name": "High Risk ANC", "program": "Maternal Health"},
            ],
            "concepts": [
                "gestational-age",
                "high-risk-factors",
                "lmp-date",
                "bp-systolic",
            ],
        },
        "rule_request": "Schedule ANC Follow Up at 20 weeks if gestational age is less than 16 weeks, otherwise at 28 weeks",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEncounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEncounter });
  
  const hasExitedProgram = (programEncounter) => programEncounter.programEnrolment.programExitDateTime;
  if(hasExitedProgram(programEncounter)) return scheduleBuilder.getAll();

  const moment = imports.moment;
  const gestationalAge = programEncounter.getObservationReadableValue('gestational-age');
  const lmpDate = programEncounter.getObservationReadableValue('lmp-date');
  
  let targetWeeks;
  if (gestationalAge < 16) {
    targetWeeks = 20;
  } else {
    targetWeeks = 28;
  }
  
  const earliestDate = moment(lmpDate).add(targetWeeks, 'weeks').toDate();
  const maxDate = moment(earliestDate).add(2, 'weeks').toDate();
  
  scheduleBuilder.add({
    name: "ANC - Follow Up",
    encounterType: "ANC - Follow Up",
    earliestDate,
    maxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 4,
        "scenario": "Child immunization follow-up based on age",
        "context": {
            "formType": "ProgramEncounter",
            "encounterType": "Child Immunization",
            "encounterTypes": [
                {"name": "Child Immunization", "program": "Child Health"},
                {"name": "Child Followup", "program": "Child Health"},
                {"name": "Immunization Catchup", "program": "Child Health"},
            ],
            "concepts": [
                "immunization-type",
                "child-age-months",
                "next-due-vaccine",
                "missed-vaccines",
            ],
        },
        "rule_request": "Schedule Child Followup in 6 weeks for next immunization dose based on child's current age",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEncounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEncounter });
  
  const hasExitedProgram = (programEncounter) => programEncounter.programEnrolment.programExitDateTime;
  if(hasExitedProgram(programEncounter)) return scheduleBuilder.getAll();

  const moment = imports.moment;
  const childAgeMonths = programEncounter.getObservationReadableValue('child-age-months');
  
  // Schedule next immunization based on age
  const earliestDate = moment(programEncounter.encounterDateTime).add(6, 'weeks').toDate();
  const maxDate = moment(earliestDate).add(1, 'week').toDate();
  
  scheduleBuilder.add({
    name: "Child Followup",
    encounterType: "Child Followup",
    earliestDate,
    maxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 5,
        "scenario": "PNC visit based on delivery complications",
        "context": {
            "formType": "ProgramEncounter",
            "encounterType": "Delivery",
            "encounterTypes": [
                {"name": "Delivery", "program": "Maternal Health"},
                {"name": "PNC", "program": "Maternal Health"},
                {"name": "Emergency PNC", "program": "Maternal Health"},
            ],
            "concepts": [
                "delivery-complications",
                "c-section",
                "bleeding",
                "infection-signs",
            ],
        },
        "rule_request": "Schedule Emergency PNC in 3 days if delivery complications present, otherwise regular PNC in 7 days",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEncounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEncounter });
  
  const hasExitedProgram = (programEncounter) => programEncounter.programEnrolment.programExitDateTime;
  if(hasExitedProgram(programEncounter)) return scheduleBuilder.getAll();

  const moment = imports.moment;
  const deliveryComplications = programEncounter.getObservationReadableValue('delivery-complications');
  
  let encounterType, dayOffset;
  if (deliveryComplications === 'Yes') {
    encounterType = "Emergency PNC";
    dayOffset = 3;
  } else {
    encounterType = "PNC";
    dayOffset = 7;
  }
  
  const earliestDate = moment(programEncounter.encounterDateTime).add(dayOffset, 'days').toDate();
  const maxDate = moment(earliestDate).add(3, 'days').toDate();
  
  scheduleBuilder.add({
    name: encounterType,
    encounterType: encounterType,
    earliestDate,
    maxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 6,
        "scenario": "Adolescent health follow-up with age restriction",
        "context": {
            "formType": "ProgramEncounter",
            "encounterType": "Adolescent Health Check",
            "encounterTypes": [
                {"name": "Adolescent Health Check", "program": "Adolescent Health"},
                {"name": "Adolescent Followup", "program": "Adolescent Health"},
                {"name": "Adolescent Counseling", "program": "Adolescent Health"},
            ],
            "concepts": [
                "age-years",
                "health-concerns",
                "menstrual-irregularities",
                "substance-use",
            ],
        },
        "rule_request": "Schedule Adolescent Followup in 3 months, but only for individuals aged 10-19 years",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEncounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEncounter });
  
  const hasExitedProgram = (programEncounter) => programEncounter.programEnrolment.programExitDateTime;
  if(hasExitedProgram(programEncounter)) return scheduleBuilder.getAll();

  const moment = imports.moment;
  const ageYears = programEncounter.programEnrolment.individual.getAgeInYears();
  
  // Only schedule for adolescents aged 10-19
  if (ageYears >= 10 && ageYears <= 19) {
    const earliestDate = moment(programEncounter.encounterDateTime).add(3, 'months').toDate();
    const maxDate = moment(earliestDate).add(2, 'weeks').toDate();
    
    scheduleBuilder.add({
      name: "Adolescent Followup",
      encounterType: "Adolescent Followup",
      earliestDate,
      maxDate
    });
  }
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 7,
        "scenario": "Diabetes management based on HbA1c levels",
        "context": {
            "formType": "ProgramEncounter",
            "encounterType": "Diabetes Review",
            "encounterTypes": [
                {"name": "Diabetes Review", "program": "NCD Management"},
                {"name": "Diabetes Follow-up", "program": "NCD Management"},
                {"name": "Emergency Diabetes Care", "program": "NCD Management"},
            ],
            "concepts": [
                "hba1c-level",
                "blood-glucose",
                "medication-compliance",
                "complications",
            ],
        },
        "rule_request": "Schedule Emergency Diabetes Care in 1 week if HbA1c > 9%, Diabetes Follow-up in 1 month if HbA1c 7-9%, otherwise in 3 months",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEncounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEncounter });
  
  const hasExitedProgram = (programEncounter) => programEncounter.programEnrolment.programExitDateTime;
  if(hasExitedProgram(programEncounter)) return scheduleBuilder.getAll();

  const moment = imports.moment;
  const hba1cLevel = programEncounter.getObservationReadableValue('hba1c-level');
  
  let encounterType, timeOffset, timeUnit;
  
  if (hba1cLevel > 9) {
    encounterType = "Emergency Diabetes Care";
    timeOffset = 1;
    timeUnit = 'week';
  } else if (hba1cLevel >= 7 && hba1cLevel <= 9) {
    encounterType = "Diabetes Follow-up";
    timeOffset = 1;
    timeUnit = 'month';
  } else {
    encounterType = "Diabetes Follow-up";
    timeOffset = 3;
    timeUnit = 'months';
  }
  
  const earliestDate = moment(programEncounter.encounterDateTime).add(timeOffset, timeUnit).toDate();
  const maxDate = moment(earliestDate).add(1, 'week').toDate();
  
  scheduleBuilder.add({
    name: encounterType,
    encounterType: encounterType,
    earliestDate,
    maxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 8,
        "scenario": "Hypertension follow-up based on blood pressure",
        "context": {
            "formType": "ProgramEncounter",
            "encounterType": "Hypertension Check",
            "encounterTypes": [
                {"name": "Hypertension Check", "program": "NCD Management"},
                {"name": "Hypertension Follow-up", "program": "NCD Management"},
                {"name": "BP Monitoring", "program": "NCD Management"},
            ],
            "concepts": [
                "systolic-bp",
                "diastolic-bp",
                "medication-adherence",
                "lifestyle-changes",
            ],
        },
        "rule_request": "Schedule BP Monitoring in 2 weeks if systolic BP > 160 or diastolic BP > 100, otherwise Hypertension Follow-up in 1 month",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEncounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEncounter });
  
  const hasExitedProgram = (programEncounter) => programEncounter.programEnrolment.programExitDateTime;
  if(hasExitedProgram(programEncounter)) return scheduleBuilder.getAll();

  const moment = imports.moment;
  const systolicBP = programEncounter.getObservationReadableValue('systolic-bp');
  const diastolicBP = programEncounter.getObservationReadableValue('diastolic-bp');
  
  let encounterType, timeOffset, timeUnit;
  
  if (systolicBP > 160 || diastolicBP > 100) {
    encounterType = "BP Monitoring";
    timeOffset = 2;
    timeUnit = 'weeks';
  } else {
    encounterType = "Hypertension Follow-up";
    timeOffset = 1;
    timeUnit = 'month';
  }
  
  const earliestDate = moment(programEncounter.encounterDateTime).add(timeOffset, timeUnit).toDate();
  const maxDate = moment(earliestDate).add(1, 'week').toDate();
  
  scheduleBuilder.add({
    name: encounterType,
    encounterType: encounterType,
    earliestDate,
    maxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 9,
        "scenario": "Child development assessment scheduling",
        "context": {
            "formType": "ProgramEncounter",
            "encounterType": "Child Development",
            "encounterTypes": [
                {"name": "Child Development", "program": "Child Health"},
                {"name": "Development Follow-up", "program": "Child Health"},
                {"name": "Early Intervention", "program": "Child Health"},
            ],
            "concepts": [
                "developmental-milestones",
                "motor-skills",
                "speech-delay",
                "child-age-months",
            ],
        },
        "rule_request": "Schedule Development Follow-up in 1 month if developmental delays detected, otherwise in 6 months",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEncounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEncounter });
  
  const hasExitedProgram = (programEncounter) => programEncounter.programEnrolment.programExitDateTime;
  if(hasExitedProgram(programEncounter)) return scheduleBuilder.getAll();

  const moment = imports.moment;
  const developmentalMilestones = programEncounter.getObservationReadableValue('developmental-milestones');
  
  let timeOffset;
  if (developmentalMilestones === 'Delayed' || developmentalMilestones === 'Concerning') {
    timeOffset = 1;
  } else {
    timeOffset = 6;
  }
  
  const earliestDate = moment(programEncounter.encounterDateTime).add(timeOffset, 'months').toDate();
  const maxDate = moment(earliestDate).add(2, 'weeks').toDate();
  
  scheduleBuilder.add({
    name: "Development Follow-up",
    encounterType: "Development Follow-up",
    earliestDate,
    maxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 10,
        "scenario": "TB treatment follow-up",
        "context": {
            "formType": "ProgramEncounter",
            "encounterType": "TB Treatment Review",
            "encounterTypes": [
                {"name": "TB Treatment Review", "program": "TB Program"},
                {"name": "TB Follow-up", "program": "TB Program"},
                {"name": "TB Sputum Test", "program": "TB Program"},
            ],
            "concepts": [
                "sputum-result",
                "treatment-month",
                "side-effects",
                "weight-gain",
            ],
        },
        "rule_request": "Schedule TB Sputum Test every 2 months during intensive phase, every 3 months during continuation phase",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEncounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEncounter });
  
  const hasExitedProgram = (programEncounter) => programEncounter.programEnrolment.programExitDateTime;
  if(hasExitedProgram(programEncounter)) return scheduleBuilder.getAll();

  const moment = imports.moment;
  const treatmentMonth = programEncounter.getObservationReadableValue('treatment-month');
  
  let timeOffset;
  if (treatmentMonth <= 2) {
    // Intensive phase - every 2 months
    timeOffset = 2;
  } else {
    // Continuation phase - every 3 months
    timeOffset = 3;
  }
  
  const earliestDate = moment(programEncounter.encounterDateTime).add(timeOffset, 'months').toDate();
  const maxDate = moment(earliestDate).add(1, 'week').toDate();
  
  scheduleBuilder.add({
    name: "TB Sputum Test",
    encounterType: "TB Sputum Test",
    earliestDate,
    maxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 11,
        "scenario": "Mental health follow-up based on severity",
        "context": {
            "formType": "ProgramEncounter",
            "encounterType": "Mental Health Assessment",
            "encounterTypes": [
                {"name": "Mental Health Assessment", "program": "Mental Health"},
                {"name": "Mental Health Follow-up", "program": "Mental Health"},
                {"name": "Crisis Intervention", "program": "Mental Health"},
            ],
            "concepts": [
                "phq9-score",
                "gad7-score",
                "suicidal-ideation",
                "medication-response",
            ],
        },
        "rule_request": "Schedule Crisis Intervention in 1 week if PHQ-9 score > 15, Mental Health Follow-up in 2 weeks if score 10-15, otherwise in 1 month",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEncounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEncounter });
  
  const hasExitedProgram = (programEncounter) => programEncounter.programEnrolment.programExitDateTime;
  if(hasExitedProgram(programEncounter)) return scheduleBuilder.getAll();

  const moment = imports.moment;
  const phq9Score = programEncounter.getObservationReadableValue('phq9-score');
  
  let encounterType, timeOffset, timeUnit;
  
  if (phq9Score > 15) {
    encounterType = "Crisis Intervention";
    timeOffset = 1;
    timeUnit = 'week';
  } else if (phq9Score >= 10 && phq9Score <= 15) {
    encounterType = "Mental Health Follow-up";
    timeOffset = 2;
    timeUnit = 'weeks';
  } else {
    encounterType = "Mental Health Follow-up";
    timeOffset = 1;
    timeUnit = 'month';
  }
  
  const earliestDate = moment(programEncounter.encounterDateTime).add(timeOffset, timeUnit).toDate();
  const maxDate = moment(earliestDate).add(3, 'days').toDate();
  
  scheduleBuilder.add({
    name: encounterType,
    encounterType: encounterType,
    earliestDate,
    maxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 12,
        "scenario": "Newborn care scheduling based on birth weight",
        "context": {
            "formType": "ProgramEncounter",
            "encounterType": "Newborn Care",
            "encounterTypes": [
                {"name": "Newborn Care", "program": "Child Health"},
                {"name": "LBW Follow-up", "program": "Child Health"},
                {"name": "NICU Follow-up", "program": "Child Health"},
            ],
            "concepts": [
                "birth-weight",
                "gestational-age-birth",
                "feeding-issues",
                "jaundice",
            ],
        },
        "rule_request": "Schedule LBW Follow-up in 3 days if birth weight < 2.5kg, otherwise regular Newborn Care in 1 week",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEncounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEncounter });
  
  const hasExitedProgram = (programEncounter) => programEncounter.programEnrolment.programExitDateTime;
  if(hasExitedProgram(programEncounter)) return scheduleBuilder.getAll();

  const moment = imports.moment;
  const birthWeight = programEncounter.getObservationReadableValue('birth-weight');
  
  let encounterType, dayOffset;
  if (birthWeight < 2.5) {
    encounterType = "LBW Follow-up";
    dayOffset = 3;
  } else {
    encounterType = "Newborn Care";
    dayOffset = 7;
  }
  
  const earliestDate = moment(programEncounter.encounterDateTime).add(dayOffset, 'days').toDate();
  const maxDate = moment(earliestDate).add(2, 'days').toDate();
  
  scheduleBuilder.add({
    name: encounterType,
    encounterType: encounterType,
    earliestDate,
    maxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 13,
        "scenario": "Family planning follow-up based on method",
        "context": {
            "formType": "ProgramEncounter",
            "encounterType": "Family Planning",
            "encounterTypes": [
                {"name": "Family Planning", "program": "Reproductive Health"},
                {"name": "FP Follow-up", "program": "Reproductive Health"},
                {"name": "Method Change", "program": "Reproductive Health"},
            ],
            "concepts": [
                "contraceptive-method",
                "side-effects",
                "method-satisfaction",
                "bleeding-pattern",
            ],
        },
        "rule_request": "Schedule FP Follow-up in 3 months for oral contraceptives, 6 months for injectables, 1 year for IUD/implants",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEncounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEncounter });
  
  const hasExitedProgram = (programEncounter) => programEncounter.programEnrolment.programExitDateTime;
  if(hasExitedProgram(programEncounter)) return scheduleBuilder.getAll();

  const moment = imports.moment;
  const contraceptiveMethod = programEncounter.getObservationReadableValue('contraceptive-method');
  
  let timeOffset, timeUnit;
  if (contraceptiveMethod === 'Oral Contraceptives' || contraceptiveMethod === 'Pills') {
    timeOffset = 3;
    timeUnit = 'months';
  } else if (contraceptiveMethod === 'Injectable' || contraceptiveMethod === 'DMPA') {
    timeOffset = 6;
    timeUnit = 'months';
  } else if (contraceptiveMethod === 'IUD' || contraceptiveMethod === 'Implant') {
    timeOffset = 1;
    timeUnit = 'year';
  } else {
    timeOffset = 6; // Default
    timeUnit = 'months';
  }
  
  const earliestDate = moment(programEncounter.encounterDateTime).add(timeOffset, timeUnit).toDate();
  const maxDate = moment(earliestDate).add(2, 'weeks').toDate();
  
  scheduleBuilder.add({
    name: "FP Follow-up",
    encounterType: "FP Follow-up",
    earliestDate,
    maxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 14,
        "scenario": "Malnutrition treatment based on MUAC measurement",
        "context": {
            "formType": "ProgramEncounter",
            "encounterType": "Nutrition Assessment",
            "encounterTypes": [
                {"name": "Nutrition Assessment", "program": "Nutrition"},
                {"name": "SAM Treatment", "program": "Nutrition"},
                {"name": "MAM Treatment", "program": "Nutrition"},
            ],
            "concepts": [
                "muac-measurement",
                "weight-for-height",
                "appetite-test",
                "medical-complications",
            ],
        },
        "rule_request": "Schedule SAM Treatment immediately if MUAC < 11.5cm, MAM Treatment if 11.5-12.5cm, otherwise routine follow-up in 1 month",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEncounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEncounter });
  
  const hasExitedProgram = (programEncounter) => programEncounter.programEnrolment.programExitDateTime;
  if(hasExitedProgram(programEncounter)) return scheduleBuilder.getAll();

  const moment = imports.moment;
  const muacMeasurement = programEncounter.getObservationReadableValue('muac-measurement');
  
  let encounterType, timeOffset, timeUnit;
  if (muacMeasurement < 11.5) {
    encounterType = "SAM Treatment";
    timeOffset = 0;
    timeUnit = 'days';
  } else if (muacMeasurement >= 11.5 && muacMeasurement <= 12.5) {
    encounterType = "MAM Treatment";
    timeOffset = 3;
    timeUnit = 'days';
  } else {
    encounterType = "Nutrition Assessment";
    timeOffset = 1;
    timeUnit = 'month';
  }
  
  const earliestDate = moment(programEncounter.encounterDateTime).add(timeOffset, timeUnit).toDate();
  const maxDate = moment(earliestDate).add(3, 'days').toDate();
  
  scheduleBuilder.add({
    name: encounterType,
    encounterType: encounterType,
    earliestDate,
    maxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 15,
        "scenario": "COPD management based on symptoms",
        "context": {
            "formType": "ProgramEncounter",
            "encounterType": "COPD Review",
            "encounterTypes": [
                {"name": "COPD Review", "program": "NCD Management"},
                {"name": "COPD Exacerbation", "program": "NCD Management"},
                {"name": "Pulmonary Rehab", "program": "NCD Management"},
            ],
            "concepts": [
                "breathlessness-score",
                "exacerbation-frequency",
                "oxygen-saturation",
                "inhaler-technique",
            ],
        },
        "rule_request": "Schedule COPD Exacerbation care in 3 days if breathlessness worsening, otherwise routine review in 3 months",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEncounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEncounter });
  
  const hasExitedProgram = (programEncounter) => programEncounter.programEnrolment.programExitDateTime;
  if(hasExitedProgram(programEncounter)) return scheduleBuilder.getAll();

  const moment = imports.moment;
  const breathlessnessScore = programEncounter.getObservationReadableValue('breathlessness-score');
  
  let encounterType, timeOffset, timeUnit;
  if (breathlessnessScore > 3 || breathlessnessScore === 'Worsening') {
    encounterType = "COPD Exacerbation";
    timeOffset = 3;
    timeUnit = 'days';
  } else {
    encounterType = "COPD Review";
    timeOffset = 3;
    timeUnit = 'months';
  }
  
  const earliestDate = moment(programEncounter.encounterDateTime).add(timeOffset, timeUnit).toDate();
  const maxDate = moment(earliestDate).add(1, 'week').toDate();
  
  scheduleBuilder.add({
    name: encounterType,
    encounterType: encounterType,
    earliestDate,
    maxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 16,
        "scenario": "Asthma control assessment",
        "context": {
            "formType": "ProgramEncounter",
            "encounterType": "Asthma Review",
            "encounterTypes": [
                {"name": "Asthma Review", "program": "Respiratory Care"},
                {"name": "Asthma Education", "program": "Respiratory Care"},
                {"name": "Peak Flow Monitor", "program": "Respiratory Care"},
            ],
            "concepts": [
                "asthma-control-test",
                "peak-flow",
                "inhaler-technique",
                "trigger-avoidance",
            ],
        },
        "rule_request": "Schedule Asthma Education in 1 week if poor control (ACT score < 15), otherwise routine review in 3 months",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEncounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEncounter });
  
  const hasExitedProgram = (programEncounter) => programEncounter.programEnrolment.programExitDateTime;
  if(hasExitedProgram(programEncounter)) return scheduleBuilder.getAll();

  const moment = imports.moment;
  const asthmaControlTest = programEncounter.getObservationReadableValue('asthma-control-test');
  
  let encounterType, timeOffset, timeUnit;
  if (asthmaControlTest < 15) {
    encounterType = "Asthma Education";
    timeOffset = 1;
    timeUnit = 'week';
  } else {
    encounterType = "Asthma Review";
    timeOffset = 3;
    timeUnit = 'months';
  }
  
  const earliestDate = moment(programEncounter.encounterDateTime).add(timeOffset, timeUnit).toDate();
  const maxDate = moment(earliestDate).add(1, 'week').toDate();
  
  scheduleBuilder.add({
    name: encounterType,
    encounterType: encounterType,
    earliestDate,
    maxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 17,
        "scenario": "Eye care screening for diabetics",
        "context": {
            "formType": "ProgramEncounter",
            "encounterType": "Eye Screening",
            "encounterTypes": [
                {"name": "Eye Screening", "program": "Eye Care"},
                {"name": "Retinal Exam", "program": "Eye Care"},
                {"name": "Urgent Ophthalmology", "program": "Eye Care"},
            ],
            "concepts": [
                "visual-acuity",
                "retinal-changes",
                "diabetes-duration",
                "blood-sugar-control",
            ],
        },
        "rule_request": "Schedule Urgent Ophthalmology if retinal changes detected, otherwise annual Retinal Exam for diabetics",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEncounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEncounter });
  
  const hasExitedProgram = (programEncounter) => programEncounter.programEnrolment.programExitDateTime;
  if(hasExitedProgram(programEncounter)) return scheduleBuilder.getAll();

  const moment = imports.moment;
  const retinalChanges = programEncounter.getObservationReadableValue('retinal-changes');
  
  let encounterType, timeOffset, timeUnit;
  if (retinalChanges === 'Yes' || retinalChanges === 'Abnormal') {
    encounterType = "Urgent Ophthalmology";
    timeOffset = 1;
    timeUnit = 'week';
  } else {
    encounterType = "Retinal Exam";
    timeOffset = 1;
    timeUnit = 'year';
  }
  
  const earliestDate = moment(programEncounter.encounterDateTime).add(timeOffset, timeUnit).toDate();
  const maxDate = moment(earliestDate).add(2, 'weeks').toDate();
  
  scheduleBuilder.add({
    name: encounterType,
    encounterType: encounterType,
    earliestDate,
    maxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    # ============== ENCOUNTER EXAMPLES (17) ==============
    {
        "id": 18,
        "scenario": "General health screening follow-up",
        "context": {
            "formType": "Encounter",
            "encounterType": "Health Screening",
            "encounterTypes": [
                {"name": "Health Screening"},
                {"name": "Follow-up Visit"},
                {"name": "Specialist Referral"},
            ],
            "concepts": ["blood-pressure", "bmi", "cholesterol", "blood-glucose"],
        },
        "rule_request": "Schedule Follow-up Visit in 6 months for routine screening, earlier if abnormal values detected",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const encounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ encounter });
  
  const moment = imports.moment;
  const bloodPressure = encounter.getObservationReadableValue('blood-pressure');
  const cholesterol = encounter.getObservationReadableValue('cholesterol');
  const bloodGlucose = encounter.getObservationReadableValue('blood-glucose');
  
  let timeOffset;
  // Check for abnormal values
  if (bloodPressure > 140 || cholesterol > 200 || bloodGlucose > 126) {
    timeOffset = 1; // 1 month for abnormal values
  } else {
    timeOffset = 6; // 6 months for routine
  }
  
  const earliestDate = moment(encounter.encounterDateTime).add(timeOffset, 'months').toDate();
  const maxDate = moment(earliestDate).add(2, 'weeks').toDate();
  
  scheduleBuilder.add({
    name: "Follow-up Visit",
    encounterType: "Follow-up Visit",
    earliestDate,
    maxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 19,
        "scenario": "Emergency department follow-up",
        "context": {
            "formType": "Encounter",
            "encounterType": "Emergency Care",
            "encounterTypes": [
                {"name": "Emergency Care"},
                {"name": "ED Follow-up"},
                {"name": "Primary Care Handover"},
            ],
            "concepts": [
                "discharge-diagnosis",
                "follow-up-needed",
                "medication-changes",
                "red-flags",
            ],
        },
        "rule_request": "Schedule ED Follow-up in 72 hours if discharged with ongoing concerns, otherwise Primary Care Handover in 1 week",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const encounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ encounter });
  
  const moment = imports.moment;
  const followupNeeded = encounter.getObservationReadableValue('follow-up-needed');
  const redFlags = encounter.getObservationReadableValue('red-flags');
  
  let encounterType, timeOffset, timeUnit;
  if (followupNeeded === 'Yes' || redFlags === 'Present') {
    encounterType = "ED Follow-up";
    timeOffset = 72;
    timeUnit = 'hours';
  } else {
    encounterType = "Primary Care Handover";
    timeOffset = 1;
    timeUnit = 'week';
  }
  
  const earliestDate = moment(encounter.encounterDateTime).add(timeOffset, timeUnit).toDate();
  const maxDate = moment(earliestDate).add(1, 'day').toDate();
  
  scheduleBuilder.add({
    name: encounterType,
    encounterType: encounterType,
    earliestDate,
    maxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 20,
        "scenario": "Outpatient procedure follow-up",
        "context": {
            "formType": "Encounter",
            "encounterType": "Minor Procedure",
            "encounterTypes": [
                {"name": "Minor Procedure"},
                {"name": "Wound Check"},
                {"name": "Suture Removal"},
            ],
            "concepts": [
                "procedure-type",
                "wound-healing",
                "complications",
                "pain-level",
            ],
        },
        "rule_request": "Schedule Wound Check in 3 days, then Suture Removal in 7-10 days depending on procedure type",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const encounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ encounter });
  
  const moment = imports.moment;
  const procedureType = encounter.getObservationReadableValue('procedure-type');
  
  // Schedule Wound Check first
  const woundCheckDate = moment(encounter.encounterDateTime).add(3, 'days').toDate();
  const woundCheckMaxDate = moment(woundCheckDate).add(1, 'day').toDate();
  
  scheduleBuilder.add({
    name: "Wound Check",
    encounterType: "Wound Check",
    earliestDate: woundCheckDate,
    maxDate: woundCheckMaxDate
  });
  
  // Schedule Suture Removal based on procedure type
  let sutureRemovalDays;
  if (procedureType === 'Face' || procedureType === 'Cosmetic') {
    sutureRemovalDays = 7;
  } else if (procedureType === 'Joint' || procedureType === 'High Tension') {
    sutureRemovalDays = 10;
  } else {
    sutureRemovalDays = 7; // Default
  }
  
  const sutureRemovalDate = moment(encounter.encounterDateTime).add(sutureRemovalDays, 'days').toDate();
  const sutureRemovalMaxDate = moment(sutureRemovalDate).add(2, 'days').toDate();
  
  scheduleBuilder.add({
    name: "Suture Removal",
    encounterType: "Suture Removal",
    earliestDate: sutureRemovalDate,
    maxDate: sutureRemovalMaxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 21,
        "scenario": "Medication review scheduling",
        "context": {
            "formType": "Encounter",
            "encounterType": "Medication Review",
            "encounterTypes": [
                {"name": "Medication Review"},
                {"name": "Pharmacy Consultation"},
                {"name": "Drug Interaction Check"},
            ],
            "concepts": [
                "medication-count",
                "side-effects",
                "drug-interactions",
                "adherence-issues",
            ],
        },
        "rule_request": "Schedule Pharmacy Consultation in 2 weeks if multiple medications or interactions, otherwise review in 3 months",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const encounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ encounter });
  
  const moment = imports.moment;
  const medicationCount = encounter.getObservationReadableValue('medication-count');
  const drugInteractions = encounter.getObservationReadableValue('drug-interactions');
  
  let encounterType, timeOffset, timeUnit;
  if (medicationCount > 5 || drugInteractions === 'Yes') {
    encounterType = "Pharmacy Consultation";
    timeOffset = 2;
    timeUnit = 'weeks';
  } else {
    encounterType = "Medication Review";
    timeOffset = 3;
    timeUnit = 'months';
  }
  
  const earliestDate = moment(encounter.encounterDateTime).add(timeOffset, timeUnit).toDate();
  const maxDate = moment(earliestDate).add(1, 'week').toDate();
  
  scheduleBuilder.add({
    name: encounterType,
    encounterType: encounterType,
    earliestDate,
    maxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 22,
        "scenario": "Diagnostic test result review",
        "context": {
            "formType": "Encounter",
            "encounterType": "Test Results",
            "encounterTypes": [
                {"name": "Test Results"},
                {"name": "Results Discussion"},
                {"name": "Further Testing"},
            ],
            "concepts": [
                "test-type",
                "abnormal-results",
                "urgent-action-needed",
                "patient-anxiety",
            ],
        },
        "rule_request": "Schedule Results Discussion within 48 hours if abnormal results, otherwise routine appointment in 1 week",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const encounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ encounter });
  
  const moment = imports.moment;
  const abnormalResults = encounter.getObservationReadableValue('abnormal-results');
  const urgentActionNeeded = encounter.getObservationReadableValue('urgent-action-needed');
  
  let encounterType, timeOffset, timeUnit;
  if (abnormalResults === 'Yes' || urgentActionNeeded === 'Yes') {
    encounterType = "Results Discussion";
    timeOffset = 48;
    timeUnit = 'hours';
  } else {
    encounterType = "Results Discussion";
    timeOffset = 1;
    timeUnit = 'week';
  }
  
  const earliestDate = moment(encounter.encounterDateTime).add(timeOffset, timeUnit).toDate();
  const maxDate = moment(earliestDate).add(1, 'day').toDate();
  
  scheduleBuilder.add({
    name: encounterType,
    encounterType: encounterType,
    earliestDate,
    maxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 23,
        "scenario": "Vaccination follow-up scheduling",
        "context": {
            "formType": "Encounter",
            "encounterType": "Vaccination",
            "encounterTypes": [
                {"name": "Vaccination"},
                {"name": "Vaccine Follow-up"},
                {"name": "Adverse Reaction Review"},
            ],
            "concepts": [
                "vaccine-type",
                "adverse-reactions",
                "series-completion",
                "next-dose-due",
            ],
        },
        "rule_request": "Schedule Adverse Reaction Review in 24 hours if reactions reported, otherwise next dose as per schedule",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const encounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ encounter });
  
  const moment = imports.moment;
  const adverseReactions = encounter.getObservationReadableValue('adverse-reactions');
  const nextDoseDue = encounter.getObservationReadableValue('next-dose-due');
  
  if (adverseReactions === 'Yes' || adverseReactions === 'Severe') {
    const earliestDate = moment(encounter.encounterDateTime).add(24, 'hours').toDate();
    const maxDate = moment(earliestDate).add(4, 'hours').toDate();
    
    scheduleBuilder.add({
      name: "Adverse Reaction Review",
      encounterType: "Adverse Reaction Review",
      earliestDate,
      maxDate
    });
  } else if (nextDoseDue) {
    const nextDoseDate = moment(nextDoseDue).toDate();
    const maxDate = moment(nextDoseDate).add(7, 'days').toDate();
    
    scheduleBuilder.add({
      name: "Vaccination",
      encounterType: "Vaccination",
      earliestDate: nextDoseDate,
      maxDate
    });
  }
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 24,
        "scenario": "Physical therapy assessment",
        "context": {
            "formType": "Encounter",
            "encounterType": "PT Assessment",
            "encounterTypes": [
                {"name": "PT Assessment"},
                {"name": "PT Session"},
                {"name": "Home Exercise Review"},
            ],
            "concepts": [
                "mobility-assessment",
                "pain-level",
                "functional-goals",
                "exercise-compliance",
            ],
        },
        "rule_request": "Schedule PT Session twice weekly for 4 weeks, then Home Exercise Review monthly",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const encounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ encounter });
  
  const moment = imports.moment;
  
  // Schedule PT Sessions twice weekly for 4 weeks
  for (let week = 1; week <= 4; week++) {
    // First session of the week
    const firstSessionDate = moment(encounter.encounterDateTime).add(week * 7 - 5, 'days').toDate();
    const firstSessionMaxDate = moment(firstSessionDate).add(1, 'day').toDate();
    
    scheduleBuilder.add({
      name: `PT Session Week ${week} - 1`,
      encounterType: "PT Session",
      earliestDate: firstSessionDate,
      maxDate: firstSessionMaxDate
    });
    
    // Second session of the week
    const secondSessionDate = moment(encounter.encounterDateTime).add(week * 7 - 2, 'days').toDate();
    const secondSessionMaxDate = moment(secondSessionDate).add(1, 'day').toDate();
    
    scheduleBuilder.add({
      name: `PT Session Week ${week} - 2`,
      encounterType: "PT Session",
      earliestDate: secondSessionDate,
      maxDate: secondSessionMaxDate
    });
  }
  
  // Schedule monthly Home Exercise Review after 4 weeks
  const homeExerciseDate = moment(encounter.encounterDateTime).add(5, 'weeks').toDate();
  const homeExerciseMaxDate = moment(homeExerciseDate).add(1, 'week').toDate();
  
  scheduleBuilder.add({
    name: "Home Exercise Review",
    encounterType: "Home Exercise Review",
    earliestDate: homeExerciseDate,
    maxDate: homeExerciseMaxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 25,
        "scenario": "Specialist consultation scheduling",
        "context": {
            "formType": "Encounter",
            "encounterType": "Specialist Consult",
            "encounterTypes": [
                {"name": "Specialist Consult"},
                {"name": "Treatment Planning"},
                {"name": "Second Opinion"},
            ],
            "concepts": [
                "specialty-type",
                "urgency-level",
                "treatment-options",
                "patient-preference",
            ],
        },
        "rule_request": "Schedule Treatment Planning within 1 week if urgent specialty referral, otherwise in 4-6 weeks",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const encounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ encounter });
  
  const moment = imports.moment;
  const urgencyLevel = encounter.getObservationReadableValue('urgency-level');
  
  let timeOffset, timeUnit;
  if (urgencyLevel === 'Urgent' || urgencyLevel === 'High') {
    timeOffset = 1;
    timeUnit = 'week';
  } else {
    timeOffset = 5; // Middle of 4-6 weeks range
    timeUnit = 'weeks';
  }
  
  const earliestDate = moment(encounter.encounterDateTime).add(timeOffset, timeUnit).toDate();
  const maxDate = moment(earliestDate).add(1, 'week').toDate();
  
  scheduleBuilder.add({
    name: "Treatment Planning",
    encounterType: "Treatment Planning",
    earliestDate,
    maxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 26,
        "scenario": "Mental health crisis intervention",
        "context": {
            "formType": "Encounter",
            "encounterType": "Crisis Intervention",
            "encounterTypes": [
                {"name": "Crisis Intervention"},
                {"name": "Safety Planning"},
                {"name": "Psychiatric Evaluation"},
            ],
            "concepts": [
                "suicide-risk",
                "safety-plan",
                "support-system",
                "medication-compliance",
            ],
        },
        "rule_request": "Schedule Safety Planning within 24 hours if high suicide risk, Psychiatric Evaluation within 72 hours",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const encounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ encounter });
  
  const moment = imports.moment;
  const suicideRisk = encounter.getObservationReadableValue('suicide-risk');
  
  if (suicideRisk === 'High' || suicideRisk === 'Imminent') {
    // Schedule Safety Planning immediately
    const safetyPlanningDate = moment(encounter.encounterDateTime).add(24, 'hours').toDate();
    const safetyPlanningMaxDate = moment(safetyPlanningDate).add(2, 'hours').toDate();
    
    scheduleBuilder.add({
      name: "Safety Planning",
      encounterType: "Safety Planning",
      earliestDate: safetyPlanningDate,
      maxDate: safetyPlanningMaxDate
    });
  }
  
  // Always schedule psychiatric evaluation
  const psychiatricEvalDate = moment(encounter.encounterDateTime).add(72, 'hours').toDate();
  const psychiatricEvalMaxDate = moment(psychiatricEvalDate).add(12, 'hours').toDate();
  
  scheduleBuilder.add({
    name: "Psychiatric Evaluation",
    encounterType: "Psychiatric Evaluation",
    earliestDate: psychiatricEvalDate,
    maxDate: psychiatricEvalMaxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 27,
        "scenario": "Nutritional counseling follow-up",
        "context": {
            "formType": "Encounter",
            "encounterType": "Nutrition Counseling",
            "encounterTypes": [
                {"name": "Nutrition Counseling"},
                {"name": "Dietary Review"},
                {"name": "Weight Management"},
            ],
            "concepts": [
                "dietary-goals",
                "weight-change",
                "nutritional-deficits",
                "eating-habits",
            ],
        },
        "rule_request": "Schedule Dietary Review in 2 weeks for weight loss goals, monthly for maintenance",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const encounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ encounter });
  
  const moment = imports.moment;
  const dietaryGoals = encounter.getObservationReadableValue('dietary-goals');
  
  let timeOffset, timeUnit;
  if (dietaryGoals === 'Weight Loss' || dietaryGoals === 'Active Weight Management') {
    timeOffset = 2;
    timeUnit = 'weeks';
  } else {
    timeOffset = 1;
    timeUnit = 'month';
  }
  
  const earliestDate = moment(encounter.encounterDateTime).add(timeOffset, timeUnit).toDate();
  const maxDate = moment(earliestDate).add(1, 'week').toDate();
  
  scheduleBuilder.add({
    name: "Dietary Review",
    encounterType: "Dietary Review",
    earliestDate,
    maxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 28,
        "scenario": "Sleep study follow-up",
        "context": {
            "formType": "Encounter",
            "encounterType": "Sleep Assessment",
            "encounterTypes": [
                {"name": "Sleep Assessment"},
                {"name": "CPAP Titration"},
                {"name": "Sleep Hygiene Education"},
            ],
            "concepts": [
                "sleep-apnea-severity",
                "cpap-compliance",
                "sleep-quality",
                "daytime-sleepiness",
            ],
        },
        "rule_request": "Schedule CPAP Titration in 1 week if severe sleep apnea, otherwise Sleep Hygiene Education in 1 month",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const encounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ encounter });
  
  const moment = imports.moment;
  const sleepApneaSeverity = encounter.getObservationReadableValue('sleep-apnea-severity');
  
  let encounterType, timeOffset, timeUnit;
  if (sleepApneaSeverity === 'Severe' || sleepApneaSeverity === 'Critical') {
    encounterType = "CPAP Titration";
    timeOffset = 1;
    timeUnit = 'week';
  } else {
    encounterType = "Sleep Hygiene Education";
    timeOffset = 1;
    timeUnit = 'month';
  }
  
  const earliestDate = moment(encounter.encounterDateTime).add(timeOffset, timeUnit).toDate();
  const maxDate = moment(earliestDate).add(1, 'week').toDate();
  
  scheduleBuilder.add({
    name: encounterType,
    encounterType: encounterType,
    earliestDate,
    maxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 29,
        "scenario": "Allergy testing follow-up",
        "context": {
            "formType": "Encounter",
            "encounterType": "Allergy Testing",
            "encounterTypes": [
                {"name": "Allergy Testing"},
                {"name": "Allergy Management"},
                {"name": "Immunotherapy Follow-up"},
            ],
            "concepts": [
                "allergen-identification",
                "reaction-severity",
                "avoidance-strategies",
                "treatment-plan",
            ],
        },
        "rule_request": "Schedule Allergy Management in 1 week if severe reactions, Immunotherapy Follow-up monthly if on treatment",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const encounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ encounter });
  
  const moment = imports.moment;
  const reactionSeverity = encounter.getObservationReadableValue('reaction-severity');
  const treatmentPlan = encounter.getObservationReadableValue('treatment-plan');
  
  if (reactionSeverity === 'Severe' || reactionSeverity === 'Anaphylactic') {
    const earliestDate = moment(encounter.encounterDateTime).add(1, 'week').toDate();
    const maxDate = moment(earliestDate).add(2, 'days').toDate();
    
    scheduleBuilder.add({
      name: "Allergy Management",
      encounterType: "Allergy Management",
      earliestDate,
      maxDate
    });
  }
  
  if (treatmentPlan === 'Immunotherapy' || treatmentPlan === 'Ongoing Treatment') {
    const immunotherapyDate = moment(encounter.encounterDateTime).add(1, 'month').toDate();
    const immunotherapyMaxDate = moment(immunotherapyDate).add(1, 'week').toDate();
    
    scheduleBuilder.add({
      name: "Immunotherapy Follow-up",
      encounterType: "Immunotherapy Follow-up",
      earliestDate: immunotherapyDate,
      maxDate: immunotherapyMaxDate
    });
  }
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 30,
        "scenario": "Sports medicine injury follow-up",
        "context": {
            "formType": "Encounter",
            "encounterType": "Sports Injury",
            "encounterTypes": [
                {"name": "Sports Injury"},
                {"name": "Return to Play"},
                {"name": "Performance Assessment"},
            ],
            "concepts": [
                "injury-type",
                "recovery-progress",
                "functional-testing",
                "return-to-sport",
            ],
        },
        "rule_request": "Schedule Return to Play assessment when functional milestones met, Performance Assessment post-recovery",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const encounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ encounter });
  
  const moment = imports.moment;
  const recoveryProgress = encounter.getObservationReadableValue('recovery-progress');
  const functionalTesting = encounter.getObservationReadableValue('functional-testing');
  
  if (recoveryProgress === 'Good' && functionalTesting === 'Passed') {
    const returnToPlayDate = moment(encounter.encounterDateTime).add(1, 'week').toDate();
    const returnToPlayMaxDate = moment(returnToPlayDate).add(3, 'days').toDate();
    
    scheduleBuilder.add({
      name: "Return to Play",
      encounterType: "Return to Play",
      earliestDate: returnToPlayDate,
      maxDate: returnToPlayMaxDate
    });
    
    // Schedule Performance Assessment post-recovery (4 weeks later)
    const performanceAssessmentDate = moment(encounter.encounterDateTime).add(4, 'weeks').toDate();
    const performanceAssessmentMaxDate = moment(performanceAssessmentDate).add(1, 'week').toDate();
    
    scheduleBuilder.add({
      name: "Performance Assessment",
      encounterType: "Performance Assessment",
      earliestDate: performanceAssessmentDate,
      maxDate: performanceAssessmentMaxDate
    });
  }
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 31,
        "scenario": "Wound clinic follow-up",
        "context": {
            "formType": "Encounter",
            "encounterType": "Wound Clinic",
            "encounterTypes": [
                {"name": "Wound Clinic"},
                {"name": "Dressing Change"},
                {"name": "Wound Debridement"},
            ],
            "concepts": [
                "wound-type",
                "healing-rate",
                "infection-signs",
                "treatment-response",
            ],
        },
        "rule_request": "Schedule Dressing Change every 2-3 days for acute wounds, weekly for chronic wounds",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const encounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ encounter });
  
  const moment = imports.moment;
  const woundType = encounter.getObservationReadableValue('wound-type');
  
  let dayInterval;
  if (woundType === 'Acute' || woundType === 'Surgical') {
    dayInterval = 3; // Every 2-3 days for acute wounds
  } else {
    dayInterval = 7; // Weekly for chronic wounds
  }
  
  // Schedule multiple dressing changes
  for (let i = 1; i <= 4; i++) {
    const dressingDate = moment(encounter.encounterDateTime).add(i * dayInterval, 'days').toDate();
    const dressingMaxDate = moment(dressingDate).add(1, 'day').toDate();
    
    scheduleBuilder.add({
      name: `Dressing Change ${i}`,
      encounterType: "Dressing Change",
      earliestDate: dressingDate,
      maxDate: dressingMaxDate
    });
  }
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 32,
        "scenario": "Pain management follow-up",
        "context": {
            "formType": "Encounter",
            "encounterType": "Pain Management",
            "encounterTypes": [
                {"name": "Pain Management"},
                {"name": "Medication Adjustment"},
                {"name": "Pain Psychology"},
            ],
            "concepts": [
                "pain-score",
                "functional-improvement",
                "medication-effectiveness",
                "side-effects",
            ],
        },
        "rule_request": "Schedule Medication Adjustment in 1 week if inadequate pain control, Pain Psychology if chronic pain",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const encounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ encounter });
  
  const moment = imports.moment;
  const painScore = encounter.getObservationReadableValue('pain-score');
  const medicationEffectiveness = encounter.getObservationReadableValue('medication-effectiveness');
  const painDuration = encounter.getObservationReadableValue('pain-duration');
  
  if (painScore > 6 || medicationEffectiveness === 'Poor') {
    const medicationAdjustmentDate = moment(encounter.encounterDateTime).add(1, 'week').toDate();
    const medicationAdjustmentMaxDate = moment(medicationAdjustmentDate).add(2, 'days').toDate();
    
    scheduleBuilder.add({
      name: "Medication Adjustment",
      encounterType: "Medication Adjustment",
      earliestDate: medicationAdjustmentDate,
      maxDate: medicationAdjustmentMaxDate
    });
  }
  
  if (painDuration > 90) { // Chronic pain (>3 months)
    const painPsychologyDate = moment(encounter.encounterDateTime).add(2, 'weeks').toDate();
    const painPsychologyMaxDate = moment(painPsychologyDate).add(1, 'week').toDate();
    
    scheduleBuilder.add({
      name: "Pain Psychology",
      encounterType: "Pain Psychology",
      earliestDate: painPsychologyDate,
      maxDate: painPsychologyMaxDate
    });
  }
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 33,
        "scenario": "Telehealth follow-up scheduling",
        "context": {
            "formType": "Encounter",
            "encounterType": "Telehealth",
            "encounterTypes": [
                {"name": "Telehealth"},
                {"name": "Virtual Follow-up"},
                {"name": "In-Person Required"},
            ],
            "concepts": [
                "technology-access",
                "clinical-stability",
                "examination-needs",
                "patient-preference",
            ],
        },
        "rule_request": "Schedule Virtual Follow-up in 1 week if stable, In-Person Required if examination needed",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const encounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ encounter });
  
  const moment = imports.moment;
  const clinicalStability = encounter.getObservationReadableValue('clinical-stability');
  const examinationNeeds = encounter.getObservationReadableValue('examination-needs');
  
  let encounterType, timeOffset;
  if (clinicalStability === 'Stable' && examinationNeeds === 'No') {
    encounterType = "Virtual Follow-up";
    timeOffset = 1;
  } else {
    encounterType = "In-Person Required";
    timeOffset = 3; // Sooner for in-person needs
  }
  
  const earliestDate = moment(encounter.encounterDateTime).add(timeOffset, 'weeks').toDate();
  const maxDate = moment(earliestDate).add(3, 'days').toDate();
  
  scheduleBuilder.add({
    name: encounterType,
    encounterType: encounterType,
    earliestDate,
    maxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 34,
        "scenario": "Pre-operative assessment",
        "context": {
            "formType": "Encounter",
            "encounterType": "Pre-Op Assessment",
            "encounterTypes": [
                {"name": "Pre-Op Assessment"},
                {"name": "Surgical Clearance"},
                {"name": "Anesthesia Consult"},
            ],
            "concepts": [
                "surgical-risk",
                "medical-optimization",
                "anesthesia-type",
                "post-op-planning",
            ],
        },
        "rule_request": "Schedule Anesthesia Consult within 1 week of surgery, Surgical Clearance when medically optimized",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const encounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ encounter });
  
  const moment = imports.moment;
  const surgeryDate = encounter.getObservationReadableValue('surgery-date');
  const medicalOptimization = encounter.getObservationReadableValue('medical-optimization');
  
  if (surgeryDate) {
    // Schedule Anesthesia Consult 1 week before surgery
    const anesthesiaConsultDate = moment(surgeryDate).subtract(1, 'week').toDate();
    const anesthesiaConsultMaxDate = moment(anesthesiaConsultDate).add(2, 'days').toDate();
    
    scheduleBuilder.add({
      name: "Anesthesia Consult",
      encounterType: "Anesthesia Consult",
      earliestDate: anesthesiaConsultDate,
      maxDate: anesthesiaConsultMaxDate
    });
  }
  
  if (medicalOptimization === 'Complete' || medicalOptimization === 'Optimized') {
    const surgicalClearanceDate = moment(encounter.encounterDateTime).add(3, 'days').toDate();
    const surgicalClearanceMaxDate = moment(surgicalClearanceDate).add(2, 'days').toDate();
    
    scheduleBuilder.add({
      name: "Surgical Clearance",
      encounterType: "Surgical Clearance",
      earliestDate: surgicalClearanceDate,
      maxDate: surgicalClearanceMaxDate
    });
  }
  
  return scheduleBuilder.getAll();
};
""",
    },
    # ============== PROGRAM ENROLMENT EXAMPLES (17) ==============
    {
        "id": 35,
        "scenario": "Maternal health program enrollment",
        "context": {
            "formType": "ProgramEnrolment",
            "encounterType": "Pregnancy Registration",
            "encounterTypes": [
                {"name": "First ANC", "program": "Maternal Health"},
                {"name": "Risk Assessment", "program": "Maternal Health"},
                {"name": "Baseline Tests", "program": "Maternal Health"},
            ],
            "concepts": [
                "lmp-date",
                "edd-date",
                "gravida",
                "parity",
                "high-risk-factors",
            ],
        },
        "rule_request": "Schedule First ANC within 2 weeks of enrollment, Risk Assessment immediately if high-risk factors",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEnrolment = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEnrolment });
  
  const moment = imports.moment;
  const highRiskFactors = programEnrolment.getObservationReadableValue('high-risk-factors');
  
  // Schedule First ANC within 2 weeks
  const firstANCDate = moment(programEnrolment.enrolmentDateTime).add(2, 'weeks').toDate();
  const firstANCMaxDate = moment(firstANCDate).add(1, 'week').toDate();
  
  scheduleBuilder.add({
    name: "First ANC",
    encounterType: "First ANC",
    earliestDate: firstANCDate,
    maxDate: firstANCMaxDate
  });
  
  // Schedule Risk Assessment immediately if high-risk
  if (highRiskFactors === 'Yes' || highRiskFactors === 'Multiple') {
    const riskAssessmentDate = moment(programEnrolment.enrolmentDateTime).add(2, 'days').toDate();
    const riskAssessmentMaxDate = moment(riskAssessmentDate).add(1, 'day').toDate();
    
    scheduleBuilder.add({
      name: "Risk Assessment",
      encounterType: "Risk Assessment",
      earliestDate: riskAssessmentDate,
      maxDate: riskAssessmentMaxDate
    });
  }
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 36,
        "scenario": "Child health program enrollment at birth",
        "context": {
            "formType": "ProgramEnrolment",
            "encounterType": "Child Registration",
            "encounterTypes": [
                {"name": "Newborn Assessment", "program": "Child Health"},
                {"name": "First Immunization", "program": "Child Health"},
                {"name": "Growth Monitoring", "program": "Child Health"},
            ],
            "concepts": [
                "birth-weight",
                "gestational-age",
                "birth-complications",
                "feeding-method",
            ],
        },
        "rule_request": "Schedule Newborn Assessment within 48 hours, First Immunization at 6 weeks, Growth Monitoring at 1 month",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEnrolment = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEnrolment });
  
  const moment = imports.moment;
  
  // Schedule Newborn Assessment within 48 hours
  const newbornAssessmentDate = moment(programEnrolment.enrolmentDateTime).add(48, 'hours').toDate();
  const newbornAssessmentMaxDate = moment(newbornAssessmentDate).add(12, 'hours').toDate();
  
  scheduleBuilder.add({
    name: "Newborn Assessment",
    encounterType: "Newborn Assessment",
    earliestDate: newbornAssessmentDate,
    maxDate: newbornAssessmentMaxDate
  });
  
  // Schedule First Immunization at 6 weeks
  const firstImmunizationDate = moment(programEnrolment.enrolmentDateTime).add(6, 'weeks').toDate();
  const firstImmunizationMaxDate = moment(firstImmunizationDate).add(1, 'week').toDate();
  
  scheduleBuilder.add({
    name: "First Immunization",
    encounterType: "First Immunization",
    earliestDate: firstImmunizationDate,
    maxDate: firstImmunizationMaxDate
  });
  
  // Schedule Growth Monitoring at 1 month
  const growthMonitoringDate = moment(programEnrolment.enrolmentDateTime).add(1, 'month').toDate();
  const growthMonitoringMaxDate = moment(growthMonitoringDate).add(1, 'week').toDate();
  
  scheduleBuilder.add({
    name: "Growth Monitoring",
    encounterType: "Growth Monitoring",
    earliestDate: growthMonitoringDate,
    maxDate: growthMonitoringMaxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 37,
        "scenario": "Diabetes management program enrollment",
        "context": {
            "formType": "ProgramEnrolment",
            "encounterType": "Diabetes Enrollment",
            "encounterTypes": [
                {"name": "Baseline Assessment", "program": "Diabetes Care"},
                {"name": "Diabetes Education", "program": "Diabetes Care"},
                {"name": "Medication Initiation", "program": "Diabetes Care"},
            ],
            "concepts": [
                "diabetes-type",
                "hba1c-baseline",
                "complications-present",
                "medication-history",
            ],
        },
        "rule_request": "Schedule Baseline Assessment within 1 week, Diabetes Education within 2 weeks, Medication Initiation based on assessment",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEnrolment = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEnrolment });
  
  const moment = imports.moment;
  
  // Schedule Baseline Assessment within 1 week
  const baselineAssessmentDate = moment(programEnrolment.enrolmentDateTime).add(1, 'week').toDate();
  const baselineAssessmentMaxDate = moment(baselineAssessmentDate).add(2, 'days').toDate();
  
  scheduleBuilder.add({
    name: "Baseline Assessment",
    encounterType: "Baseline Assessment",
    earliestDate: baselineAssessmentDate,
    maxDate: baselineAssessmentMaxDate
  });
  
  // Schedule Diabetes Education within 2 weeks
  const diabetesEducationDate = moment(programEnrolment.enrolmentDateTime).add(2, 'weeks').toDate();
  const diabetesEducationMaxDate = moment(diabetesEducationDate).add(3, 'days').toDate();
  
  scheduleBuilder.add({
    name: "Diabetes Education",
    encounterType: "Diabetes Education",
    earliestDate: diabetesEducationDate,
    maxDate: diabetesEducationMaxDate
  });
  
  // Schedule Medication Initiation (conditional based on baseline findings)
  const medicationInitiationDate = moment(programEnrolment.enrolmentDateTime).add(10, 'days').toDate();
  const medicationInitiationMaxDate = moment(medicationInitiationDate).add(3, 'days').toDate();
  
  scheduleBuilder.add({
    name: "Medication Initiation",
    encounterType: "Medication Initiation",
    earliestDate: medicationInitiationDate,
    maxDate: medicationInitiationMaxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 38,
        "scenario": "Hypertension management program",
        "context": {
            "formType": "ProgramEnrolment",
            "encounterType": "HTN Enrollment",
            "encounterTypes": [
                {"name": "BP Monitoring Setup", "program": "Hypertension Care"},
                {"name": "Lifestyle Counseling", "program": "Hypertension Care"},
                {"name": "Medication Review", "program": "Hypertension Care"},
            ],
            "concepts": [
                "baseline-bp",
                "cardiovascular-risk",
                "target-bp",
                "lifestyle-factors",
            ],
        },
        "rule_request": "Schedule BP Monitoring Setup immediately, Lifestyle Counseling within 1 week, Medication Review if BP not controlled",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEnrolment = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEnrolment });
  
  const moment = imports.moment;
  const baselineBP = programEnrolment.getObservationReadableValue('baseline-bp');
  
  // Schedule BP Monitoring Setup immediately
  const bpMonitoringSetupDate = moment(programEnrolment.enrolmentDateTime).add(1, 'day').toDate();
  const bpMonitoringSetupMaxDate = moment(bpMonitoringSetupDate).add(1, 'day').toDate();
  
  scheduleBuilder.add({
    name: "BP Monitoring Setup",
    encounterType: "BP Monitoring Setup",
    earliestDate: bpMonitoringSetupDate,
    maxDate: bpMonitoringSetupMaxDate
  });
  
  // Schedule Lifestyle Counseling within 1 week
  const lifestyleCounselingDate = moment(programEnrolment.enrolmentDateTime).add(1, 'week').toDate();
  const lifestyleCounselingMaxDate = moment(lifestyleCounselingDate).add(2, 'days').toDate();
  
  scheduleBuilder.add({
    name: "Lifestyle Counseling",
    encounterType: "Lifestyle Counseling",
    earliestDate: lifestyleCounselingDate,
    maxDate: lifestyleCounselingMaxDate
  });
  
  // Schedule Medication Review if BP not controlled
  if (baselineBP >= 140) {
    const medicationReviewDate = moment(programEnrolment.enrolmentDateTime).add(2, 'weeks').toDate();
    const medicationReviewMaxDate = moment(medicationReviewDate).add(3, 'days').toDate();
    
    scheduleBuilder.add({
      name: "Medication Review",
      encounterType: "Medication Review",
      earliestDate: medicationReviewDate,
      maxDate: medicationReviewMaxDate
    });
  }
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 39,
        "scenario": "TB treatment program enrollment",
        "context": {
            "formType": "ProgramEnrolment",
            "encounterType": "TB Program Entry",
            "encounterTypes": [
                {"name": "Treatment Initiation", "program": "TB Program"},
                {"name": "Contact Tracing", "program": "TB Program"},
                {"name": "Baseline Tests", "program": "TB Program"},
            ],
            "concepts": [
                "tb-type",
                "drug-susceptibility",
                "hiv-status",
                "contact-details",
            ],
        },
        "rule_request": "Schedule Treatment Initiation immediately after enrollment, Contact Tracing within 48 hours, Baseline Tests within 1 week",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEnrolment = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEnrolment });
  
  const moment = imports.moment;
  
  // Schedule Treatment Initiation immediately
  const treatmentInitiationDate = moment(programEnrolment.enrolmentDateTime).add(1, 'day').toDate();
  const treatmentInitiationMaxDate = moment(treatmentInitiationDate).add(6, 'hours').toDate();
  
  scheduleBuilder.add({
    name: "Treatment Initiation",
    encounterType: "Treatment Initiation",
    earliestDate: treatmentInitiationDate,
    maxDate: treatmentInitiationMaxDate
  });
  
  // Schedule Contact Tracing within 48 hours
  const contactTracingDate = moment(programEnrolment.enrolmentDateTime).add(48, 'hours').toDate();
  const contactTracingMaxDate = moment(contactTracingDate).add(12, 'hours').toDate();
  
  scheduleBuilder.add({
    name: "Contact Tracing",
    encounterType: "Contact Tracing",
    earliestDate: contactTracingDate,
    maxDate: contactTracingMaxDate
  });
  
  // Schedule Baseline Tests within 1 week
  const baselineTestsDate = moment(programEnrolment.enrolmentDateTime).add(1, 'week').toDate();
  const baselineTestsMaxDate = moment(baselineTestsDate).add(2, 'days').toDate();
  
  scheduleBuilder.add({
    name: "Baseline Tests",
    encounterType: "Baseline Tests",
    earliestDate: baselineTestsDate,
    maxDate: baselineTestsMaxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 40,
        "scenario": "Mental health program enrollment",
        "context": {
            "formType": "ProgramEnrolment",
            "encounterType": "Mental Health Intake",
            "encounterTypes": [
                {"name": "Psychiatric Assessment", "program": "Mental Health"},
                {"name": "Treatment Planning", "program": "Mental Health"},
                {"name": "Crisis Plan", "program": "Mental Health"},
            ],
            "concepts": [
                "presenting-symptoms",
                "suicide-risk",
                "substance-use",
                "social-support",
            ],
        },
        "rule_request": "Schedule Psychiatric Assessment within 72 hours if high risk, otherwise within 2 weeks, Crisis Plan if suicide risk",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEnrolment = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEnrolment });
  
  const moment = imports.moment;
  const suicideRisk = programEnrolment.getObservationReadableValue('suicide-risk');
  const presentingSymptoms = programEnrolment.getObservationReadableValue('presenting-symptoms');
  
  // Schedule Psychiatric Assessment based on risk level
  let psychiatricAssessmentDate, psychiatricAssessmentMaxDate;
  if (suicideRisk === 'High' || presentingSymptoms === 'Severe') {
    psychiatricAssessmentDate = moment(programEnrolment.enrolmentDateTime).add(72, 'hours').toDate();
    psychiatricAssessmentMaxDate = moment(psychiatricAssessmentDate).add(6, 'hours').toDate();
  } else {
    psychiatricAssessmentDate = moment(programEnrolment.enrolmentDateTime).add(2, 'weeks').toDate();
    psychiatricAssessmentMaxDate = moment(psychiatricAssessmentDate).add(2, 'days').toDate();
  }
  
  scheduleBuilder.add({
    name: "Psychiatric Assessment",
    encounterType: "Psychiatric Assessment",
    earliestDate: psychiatricAssessmentDate,
    maxDate: psychiatricAssessmentMaxDate
  });
  
  // Schedule Crisis Plan if suicide risk present
  if (suicideRisk === 'High' || suicideRisk === 'Medium') {
    const crisisPlanDate = moment(programEnrolment.enrolmentDateTime).add(24, 'hours').toDate();
    const crisisPlanMaxDate = moment(crisisPlanDate).add(4, 'hours').toDate();
    
    scheduleBuilder.add({
      name: "Crisis Plan",
      encounterType: "Crisis Plan",
      earliestDate: crisisPlanDate,
      maxDate: crisisPlanMaxDate
    });
  }
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 41,
        "scenario": "Cancer care program enrollment",
        "context": {
            "formType": "ProgramEnrolment",
            "encounterType": "Oncology Intake",
            "encounterTypes": [
                {"name": "Staging Assessment", "program": "Cancer Care"},
                {"name": "Treatment Planning", "program": "Cancer Care"},
                {"name": "Palliative Consult", "program": "Cancer Care"},
            ],
            "concepts": [
                "cancer-type",
                "cancer-stage",
                "performance-status",
                "treatment-goals",
            ],
        },
        "rule_request": "Schedule Staging Assessment within 1 week, Treatment Planning within 2 weeks, Palliative Consult if advanced stage",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEnrolment = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEnrolment });
  
  const moment = imports.moment;
  const cancerStage = programEnrolment.getObservationReadableValue('cancer-stage');
  
  // Schedule Staging Assessment within 1 week
  const stagingAssessmentDate = moment(programEnrolment.enrolmentDateTime).add(1, 'week').toDate();
  const stagingAssessmentMaxDate = moment(stagingAssessmentDate).add(2, 'days').toDate();
  
  scheduleBuilder.add({
    name: "Staging Assessment",
    encounterType: "Staging Assessment",
    earliestDate: stagingAssessmentDate,
    maxDate: stagingAssessmentMaxDate
  });
  
  // Schedule Treatment Planning within 2 weeks
  const treatmentPlanningDate = moment(programEnrolment.enrolmentDateTime).add(2, 'weeks').toDate();
  const treatmentPlanningMaxDate = moment(treatmentPlanningDate).add(3, 'days').toDate();
  
  scheduleBuilder.add({
    name: "Treatment Planning",
    encounterType: "Treatment Planning",
    earliestDate: treatmentPlanningDate,
    maxDate: treatmentPlanningMaxDate
  });
  
  // Schedule Palliative Consult if advanced stage
  if (cancerStage === 'Stage IV' || cancerStage === 'Advanced' || cancerStage === 'Metastatic') {
    const palliativeConsultDate = moment(programEnrolment.enrolmentDateTime).add(1, 'week').toDate();
    const palliativeConsultMaxDate = moment(palliativeConsultDate).add(2, 'days').toDate();
    
    scheduleBuilder.add({
      name: "Palliative Consult",
      encounterType: "Palliative Consult",
      earliestDate: palliativeConsultDate,
      maxDate: palliativeConsultMaxDate
    });
  }
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 42,
        "scenario": "Addiction treatment program",
        "context": {
            "formType": "ProgramEnrolment",
            "encounterType": "Addiction Intake",
            "encounterTypes": [
                {"name": "Detox Assessment", "program": "Addiction Treatment"},
                {"name": "Treatment Plan", "program": "Addiction Treatment"},
                {"name": "Family Meeting", "program": "Addiction Treatment"},
            ],
            "concepts": [
                "substance-type",
                "addiction-severity",
                "withdrawal-risk",
                "motivation-level",
            ],
        },
        "rule_request": "Schedule Detox Assessment immediately if withdrawal risk, Treatment Plan within 48 hours, Family Meeting within 1 week",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEnrolment = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEnrolment });
  
  const moment = imports.moment;
  const withdrawalRisk = programEnrolment.getObservationReadableValue('withdrawal-risk');
  
  // Schedule Detox Assessment immediately if withdrawal risk
  if (withdrawalRisk === 'High' || withdrawalRisk === 'Severe') {
    const detoxAssessmentDate = moment(programEnrolment.enrolmentDateTime).add(6, 'hours').toDate();
    const detoxAssessmentMaxDate = moment(detoxAssessmentDate).add(2, 'hours').toDate();
    
    scheduleBuilder.add({
      name: "Detox Assessment",
      encounterType: "Detox Assessment",
      earliestDate: detoxAssessmentDate,
      maxDate: detoxAssessmentMaxDate
    });
  }
  
  // Schedule Treatment Plan within 48 hours
  const treatmentPlanDate = moment(programEnrolment.enrolmentDateTime).add(48, 'hours').toDate();
  const treatmentPlanMaxDate = moment(treatmentPlanDate).add(6, 'hours').toDate();
  
  scheduleBuilder.add({
    name: "Treatment Plan",
    encounterType: "Treatment Plan",
    earliestDate: treatmentPlanDate,
    maxDate: treatmentPlanMaxDate
  });
  
  // Schedule Family Meeting within 1 week
  const familyMeetingDate = moment(programEnrolment.enrolmentDateTime).add(1, 'week').toDate();
  const familyMeetingMaxDate = moment(familyMeetingDate).add(2, 'days').toDate();
  
  scheduleBuilder.add({
    name: "Family Meeting",
    encounterType: "Family Meeting",
    earliestDate: familyMeetingDate,
    maxDate: familyMeetingMaxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 43,
        "scenario": "Chronic kidney disease program",
        "context": {
            "formType": "ProgramEnrolment",
            "encounterType": "CKD Enrollment",
            "encounterTypes": [
                {"name": "Nephrology Consult", "program": "CKD Care"},
                {"name": "Education Session", "program": "CKD Care"},
                {"name": "Preparation Planning", "program": "CKD Care"},
            ],
            "concepts": ["ckd-stage", "gfr-level", "proteinuria", "progression-risk"],
        },
        "rule_request": "Schedule Nephrology Consult within 1 month, Education Session within 2 weeks, Preparation Planning if stage 4-5",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEnrolment = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEnrolment });
  
  const moment = imports.moment;
  const ckdStage = programEnrolment.getObservationReadableValue('ckd-stage');
  
  // Schedule Nephrology Consult within 1 month
  const nephrologyConsultDate = moment(programEnrolment.enrolmentDateTime).add(1, 'month').toDate();
  const nephrologyConsultMaxDate = moment(nephrologyConsultDate).add(1, 'week').toDate();
  
  scheduleBuilder.add({
    name: "Nephrology Consult",
    encounterType: "Nephrology Consult",
    earliestDate: nephrologyConsultDate,
    maxDate: nephrologyConsultMaxDate
  });
  
  // Schedule Education Session within 2 weeks
  const educationSessionDate = moment(programEnrolment.enrolmentDateTime).add(2, 'weeks').toDate();
  const educationSessionMaxDate = moment(educationSessionDate).add(3, 'days').toDate();
  
  scheduleBuilder.add({
    name: "Education Session",
    encounterType: "Education Session",
    earliestDate: educationSessionDate,
    maxDate: educationSessionMaxDate
  });
  
  // Schedule Preparation Planning if stage 4-5
  if (ckdStage === 'Stage 4' || ckdStage === 'Stage 5') {
    const preparationPlanningDate = moment(programEnrolment.enrolmentDateTime).add(3, 'weeks').toDate();
    const preparationPlanningMaxDate = moment(preparationPlanningDate).add(1, 'week').toDate();
    
    scheduleBuilder.add({
      name: "Preparation Planning",
      encounterType: "Preparation Planning",
      earliestDate: preparationPlanningDate,
      maxDate: preparationPlanningMaxDate
    });
  }
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 44,
        "scenario": "Heart failure management program",
        "context": {
            "formType": "ProgramEnrolment",
            "encounterType": "Heart Failure Intake",
            "encounterTypes": [
                {"name": "Cardiology Consult", "program": "Heart Failure"},
                {"name": "Medication Optimization", "program": "Heart Failure"},
                {"name": "Device Assessment", "program": "Heart Failure"},
            ],
            "concepts": [
                "ejection-fraction",
                "nyha-class",
                "medication-tolerance",
                "device-eligibility",
            ],
        },
        "rule_request": "Schedule Cardiology Consult within 1 week, Medication Optimization within 2 weeks, Device Assessment if indicated",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEnrolment = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEnrolment });
  
  const moment = imports.moment;
  const ejectionFraction = programEnrolment.getObservationReadableValue('ejection-fraction');
  const deviceEligibility = programEnrolment.getObservationReadableValue('device-eligibility');
  
  // Schedule Cardiology Consult within 1 week
  const cardiologyConsultDate = moment(programEnrolment.enrolmentDateTime).add(1, 'week').toDate();
  const cardiologyConsultMaxDate = moment(cardiologyConsultDate).add(2, 'days').toDate();
  
  scheduleBuilder.add({
    name: "Cardiology Consult",
    encounterType: "Cardiology Consult",
    earliestDate: cardiologyConsultDate,
    maxDate: cardiologyConsultMaxDate
  });
  
  // Schedule Medication Optimization within 2 weeks
  const medicationOptimizationDate = moment(programEnrolment.enrolmentDateTime).add(2, 'weeks').toDate();
  const medicationOptimizationMaxDate = moment(medicationOptimizationDate).add(3, 'days').toDate();
  
  scheduleBuilder.add({
    name: "Medication Optimization",
    encounterType: "Medication Optimization",
    earliestDate: medicationOptimizationDate,
    maxDate: medicationOptimizationMaxDate
  });
  
  // Schedule Device Assessment if indicated
  if (ejectionFraction < 35 || deviceEligibility === 'Yes') {
    const deviceAssessmentDate = moment(programEnrolment.enrolmentDateTime).add(3, 'weeks').toDate();
    const deviceAssessmentMaxDate = moment(deviceAssessmentDate).add(1, 'week').toDate();
    
    scheduleBuilder.add({
      name: "Device Assessment",
      encounterType: "Device Assessment",
      earliestDate: deviceAssessmentDate,
      maxDate: deviceAssessmentMaxDate
    });
  }
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 45,
        "scenario": "Stroke rehabilitation program",
        "context": {
            "formType": "ProgramEnrolment",
            "encounterType": "Stroke Rehab Intake",
            "encounterTypes": [
                {"name": "Rehab Assessment", "program": "Stroke Rehab"},
                {"name": "Therapy Initiation", "program": "Stroke Rehab"},
                {"name": "Caregiver Training", "program": "Stroke Rehab"},
            ],
            "concepts": [
                "stroke-severity",
                "functional-deficits",
                "rehabilitation-potential",
                "caregiver-availability",
            ],
        },
        "rule_request": "Schedule Rehab Assessment within 3 days of stroke, Therapy Initiation within 1 week, Caregiver Training as needed",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEnrolment = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEnrolment });
  
  const moment = imports.moment;
  const caregiverAvailability = programEnrolment.getObservationReadableValue('caregiver-availability');
  
  // Schedule Rehab Assessment within 3 days of stroke
  const rehabAssessmentDate = moment(programEnrolment.enrolmentDateTime).add(3, 'days').toDate();
  const rehabAssessmentMaxDate = moment(rehabAssessmentDate).add(1, 'day').toDate();
  
  scheduleBuilder.add({
    name: "Rehab Assessment",
    encounterType: "Rehab Assessment",
    earliestDate: rehabAssessmentDate,
    maxDate: rehabAssessmentMaxDate
  });
  
  // Schedule Therapy Initiation within 1 week
  const therapyInitiationDate = moment(programEnrolment.enrolmentDateTime).add(1, 'week').toDate();
  const therapyInitiationMaxDate = moment(therapyInitiationDate).add(2, 'days').toDate();
  
  scheduleBuilder.add({
    name: "Therapy Initiation",
    encounterType: "Therapy Initiation",
    earliestDate: therapyInitiationDate,
    maxDate: therapyInitiationMaxDate
  });
  
  // Schedule Caregiver Training as needed
  if (caregiverAvailability === 'Yes' || caregiverAvailability === 'Available') {
    const caregiverTrainingDate = moment(programEnrolment.enrolmentDateTime).add(1, 'week').toDate();
    const caregiverTrainingMaxDate = moment(caregiverTrainingDate).add(3, 'days').toDate();
    
    scheduleBuilder.add({
      name: "Caregiver Training",
      encounterType: "Caregiver Training",
      earliestDate: caregiverTrainingDate,
      maxDate: caregiverTrainingMaxDate
    });
  }
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 46,
        "scenario": "Asthma management program",
        "context": {
            "formType": "ProgramEnrolment",
            "encounterType": "Asthma Enrollment",
            "encounterTypes": [
                {"name": "Pulmonary Function", "program": "Asthma Care"},
                {"name": "Trigger Assessment", "program": "Asthma Care"},
                {"name": "Inhaler Training", "program": "Asthma Care"},
            ],
            "concepts": [
                "asthma-severity",
                "trigger-identification",
                "medication-history",
                "control-status",
            ],
        },
        "rule_request": "Schedule Pulmonary Function within 1 week, Trigger Assessment within 2 weeks, Inhaler Training immediately",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEnrolment = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEnrolment });
  
  const moment = imports.moment;
  
  // Schedule Pulmonary Function within 1 week
  const pulmonaryFunctionDate = moment(programEnrolment.enrolmentDateTime).add(1, 'week').toDate();
  const pulmonaryFunctionMaxDate = moment(pulmonaryFunctionDate).add(2, 'days').toDate();
  
  scheduleBuilder.add({
    name: "Pulmonary Function",
    encounterType: "Pulmonary Function",
    earliestDate: pulmonaryFunctionDate,
    maxDate: pulmonaryFunctionMaxDate
  });
  
  // Schedule Trigger Assessment within 2 weeks
  const triggerAssessmentDate = moment(programEnrolment.enrolmentDateTime).add(2, 'weeks').toDate();
  const triggerAssessmentMaxDate = moment(triggerAssessmentDate).add(3, 'days').toDate();
  
  scheduleBuilder.add({
    name: "Trigger Assessment",
    encounterType: "Trigger Assessment",
    earliestDate: triggerAssessmentDate,
    maxDate: triggerAssessmentMaxDate
  });
  
  // Schedule Inhaler Training immediately
  const inhalerTrainingDate = moment(programEnrolment.enrolmentDateTime).add(1, 'day').toDate();
  const inhalerTrainingMaxDate = moment(inhalerTrainingDate).add(4, 'hours').toDate();
  
  scheduleBuilder.add({
    name: "Inhaler Training",
    encounterType: "Inhaler Training",
    earliestDate: inhalerTrainingDate,
    maxDate: inhalerTrainingMaxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 47,
        "scenario": "Palliative care program enrollment",
        "context": {
            "formType": "ProgramEnrolment",
            "encounterType": "Palliative Intake",
            "encounterTypes": [
                {"name": "Symptom Assessment", "program": "Palliative Care"},
                {"name": "Goals Discussion", "program": "Palliative Care"},
                {"name": "Family Meeting", "program": "Palliative Care"},
            ],
            "concepts": ["symptom-burden", "prognosis", "care-goals", "family-support"],
        },
        "rule_request": "Schedule Symptom Assessment within 24 hours, Goals Discussion within 48 hours, Family Meeting within 1 week",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEnrolment = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEnrolment });
  
  const moment = imports.moment;
  
  // Schedule Symptom Assessment within 24 hours
  const symptomAssessmentDate = moment(programEnrolment.enrolmentDateTime).add(24, 'hours').toDate();
  const symptomAssessmentMaxDate = moment(symptomAssessmentDate).add(2, 'hours').toDate();
  
  scheduleBuilder.add({
    name: "Symptom Assessment",
    encounterType: "Symptom Assessment",
    earliestDate: symptomAssessmentDate,
    maxDate: symptomAssessmentMaxDate
  });
  
  // Schedule Goals Discussion within 48 hours
  const goalsDiscussionDate = moment(programEnrolment.enrolmentDateTime).add(48, 'hours').toDate();
  const goalsDiscussionMaxDate = moment(goalsDiscussionDate).add(4, 'hours').toDate();
  
  scheduleBuilder.add({
    name: "Goals Discussion",
    encounterType: "Goals Discussion",
    earliestDate: goalsDiscussionDate,
    maxDate: goalsDiscussionMaxDate
  });
  
  // Schedule Family Meeting within 1 week
  const familyMeetingDate = moment(programEnrolment.enrolmentDateTime).add(1, 'week').toDate();
  const familyMeetingMaxDate = moment(familyMeetingDate).add(1, 'day').toDate();
  
  scheduleBuilder.add({
    name: "Family Meeting",
    encounterType: "Family Meeting",
    earliestDate: familyMeetingDate,
    maxDate: familyMeetingMaxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 48,
        "scenario": "Obesity management program",
        "context": {
            "formType": "ProgramEnrolment",
            "encounterType": "Weight Management Intake",
            "encounterTypes": [
                {"name": "Metabolic Assessment", "program": "Weight Management"},
                {"name": "Nutrition Counseling", "program": "Weight Management"},
                {"name": "Exercise Planning", "program": "Weight Management"},
            ],
            "concepts": [
                "bmi",
                "metabolic-syndrome",
                "weight-history",
                "motivation-level",
            ],
        },
        "rule_request": "Schedule Metabolic Assessment within 2 weeks, Nutrition Counseling within 1 week, Exercise Planning within 3 weeks",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEnrolment = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEnrolment });
  
  const moment = imports.moment;
  
  // Schedule Metabolic Assessment within 2 weeks
  const metabolicAssessmentDate = moment(programEnrolment.enrolmentDateTime).add(2, 'weeks').toDate();
  const metabolicAssessmentMaxDate = moment(metabolicAssessmentDate).add(3, 'days').toDate();
  
  scheduleBuilder.add({
    name: "Metabolic Assessment",
    encounterType: "Metabolic Assessment",
    earliestDate: metabolicAssessmentDate,
    maxDate: metabolicAssessmentMaxDate
  });
  
  // Schedule Nutrition Counseling within 1 week
  const nutritionCounselingDate = moment(programEnrolment.enrolmentDateTime).add(1, 'week').toDate();
  const nutritionCounselingMaxDate = moment(nutritionCounselingDate).add(2, 'days').toDate();
  
  scheduleBuilder.add({
    name: "Nutrition Counseling",
    encounterType: "Nutrition Counseling",
    earliestDate: nutritionCounselingDate,
    maxDate: nutritionCounselingMaxDate
  });
  
  // Schedule Exercise Planning within 3 weeks
  const exercisePlanningDate = moment(programEnrolment.enrolmentDateTime).add(3, 'weeks').toDate();
  const exercisePlanningMaxDate = moment(exercisePlanningDate).add(1, 'week').toDate();
  
  scheduleBuilder.add({
    name: "Exercise Planning",
    encounterType: "Exercise Planning",
    earliestDate: exercisePlanningDate,
    maxDate: exercisePlanningMaxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 49,
        "scenario": "Pain management program enrollment",
        "context": {
            "formType": "ProgramEnrolment",
            "encounterType": "Pain Clinic Intake",
            "encounterTypes": [
                {"name": "Pain Assessment", "program": "Pain Management"},
                {"name": "Medication Review", "program": "Pain Management"},
                {"name": "Psychology Consult", "program": "Pain Management"},
            ],
            "concepts": [
                "pain-duration",
                "pain-intensity",
                "functional-impact",
                "psychological-factors",
            ],
        },
        "rule_request": "Schedule Pain Assessment within 1 week, Medication Review within 2 weeks, Psychology Consult if chronic pain",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEnrolment = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEnrolment });
  
  const moment = imports.moment;
  const painDuration = programEnrolment.getObservationReadableValue('pain-duration');
  
  // Schedule Pain Assessment within 1 week
  const painAssessmentDate = moment(programEnrolment.enrolmentDateTime).add(1, 'week').toDate();
  const painAssessmentMaxDate = moment(painAssessmentDate).add(2, 'days').toDate();
  
  scheduleBuilder.add({
    name: "Pain Assessment",
    encounterType: "Pain Assessment",
    earliestDate: painAssessmentDate,
    maxDate: painAssessmentMaxDate
  });
  
  // Schedule Medication Review within 2 weeks
  const medicationReviewDate = moment(programEnrolment.enrolmentDateTime).add(2, 'weeks').toDate();
  const medicationReviewMaxDate = moment(medicationReviewDate).add(3, 'days').toDate();
  
  scheduleBuilder.add({
    name: "Medication Review",
    encounterType: "Medication Review",
    earliestDate: medicationReviewDate,
    maxDate: medicationReviewMaxDate
  });
  
  // Schedule Psychology Consult if chronic pain (>3 months)
  if (painDuration > 90) {
    const psychologyConsultDate = moment(programEnrolment.enrolmentDateTime).add(3, 'weeks').toDate();
    const psychologyConsultMaxDate = moment(psychologyConsultDate).add(1, 'week').toDate();
    
    scheduleBuilder.add({
      name: "Psychology Consult",
      encounterType: "Psychology Consult",
      earliestDate: psychologyConsultDate,
      maxDate: psychologyConsultMaxDate
    });
  }
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 50,
        "scenario": "Sleep disorders program",
        "context": {
            "formType": "ProgramEnrolment",
            "encounterType": "Sleep Clinic Intake",
            "encounterTypes": [
                {"name": "Sleep Study", "program": "Sleep Medicine"},
                {"name": "CPAP Setup", "program": "Sleep Medicine"},
                {"name": "Sleep Hygiene", "program": "Sleep Medicine"},
            ],
            "concepts": [
                "sleep-symptoms",
                "apnea-risk",
                "sleep-quality",
                "daytime-functioning",
            ],
        },
        "rule_request": "Schedule Sleep Study within 4 weeks, CPAP Setup if apnea confirmed, Sleep Hygiene education immediately",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEnrolment = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEnrolment });
  
  const moment = imports.moment;
  const apneaRisk = programEnrolment.getObservationReadableValue('apnea-risk');
  
  // Schedule Sleep Study within 4 weeks
  const sleepStudyDate = moment(programEnrolment.enrolmentDateTime).add(4, 'weeks').toDate();
  const sleepStudyMaxDate = moment(sleepStudyDate).add(1, 'week').toDate();
  
  scheduleBuilder.add({
    name: "Sleep Study",
    encounterType: "Sleep Study",
    earliestDate: sleepStudyDate,
    maxDate: sleepStudyMaxDate
  });
  
  // Schedule CPAP Setup if apnea risk is high (anticipating confirmation)
  if (apneaRisk === 'High' || apneaRisk === 'Severe') {
    const cpapSetupDate = moment(programEnrolment.enrolmentDateTime).add(5, 'weeks').toDate();
    const cpapSetupMaxDate = moment(cpapSetupDate).add(1, 'week').toDate();
    
    scheduleBuilder.add({
      name: "CPAP Setup",
      encounterType: "CPAP Setup",
      earliestDate: cpapSetupDate,
      maxDate: cpapSetupMaxDate
    });
  }
  
  // Schedule Sleep Hygiene education immediately
  const sleepHygieneDate = moment(programEnrolment.enrolmentDateTime).add(1, 'day').toDate();
  const sleepHygieneMaxDate = moment(sleepHygieneDate).add(2, 'days').toDate();
  
  scheduleBuilder.add({
    name: "Sleep Hygiene",
    encounterType: "Sleep Hygiene",
    earliestDate: sleepHygieneDate,
    maxDate: sleepHygieneMaxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 51,
        "scenario": "Adolescent health program enrollment",
        "context": {
            "formType": "ProgramEnrolment",
            "encounterType": "Adolescent Health Intake",
            "encounterTypes": [
                {"name": "Health Screening", "program": "Adolescent Health"},
                {"name": "Risk Behavior Assessment", "program": "Adolescent Health"},
                {"name": "Reproductive Health", "program": "Adolescent Health"},
            ],
            "concepts": [
                "age-years",
                "risk-behaviors",
                "sexual-health",
                "mental-health-screen",
            ],
        },
        "rule_request": "Schedule Health Screening within 2 weeks, Risk Behavior Assessment within 1 week, Reproductive Health if sexually active",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEnrolment = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEnrolment });
  
  const moment = imports.moment;
  const sexualHealth = programEnrolment.getObservationReadableValue('sexual-health');
  
  // Schedule Health Screening within 2 weeks
  const healthScreeningDate = moment(programEnrolment.enrolmentDateTime).add(2, 'weeks').toDate();
  const healthScreeningMaxDate = moment(healthScreeningDate).add(3, 'days').toDate();
  
  scheduleBuilder.add({
    name: "Health Screening",
    encounterType: "Health Screening",
    earliestDate: healthScreeningDate,
    maxDate: healthScreeningMaxDate
  });
  
  // Schedule Risk Behavior Assessment within 1 week
  const riskBehaviorDate = moment(programEnrolment.enrolmentDateTime).add(1, 'week').toDate();
  const riskBehaviorMaxDate = moment(riskBehaviorDate).add(2, 'days').toDate();
  
  scheduleBuilder.add({
    name: "Risk Behavior Assessment",
    encounterType: "Risk Behavior Assessment",
    earliestDate: riskBehaviorDate,
    maxDate: riskBehaviorMaxDate
  });
  
  // Schedule Reproductive Health if sexually active
  if (sexualHealth === 'Active' || sexualHealth === 'Sexually Active') {
    const reproductiveHealthDate = moment(programEnrolment.enrolmentDateTime).add(3, 'weeks').toDate();
    const reproductiveHealthMaxDate = moment(reproductiveHealthDate).add(1, 'week').toDate();
    
    scheduleBuilder.add({
      name: "Reproductive Health",
      encounterType: "Reproductive Health",
      earliestDate: reproductiveHealthDate,
      maxDate: reproductiveHealthMaxDate
    });
  }
  
  return scheduleBuilder.getAll();
};
""",
    },
    # ============== PROGRAM ENCOUNTER CANCELLATION EXAMPLES (17) ==============
    {
        "id": 52,
        "scenario": "ANC visit cancellation with migration",
        "context": {
            "formType": "ProgramEncounterCancellation",
            "encounterType": "ANC",
            "encounterTypes": [
                {"name": "ANC", "program": "Maternal Health"},
                {"name": "ANC - Follow Up", "program": "Maternal Health"},
            ],
            "concepts": [
                "cancellation-reason",
                "migration-destination",
                "follow-up-arranged",
            ],
        },
        "rule_request": "If cancellation reason is 'Migrated' do not reschedule. Otherwise schedule ANC Follow Up on 1st of next month",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEncounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEncounter });
  
  const hasExitedProgram = (programEncounter) => programEncounter.programEnrolment.programExitDateTime;
  if(hasExitedProgram(programEncounter)) return scheduleBuilder.getAll();

  const moment = imports.moment;
  const cancellationReason = programEncounter.getCancelReason();
  
  // Do not reschedule if migrated
  if (cancellationReason === 'Migrated' || cancellationReason === 'Migration') {
    return scheduleBuilder.getAll();
  }
  
  // Schedule ANC Follow Up on 1st of next month
  const nextMonth = moment(programEncounter.cancelDateTime).add(1, 'month');
  const earliestDate = nextMonth.date(1).startOf('day').toDate();
  const maxDate = moment(earliestDate).add(1, 'week').toDate();
  
  scheduleBuilder.add({
    name: "ANC - Follow Up",
    encounterType: "ANC - Follow Up",
    earliestDate,
    maxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 53,
        "scenario": "Child followup cancellation rescheduling",
        "context": {
            "formType": "ProgramEncounterCancellation",
            "encounterType": "Child Followup",
            "encounterTypes": [
                {"name": "Child Followup", "program": "Child Health"},
                {"name": "Growth Monitoring", "program": "Child Health"},
            ],
            "concepts": ["cancellation-reason", "child-age", "urgent-follow-up-needed"],
        },
        "rule_request": "Always schedule Growth Monitoring 2 weeks from cancellation date regardless of cancellation reason",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEncounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEncounter });
  
  const hasExitedProgram = (programEncounter) => programEncounter.programEnrolment.programExitDateTime;
  if(hasExitedProgram(programEncounter)) return scheduleBuilder.getAll();

  const moment = imports.moment;
  
  // Always schedule Growth Monitoring 2 weeks from cancellation
  const earliestDate = moment(programEncounter.cancelDateTime).add(2, 'weeks').toDate();
  const maxDate = moment(earliestDate).add(3, 'days').toDate();
  
  scheduleBuilder.add({
    name: "Growth Monitoring",
    encounterType: "Growth Monitoring",
    earliestDate,
    maxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 54,
        "scenario": "Diabetes follow-up cancellation",
        "context": {
            "formType": "ProgramEncounterCancellation",
            "encounterType": "Diabetes Follow-up",
            "encounterTypes": [
                {"name": "Diabetes Follow-up", "program": "Diabetes Care"},
                {"name": "Emergency Diabetes Care", "program": "Diabetes Care"},
            ],
            "concepts": [
                "cancellation-reason",
                "blood-sugar-last",
                "medication-compliance",
            ],
        },
        "rule_request": "If cancelled due to emergency, schedule Emergency Diabetes Care in 3 days. Otherwise reschedule in 2 weeks",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEncounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEncounter });
  
  const hasExitedProgram = (programEncounter) => programEncounter.programEnrolment.programExitDateTime;
  if(hasExitedProgram(programEncounter)) return scheduleBuilder.getAll();

  const moment = imports.moment;
  const cancellationReason = programEncounter.getCancelReason();
  
  let encounterType, timeOffset, timeUnit;
  if (cancellationReason === 'Emergency' || cancellationReason === 'Medical Emergency') {
    encounterType = "Emergency Diabetes Care";
    timeOffset = 3;
    timeUnit = 'days';
  } else {
    encounterType = "Diabetes Follow-up";
    timeOffset = 2;
    timeUnit = 'weeks';
  }
  
  const earliestDate = moment(programEncounter.cancelDateTime).add(timeOffset, timeUnit).toDate();
  const maxDate = moment(earliestDate).add(3, 'days').toDate();
  
  scheduleBuilder.add({
    name: encounterType,
    encounterType: encounterType,
    earliestDate,
    maxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 55,
        "scenario": "TB treatment visit cancellation",
        "context": {
            "formType": "ProgramEncounterCancellation",
            "encounterType": "TB Treatment Review",
            "encounterTypes": [
                {"name": "TB Treatment Review", "program": "TB Program"},
                {"name": "DOT Supervision", "program": "TB Program"},
            ],
            "concepts": ["cancellation-reason", "treatment-phase", "default-risk"],
        },
        "rule_request": "If cancelled due to 'Patient unavailable', schedule DOT Supervision next day. Otherwise reschedule in 1 week",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEncounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEncounter });
  
  const hasExitedProgram = (programEncounter) => programEncounter.programEnrolment.programExitDateTime;
  if(hasExitedProgram(programEncounter)) return scheduleBuilder.getAll();

  const moment = imports.moment;
  const cancellationReason = programEncounter.getCancelReason();
  
  let encounterType, timeOffset, timeUnit;
  if (cancellationReason === 'Patient unavailable' || cancellationReason === 'Patient not found') {
    encounterType = "DOT Supervision";
    timeOffset = 1;
    timeUnit = 'day';
  } else {
    encounterType = "TB Treatment Review";
    timeOffset = 1;
    timeUnit = 'week';
  }
  
  const earliestDate = moment(programEncounter.cancelDateTime).add(timeOffset, timeUnit).toDate();
  const maxDate = moment(earliestDate).add(1, 'day').toDate();
  
  scheduleBuilder.add({
    name: encounterType,
    encounterType: encounterType,
    earliestDate,
    maxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 56,
        "scenario": "Mental health appointment cancellation",
        "context": {
            "formType": "ProgramEncounterCancellation",
            "encounterType": "Mental Health Follow-up",
            "encounterTypes": [
                {"name": "Mental Health Follow-up", "program": "Mental Health"},
                {"name": "Crisis Intervention", "program": "Mental Health"},
            ],
            "concepts": [
                "cancellation-reason",
                "suicide-risk-last",
                "crisis-indicators",
            ],
        },
        "rule_request": "If cancelled due to 'Crisis', schedule Crisis Intervention immediately. Otherwise reschedule in 1 week",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEncounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEncounter });
  
  const hasExitedProgram = (programEncounter) => programEncounter.programEnrolment.programExitDateTime;
  if(hasExitedProgram(programEncounter)) return scheduleBuilder.getAll();

  const moment = imports.moment;
  const cancellationReason = programEncounter.getCancelReason();
  
  let encounterType, timeOffset, timeUnit;
  if (cancellationReason === 'Crisis' || cancellationReason === 'Mental Health Crisis') {
    encounterType = "Crisis Intervention";
    timeOffset = 2;
    timeUnit = 'hours';
  } else {
    encounterType = "Mental Health Follow-up";
    timeOffset = 1;
    timeUnit = 'week';
  }
  
  const earliestDate = moment(programEncounter.cancelDateTime).add(timeOffset, timeUnit).toDate();
  const maxDate = moment(earliestDate).add(4, 'hours').toDate();
  
  scheduleBuilder.add({
    name: encounterType,
    encounterType: encounterType,
    earliestDate,
    maxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 57,
        "scenario": "Cancer treatment cancellation",
        "context": {
            "formType": "ProgramEncounterCancellation",
            "encounterType": "Cancer Treatment",
            "encounterTypes": [
                {"name": "Cancer Treatment", "program": "Cancer Care"},
                {"name": "Urgent Oncology", "program": "Cancer Care"},
            ],
            "concepts": [
                "cancellation-reason",
                "treatment-urgency",
                "disease-progression",
            ],
        },
        "rule_request": "If cancelled due to 'Medical Reason', schedule Urgent Oncology within 48 hours. Otherwise reschedule same day next week",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEncounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEncounter });
  
  const hasExitedProgram = (programEncounter) => programEncounter.programEnrolment.programExitDateTime;
  if(hasExitedProgram(programEncounter)) return scheduleBuilder.getAll();

  const moment = imports.moment;
  const cancellationReason = programEncounter.getCancelReason();
  
  let encounterType, timeOffset, timeUnit;
  if (cancellationReason === 'Medical Reason' || cancellationReason === 'Treatment Complication') {
    encounterType = "Urgent Oncology";
    timeOffset = 48;
    timeUnit = 'hours';
  } else {
    encounterType = "Cancer Treatment";
    timeOffset = 1;
    timeUnit = 'week';
  }
  
  const earliestDate = moment(programEncounter.cancelDateTime).add(timeOffset, timeUnit).toDate();
  const maxDate = moment(earliestDate).add(6, 'hours').toDate();
  
  scheduleBuilder.add({
    name: encounterType,
    encounterType: encounterType,
    earliestDate,
    maxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 58,
        "scenario": "Immunization visit cancellation",
        "context": {
            "formType": "ProgramEncounterCancellation",
            "encounterType": "Child Immunization",
            "encounterTypes": [
                {"name": "Child Immunization", "program": "Child Health"},
                {"name": "Catch-up Immunization", "program": "Child Health"},
            ],
            "concepts": ["cancellation-reason", "vaccine-due", "delay-acceptable"],
        },
        "rule_request": "If cancelled due to 'Illness', reschedule in 1 week. If 'Family unavailable', schedule Catch-up Immunization in 2 weeks",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEncounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEncounter });
  
  const hasExitedProgram = (programEncounter) => programEncounter.programEnrolment.programExitDateTime;
  if(hasExitedProgram(programEncounter)) return scheduleBuilder.getAll();

  const moment = imports.moment;
  const cancellationReason = programEncounter.getCancelReason();
  
  let encounterType, timeOffset, timeUnit;
  if (cancellationReason === 'Illness' || cancellationReason === 'Child Sick') {
    encounterType = "Child Immunization";
    timeOffset = 1;
    timeUnit = 'week';
  } else if (cancellationReason === 'Family unavailable' || cancellationReason === 'Family not available') {
    encounterType = "Catch-up Immunization";
    timeOffset = 2;
    timeUnit = 'weeks';
  } else {
    encounterType = "Child Immunization";
    timeOffset = 1;
    timeUnit = 'week';
  }
  
  const earliestDate = moment(programEncounter.cancelDateTime).add(timeOffset, timeUnit).toDate();
  const maxDate = moment(earliestDate).add(3, 'days').toDate();
  
  scheduleBuilder.add({
    name: encounterType,
    encounterType: encounterType,
    earliestDate,
    maxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 59,
        "scenario": "PNC visit cancellation",
        "context": {
            "formType": "ProgramEncounterCancellation",
            "encounterType": "PNC",
            "encounterTypes": [
                {"name": "PNC", "program": "Maternal Health"},
                {"name": "Emergency PNC", "program": "Maternal Health"},
            ],
            "concepts": [
                "cancellation-reason",
                "delivery-complications",
                "postpartum-day",
            ],
        },
        "rule_request": "If cancelled due to 'Readmission', schedule Emergency PNC when discharged. Otherwise reschedule in 3 days",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEncounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEncounter });
  
  const hasExitedProgram = (programEncounter) => programEncounter.programEnrolment.programExitDateTime;
  if(hasExitedProgram(programEncounter)) return scheduleBuilder.getAll();

  const moment = imports.moment;
  const cancellationReason = programEncounter.getCancelReason();
  
  let encounterType, timeOffset, timeUnit;
  if (cancellationReason === 'Readmission' || cancellationReason === 'Hospital Readmission') {
    encounterType = "Emergency PNC";
    timeOffset = 1;
    timeUnit = 'day'; // Schedule for next day assuming discharge
  } else {
    encounterType = "PNC";
    timeOffset = 3;
    timeUnit = 'days';
  }
  
  const earliestDate = moment(programEncounter.cancelDateTime).add(timeOffset, timeUnit).toDate();
  const maxDate = moment(earliestDate).add(1, 'day').toDate();
  
  scheduleBuilder.add({
    name: encounterType,
    encounterType: encounterType,
    earliestDate,
    maxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 60,
        "scenario": "Cardiac rehabilitation cancellation",
        "context": {
            "formType": "ProgramEncounterCancellation",
            "encounterType": "Cardiac Rehab",
            "encounterTypes": [
                {"name": "Cardiac Rehab", "program": "Cardiac Care"},
                {"name": "Cardiac Assessment", "program": "Cardiac Care"},
            ],
            "concepts": [
                "cancellation-reason",
                "cardiac-symptoms",
                "exercise-tolerance",
            ],
        },
        "rule_request": "If cancelled due to 'Chest Pain', schedule Cardiac Assessment urgently. Otherwise reschedule rehab in 1 week",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEncounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEncounter });
  
  const hasExitedProgram = (programEncounter) => programEncounter.programEnrolment.programExitDateTime;
  if(hasExitedProgram(programEncounter)) return scheduleBuilder.getAll();

  const moment = imports.moment;
  const cancellationReason = programEncounter.getCancelReason();
  
  let encounterType, timeOffset, timeUnit;
  if (cancellationReason === 'Chest Pain' || cancellationReason === 'Cardiac Symptoms') {
    encounterType = "Cardiac Assessment";
    timeOffset = 4;
    timeUnit = 'hours';
  } else {
    encounterType = "Cardiac Rehab";
    timeOffset = 1;
    timeUnit = 'week';
  }
  
  const earliestDate = moment(programEncounter.cancelDateTime).add(timeOffset, timeUnit).toDate();
  const maxDate = moment(earliestDate).add(2, 'hours').toDate();
  
  scheduleBuilder.add({
    name: encounterType,
    encounterType: encounterType,
    earliestDate,
    maxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 61,
        "scenario": "COPD follow-up cancellation",
        "context": {
            "formType": "ProgramEncounterCancellation",
            "encounterType": "COPD Follow-up",
            "encounterTypes": [
                {"name": "COPD Follow-up", "program": "Respiratory Care"},
                {"name": "COPD Exacerbation", "program": "Respiratory Care"},
            ],
            "concepts": [
                "cancellation-reason",
                "breathing-difficulty",
                "medication-adherence",
            ],
        },
        "rule_request": "If cancelled due to 'Breathing Problems', schedule COPD Exacerbation care within 6 hours. Otherwise reschedule in 2 weeks",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEncounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEncounter });
  
  const hasExitedProgram = (programEncounter) => programEncounter.programEnrolment.programExitDateTime;
  if(hasExitedProgram(programEncounter)) return scheduleBuilder.getAll();

  const moment = imports.moment;
  const cancellationReason = programEncounter.getCancelReason();
  
  let encounterType, timeOffset, timeUnit;
  if (cancellationReason === 'Breathing Problems' || cancellationReason === 'Shortness of Breath') {
    encounterType = "COPD Exacerbation";
    timeOffset = 6;
    timeUnit = 'hours';
  } else {
    encounterType = "COPD Follow-up";
    timeOffset = 2;
    timeUnit = 'weeks';
  }
  
  const earliestDate = moment(programEncounter.cancelDateTime).add(timeOffset, timeUnit).toDate();
  const maxDate = moment(earliestDate).add(2, 'hours').toDate();
  
  scheduleBuilder.add({
    name: encounterType,
    encounterType: encounterType,
    earliestDate,
    maxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 62,
        "scenario": "Pain management cancellation",
        "context": {
            "formType": "ProgramEncounterCancellation",
            "encounterType": "Pain Management",
            "encounterTypes": [
                {"name": "Pain Management", "program": "Pain Care"},
                {"name": "Emergency Pain Care", "program": "Pain Care"},
            ],
            "concepts": [
                "cancellation-reason",
                "pain-escalation",
                "medication-running-out",
            ],
        },
        "rule_request": "If cancelled due to 'Severe Pain', schedule Emergency Pain Care same day. Otherwise reschedule in 5 days",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEncounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEncounter });
  
  const hasExitedProgram = (programEncounter) => programEncounter.programEnrolment.programExitDateTime;
  if(hasExitedProgram(programEncounter)) return scheduleBuilder.getAll();

  const moment = imports.moment;
  const cancellationReason = programEncounter.getCancelReason();
  
  let encounterType, timeOffset, timeUnit;
  if (cancellationReason === 'Severe Pain' || cancellationReason === 'Pain Crisis') {
    encounterType = "Emergency Pain Care";
    timeOffset = 4;
    timeUnit = 'hours';
  } else {
    encounterType = "Pain Management";
    timeOffset = 5;
    timeUnit = 'days';
  }
  
  const earliestDate = moment(programEncounter.cancelDateTime).add(timeOffset, timeUnit).toDate();
  const maxDate = moment(earliestDate).add(2, 'hours').toDate();
  
  scheduleBuilder.add({
    name: encounterType,
    encounterType: encounterType,
    earliestDate,
    maxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 63,
        "scenario": "Pregnancy termination counseling cancellation",
        "context": {
            "formType": "ProgramEncounterCancellation",
            "encounterType": "Termination Counseling",
            "encounterTypes": [
                {"name": "Termination Counseling", "program": "Reproductive Health"},
                {"name": "Crisis Pregnancy Support", "program": "Reproductive Health"},
            ],
            "concepts": [
                "cancellation-reason",
                "gestational-age",
                "emotional-support-needed",
            ],
        },
        "rule_request": "If cancelled due to 'Changed Mind', schedule Crisis Pregnancy Support within 48 hours. Do not reschedule if 'Completed Elsewhere'",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEncounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEncounter });
  
  const hasExitedProgram = (programEncounter) => programEncounter.programEnrolment.programExitDateTime;
  if(hasExitedProgram(programEncounter)) return scheduleBuilder.getAll();

  const moment = imports.moment;
  const cancellationReason = programEncounter.getCancelReason();
  
  // Do not reschedule if completed elsewhere
  if (cancellationReason === 'Completed Elsewhere' || cancellationReason === 'Procedure Done Elsewhere') {
    return scheduleBuilder.getAll();
  }
  
  // Schedule Crisis Pregnancy Support if changed mind
  if (cancellationReason === 'Changed Mind' || cancellationReason === 'Reconsidering Decision') {
    const earliestDate = moment(programEncounter.cancelDateTime).add(48, 'hours').toDate();
    const maxDate = moment(earliestDate).add(6, 'hours').toDate();
    
    scheduleBuilder.add({
      name: "Crisis Pregnancy Support",
      encounterType: "Crisis Pregnancy Support",
      earliestDate,
      maxDate
    });
  }
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 64,
        "scenario": "Substance abuse counseling cancellation",
        "context": {
            "formType": "ProgramEncounterCancellation",
            "encounterType": "Substance Counseling",
            "encounterTypes": [
                {"name": "Substance Counseling", "program": "Addiction Treatment"},
                {"name": "Relapse Prevention", "program": "Addiction Treatment"},
            ],
            "concepts": ["cancellation-reason", "relapse-risk", "support-system"],
        },
        "rule_request": "If cancelled due to 'Relapse', schedule Relapse Prevention within 24 hours. Otherwise reschedule counseling in 1 week",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEncounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEncounter });
  
  const hasExitedProgram = (programEncounter) => programEncounter.programEnrolment.programExitDateTime;
  if(hasExitedProgram(programEncounter)) return scheduleBuilder.getAll();

  const moment = imports.moment;
  const cancellationReason = programEncounter.getCancelReason();
  
  let encounterType, timeOffset, timeUnit;
  if (cancellationReason === 'Relapse' || cancellationReason === 'Substance Use Relapse') {
    encounterType = "Relapse Prevention";
    timeOffset = 24;
    timeUnit = 'hours';
  } else {
    encounterType = "Substance Counseling";
    timeOffset = 1;
    timeUnit = 'week';
  }
  
  const earliestDate = moment(programEncounter.cancelDateTime).add(timeOffset, timeUnit).toDate();
  const maxDate = moment(earliestDate).add(4, 'hours').toDate();
  
  scheduleBuilder.add({
    name: encounterType,
    encounterType: encounterType,
    earliestDate,
    maxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 65,
        "scenario": "Hospice care visit cancellation",
        "context": {
            "formType": "ProgramEncounterCancellation",
            "encounterType": "Hospice Care",
            "encounterTypes": [
                {"name": "Hospice Care", "program": "Palliative Care"},
                {"name": "End of Life Support", "program": "Palliative Care"},
            ],
            "concepts": ["cancellation-reason", "patient-status", "family-needs"],
        },
        "rule_request": "If cancelled due to 'Patient Deteriorated', schedule End of Life Support immediately. Do not reschedule if 'Patient Passed Away'",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEncounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEncounter });
  
  const hasExitedProgram = (programEncounter) => programEncounter.programEnrolment.programExitDateTime;
  if(hasExitedProgram(programEncounter)) return scheduleBuilder.getAll();

  const moment = imports.moment;
  const cancellationReason = programEncounter.getCancelReason();
  
  // Do not reschedule if patient passed away
  if (cancellationReason === 'Patient Passed Away' || cancellationReason === 'Death') {
    return scheduleBuilder.getAll();
  }
  
  // Schedule End of Life Support if patient deteriorated
  if (cancellationReason === 'Patient Deteriorated' || cancellationReason === 'Condition Worsened') {
    const earliestDate = moment(programEncounter.cancelDateTime).add(2, 'hours').toDate();
    const maxDate = moment(earliestDate).add(1, 'hour').toDate();
    
    scheduleBuilder.add({
      name: "End of Life Support",
      encounterType: "End of Life Support",
      earliestDate,
      maxDate
    });
  } else {
    // Regular hospice care rescheduling
    const earliestDate = moment(programEncounter.cancelDateTime).add(1, 'day').toDate();
    const maxDate = moment(earliestDate).add(4, 'hours').toDate();
    
    scheduleBuilder.add({
      name: "Hospice Care",
      encounterType: "Hospice Care",
      earliestDate,
      maxDate
    });
  }
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 66,
        "scenario": "Hypertension monitoring cancellation",
        "context": {
            "formType": "ProgramEncounterCancellation",
            "encounterType": "BP Monitoring",
            "encounterTypes": [
                {"name": "BP Monitoring", "program": "Hypertension Care"},
                {"name": "Emergency BP Check", "program": "Hypertension Care"},
            ],
            "concepts": [
                "cancellation-reason",
                "bp-last-reading",
                "medication-changes",
            ],
        },
        "rule_request": "If cancelled due to 'High BP Symptoms', schedule Emergency BP Check same day. Otherwise reschedule in 1 week",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEncounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEncounter });
  
  const hasExitedProgram = (programEncounter) => programEncounter.programEnrolment.programExitDateTime;
  if(hasExitedProgram(programEncounter)) return scheduleBuilder.getAll();

  const moment = imports.moment;
  const cancellationReason = programEncounter.getCancelReason();
  
  let encounterType, timeOffset, timeUnit;
  if (cancellationReason === 'High BP Symptoms' || cancellationReason === 'Hypertensive Crisis') {
    encounterType = "Emergency BP Check";
    timeOffset = 6;
    timeUnit = 'hours';
  } else {
    encounterType = "BP Monitoring";
    timeOffset = 1;
    timeUnit = 'week';
  }
  
  const earliestDate = moment(programEncounter.cancelDateTime).add(timeOffset, timeUnit).toDate();
  const maxDate = moment(earliestDate).add(2, 'hours').toDate();
  
  scheduleBuilder.add({
    name: encounterType,
    encounterType: encounterType,
    earliestDate,
    maxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 67,
        "scenario": "Eye screening cancellation for diabetics",
        "context": {
            "formType": "ProgramEncounterCancellation",
            "encounterType": "Diabetic Eye Screening",
            "encounterTypes": [
                {"name": "Diabetic Eye Screening", "program": "Diabetes Care"},
                {"name": "Urgent Eye Exam", "program": "Diabetes Care"},
            ],
            "concepts": [
                "cancellation-reason",
                "vision-complaints",
                "diabetes-control",
            ],
        },
        "rule_request": "If cancelled due to 'Vision Problems', schedule Urgent Eye Exam within 1 week. Otherwise reschedule in 1 month",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEncounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEncounter });
  
  const hasExitedProgram = (programEncounter) => programEncounter.programEnrolment.programExitDateTime;
  if(hasExitedProgram(programEncounter)) return scheduleBuilder.getAll();

  const moment = imports.moment;
  const cancellationReason = programEncounter.getCancelReason();
  
  let encounterType, timeOffset, timeUnit;
  if (cancellationReason === 'Vision Problems' || cancellationReason === 'Eye Pain') {
    encounterType = "Urgent Eye Exam";
    timeOffset = 1;
    timeUnit = 'week';
  } else {
    encounterType = "Diabetic Eye Screening";
    timeOffset = 1;
    timeUnit = 'month';
  }
  
  const earliestDate = moment(programEncounter.cancelDateTime).add(timeOffset, timeUnit).toDate();
  const maxDate = moment(earliestDate).add(3, 'days').toDate();
  
  scheduleBuilder.add({
    name: encounterType,
    encounterType: encounterType,
    earliestDate,
    maxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 68,
        "scenario": "Wound care cancellation",
        "context": {
            "formType": "ProgramEncounterCancellation",
            "encounterType": "Wound Care",
            "encounterTypes": [
                {"name": "Wound Care", "program": "Wound Management"},
                {"name": "Emergency Wound Care", "program": "Wound Management"},
            ],
            "concepts": ["cancellation-reason", "wound-status", "infection-signs"],
        },
        "rule_request": "If cancelled due to 'Wound Deterioration', schedule Emergency Wound Care within 24 hours. Otherwise reschedule in 3 days",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEncounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEncounter });
  
  const hasExitedProgram = (programEncounter) => programEncounter.programEnrolment.programExitDateTime;
  if(hasExitedProgram(programEncounter)) return scheduleBuilder.getAll();

  const moment = imports.moment;
  const cancellationReason = programEncounter.getCancelReason();
  
  let encounterType, timeOffset, timeUnit;
  if (cancellationReason === 'Wound Deterioration' || cancellationReason === 'Infection Signs') {
    encounterType = "Emergency Wound Care";
    timeOffset = 24;
    timeUnit = 'hours';
  } else {
    encounterType = "Wound Care";
    timeOffset = 3;
    timeUnit = 'days';
  }
  
  const earliestDate = moment(programEncounter.cancelDateTime).add(timeOffset, timeUnit).toDate();
  const maxDate = moment(earliestDate).add(4, 'hours').toDate();
  
  scheduleBuilder.add({
    name: encounterType,
    encounterType: encounterType,
    earliestDate,
    maxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    # ============== INDIVIDUAL ENCOUNTER CANCELLATION EXAMPLES (16) ==============
    {
        "id": 69,
        "scenario": "General health screening cancellation",
        "context": {
            "formType": "IndividualEncounterCancellation",
            "encounterType": "Health Screening",
            "encounterTypes": [
                {"name": "Health Screening"},
                {"name": "Urgent Health Check"},
            ],
            "concepts": ["cancellation-reason", "symptoms-reported", "risk-factors"],
        },
        "rule_request": "If cancelled due to 'Symptoms', schedule Urgent Health Check within 2 days. Otherwise reschedule in 1 month",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const encounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ encounter });
  
  const moment = imports.moment;
  const cancellationReason = encounter.getCancelReason();
  
  let encounterType, timeOffset, timeUnit;
  if (cancellationReason === 'Symptoms' || cancellationReason === 'New Symptoms') {
    encounterType = "Urgent Health Check";
    timeOffset = 2;
    timeUnit = 'days';
  } else {
    encounterType = "Health Screening";
    timeOffset = 1;
    timeUnit = 'month';
  }
  
  const earliestDate = moment(encounter.cancelDateTime).add(timeOffset, timeUnit).toDate();
  const maxDate = moment(earliestDate).add(1, 'day').toDate();
  
  scheduleBuilder.add({
    name: encounterType,
    encounterType: encounterType,
    earliestDate,
    maxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 70,
        "scenario": "Specialist consultation cancellation",
        "context": {
            "formType": "IndividualEncounterCancellation",
            "encounterType": "Specialist Consult",
            "encounterTypes": [
                {"name": "Specialist Consult"},
                {"name": "Urgent Specialist"},
            ],
            "concepts": [
                "cancellation-reason",
                "referral-urgency",
                "condition-worsening",
            ],
        },
        "rule_request": "If cancelled due to 'Condition Worsened', schedule Urgent Specialist next available slot. Otherwise reschedule in 4 weeks",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const encounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ encounter });
  
  const moment = imports.moment;
  const cancellationReason = encounter.getCancelReason();
  
  let encounterType, timeOffset, timeUnit;
  if (cancellationReason === 'Condition Worsened' || cancellationReason === 'Urgent Need') {
    encounterType = "Urgent Specialist";
    timeOffset = 1;
    timeUnit = 'day'; // Next available slot
  } else {
    encounterType = "Specialist Consult";
    timeOffset = 4;
    timeUnit = 'weeks';
  }
  
  const earliestDate = moment(encounter.cancelDateTime).add(timeOffset, timeUnit).toDate();
  const maxDate = moment(earliestDate).add(2, 'days').toDate();
  
  scheduleBuilder.add({
    name: encounterType,
    encounterType: encounterType,
    earliestDate,
    maxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 71,
        "scenario": "Physical therapy cancellation",
        "context": {
            "formType": "IndividualEncounterCancellation",
            "encounterType": "Physical Therapy",
            "encounterTypes": [
                {"name": "Physical Therapy"},
                {"name": "Home Exercise Review"},
            ],
            "concepts": ["cancellation-reason", "pain-level", "functional-decline"],
        },
        "rule_request": "If cancelled due to 'Pain Increase', schedule Home Exercise Review in 1 week. Otherwise reschedule PT in 3 days",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const encounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ encounter });
  
  const moment = imports.moment;
  const cancellationReason = encounter.getCancelReason();
  
  let encounterType, timeOffset, timeUnit;
  if (cancellationReason === 'Pain Increase' || cancellationReason === 'Too Painful') {
    encounterType = "Home Exercise Review";
    timeOffset = 1;
    timeUnit = 'week';
  } else {
    encounterType = "Physical Therapy";
    timeOffset = 3;
    timeUnit = 'days';
  }
  
  const earliestDate = moment(encounter.cancelDateTime).add(timeOffset, timeUnit).toDate();
  const maxDate = moment(earliestDate).add(1, 'day').toDate();
  
  scheduleBuilder.add({
    name: encounterType,
    encounterType: encounterType,
    earliestDate,
    maxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 72,
        "scenario": "Emergency wound care cancellation",
        "context": {
            "formType": "IndividualEncounterCancellation",
            "encounterType": "Wound Care",
            "encounterTypes": [
                {"name": "Wound Care"},
                {"name": "Emergency Wound Care"},
            ],
            "concepts": ["cancellation-reason", "wound-status", "infection-signs"],
        },
        "rule_request": "If cancelled due to 'Infection Concern', schedule Emergency Wound Care same day. Otherwise reschedule in 2 days",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const encounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ encounter });
  
  const moment = imports.moment;
  const cancellationReason = encounter.getCancelReason();
  
  let encounterType, timeOffset, timeUnit;
  if (cancellationReason === 'Infection Concern' || cancellationReason === 'Signs of Infection') {
    encounterType = "Emergency Wound Care";
    timeOffset = 4;
    timeUnit = 'hours';
  } else {
    encounterType = "Wound Care";
    timeOffset = 2;
    timeUnit = 'days';
  }
  
  const earliestDate = moment(encounter.cancelDateTime).add(timeOffset, timeUnit).toDate();
  const maxDate = moment(earliestDate).add(2, 'hours').toDate();
  
  scheduleBuilder.add({
    name: encounterType,
    encounterType: encounterType,
    earliestDate,
    maxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 73,
        "scenario": "Medication review cancellation",
        "context": {
            "formType": "IndividualEncounterCancellation",
            "encounterType": "Medication Review",
            "encounterTypes": [
                {"name": "Medication Review"},
                {"name": "Urgent Med Review"},
            ],
            "concepts": ["cancellation-reason", "medication-issues", "side-effects"],
        },
        "rule_request": "If cancelled due to 'Side Effects', schedule Urgent Med Review within 48 hours. Otherwise reschedule in 1 week",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const encounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ encounter });
  
  const moment = imports.moment;
  const cancellationReason = encounter.getCancelReason();
  
  let encounterType, timeOffset, timeUnit;
  if (cancellationReason === 'Side Effects' || cancellationReason === 'Adverse Reaction') {
    encounterType = "Urgent Med Review";
    timeOffset = 48;
    timeUnit = 'hours';
  } else {
    encounterType = "Medication Review";
    timeOffset = 1;
    timeUnit = 'week';
  }
  
  const earliestDate = moment(encounter.cancelDateTime).add(timeOffset, timeUnit).toDate();
  const maxDate = moment(earliestDate).add(4, 'hours').toDate();
  
  scheduleBuilder.add({
    name: encounterType,
    encounterType: encounterType,
    earliestDate,
    maxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 74,
        "scenario": "Sleep study cancellation",
        "context": {
            "formType": "IndividualEncounterCancellation",
            "encounterType": "Sleep Study",
            "encounterTypes": [
                {"name": "Sleep Study"},
                {"name": "Urgent Sleep Consult"},
            ],
            "concepts": ["cancellation-reason", "sleep-symptoms", "safety-concerns"],
        },
        "rule_request": "If cancelled due to 'Safety Concerns', schedule Urgent Sleep Consult within 1 week. Otherwise reschedule sleep study in 6 weeks",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const encounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ encounter });
  
  const moment = imports.moment;
  const cancellationReason = encounter.getCancelReason();
  
  let encounterType, timeOffset, timeUnit;
  if (cancellationReason === 'Safety Concerns' || cancellationReason === 'Driving Safety') {
    encounterType = "Urgent Sleep Consult";
    timeOffset = 1;
    timeUnit = 'week';
  } else {
    encounterType = "Sleep Study";
    timeOffset = 6;
    timeUnit = 'weeks';
  }
  
  const earliestDate = moment(encounter.cancelDateTime).add(timeOffset, timeUnit).toDate();
  const maxDate = moment(earliestDate).add(3, 'days').toDate();
  
  scheduleBuilder.add({
    name: encounterType,
    encounterType: encounterType,
    earliestDate,
    maxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 75,
        "scenario": "Dermatology appointment cancellation",
        "context": {
            "formType": "IndividualEncounterCancellation",
            "encounterType": "Dermatology",
            "encounterTypes": [
                {"name": "Dermatology"},
                {"name": "Urgent Skin Consult"},
            ],
            "concepts": ["cancellation-reason", "lesion-changes", "skin-concerns"],
        },
        "rule_request": "If cancelled due to 'Lesion Changes', schedule Urgent Skin Consult within 1 week. Otherwise reschedule in 8 weeks",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const encounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ encounter });
  
  const moment = imports.moment;
  const cancellationReason = encounter.getCancelReason();
  
  let encounterType, timeOffset, timeUnit;
  if (cancellationReason === 'Lesion Changes' || cancellationReason === 'Skin Changes') {
    encounterType = "Urgent Skin Consult";
    timeOffset = 1;
    timeUnit = 'week';
  } else {
    encounterType = "Dermatology";
    timeOffset = 8;
    timeUnit = 'weeks';
  }
  
  const earliestDate = moment(encounter.cancelDateTime).add(timeOffset, timeUnit).toDate();
  const maxDate = moment(earliestDate).add(1, 'week').toDate();
  
  scheduleBuilder.add({
    name: encounterType,
    encounterType: encounterType,
    earliestDate,
    maxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 76,
        "scenario": "Eye care cancellation",
        "context": {
            "formType": "IndividualEncounterCancellation",
            "encounterType": "Eye Examination",
            "encounterTypes": [
                {"name": "Eye Examination"},
                {"name": "Emergency Eye Care"},
            ],
            "concepts": ["cancellation-reason", "vision-changes", "eye-pain"],
        },
        "rule_request": "If cancelled due to 'Vision Loss', schedule Emergency Eye Care immediately. Otherwise reschedule in 4 weeks",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const encounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ individual: encounter.individual });
  
  const moment = imports.moment;
  const cancellationReason = encounter.getCancelReason();
  
  let encounterType, timeOffset, timeUnit;
  if (cancellationReason === 'Vision Loss' || cancellationReason === 'Sudden Vision Change') {
    encounterType = "Emergency Eye Care";
    timeOffset = 0;
    timeUnit = 'hours';
  } else {
    encounterType = "Eye Examination";
    timeOffset = 4;
    timeUnit = 'weeks';
  }
  
  const earliestDate = moment(encounter.cancelDateTime).add(timeOffset, timeUnit).toDate();
  const maxDate = moment(earliestDate).add(1, 'day').toDate();
  
  scheduleBuilder.add({
    name: encounterType,
    encounterType: encounterType,
    earliestDate,
    maxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 77,
        "scenario": "Occupational health cancellation",
        "context": {
            "formType": "IndividualEncounterCancellation",
            "encounterType": "Occupational Health",
            "encounterTypes": [
                {"name": "Occupational Health"},
                {"name": "Work Injury Assessment"},
            ],
            "concepts": ["cancellation-reason", "work-injury", "exposure-incident"],
        },
        "rule_request": "If cancelled due to 'Work Injury', schedule Work Injury Assessment within 24 hours. Otherwise reschedule in 3 months",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const encounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ individual: encounter.individual });
  
  const moment = imports.moment;
  const cancellationReason = encounter.getCancelReason();
  
  let encounterType, timeOffset, timeUnit;
  if (cancellationReason === 'Work Injury' || cancellationReason === 'Exposure Incident') {
    encounterType = "Work Injury Assessment";
    timeOffset = 24;
    timeUnit = 'hours';
  } else {
    encounterType = "Occupational Health";
    timeOffset = 3;
    timeUnit = 'months';
  }
  
  const earliestDate = moment(encounter.cancelDateTime).add(timeOffset, timeUnit).toDate();
  const maxDate = moment(earliestDate).add(2, 'days').toDate();
  
  scheduleBuilder.add({
    name: encounterType,
    encounterType: encounterType,
    earliestDate,
    maxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 78,
        "scenario": "Vaccination cancellation",
        "context": {
            "formType": "IndividualEncounterCancellation",
            "encounterType": "Vaccination",
            "encounterTypes": [{"name": "Vaccination"}, {"name": "Urgent Vaccination"}],
            "concepts": ["cancellation-reason", "vaccine-urgency", "exposure-risk"],
        },
        "rule_request": "If cancelled due to 'Exposure Risk', schedule Urgent Vaccination within 24 hours. Otherwise reschedule per vaccine schedule",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const encounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ individual: encounter.individual });
  
  const moment = imports.moment;
  const cancellationReason = encounter.getCancelReason();
  
  let encounterType, timeOffset, timeUnit;
  if (cancellationReason === 'Exposure Risk' || cancellationReason === 'Disease Exposure') {
    encounterType = "Urgent Vaccination";
    timeOffset = 24;
    timeUnit = 'hours';
  } else {
    encounterType = "Vaccination";
    timeOffset = 2;
    timeUnit = 'weeks';
  }
  
  const earliestDate = moment(encounter.cancelDateTime).add(timeOffset, timeUnit).toDate();
  const maxDate = moment(earliestDate).add(1, 'day').toDate();
  
  scheduleBuilder.add({
    name: encounterType,
    encounterType: encounterType,
    earliestDate,
    maxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 79,
        "scenario": "Mental health crisis cancellation",
        "context": {
            "formType": "IndividualEncounterCancellation",
            "encounterType": "Mental Health Consult",
            "encounterTypes": [
                {"name": "Mental Health Consult"},
                {"name": "Emergency Psychiatric"},
            ],
            "concepts": ["cancellation-reason", "crisis-indicators", "safety-concerns"],
        },
        "rule_request": "If cancelled due to 'Safety Risk', schedule Emergency Psychiatric within 2 hours. Otherwise reschedule in 1 week",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const encounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ individual: encounter.individual });
  
  const moment = imports.moment;
  const cancellationReason = encounter.getCancelReason();
  
  let encounterType, timeOffset, timeUnit;
  if (cancellationReason === 'Safety Risk' || cancellationReason === 'Crisis') {
    encounterType = "Emergency Psychiatric";
    timeOffset = 2;
    timeUnit = 'hours';
  } else {
    encounterType = "Mental Health Consult";
    timeOffset = 1;
    timeUnit = 'week';
  }
  
  const earliestDate = moment(encounter.cancelDateTime).add(timeOffset, timeUnit).toDate();
  const maxDate = moment(earliestDate).add(4, 'hours').toDate();
  
  scheduleBuilder.add({
    name: encounterType,
    encounterType: encounterType,
    earliestDate,
    maxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 80,
        "scenario": "Cardiac consultation cancellation",
        "context": {
            "formType": "IndividualEncounterCancellation",
            "encounterType": "Cardiology Consult",
            "encounterTypes": [
                {"name": "Cardiology Consult"},
                {"name": "Emergency Cardiac"},
            ],
            "concepts": [
                "cancellation-reason",
                "cardiac-symptoms",
                "risk-stratification",
            ],
        },
        "rule_request": "If cancelled due to 'Chest Pain', schedule Emergency Cardiac immediately. Otherwise reschedule in 2 weeks",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const encounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ individual: encounter.individual });
  
  const moment = imports.moment;
  const cancellationReason = encounter.getCancelReason();
  
  let encounterType, timeOffset, timeUnit;
  if (cancellationReason === 'Chest Pain' || cancellationReason === 'Cardiac Symptoms') {
    encounterType = "Emergency Cardiac";
    timeOffset = 0;
    timeUnit = 'hours';
  } else {
    encounterType = "Cardiology Consult";
    timeOffset = 2;
    timeUnit = 'weeks';
  }
  
  const earliestDate = moment(encounter.cancelDateTime).add(timeOffset, timeUnit).toDate();
  const maxDate = moment(earliestDate).add(1, 'hour').toDate();
  
  scheduleBuilder.add({
    name: encounterType,
    encounterType: encounterType,
    earliestDate,
    maxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 81,
        "scenario": "Allergy testing cancellation",
        "context": {
            "formType": "IndividualEncounterCancellation",
            "encounterType": "Allergy Testing",
            "encounterTypes": [
                {"name": "Allergy Testing"},
                {"name": "Emergency Allergy Care"},
            ],
            "concepts": ["cancellation-reason", "allergic-reaction", "testing-urgency"],
        },
        "rule_request": "If cancelled due to 'Severe Reaction', schedule Emergency Allergy Care within 4 hours. Otherwise reschedule in 4 weeks",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const encounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ individual: encounter.individual });
  
  const moment = imports.moment;
  const cancellationReason = encounter.getCancelReason();
  
  let encounterType, timeOffset, timeUnit;
  if (cancellationReason === 'Severe Reaction' || cancellationReason === 'Allergic Emergency') {
    encounterType = "Emergency Allergy Care";
    timeOffset = 4;
    timeUnit = 'hours';
  } else {
    encounterType = "Allergy Testing";
    timeOffset = 4;
    timeUnit = 'weeks';
  }
  
  const earliestDate = moment(encounter.cancelDateTime).add(timeOffset, timeUnit).toDate();
  const maxDate = moment(earliestDate).add(1, 'day').toDate();
  
  scheduleBuilder.add({
    name: encounterType,
    encounterType: encounterType,
    earliestDate,
    maxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 82,
        "scenario": "Nutrition counseling cancellation",
        "context": {
            "formType": "IndividualEncounterCancellation",
            "encounterType": "Nutrition Counseling",
            "encounterTypes": [
                {"name": "Nutrition Counseling"},
                {"name": "Emergency Nutrition"},
            ],
            "concepts": ["cancellation-reason", "nutritional-crisis", "weight-changes"],
        },
        "rule_request": "If cancelled due to 'Nutritional Emergency', schedule Emergency Nutrition within 24 hours. Otherwise reschedule in 2 weeks",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const encounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ individual: encounter.individual });
  
  const moment = imports.moment;
  const cancellationReason = encounter.getCancelReason();
  
  let encounterType, timeOffset, timeUnit;
  if (cancellationReason === 'Nutritional Emergency' || cancellationReason === 'Critical Weight Loss') {
    encounterType = "Emergency Nutrition";
    timeOffset = 24;
    timeUnit = 'hours';
  } else {
    encounterType = "Nutrition Counseling";
    timeOffset = 2;
    timeUnit = 'weeks';
  }
  
  const earliestDate = moment(encounter.cancelDateTime).add(timeOffset, timeUnit).toDate();
  const maxDate = moment(earliestDate).add(2, 'days').toDate();
  
  scheduleBuilder.add({
    name: encounterType,
    encounterType: encounterType,
    earliestDate,
    maxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 83,
        "scenario": "Respiratory therapy cancellation",
        "context": {
            "formType": "IndividualEncounterCancellation",
            "encounterType": "Respiratory Therapy",
            "encounterTypes": [
                {"name": "Respiratory Therapy"},
                {"name": "Emergency Respiratory"},
            ],
            "concepts": [
                "cancellation-reason",
                "breathing-difficulty",
                "oxygen-saturation",
            ],
        },
        "rule_request": "If cancelled due to 'Breathing Emergency', schedule Emergency Respiratory within 1 hour. Otherwise reschedule in 3 days",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const encounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ individual: encounter.individual });
  
  const moment = imports.moment;
  const cancellationReason = encounter.getCancelReason();
  
  let encounterType, timeOffset, timeUnit;
  if (cancellationReason === 'Breathing Emergency' || cancellationReason === 'Respiratory Distress') {
    encounterType = "Emergency Respiratory";
    timeOffset = 1;
    timeUnit = 'hour';
  } else {
    encounterType = "Respiratory Therapy";
    timeOffset = 3;
    timeUnit = 'days';
  }
  
  const earliestDate = moment(encounter.cancelDateTime).add(timeOffset, timeUnit).toDate();
  const maxDate = moment(earliestDate).add(30, 'minutes').toDate();
  
  scheduleBuilder.add({
    name: encounterType,
    encounterType: encounterType,
    earliestDate,
    maxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 84,
        "scenario": "Genetic counseling cancellation",
        "context": {
            "formType": "IndividualEncounterCancellation",
            "encounterType": "Genetic Counseling",
            "encounterTypes": [
                {"name": "Genetic Counseling"},
                {"name": "Urgent Genetic Consult"},
            ],
            "concepts": ["cancellation-reason", "test-urgency", "family-history"],
        },
        "rule_request": "If cancelled due to 'Test Results Available', schedule Urgent Genetic Consult within 1 week. Otherwise reschedule in 1 month",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const encounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ individual: encounter.individual });
  
  const moment = imports.moment;
  const cancellationReason = encounter.getCancelReason();
  
  let encounterType, timeOffset, timeUnit;
  if (cancellationReason === 'Test Results Available' || cancellationReason === 'Urgent Results') {
    encounterType = "Urgent Genetic Consult";
    timeOffset = 1;
    timeUnit = 'week';
  } else {
    encounterType = "Genetic Counseling";
    timeOffset = 1;
    timeUnit = 'month';
  }
  
  const earliestDate = moment(encounter.cancelDateTime).add(timeOffset, timeUnit).toDate();
  const maxDate = moment(earliestDate).add(1, 'week').toDate();
  
  scheduleBuilder.add({
    name: encounterType,
    encounterType: encounterType,
    earliestDate,
    maxDate
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    # ============== PROGRAM EXIT EXAMPLES (16) ==============
    {
        "id": 85,
        "scenario": "Maternal health program exit after delivery",
        "context": {
            "formType": "ProgramExit",
            "encounterType": "Pregnancy Completion",
            "encounterTypes": [
                {"name": "Final PNC", "program": "Maternal Health"},
                {"name": "Child Health Transition", "program": "Child Health"},
                {"name": "Family Planning Consult", "program": "Reproductive Health"},
            ],
            "concepts": [
                "delivery-outcome",
                "maternal-complications",
                "contraceptive-needs",
                "breastfeeding-status",
            ],
        },
        "rule_request": "Schedule Final PNC 6 weeks after delivery, Child Health Transition for newborn immediately, Family Planning Consult at 8 weeks",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEnrolment = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEnrolment });
  
  const moment = imports.moment;
  const individual = programEnrolment.individual;
  const deliveryDate = individual.getObservationValue('delivery-date');
  
  if (deliveryDate) {
    // Final PNC at 6 weeks
    const finalPNCDate = moment(deliveryDate).add(6, 'weeks').toDate();
    scheduleBuilder.add({
      name: "Final PNC",
      encounterType: "Final PNC",
      earliestDate: finalPNCDate,
      maxDate: moment(finalPNCDate).add(1, 'week').toDate()
    });
    
    // Child Health Transition immediately
    const childTransitionDate = moment(deliveryDate).add(1, 'day').toDate();
    scheduleBuilder.add({
      name: "Child Health Transition",
      encounterType: "Child Health Transition",
      earliestDate: childTransitionDate,
      maxDate: moment(childTransitionDate).add(3, 'days').toDate()
    });
    
    // Family Planning Consult at 8 weeks
    const familyPlanningDate = moment(deliveryDate).add(8, 'weeks').toDate();
    scheduleBuilder.add({
      name: "Family Planning Consult", 
      encounterType: "Family Planning Consult",
      earliestDate: familyPlanningDate,
      maxDate: moment(familyPlanningDate).add(2, 'weeks').toDate()
    });
  }
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 86,
        "scenario": "Child health program exit at age 5",
        "context": {
            "formType": "ProgramExit",
            "encounterType": "Child Program Graduation",
            "encounterTypes": [
                {"name": "School Health Transition", "program": "School Health"},
                {"name": "Final Growth Assessment", "program": "Child Health"},
                {"name": "Adolescent Program Referral", "program": "Adolescent Health"},
            ],
            "concepts": [
                "final-growth-assessment",
                "school-readiness",
                "immunization-status",
                "developmental-milestones",
            ],
        },
        "rule_request": "Schedule Final Growth Assessment before program exit, School Health Transition if enrolling in school, Adolescent Program Referral at age 10",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEnrolment = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEnrolment });
  
  const moment = imports.moment;
  const individual = programEnrolment.individual;
  const dateOfBirth = individual.dateOfBirth;
  const schoolEnrollment = individual.getObservationValue('school-readiness');
  
  // Final Growth Assessment before exit
  const finalAssessmentDate = moment().add(1, 'week').toDate();
  scheduleBuilder.add({
    name: "Final Growth Assessment",
    encounterType: "Final Growth Assessment", 
    earliestDate: finalAssessmentDate,
    maxDate: moment(finalAssessmentDate).add(2, 'weeks').toDate()
  });
  
  // School Health Transition if enrolling
  if (schoolEnrollment === 'Yes' || schoolEnrollment === 'Ready for School') {
    const schoolTransitionDate = moment().add(2, 'weeks').toDate();
    scheduleBuilder.add({
      name: "School Health Transition",
      encounterType: "School Health Transition",
      earliestDate: schoolTransitionDate,
      maxDate: moment(schoolTransitionDate).add(1, 'month').toDate()
    });
  }
  
  // Adolescent Program Referral at age 10
  if (dateOfBirth) {
    const age10Date = moment(dateOfBirth).add(10, 'years').toDate();
    if (moment().isBefore(age10Date)) {
      scheduleBuilder.add({
        name: "Adolescent Program Referral",
        encounterType: "Adolescent Program Referral",
        earliestDate: age10Date,
        maxDate: moment(age10Date).add(1, 'month').toDate()
      });
    }
  }
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 87,
        "scenario": "TB treatment program completion",
        "context": {
            "formType": "ProgramExit",
            "encounterType": "TB Treatment Completion",
            "encounterTypes": [
                {"name": "Treatment Success Assessment", "program": "TB Program"},
                {"name": "Contact Follow-up", "program": "TB Program"},
                {"name": "Long-term Monitoring", "program": "General Health"},
            ],
            "concepts": [
                "treatment-outcome",
                "sputum-conversion",
                "contact-screening-complete",
                "relapse-risk",
            ],
        },
        "rule_request": "Schedule Treatment Success Assessment at completion, Contact Follow-up for all contacts, Long-term Monitoring every 6 months for 2 years",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEnrolment = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEnrolment });
  
  const moment = imports.moment;
  const individual = programEnrolment.individual;
  const treatmentEndDate = programEnrolment.programExitDateTime || moment().toDate();
  
  // Treatment Success Assessment at completion
  const successAssessmentDate = moment(treatmentEndDate).add(1, 'week').toDate();
  scheduleBuilder.add({
    name: "Treatment Success Assessment",
    encounterType: "Treatment Success Assessment",
    earliestDate: successAssessmentDate,
    maxDate: moment(successAssessmentDate).add(2, 'weeks').toDate()
  });
  
  // Contact Follow-up
  const contactFollowupDate = moment(treatmentEndDate).add(2, 'weeks').toDate();
  scheduleBuilder.add({
    name: "Contact Follow-up",
    encounterType: "Contact Follow-up",
    earliestDate: contactFollowupDate,
    maxDate: moment(contactFollowupDate).add(1, 'month').toDate()
  });
  
  // Long-term Monitoring every 6 months for 2 years
  for (let i = 1; i <= 4; i++) {
    const monitoringDate = moment(treatmentEndDate).add(i * 6, 'months').toDate();
    scheduleBuilder.add({
      name: "Long-term Monitoring",
      encounterType: "Long-term Monitoring",
      earliestDate: monitoringDate,
      maxDate: moment(monitoringDate).add(1, 'month').toDate()
    });
  }
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 88,
        "scenario": "Diabetes program exit due to death",
        "context": {
            "formType": "ProgramExit",
            "encounterType": "Patient Death",
            "encounterTypes": [
                {"name": "Death Verification", "program": "Diabetes Care"},
                {"name": "Family Counseling", "program": "Family Support"},
                {"name": "Program Closure", "program": "Diabetes Care"},
            ],
            "concepts": [
                "death-cause",
                "family-notification",
                "program-closure-reason",
                "data-completion",
            ],
        },
        "rule_request": "Do not schedule any follow-up visits after death verification. Schedule Family Counseling if requested, Program Closure administrative tasks",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEnrolment = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEnrolment });
  
  const moment = imports.moment;
  const individual = programEnrolment.individual;
  const deathDate = individual.getObservationValue('death-date') || programEnrolment.programExitDateTime;
  const familyCounselingRequested = individual.getObservationValue('family-notification');
  
  if (deathDate) {
    // Family Counseling if requested
    if (familyCounselingRequested === 'Yes' || familyCounselingRequested === 'Requested') {
      const counselingDate = moment(deathDate).add(3, 'days').toDate();
      scheduleBuilder.add({
        name: "Family Counseling",
        encounterType: "Family Counseling",
        earliestDate: counselingDate,
        maxDate: moment(counselingDate).add(1, 'week').toDate()
      });
    }
    
    // Program Closure administrative tasks
    const closureDate = moment(deathDate).add(1, 'week').toDate();
    scheduleBuilder.add({
      name: "Program Closure",
      encounterType: "Program Closure",
      earliestDate: closureDate,
      maxDate: moment(closureDate).add(2, 'weeks').toDate()
    });
  }
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 89,
        "scenario": "Mental health program successful completion",
        "context": {
            "formType": "ProgramExit",
            "encounterType": "Mental Health Recovery",
            "encounterTypes": [
                {"name": "Final Assessment", "program": "Mental Health"},
                {"name": "Relapse Prevention Plan", "program": "Mental Health"},
                {
                    "name": "Community Support Linkage",
                    "program": "Community Mental Health",
                },
            ],
            "concepts": [
                "recovery-status",
                "coping-skills",
                "support-network",
                "relapse-prevention",
            ],
        },
        "rule_request": "Schedule Final Assessment before exit, Relapse Prevention Plan session, Community Support Linkage within 2 weeks of exit",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEnrolment = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEnrolment });
  
  const moment = imports.moment;
  const individual = programEnrolment.individual;
  const exitDate = programEnrolment.programExitDateTime || moment().add(1, 'week').toDate();
  
  // Final Assessment before exit
  const finalAssessmentDate = moment(exitDate).subtract(1, 'week').toDate();
  scheduleBuilder.add({
    name: "Final Assessment",
    encounterType: "Final Assessment",
    earliestDate: finalAssessmentDate,
    maxDate: moment(exitDate).toDate()
  });
  
  // Relapse Prevention Plan session
  const preventionPlanDate = moment(exitDate).subtract(3, 'days').toDate();
  scheduleBuilder.add({
    name: "Relapse Prevention Plan",
    encounterType: "Relapse Prevention Plan",
    earliestDate: preventionPlanDate,
    maxDate: moment(exitDate).add(1, 'day').toDate()
  });
  
  // Community Support Linkage within 2 weeks of exit
  const communitySupportDate = moment(exitDate).add(1, 'week').toDate();
  scheduleBuilder.add({
    name: "Community Support Linkage",
    encounterType: "Community Support Linkage",
    earliestDate: communitySupportDate,
    maxDate: moment(exitDate).add(2, 'weeks').toDate()
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 90,
        "scenario": "Cancer care program exit after cure",
        "context": {
            "formType": "ProgramExit",
            "encounterType": "Cancer Remission",
            "encounterTypes": [
                {"name": "Survivorship Plan", "program": "Cancer Care"},
                {"name": "Long-term Follow-up", "program": "Oncology Surveillance"},
                {"name": "Quality of Life Assessment", "program": "Cancer Care"},
            ],
            "concepts": [
                "remission-status",
                "treatment-side-effects",
                "surveillance-needs",
                "psychosocial-support",
            ],
        },
        "rule_request": "Schedule Survivorship Plan before exit, Long-term Follow-up annually for 5 years, Quality of Life Assessment at 6 months",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEnrolment = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEnrolment });
  
  const moment = imports.moment;
  const individual = programEnrolment.individual;
  const exitDate = programEnrolment.programExitDateTime || moment().toDate();
  
  // Survivorship Plan before exit
  const survivorshipPlanDate = moment(exitDate).subtract(1, 'week').toDate();
  scheduleBuilder.add({
    name: "Survivorship Plan",
    encounterType: "Survivorship Plan",
    earliestDate: survivorshipPlanDate,
    maxDate: moment(exitDate).toDate()
  });
  
  // Long-term Follow-up annually for 5 years
  for (let i = 1; i <= 5; i++) {
    const followupDate = moment(exitDate).add(i, 'years').toDate();
    scheduleBuilder.add({
      name: "Long-term Follow-up",
      encounterType: "Long-term Follow-up",
      earliestDate: followupDate,
      maxDate: moment(followupDate).add(1, 'month').toDate()
    });
  }
  
  // Quality of Life Assessment at 6 months
  const qualityOfLifeDate = moment(exitDate).add(6, 'months').toDate();
  scheduleBuilder.add({
    name: "Quality of Life Assessment",
    encounterType: "Quality of Life Assessment",
    earliestDate: qualityOfLifeDate,
    maxDate: moment(qualityOfLifeDate).add(2, 'weeks').toDate()
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 91,
        "scenario": "Addiction treatment program completion",
        "context": {
            "formType": "ProgramExit",
            "encounterType": "Addiction Recovery",
            "encounterTypes": [
                {"name": "Recovery Assessment", "program": "Addiction Treatment"},
                {"name": "Aftercare Planning", "program": "Addiction Treatment"},
                {"name": "Peer Support Transition", "program": "Recovery Support"},
            ],
            "concepts": [
                "sobriety-duration",
                "relapse-risk",
                "support-system",
                "aftercare-needs",
            ],
        },
        "rule_request": "Schedule Recovery Assessment before exit, Aftercare Planning session, Peer Support Transition within 1 week of completion",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEnrolment = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEnrolment });
  
  const moment = imports.moment;
  const individual = programEnrolment.individual;
  const exitDate = programEnrolment.programExitDateTime || moment().toDate();
  
  // Recovery Assessment before exit
  const recoveryAssessmentDate = moment(exitDate).subtract(3, 'days').toDate();
  scheduleBuilder.add({
    name: "Recovery Assessment",
    encounterType: "Recovery Assessment",
    earliestDate: recoveryAssessmentDate,
    maxDate: moment(exitDate).toDate()
  });
  
  // Aftercare Planning session
  const aftercarePlanningDate = moment(exitDate).subtract(1, 'day').toDate();
  scheduleBuilder.add({
    name: "Aftercare Planning",
    encounterType: "Aftercare Planning",
    earliestDate: aftercarePlanningDate,
    maxDate: moment(exitDate).add(1, 'day').toDate()
  });
  
  // Peer Support Transition within 1 week
  const peerSupportDate = moment(exitDate).add(3, 'days').toDate();
  scheduleBuilder.add({
    name: "Peer Support Transition",
    encounterType: "Peer Support Transition",
    earliestDate: peerSupportDate,
    maxDate: moment(exitDate).add(1, 'week').toDate()
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 92,
        "scenario": "Palliative care program exit due to death",
        "context": {
            "formType": "ProgramExit",
            "encounterType": "End of Life",
            "encounterTypes": [
                {"name": "Death Certification", "program": "Palliative Care"},
                {"name": "Bereavement Support", "program": "Family Support"},
                {"name": "Program Review", "program": "Palliative Care"},
            ],
            "concepts": [
                "death-circumstances",
                "family-bereavement",
                "care-quality",
                "lessons-learned",
            ],
        },
        "rule_request": "Schedule Bereavement Support for family within 1 week, Program Review for quality improvement, no further patient visits",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEnrolment = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEnrolment });
  
  const moment = imports.moment;
  const individual = programEnrolment.individual;
  const deathDate = individual.getObservationValue('death-date') || programEnrolment.programExitDateTime;
  const familyBereavementNeeded = individual.getObservationValue('family-bereavement');
  
  if (deathDate) {
    // Bereavement Support for family within 1 week
    if (familyBereavementNeeded === 'Yes' || familyBereavementNeeded === 'Needed') {
      const bereavementDate = moment(deathDate).add(3, 'days').toDate();
      scheduleBuilder.add({
        name: "Bereavement Support",
        encounterType: "Bereavement Support",
        earliestDate: bereavementDate,
        maxDate: moment(deathDate).add(1, 'week').toDate()
      });
    }
    
    // Program Review for quality improvement
    const reviewDate = moment(deathDate).add(2, 'weeks').toDate();
    scheduleBuilder.add({
      name: "Program Review",
      encounterType: "Program Review",
      earliestDate: reviewDate,
      maxDate: moment(reviewDate).add(1, 'month').toDate()
    });
  }
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 93,
        "scenario": "Cardiac rehabilitation completion",
        "context": {
            "formType": "ProgramExit",
            "encounterType": "Cardiac Rehab Graduation",
            "encounterTypes": [
                {"name": "Exercise Tolerance Test", "program": "Cardiac Rehab"},
                {"name": "Maintenance Program", "program": "Cardiac Care"},
                {"name": "Home Exercise Plan", "program": "Cardiac Rehab"},
            ],
            "concepts": [
                "exercise-capacity",
                "cardiac-function",
                "lifestyle-changes",
                "maintenance-needs",
            ],
        },
        "rule_request": "Schedule Exercise Tolerance Test at completion, Maintenance Program enrollment, Home Exercise Plan review session",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEnrolment = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEnrolment });
  
  const moment = imports.moment;
  const individual = programEnrolment.individual;
  const exitDate = programEnrolment.programExitDateTime || moment().toDate();
  
  // Exercise Tolerance Test at completion
  const toleranceTestDate = moment(exitDate).subtract(1, 'week').toDate();
  scheduleBuilder.add({
    name: "Exercise Tolerance Test",
    encounterType: "Exercise Tolerance Test",
    earliestDate: toleranceTestDate,
    maxDate: moment(exitDate).toDate()
  });
  
  // Maintenance Program enrollment
  const maintenanceEnrollDate = moment(exitDate).add(1, 'week').toDate();
  scheduleBuilder.add({
    name: "Maintenance Program",
    encounterType: "Maintenance Program",
    earliestDate: maintenanceEnrollDate,
    maxDate: moment(maintenanceEnrollDate).add(2, 'weeks').toDate()
  });
  
  // Home Exercise Plan review session
  const homeExerciseDate = moment(exitDate).add(3, 'days').toDate();
  scheduleBuilder.add({
    name: "Home Exercise Plan",
    encounterType: "Home Exercise Plan",
    earliestDate: homeExerciseDate,
    maxDate: moment(homeExerciseDate).add(1, 'week').toDate()
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 94,
        "scenario": "Stroke rehabilitation completion",
        "context": {
            "formType": "ProgramExit",
            "encounterType": "Stroke Rehab Completion",
            "encounterTypes": [
                {"name": "Functional Assessment", "program": "Stroke Rehab"},
                {"name": "Community Reintegration", "program": "Rehabilitation"},
                {"name": "Caregiver Training", "program": "Stroke Rehab"},
            ],
            "concepts": [
                "functional-recovery",
                "independence-level",
                "caregiver-needs",
                "adaptive-equipment",
            ],
        },
        "rule_request": "Schedule Functional Assessment before exit, Community Reintegration planning, Caregiver Training if ongoing support needed",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEnrolment = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEnrolment });
  
  const moment = imports.moment;
  const individual = programEnrolment.individual;
  const exitDate = programEnrolment.programExitDateTime || moment().toDate();
  const caregiverNeed = individual.getObservationValue('caregiver-needs');
  
  // Functional Assessment before exit
  const functionalAssessmentDate = moment(exitDate).subtract(1, 'week').toDate();
  scheduleBuilder.add({
    name: "Functional Assessment",
    encounterType: "Functional Assessment",
    earliestDate: functionalAssessmentDate,
    maxDate: moment(exitDate).toDate()
  });
  
  // Community Reintegration planning
  const reintegrationDate = moment(exitDate).add(1, 'week').toDate();
  scheduleBuilder.add({
    name: "Community Reintegration",
    encounterType: "Community Reintegration",
    earliestDate: reintegrationDate,
    maxDate: moment(reintegrationDate).add(2, 'weeks').toDate()
  });
  
  // Caregiver Training if ongoing support needed
  if (caregiverNeed === 'Yes' || caregiverNeed === 'Ongoing Support Needed') {
    const caregiverTrainingDate = moment(exitDate).add(3, 'days').toDate();
    scheduleBuilder.add({
      name: "Caregiver Training",
      encounterType: "Caregiver Training",
      earliestDate: caregiverTrainingDate,
      maxDate: moment(caregiverTrainingDate).add(1, 'week').toDate()
    });
  }
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 95,
        "scenario": "Chronic kidney disease program exit for transplant",
        "context": {
            "formType": "ProgramExit",
            "encounterType": "Pre-Transplant Transition",
            "encounterTypes": [
                {"name": "Transplant Preparation", "program": "Transplant Care"},
                {"name": "CKD Program Closure", "program": "CKD Care"},
                {"name": "Post-Transplant Planning", "program": "Transplant Care"},
            ],
            "concepts": [
                "transplant-readiness",
                "medical-optimization",
                "psychosocial-preparation",
                "donor-status",
            ],
        },
        "rule_request": "Schedule Transplant Preparation immediately, CKD Program Closure when transplant occurs, Post-Transplant Planning before surgery",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEnrolment = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEnrolment });
  
  const moment = imports.moment;
  const individual = programEnrolment.individual;
  const exitDate = programEnrolment.programExitDateTime || moment().toDate();
  const transplantDate = individual.getObservationValue('transplant-date');
  
  // Transplant Preparation immediately
  const preparationDate = moment().add(1, 'day').toDate();
  scheduleBuilder.add({
    name: "Transplant Preparation",
    encounterType: "Transplant Preparation",
    earliestDate: preparationDate,
    maxDate: moment(preparationDate).add(1, 'week').toDate()
  });
  
  // CKD Program Closure when transplant occurs
  if (transplantDate) {
    const closureDate = moment(transplantDate).add(1, 'day').toDate();
    scheduleBuilder.add({
      name: "CKD Program Closure",
      encounterType: "CKD Program Closure",
      earliestDate: closureDate,
      maxDate: moment(closureDate).add(1, 'week').toDate()
    });
  }
  
  // Post-Transplant Planning before surgery
  if (transplantDate) {
    const postTransplantPlanningDate = moment(transplantDate).subtract(1, 'week').toDate();
    scheduleBuilder.add({
      name: "Post-Transplant Planning",
      encounterType: "Post-Transplant Planning",
      earliestDate: postTransplantPlanningDate,
      maxDate: moment(transplantDate).toDate()
    });
  }
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 96,
        "scenario": "Weight management program completion",
        "context": {
            "formType": "ProgramExit",
            "encounterType": "Weight Goal Achievement",
            "encounterTypes": [
                {"name": "Maintenance Planning", "program": "Weight Management"},
                {"name": "Lifestyle Sustainability", "program": "Weight Management"},
                {"name": "Long-term Support", "program": "Nutrition Support"},
            ],
            "concepts": [
                "weight-loss-achieved",
                "lifestyle-changes",
                "maintenance-confidence",
                "support-needs",
            ],
        },
        "rule_request": "Schedule Maintenance Planning before exit, Lifestyle Sustainability session, Long-term Support check-ins every 3 months",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEnrolment = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEnrolment });
  
  const moment = imports.moment;
  const individual = programEnrolment.individual;
  const exitDate = programEnrolment.programExitDateTime || moment().toDate();
  
  // Maintenance Planning before exit
  const maintenancePlanningDate = moment(exitDate).subtract(1, 'week').toDate();
  scheduleBuilder.add({
    name: "Maintenance Planning",
    encounterType: "Maintenance Planning",
    earliestDate: maintenancePlanningDate,
    maxDate: moment(exitDate).toDate()
  });
  
  // Lifestyle Sustainability session
  const sustainabilityDate = moment(exitDate).add(1, 'week').toDate();
  scheduleBuilder.add({
    name: "Lifestyle Sustainability",
    encounterType: "Lifestyle Sustainability",
    earliestDate: sustainabilityDate,
    maxDate: moment(sustainabilityDate).add(1, 'week').toDate()
  });
  
  // Long-term Support check-ins every 3 months
  for (let i = 1; i <= 4; i++) {
    const supportDate = moment(exitDate).add(i * 3, 'months').toDate();
    scheduleBuilder.add({
      name: "Long-term Support",
      encounterType: "Long-term Support",
      earliestDate: supportDate,
      maxDate: moment(supportDate).add(2, 'weeks').toDate()
    });
  }
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 97,
        "scenario": "Adolescent health program exit at age 18",
        "context": {
            "formType": "ProgramExit",
            "encounterType": "Adult Transition",
            "encounterTypes": [
                {"name": "Adult Health Transition", "program": "Adult Health"},
                {
                    "name": "Reproductive Health Consult",
                    "program": "Reproductive Health",
                },
                {
                    "name": "Health Independence Training",
                    "program": "Adolescent Health",
                },
            ],
            "concepts": [
                "adult-health-needs",
                "reproductive-counseling",
                "health-literacy",
                "independence-skills",
            ],
        },
        "rule_request": "Schedule Adult Health Transition appointment, Reproductive Health Consult if sexually active, Health Independence Training before age 18",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEnrolment = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEnrolment });
  
  const moment = imports.moment;
  const individual = programEnrolment.individual;
  const exitDate = programEnrolment.programExitDateTime || moment().toDate();
  const sexuallyActive = individual.getObservationValue('reproductive-counseling');
  
  // Adult Health Transition appointment
  const adultTransitionDate = moment(exitDate).add(1, 'week').toDate();
  scheduleBuilder.add({
    name: "Adult Health Transition",
    encounterType: "Adult Health Transition",
    earliestDate: adultTransitionDate,
    maxDate: moment(adultTransitionDate).add(2, 'weeks').toDate()
  });
  
  // Reproductive Health Consult if sexually active
  if (sexuallyActive === 'Yes' || sexuallyActive === 'Sexually Active') {
    const reproductiveConsultDate = moment(exitDate).add(3, 'days').toDate();
    scheduleBuilder.add({
      name: "Reproductive Health Consult",
      encounterType: "Reproductive Health Consult",
      earliestDate: reproductiveConsultDate,
      maxDate: moment(reproductiveConsultDate).add(1, 'week').toDate()
    });
  }
  
  // Health Independence Training before age 18
  const independenceTrainingDate = moment(exitDate).subtract(1, 'month').toDate();
  scheduleBuilder.add({
    name: "Health Independence Training",
    encounterType: "Health Independence Training",
    earliestDate: independenceTrainingDate,
    maxDate: moment(exitDate).toDate()
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 98,
        "scenario": "Immunocompromised care exit after recovery",
        "context": {
            "formType": "ProgramExit",
            "encounterType": "Immune Recovery",
            "encounterTypes": [
                {"name": "Immune Status Assessment", "program": "Immunology"},
                {"name": "Vaccination Catch-up", "program": "Immunization"},
                {"name": "Risk Assessment", "program": "General Health"},
            ],
            "concepts": [
                "immune-function",
                "infection-risk",
                "vaccination-needs",
                "ongoing-monitoring",
            ],
        },
        "rule_request": "Schedule Immune Status Assessment before exit, Vaccination Catch-up as needed, Risk Assessment for future care",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEnrolment = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEnrolment });
  
  const moment = imports.moment;
  const individual = programEnrolment.individual;
  const exitDate = programEnrolment.programExitDateTime || moment().toDate();
  const vaccinationNeeds = individual.getObservationValue('vaccination-needs');
  
  // Immune Status Assessment before exit
  const immuneAssessmentDate = moment(exitDate).subtract(1, 'week').toDate();
  scheduleBuilder.add({
    name: "Immune Status Assessment",
    encounterType: "Immune Status Assessment",
    earliestDate: immuneAssessmentDate,
    maxDate: moment(exitDate).toDate()
  });
  
  // Vaccination Catch-up as needed
  if (vaccinationNeeds === 'Yes' || vaccinationNeeds === 'Catch-up Needed') {
    const vaccinationDate = moment(exitDate).add(1, 'week').toDate();
    scheduleBuilder.add({
      name: "Vaccination Catch-up",
      encounterType: "Vaccination Catch-up",
      earliestDate: vaccinationDate,
      maxDate: moment(vaccinationDate).add(2, 'weeks').toDate()
    });
  }
  
  // Risk Assessment for future care
  const riskAssessmentDate = moment(exitDate).add(1, 'month').toDate();
  scheduleBuilder.add({
    name: "Risk Assessment",
    encounterType: "Risk Assessment",
    earliestDate: riskAssessmentDate,
    maxDate: moment(riskAssessmentDate).add(2, 'weeks').toDate()
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 99,
        "scenario": "Pain management program exit",
        "context": {
            "formType": "ProgramExit",
            "encounterType": "Pain Control Achievement",
            "encounterTypes": [
                {"name": "Pain Assessment Final", "program": "Pain Management"},
                {"name": "Self-Management Plan", "program": "Pain Management"},
                {"name": "Primary Care Transition", "program": "General Care"},
            ],
            "concepts": [
                "pain-control-level",
                "functional-improvement",
                "medication-management",
                "self-care-skills",
            ],
        },
        "rule_request": "Schedule Pain Assessment Final before exit, Self-Management Plan review, Primary Care Transition for ongoing management",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEnrolment = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEnrolment });
  
  const moment = imports.moment;
  const individual = programEnrolment.individual;
  const exitDate = programEnrolment.programExitDateTime || moment().toDate();
  
  // Pain Assessment Final before exit
  const painAssessmentDate = moment(exitDate).subtract(3, 'days').toDate();
  scheduleBuilder.add({
    name: "Pain Assessment Final",
    encounterType: "Pain Assessment Final",
    earliestDate: painAssessmentDate,
    maxDate: moment(exitDate).toDate()
  });
  
  // Self-Management Plan review
  const selfManagementDate = moment(exitDate).add(1, 'week').toDate();
  scheduleBuilder.add({
    name: "Self-Management Plan",
    encounterType: "Self-Management Plan",
    earliestDate: selfManagementDate,
    maxDate: moment(selfManagementDate).add(1, 'week').toDate()
  });
  
  // Primary Care Transition for ongoing management
  const primaryCareDate = moment(exitDate).add(2, 'weeks').toDate();
  scheduleBuilder.add({
    name: "Primary Care Transition",
    encounterType: "Primary Care Transition",
    earliestDate: primaryCareDate,
    maxDate: moment(primaryCareDate).add(2, 'weeks').toDate()
  });
  
  return scheduleBuilder.getAll();
};
""",
    },
    {
        "id": 100,
        "scenario": "Elderly care program exit due to care transition",
        "context": {
            "formType": "ProgramExit",
            "encounterType": "Care Level Transition",
            "encounterTypes": [
                {"name": "Care Needs Assessment", "program": "Elderly Care"},
                {"name": "Facility Transition", "program": "Long-term Care"},
                {"name": "Family Conference", "program": "Elderly Care"},
            ],
            "concepts": [
                "care-level-needs",
                "facility-placement",
                "family-involvement",
                "transition-planning",
            ],
        },
        "rule_request": "Schedule Care Needs Assessment before transition, Facility Transition planning, Family Conference for decision making",
        "expected_generated_rule": """
"use strict";
({ params, imports }) => {
  const programEnrolment = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEnrolment });
  
  const moment = imports.moment;
  const individual = programEnrolment.individual;
  const exitDate = programEnrolment.programExitDateTime || moment().toDate();
  const familyInvolvement = individual.getObservationValue('family-involvement');
  
  // Care Needs Assessment before transition
  const careAssessmentDate = moment(exitDate).subtract(2, 'weeks').toDate();
  scheduleBuilder.add({
    name: "Care Needs Assessment",
    encounterType: "Care Needs Assessment",
    earliestDate: careAssessmentDate,
    maxDate: moment(exitDate).subtract(1, 'week').toDate()
  });
  
  // Facility Transition planning
  const facilityTransitionDate = moment(exitDate).subtract(1, 'week').toDate();
  scheduleBuilder.add({
    name: "Facility Transition",
    encounterType: "Facility Transition",
    earliestDate: facilityTransitionDate,
    maxDate: moment(exitDate).toDate()
  });
  
  // Family Conference for decision making
  if (familyInvolvement === 'Yes' || familyInvolvement === 'Active') {
    const familyConferenceDate = moment(exitDate).subtract(10, 'days').toDate();
    scheduleBuilder.add({
      name: "Family Conference",
      encounterType: "Family Conference",
      earliestDate: familyConferenceDate,
      maxDate: moment(exitDate).subtract(3, 'days').toDate()
    });
  }
  
  return scheduleBuilder.getAll();
};
""",
    },
]


def get_all_examples():
    return VISIT_SCHEDULE_RULE_EXAMPLES
