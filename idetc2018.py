import pkg_resources
import SVSmetrics

# Read in the data
temp = SVSmetrics.Corpus(pkg_resources.resource_filename('tests', 'designs.csv'),
                         pkg_resources.resource_filename('tests', 'participants.csv'))

# Make sure we're only dealing with one level
temp.remove_participants("Level", 1)
temp.remove_participants("Analogical", 1)

# Compute variety for individuals
temp.compute_individual_variety()

# Get all conditions
v, c = temp.get_all_conditions(100, 4)

print(v)

SVSmetrics.plot_varieties(v, c, [[1, 1, 1, 1], [3, 3, 3, 3]], sort="mean")
