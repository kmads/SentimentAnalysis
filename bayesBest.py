# Name: Kristen Amaddio (kea218), Holliday Shuler (hls262), SangHee Kim (shk172)
# Date: May 20, 2016
# Description: A Naive Bayes classifier that analyzes the sentiment in a text,
# assigning a movie review a "positive", "negative", or "neutral" value.
# Group work statement: All group members were present and contributing during all work on this project.
# 
#

import math, os, pickle, re

class Bayes_Classifier:

   def __init__(self):
      """This method initializes and trains the Naive Bayes Sentiment Classifier.  If a 
      cache of a trained classifier has been stored, it loads this cache.  Otherwise, 
      the system will proceed through training.  After running this method, the classifier 
      is ready to classify input text."""
      # Stores the list of filenames in IFileList
      IFileList = []
      for fFileObj in os.walk("movies_reviews/"):
         IFileList = fFileObj[2]
         break

      # For each filename, parse file name and determine if it's positive (5) or negative (1)
      self.positiveFiles = [f for f in IFileList if f[7] == '5']
      self.negativeFiles = [f for f in IFileList if f[7] == '1']

      self.positiveCount = len(self.positiveFiles)
      self.negativeCount = len(self.negativeFiles)

      if len(self.positiveFiles) > len(self.negativeFiles):
         self.positiveFiles = self.positiveFiles[:self.negativeCount]
      if len(self.negativeFiles) > len(self.positiveFiles):
         self.negativeFiles = self.negativeFiles[:self.positiveCount]

      self.positiveCount = len(self.positiveFiles)
      self.negativeCount = len(self.negativeFiles)

      # If the pickled files exist, load them. Else, train the data.
      try:
         self.positiveDict = self.load('positiveDictionaryBest.p')
         self.negativeDict = self.load('negativeDictionaryBest.p')
      except IOError:
         print "Training"
         self.positiveDict = {}
         self.negativeDict = {}
         self.train()


   def train(self):   
      """Trains the Naive Bayes Sentiment Classifier."""
      # Add tokens to negative dictionary
      for filename in self.negativeFiles:
         tokens = self.tokenize(self.loadFile('movies_reviews/'+filename))
         # for each word in the tokenized file
         for word in tokens:
            # If the word doesn't exist in the negative dictionary yet
            # initialize the word with 2 (1+1 for smoothing) 
            # divided by (negative count +1 for smoothing)
            if word not in self.negativeDict:
               self.negativeDict[word] = float(2)/(self.negativeCount+1)
            # If this word doesn't exist in the positive dictionary yet
            # initialize the word with 1 (0+1 for smoothing)
            # divided by (positive count +1 for smoothing)
            if word not in self.positiveDict:
               self.positiveDict[word] = float(1)/(self.positiveCount+1)
            # Otherwise, add 1 divided by (negative count + 1) to the count
            elif word in self.negativeDict:
               self.negativeDict[word] += float(1)/(self.negativeCount+1)

      # Add tokens to positive dictionary
      for filename in self.positiveFiles:
         tokens = self.tokenize(self.loadFile('movies_reviews/'+filename))
         # for each word in the tokenized file
         for word in tokens:
            # If the word doesn't exist in the positive dictionary yet
            # initialize the word with 2 (1+1 for smoothing)
            # divided by (positive count +1 for smoothing)
            if word not in self.positiveDict:
               self.positiveDict[word] = float(2)/(self.positiveCount+1)
            # If this word doesn't exist in the negative dictionary yet
            # initialize the word with 1 (0+1 for smoothing)
            # divided by (negative count +1 for smoothing)
            if word not in self.negativeDict:
               self.negativeDict[word] = float(1)/(self.negativeCount+1)
            # Otherwise, add 1 divided by (positive count + 1) to the count
            elif word in self.positiveDict:
               self.positiveDict[word] += float(1)/(self.positiveCount+1)

      # Pickle the files
      self.save(self.positiveDict, 'positiveDictionaryBest.p')
      self.save(self.negativeDict, 'negativeDictionaryBest.p')



   def classify(self, sText):
      """Given a target string sText, this function returns the most likely document
      class to which the target string belongs (i.e., positive, negative or neutral).
      """
      # Tokenize the text
      tokens = self.tokenize(sText)

      # Initialize the probabilities to start as log of prior probabilities
      probPos = 0 #math.log(float(self.positiveCount)/(self.positiveCount+self.negativeCount))
      probNeg = 0 #math.log(float(self.negativeCount)/(self.negativeCount+self.positiveCount))

      # Add the log probabilities of each word to the positive and negative probability log sums
      for word in tokens:
         if word in self.positiveDict:
            probPos += math.log(self.positiveDict[word])
         if word in self.negativeDict:
            probNeg += math.log(self.negativeDict[word])

      # Classify the text as whichever probability was higher
      if abs(probPos - probNeg) < 2:
         return "neutral"
      elif probPos > probNeg:
         return "positive"
      else:
         return "negative"


   def loadFile(self, sFilename):
      """Given a file name, return the contents of the file as a string."""

      f = open(sFilename, "r")
      sTxt = f.read()
      f.close()
      return sTxt
   
   def save(self, dObj, sFilename):
      """Given an object and a file name, write the object to the file using pickle."""

      f = open(sFilename, "w")
      p = pickle.Pickler(f)
      p.dump(dObj)
      f.close()
   
   def load(self, sFilename):
      """Given a file name, load and return the object stored in the file."""

      f = open(sFilename, "r")
      u = pickle.Unpickler(f)
      dObj = u.load()
      f.close()
      return dObj

   def tokenize(self, sText): 
      """Given a string of text sText, returns a list of the individual tokens that 
      occur in that string (in order). Tokens have all been made lower case to avoid
      case sensitivity issues."""

      lTokens = []
      sToken = ""
      for c in sText:
         if re.match("[a-zA-Z0-9]", str(c)) != None or c == "\"" or c == "_" or c == "-":
            sToken += c.lower()
         else:
            if sToken != "":
               lTokens.append(sToken.lower())
               sToken = ""
            if c.strip() != "":
               lTokens.append(str(c.strip()).lower())
               
      if sToken != "":
         lTokens.append(sToken)

      bigrams = []
      for i in range(0, len(lTokens)):
         if i != 0:
            bigrams.append(lTokens[i] + " " + lTokens[i-1])

      return lTokens + bigrams
