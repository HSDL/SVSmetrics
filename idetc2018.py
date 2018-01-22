import pkg_resources
import TeamVariety

# Read in the data
temp = TeamVariety.Corpus(pkg_resources.resource_filename('sensitive_data', 'designs.csv'),
                          pkg_resources.resource_filename('sensitive_data', 'participants.csv'))

temp.genealogy_levels = ['PhysicalPrinciple', 'WorkingPrinciple', 'Embodiment']
temp.weights = [10, 5, 2, 1]

# Remove seniors
# temp.remove_participants("Level", 1)

# Compute variety for individuals
individual_file = pkg_resources.resource_filename('sensitive_data', 'individual_variety.csv')
temp.compute_individual_variety(individual_file)

# Get all conditions
treatment_file = pkg_resources.resource_filename('sensitive_data', 'treatments.csv')
results_file = pkg_resources.resource_filename('sensitive_data', 'results.csv')
variety, combinations, treatments = temp.get_all_conditions(100, 4, treatment_file=treatment_file, results_file=results_file)

# Plot the output
TeamVariety.plot_varieties(variety, combinations, [[1, 3, 5, 7], [5, 3, 2, 1]], sort="mean")
