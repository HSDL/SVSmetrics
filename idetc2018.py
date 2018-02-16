import pkg_resources
import TeamVariety

levels = ['PhysicalPrinciple', 'WorkingPrinciple', 'Embodiment']
weights = [10, 5, 2]

# Read in the data
seniors = TeamVariety.Corpus(pkg_resources.resource_filename('sensitive_data', 'designs.csv'),
                             pkg_resources.resource_filename('sensitive_data', 'participants.csv'),
                             levels, weights)


# Remove freshmen
seniors.remove_participants("Level", 0)

# Remove physical modality
seniors.remove_participants("Modality", 1)

# Compute variety for individuals
individual_file = pkg_resources.resource_filename('sensitive_data', 'virtualseniors_alllevels_individual_variety.csv')
seniors.compute_individual_variety(individual_file)

# Get all conditions
treatment_file = pkg_resources.resource_filename('sensitive_data', 'virtualseniors_alllevels_treatments.csv')
results_file = pkg_resources.resource_filename('sensitive_data', 'virtualseniors_alllevels_results.csv')
variety, combinations, treatments = seniors.get_all_conditions(100, 4, treatment_file=treatment_file,
                                                               results_file=results_file)


# Loop and do it again
for i, level in enumerate(levels):
    # Read in the data
    seniors = TeamVariety.Corpus(pkg_resources.resource_filename('sensitive_data', 'designs.csv'),
                                 pkg_resources.resource_filename('sensitive_data', 'participants.csv'),
                                 [level], [weights[i]])

    # Remove freshmen
    seniors.remove_participants("Level", 0)

    # Remove physical modality
    seniors.remove_participants("Modality", 1)

    # Compute variety for individuals
    individual_file = pkg_resources.resource_filename('sensitive_data', 'virtualseniors_'+level+'_individual_variety.csv')
    seniors.compute_individual_variety(individual_file)

    # Get all conditions
    treatment_file = pkg_resources.resource_filename('sensitive_data', 'virtualseniors_'+level+'_treatments.csv')
    results_file = pkg_resources.resource_filename('sensitive_data', 'virtualseniors_'+level+'_results.csv')
    variety, combinations, treatments = seniors.get_all_conditions(100, 4, treatment_file=treatment_file,
                                                                   results_file=results_file)




# Read in the data agan
freshmen = TeamVariety.Corpus(pkg_resources.resource_filename('sensitive_data', 'designs.csv'),
                              pkg_resources.resource_filename('sensitive_data', 'participants.csv'),
                              levels, weights)

# Remove seniors
freshmen.remove_participants("Level", 1)

# Remove physical modality
freshmen.remove_participants("Modality", 1)

# Compute variety for individuals
individual_file = pkg_resources.resource_filename('sensitive_data', 'virtualfreshmen_alllevels_individual_variety.csv')
freshmen.compute_individual_variety(individual_file)

# Get all conditions
treatment_file = pkg_resources.resource_filename('sensitive_data', 'virtualfreshmen_alllevels_treatments.csv')
results_file = pkg_resources.resource_filename('sensitive_data', 'virtualfreshmen_alllevels_results.csv')
variety, combinations, treatments = freshmen.get_all_conditions(100, 4, treatment_file=treatment_file,
                                                               results_file=results_file)


# Loop and do it again
for i, level in enumerate(levels):
    # Read in the data
    seniors = TeamVariety.Corpus(pkg_resources.resource_filename('sensitive_data', 'designs.csv'),
                                 pkg_resources.resource_filename('sensitive_data', 'participants.csv'),
                                 [level], [weights[i]])

    # Remove freshmen
    seniors.remove_participants("Level", 0)

    # Remove physical modality
    seniors.remove_participants("Modality", 1)

    # Compute variety for individuals
    individual_file = pkg_resources.resource_filename('sensitive_data', 'virtualfreshmen_'+level+'_individual_variety.csv')
    seniors.compute_individual_variety(individual_file)

    # Get all conditions
    treatment_file = pkg_resources.resource_filename('sensitive_data', 'virtualfreshmen_'+level+'_treatments.csv')
    results_file = pkg_resources.resource_filename('sensitive_data', 'virtualfreshmen_'+level+'_results.csv')
    variety, combinations, treatments = seniors.get_all_conditions(100, 4, treatment_file=treatment_file,
                                                                   results_file=results_file)