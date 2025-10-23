const x = ({ params, imports }) => {
    const _ = imports.lodash;

    const lastFulfilledEncounter = (individual, ...encounterTypeNames) => {
        const encounters = _.chain(individual.nonVoidedEncounters())
            .filter((encounter) =>
                _.isEmpty(encounterTypeNames)
                    ? encounter
                    : _.some(encounterTypeNames, (name) => name === _.get(encounter, ""encounterType.name""))
            )
            .filter((encounter) => encounter.encounterDateTime)
            .value();

        console.log('All Encounters:', encounters);
        const lastEncounter = _.maxBy(encounters, (encounter) => encounter.encounterDateTime);
        console.log('Last Encounter:', lastEncounter);

        return lastEncounter;
    };

    const isDistributionDone = (individual) => {
        const encounter = lastFulfilledEncounter(individual, 'Card Distribution');
        if (_.isNil(encounter)) return false;

        const status = encounter.getObservationReadableValue('Card Distribution Status');
        console.log('Card Distribution Status:', status);
        return status === 'Distribution Done'
    };

    let individualList = params.db.objects('Individual')
        .filtered(`voided = false`)
        .filter((individual) => isDistributionDone(individual));

    if (params.ruleInput) {
        const dateFilter = params.ruleInput.find(rule => rule.type === ""RegistrationDate"");

        if (dateFilter) {
            const startDate = dateFilter.filterValue.minValue;
            const endDate = dateFilter.filterValue.maxValue;
            const start = new Date(startDate);
            const end = new Date(endDate);

            individualList = individualList.filter(individual => {
                const encounter = lastFulfilledEncounter(individual, 'Card Distribution');
                if (!encounter) return false;

                const encounterDate = new Date(encounter.encounterDateTime);
                
                return encounterDate >= start && encounterDate <= end;
            });
        }
    }

    return individualList;
};
