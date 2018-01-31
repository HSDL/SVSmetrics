import pkg_resources
import TeamVariety

# Read in the data
seniors = TeamVariety.Corpus(pkg_resources.resource_filename('sensitive_data', 'designs.csv'),
                             pkg_resources.resource_filename('sensitive_data', 'participants.csv'))

seniors.genealogy_levels = ['PhysicalPrinciple', 'WorkingPrinciple', 'Embodiment']
seniors.weights = [10, 5, 2, 1]

# Remove freshmen
seniors.remove_participants("Level", 0)

# Remove physical modality
seniors.remove_participants("Modality", 1)

# Compute variety for individuals
individual_file = pkg_resources.resource_filename('sensitive_data', 'virtualseniors_individual_variety.csv')
seniors.compute_individual_variety(individual_file)

# Get all conditions
treatment_file = pkg_resources.resource_filename('sensitive_data', 'virtualseniors_treatments.csv')
results_file = pkg_resources.resource_filename('sensitive_data', 'virtualseniors_results.csv')
variety, combinations, treatments = seniors.get_all_conditions(100, 4, treatment_file=treatment_file,
                                                               results_file=results_file)



# Read in the data agan
freshmen = TeamVariety.Corpus(pkg_resources.resource_filename('sensitive_data', 'designs.csv'),
                              pkg_resources.resource_filename('sensitive_data', 'participants.csv'))

freshmen.genealogy_levels = ['PhysicalPrinciple', 'WorkingPrinciple', 'Embodiment']
freshmen.weights = [10, 5, 2, 1]

# Remove seniors
freshmen.remove_participants("Level", 1)

# Remove physical modality
freshmen.remove_participants("Modality", 1)

# Compute variety for individuals
individual_file = pkg_resources.resource_filename('sensitive_data', 'virtualfreshmen_individual_variety.csv')
freshmen.compute_individual_variety(individual_file)

# Get all conditions
treatment_file = pkg_resources.resource_filename('sensitive_data', 'virtualfreshmen_treatments.csv')
results_file = pkg_resources.resource_filename('sensitive_data', 'virtualfreshmen_results.csv')
variety, combinations, treatments = freshmen.get_all_conditions(100, 4, treatment_file=treatment_file,
                                                               results_file=results_file)

# # Plot the output
# TeamVariety.plot_varieties(variety, combinations, [[1, 3, 5, 7], [5, 3, 2, 1]], sort="mean")
