from os import listdir
import rouge
import stemmsk
import nltk
nltk.download('punkt')


class MySummarizer():

  def __init__(self, dataPath, summarizeFunc):

    self.dataPath = dataPath
    self.files = listdir(self.dataPath)
    self.summarizeFunc = summarizeFunc

    self.evaluator = rouge.Rouge(metrics=['rouge-n', 'rouge-l'],
                             max_n=2,
                             limit_length=True,
                             length_limit=100,
                             length_limit_type='words',
                             apply_avg=True,
                             apply_best=False,
                             alpha=0.5, # Default F1_score
                             weight_factor=1.2,
                             stemming=False)


  def demonstrate(self, n):

    print('f means f1 score, r means recall, p means precision\n')

    for i in range(n):
        with open(self.dataPath + self.files[i], 'r') as r:

            whole = r.read().split('\n')[:-1]
            summ, text = whole

            tr = self.summarizeFunc(text)
            
            print('TARGET: ' + summ)
            print(f'RESULT OF {self.summarizeFunc.__name__} : {tr}')
            
            scores = self.evaluator.get_scores([tr], [summ])
            print(f"rouge-l f1 score: {scores['rouge-l']['f']} \n")


  def summarizeDataset(self, nOfFilesToPrintAfter=1000):

    summarizations = []
    hypotheses = []

    for i in range(len(self.files)):
        with open(self.dataPath + self.files[i], 'r') as r:

            whole = r.read().split('\n')[:-1]
            summ, text = whole

            tr = self.summarizeFunc(text)

            summarizations.append(self.stem_sentence(summ))
            hypotheses.append(self.stem_sentence(tr))
            
            if i % nOfFilesToPrintAfter == 0:
                    print(f"{i}/{len(self.files)}")


    scores = self.evaluator.get_scores(hypotheses, summarizations)
    for metric in scores.keys():
        results = scores[metric]
        print(f"{metric} avg f1 score: {results['f']}")



  def stem_sentence(self, sentence):
      new_sentence = []
      for word in sentence.split(" "):
          new_sentence.append(stemmsk.stem(word))
      return " ".join(new_sentence)


  