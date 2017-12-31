import pandas
import numpy
import numpy.random
import typing
import itertools
import matplotlib.pyplot

DataFrame = typing.TypeVar('pandas.core.frame.DataFrame')


class Corpus(object):

    genealogy_levels = ['PhysicalPrincipal', 'WorkingPrincipal', 'Embodiment', 'Detail']

    def __init__(self, design_file_name: str, participant_file_name: str) -> None:
        # Read in the data
        self.design_data = pandas.read_csv(design_file_name)
        self.participant_data = pandas.read_csv(participant_file_name)
        self.participant_data['VarietyScore'] = numpy.zeros(self.participant_data.shape[0])

        # Check the table to make sure its ok
        self._check_tables()

    def compute_individual_variety(self) -> None:
        for i in range(self.participant_data.shape[0]):
            temp = self.design_data.loc[self.design_data['ParticipantID'] == self.participant_data['ParticipantID'][i]]
            self.participant_data.set_value(i, 'VarietyScore', self._compute_variety(temp, [10, 6, 3, 1]))

    def _compute_variety(self, data: DataFrame, weights: list) -> float:
        variety = 0
        for i, level in enumerate(self.genealogy_levels):
            variety += weights[i]*len(numpy.unique(data[level]))
        variety /= data.shape[0]

        return variety

    def _check_tables(self) -> None:
        # Make sure design identifiers are unique
        if len(numpy.unique(self.design_data['DesignID'])) is not self.design_data.shape[0]:
            raise IndexError('Design IDs are not unique.')
        # Make sure participant identifiers are unique
        if len(numpy.unique(self.design_data['ParticipantID'])) is not self.participant_data.shape[0]:
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

            varieties.append(self._compute_variety(team, [10, 6, 3, 1]))

        return varieties

    def get_all_conditions(self, number_of_samples, team_size):
        treatments = []
        for c in numpy.unique(self.participant_data["Complexity"]):
            for a in numpy.unique(self.participant_data["Analogical"]):
                for m in numpy.unique(self.participant_data["Modality"]):
                    for v in numpy.unique(self.participant_data["Level"]):
                        treatments.append(individual([c, a, m, v]))

        print(len(treatments))

        all_combs = []
        all_varieties = []
        for comb in itertools.combinations_with_replacement(range(len(treatments)), team_size):
            print(comb)
            varieties = self.get_condition(number_of_samples, treatments[comb[0]],
                                           treatments[comb[1]], treatments[comb[2]], treatments[comb[3]])
            all_combs.append(comb)
            all_varieties.append(numpy.mean(varieties))

        return all_varieties, all_combs

    def remove_participants(self, variable, value):
        self.participant_data = self.participant_data.loc[self.participant_data[variable] == value]
        self.participant_data.reset_index(drop=True, inplace=True)


def individual(camv: list) -> dict:
    complexity = camv[0]
    analogical_distance = camv[1]
    modality = camv[2]
    level = camv[3]
    return {"Complexity": complexity, "Analogical": analogical_distance, "Modality": modality, "Level": level}

def plot


