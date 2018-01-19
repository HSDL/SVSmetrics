import pkg_resources
import SVSmetrics

# Read in the data
temp = SVSmetrics.Corpus(pkg_resources.resource_filename('tests', 'designs.csv'),
                         pkg_resources.resource_filename('tests', 'participants.csv'))

# Make sure we're only dealing with one level
temp.remove_participants("Level", 1)
# temp.remove_participants("Analogical", 1)

# Compute variety for individuals
temp.compute_individual_variety()

# Get all conditions
variety, combinations = temp.get_all_conditions(100, 4)

# Plot the output
SVSmetrics.plot_varieties(variety, combinations, [[1, 3, 5, 7], [5, 3, 2, 1]], sort="mean")
