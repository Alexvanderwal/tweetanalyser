PATH = 'website/static/general/lexicons/'
JJ_LEXICON_NAMES = ('negative', 'positive')
RB_LEXICON_NAMES = ('increase', 'decrease')
jj_lexicon = {}
rb_lexicon = {}
LEXICON_COLLECTIONS = {JJ_LEXICON_NAMES: jj_lexicon, RB_LEXICON_NAMES: rb_lexicon}


def lexicons_to_lists():
    """
    Construct a individual list for all lexicons living in the constant PATH
    :return:
    """
    if not jj_lexicon and not rb_lexicon:
        for collection, lexicons_dict in LEXICON_COLLECTIONS.items():
            for index, lexicon in enumerate(collection):
                with open(PATH + lexicon + "-words.txt", "r") as file:
                    lexicons_dict[lexicon] = [line.rstrip('\n') for line in file]


class Analyser(object):
    """
    Class that calculates a sentiment score for a tweet
    """

    def __init__(self):
        lexicons_to_lists()

    def analyse(self, tweet):
        """
        Define if a section of the pos_tagged array could have sentiment
        & if the words before it could alter the value of the sentiment
        :param tweet: A pos_tagged tweet
        :return: total sentiment score of the tweet
        """

        total_score = 0.0

        for pos, section in enumerate(tweet):
            if ['JJ'] in section or ['VBP'] in section:
                if pos < 1:
                    total_score += self.define_sentiment(section)
                elif pos < 2:
                    total_score += self.define_sentiment(section, tweet[pos - 1])
                else:
                    total_score += self.define_sentiment(section, tweet[pos - 1], tweet[pos - 2])

        return total_score

    def define_sentiment(self, section, *args):
        """
        Calculate a sentiment based on the POS tags in section
        :param section: Single set of a POS tagged word
        :param args: optional words infront of the word that might decrease/increase
                     the impact of section's word
        :return:
        """
        multiplier = 1.0
        for arg in args:
            if ['RB'] in arg:
                for lexicon_type, lexicon in rb_lexicon.items():
                    if arg[0] in lexicon:
                        if lexicon_type == 'increase':
                            multiplier = 1.5
                        if lexicon_type == 'decrease':
                            multiplier = 0.5

        for lexicon_type, lexicon in jj_lexicon.items():
            if section[0] in lexicon:
                if lexicon_type == "negative":
                    return multiplier * -1.0
                elif lexicon_type == "positive":
                    return multiplier * 1.0
        return 0.0
