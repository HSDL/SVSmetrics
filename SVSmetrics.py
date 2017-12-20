import pandas
import numpy
import typing


class Corpus(object):

    genealogy_levels = ['PhysicalPrincipal', 'WorkingPrincipal', 'Embodiment','Detail']

    def __init__(self, file_name: str) -> None:
        # Read in the data
        self.design_data = pandas.read_csv(file_name)

        # Check the table to make sure its ok
        self._check_table()

        # Make the participant table
        self._make_participant_table()

    def compute_individual_variety(self) -> None:
        for i in range(self.participant_data.shape[0]):
            temp = self.design_data.loc[self.design_data['ParticipantID'] == self.participant_data['ParticipantID'][i]]
            self.participant_data.set_value(i, 'VarietyScore', self._compute_variety(temp, [10, 6, 3, 1]))

    def _compute_variety(self, data, weights) -> float:
        variety = 0
        for i, level in enumerate(self.genealogy_levels):
            variety += weights[i]*len(numpy.unique(data[level]))
        variety /= data.shape[0]

        return variety

    def _make_participant_table(self) -> None:
        # Get unique participant list
        unique_participants = numpy.unique(self.design_data['ParticipantID'])

        # Instantiate the table
        self.participant_data = pandas.DataFrame({'ParticipantID': unique_participants,
                                                  'VarietyScore': numpy.zeros(len(unique_participants))})

    def _check_table(self):
        # Make sure design identifiers are unique
        if len(numpy.unique(self.design_data['DesignID'])) is not self.design_data.shape[0]:
            raise IndexError('Design IDs are not unique.')

    def _generate_nominal_team(self, size: int, conditions: dict):

        # Get subset that meets conditions
        temp = self.design_data
        for key in conditions:
            temp = temp.loc[eval('temp["'+key+'"]'+conditions[key])]

        # Pull from this subset to make a team
        unique_participants = numpy.unique(temp['ParticipantID'])
        team = numpy.random.choice(unique_participants, size)

        # Remove teams that don't belong
        output = pandas.DataFrame(columns=temp.columns.values)
        for member in team:
            output = pandas.concat([output, temp.loc[temp['ParticipantID'] == member]], ignore_index=True)

        return output
