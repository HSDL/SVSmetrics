import pkg_resources
import TeamVariety

levels = ['PhysicalPrinciple', 'WorkingPrinciple', 'Embodiment']
weights = [10, 5, 2]

def run_a_case(levels, weights, remove, run_name):
    # Read in the data
    participants = TeamVariety.Corpus(pkg_resources.resource_filename('sensitive_data', 'designs.csv'),
                                 pkg_resources.resource_filename('sensitive_data', 'participants.csv'),
                                 levels, weights)

    # Remove things
    for key in remove:
        participants.remove_participants(key, remove[key])

    # Compute variety for individuals
    individual_file = pkg_resources.resource_filename('sensitive_data', run_name+'_alllevels_individual_variety.csv')
    participants.compute_individual_variety(individual_file)

    # Get all conditions
    treatment_file = pkg_resources.resource_filename('sensitive_data', run_name+'_alllevels_treatments.csv')
    results_file = pkg_resources.resource_filename('sensitive_data', run_name+'_alllevels_results.csv')
    variety, combinations, treatments = participants.get_all_conditions(100, 4, treatment_file=treatment_file,
                                                                        results_file=results_file)


    # Loop and do it again
    for i, level in enumerate(levels):
        # Read in the data
        participants = TeamVariety.Corpus(pkg_resources.resource_filename('sensitive_data', 'designs.csv'),
                                          pkg_resources.resource_filename('sensitive_data', 'participants.csv'),
                                          [level], [weights[i]])

        # Remove things
        for key in remove:
            participants.remove_participants(key, remove[key])

        # Compute variety for individuals
        individual_file = pkg_resources.resource_filename('sensitive_data', run_name+'_'+level+'_individual_variety.csv')
        participants.compute_individual_variety(individual_file)

        # Get all conditions
        treatment_file = pkg_resources.resource_filename('sensitive_data', run_name+'_'+level+'_treatments.csv')
        results_file = pkg_resources.resource_filename('sensitive_data', run_name+'_'+level+'_results.csv')
        variety, combinations, treatments = participants.get_all_conditions(100, 4, treatment_file=treatment_file,
                                                                            results_file=results_file)


run_a_case(levels, weights, {"Level": 0, "Modality": 1}, 'virtualseniors')
run_a_case(levels, weights, {"Level": 1, "Modality": 1}, 'virtualfreshmen')
run_a_case(levels, weights, {"Level": 0, "Modality": 0}, 'physicalseniors')
run_a_case(levels, weights, {"Level": 1, "Modality": 0}, 'physicalfreshmen')