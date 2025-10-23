const x = ({params, imports}) => {
    const _ = imports.lodash;
    const moment = imports.moment;
    
    const CARD_DISTRIBUTION_STATUS_CONCEPT_UUID = '44bec0ba-57f1-4278-8278-058418853a5f';
    const DISTRIBUTION_DONE_CONCEPT_ANSWER_UUID = 'd78d4d9b-99fe-4e99-9288-404d12725fea';
    
    // Base query to find individuals with distribution done status
    let query = `
        voided = false AND 
        SUBQUERY(encounters, $e, 
            $e.voided = false AND 
            $e.encounterType.name = 'Card Distribution' AND
            $e.cancelDateTime = null AND
            $e.earliestVisitDateTime != null AND
            $e.maxVisitDateTime != null AND
            SUBQUERY($e.observations, $o, 
                $o.concept.uuid = '${CARD_DISTRIBUTION_STATUS_CONCEPT_UUID}' AND
                $o.valueJSON CONTAINS '${DISTRIBUTION_DONE_CONCEPT_ANSWER_UUID}'
            ).@count > 0
        ).@count > 0
    `;
    
    // Apply date filter if provided
    if (params.ruleInput) {
        const dateFilter = _.find(params.ruleInput, {type: ""RegistrationDate""});
        if (dateFilter && dateFilter.filterValue) {
            const {minValue: startDate, maxValue: endDate} = dateFilter.filterValue;
            query += ` AND SUBQUERY(encounters, $e, 
                $e.voided = false AND 
                $e.encounterType.name = 'Card Distribution' AND
                $e.encounterDateTime >= $0 AND 
                $e.encounterDateTime <= $1
            ).@count > 0`;
            
            return params.db.objects('Individual')
                .filtered(query, new Date(startDate), new Date(endDate));
        }
    }
    
    return params.db.objects('Individual').filtered(query);
};