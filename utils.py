from sentimental.models import Sentence, Project
from reverend.thomas import Bayes

def train_thomas(sentences):
    guesser = Bayes()
    for sentence in sentences:
        guesser.train(sentence.classification, sentence.sentence)
    return guesser
