import pandas
import numpy
import numpy.random
import typing
import itertools
import matplotlib.pyplot
import scipy.stats

DataFrame = typing.TypeVar('pandas.core.frame.DataFrame')


class Corpus(object):

    def __init__(self, design_file_name: str, participant_file_name: str) -> None:
        # Read in the data
        self.design_data = pandas.read_csv(design_file_name)
        self.participant_data = pandas.read_csv(participant_file_name)
        self.participant_data['VarietyScore'] = numpy.zeros(self.participant_data.shape[0])

        # Check the table to make sure its ok
        self._check_tables()

        # Define dummies
        self.genealogy_levels = []
        self.weights = []

    def compute_individual_variety(self) -> None:
        for i in range(self.participant_data.shape[0]):
            print(self.participant_data['ParticipantID'][i])
            temp = self.design_data.loc[self.design_data['ParticipantID'] == self.participant_data['ParticipantID'][i]]
            if temp.shape[0] == 0:
                self.participant_data.set_value(i, 'VarietyScore', 0)
            else:
                self.participant_data.set_value(i, 'VarietyScore', self._compute_variety(temp))

    def _compute_variety(self, data: DataFrame) -> float:
        variety = 0
        nlast = 1
        for i, level in enumerate(self.genealogy_levels):
            # Remove duplicates
            temp = data.drop_duplicates(self.genealogy_levels[0:(i+1)], inplace=False)

            # Find how many unique rows
            n = temp.shape[0]

            # Update variety
            variety += self.weights[i]*(n-nlast)
            nlast = n

        return variety/data.shape[0]

    def _check_tables(self) -> None:
        # Make sure design identifiers are unique
        if len(numpy.unique(self.design_data['DesignID'])) != self.design_data.shape[0]:
            print(len(numpy.unique(self.design_data['DesignID'])), self.design_data.shape[0])
            raise IndexError('Design IDs are not unique.')
        # Make sure participant identifiers are unique
        if len(numpy.unique(self.design_data['ParticipantID'])) != self.participant_data.shape[0]:
            raise IndexError('Design IDs are not unique.')

    def get_individuals(self, condition: dict) -> list:
        c = self.participant_data['Complexity'] == condition['Complexity']
        a = self.participant_data['Analogical'] == condition['Analogical']
        m = self.participant_data['Modality'] == condition['Modality']
        v = self.participant_data['Level'] == condition['Level']

        idx = c & a & m & v

        return self.participant_data['ParticipantID'].loc[idx].tolist()

    def get_condition(self, number_of_samples: int, member1: dict, member2: dict, member3: dict, member4: dict) -> list:
        member1_options = self.get_individuals(member1)
        member2_options = self.get_individuals(member2)
        member3_options = self.get_individuals(member3)
        member4_options = self.get_individuals(member4)

        varieties = []
        for _ in range(number_of_samples):

            # Select individuals
            m1 = numpy.random.choice(member1_options, 1)[0]
            m2 = numpy.random.choice(member2_options, 1)[0]
            m3 = numpy.random.choice(member3_options, 1)[0]
            m4 = numpy.random.choice(member4_options, 1)[0]

            team = pandas.concat([self.design_data.loc[self.design_data['ParticipantID'] == m1],
                                  self.design_data.loc[self.design_data['ParticipantID'] == m2],
                                  self.design_data.loc[self.design_data['ParticipantID'] == m3],
                                  self.design_data.loc[self.design_data['ParticipantID'] == m4]], ignore_index=True)

            varieties.append(self._compute_variety(team))

        return varieties

    def get_all_conditions(self, number_of_samples, team_size, treatment_file=None, results_file=None):
        treatments = []
        for c in numpy.unique(self.participant_data["Complexity"]):
            for a in numpy.unique(self.participant_data["Analogical"]):
                for m in numpy.unique(self.participant_data["Modality"]):
                    for v in numpy.unique(self.participant_data["Level"]):
                        treatments.append(individual([c, a, m, v]))

        if treatment_file is not None:
            pandas.DataFrame(treatments).to_csv(treatment_file)

        all_combs = []
        all_varieties = []
        for comb in itertools.combinations_with_replacement(range(len(treatments)), team_size):
            print(comb)
            varieties = self.get_condition(number_of_samples, treatments[comb[0]],
                                           treatments[comb[1]], treatments[comb[2]], treatments[comb[3]])
            all_combs.append(comb)
            all_varieties.append(varieties)

        if results_file is not None:
            variety_scores = pandas.DataFrame(all_varieties)
            variety_scores.columns = ["Trial "+str(x) for x in range(number_of_samples)]
            combos = pandas.DataFrame(all_combs)
            combos.columns = ["Teammate "+str(x+1) for x in range(team_size)]
            temp = pandas.concat([combos, variety_scores], axis=1)
            temp.to_csv(results_file)

        return all_varieties, all_combs, treatments

    def remove_participants(self, variable, value):
        self.participant_data = self.participant_data.loc[self.participant_data[variable] != value]
        self.participant_data.reset_index(drop=True, inplace=True)


def individual(camv: list) -> dict:
    complexity = camv[0]
    analogical_distance = camv[1]
    modality = camv[2]
    level = camv[3]
    return {"Complexity": complexity, "Analogical": analogical_distance, "Modality": modality, "Level": level}


def plot_varieties(varieties, combinations, combs_to_show=[], sort=False) -> None:
    ax = matplotlib.pyplot.axes()

    # get means and stds
    m = []
    std = []
    stdem = []
    for variety in varieties:
        m.append(numpy.mean(variety))
        std.append(numpy.std(variety))
        stdem.append(scipy.stats.sem(variety))

    m = numpy.array(m)
    std = numpy.array(std)
    stdem = numpy.array(stdem)
    combinations = numpy.array(combinations)

    if sort is not False:
        if sort == "mean":
            idx = numpy.argsort(m)
        elif sort == "95+":
            idx = numpy.argsort(m + 2*std)
        elif sort == "95-":
            idx = numpy.argsort(m - 2*std)
        else:
            idx = range(len(m))

        print(combinations)

        combinations = combinations[idx, :]
        m = m[idx]
        std = std[idx]
        stdem = stdem[idx]

    ax.set_xticklabels([])
    ax.set_xticks([])

    ax.bar(range(len(m)), m)

    xt = []
    xtl = []
    for comb in combs_to_show:
        for idx, combination in enumerate(combinations):
            if set(combination) == set(comb):
                xt.append(idx)
                xtl.append(str(comb).replace("[", '').replace(", ", "").replace("]", ""))

    # Add the best and worst
    xt.append(0)
    xt.append(len(m)-1)
    xtl.append(str(combinations[0]).replace("[", '').replace(",", "").replace(" ", "").replace("]", ""))
    xtl.append(str(combinations[-1]).replace("[", '').replace(",", "").replace(" ", "").replace("]", ""))

    ax.bar(xt, m[xt], color='orange')

    matplotlib.pyplot.xticks(xt, xtl, rotation=45)

    matplotlib.pyplot.show()
