from queue import Queue
from threading import Thread

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
                with open(PATH + lexicon + "-words.txt" , "r") as file:
                    lexicons_dict[lexicon] = [line.rstrip('\n') for line in file]

class AnalyserWorker(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            #get work from the queue and expand the tuple
            self.queue.task_done()
class Analyser(object):

    def analyse(self,tweet):
        '''
        :param tweet: A pos_tagged tweet
        :return:
        '''
        total_score = 0.0
        lexicons_to_lists()
        for pos, set in enumerate(tweet):
            if ['JJ'] in set or ['VBP'] in set:
                if pos < 1:
                    total_score += self.define_sentiment(set)
                elif pos < 2:
                    total_score += self.define_sentiment(set, tweet[pos-1])
                else:
                    total_score += self.define_sentiment(set, tweet[pos-1], tweet[pos-2])

        return total_score



    def define_sentiment(self,set, *args):
        multiplier = 1.0
        for arg in args:
            if ['RB'] in arg:
                for type, lexicon in rb_lexicon.items():
                    if arg[0] in lexicon:
                        if type == 'increase':
                            multiplier = 1.5
                        if type == 'decrease':
                            multiplier = 0.5

        for type, lexicon in jj_lexicon.items():
            # print("is " + str(set[0]) +
            #       " in the lexicon? " +
            #       str(type) + str(set[0] in lexicon))
            if set[0] in lexicon:
                print(type)
                if type ==  "negative":
                    return multiplier * -1.0
                elif type == "positive":
                    return multiplier * 1.0
        return 0.0




