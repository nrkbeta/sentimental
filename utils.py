from sentimental.models import Sentence, Project
from reverend.thomas import Bayes


class Guesser(object):
    
    def __init__(self, project):
        self.project = project
        self.bayes = Bayes()
        self._train()
        self.data = []
        self.best = []
    
    def _train(self):
        for sentence in self.project.classified():
            self.bayes.train(sentence.classification, sentence.sentence)
    
    def guess(self):
        for sentence in self.project.to_classify():
            self.data.append(self.bayes.guess(sentence.sentence))
        return self.data
    
    def best_matches(self):
        if not self.data: return []
        for matches in self.data:
            try:
                match = sorted(matches, key=lambda x:x[1], reverse=True)[0]
            except:
                match = (None, None)
            self.best.append(match)
        return self.best
            
