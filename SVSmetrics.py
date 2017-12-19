import pandas


class Corpus(object):

    def __init__(self, file_name):
        self.data = pandas.read_csv(file_name)
        print(self.data.to_string())