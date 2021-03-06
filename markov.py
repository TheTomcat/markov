import random
from itertools import islice, chain
from collections import deque, defaultdict
from tools import window
class startMarker():
    pass
class endMarker():
    pass

class Markov(object):
    """
    Markov class (submarine!)

    Methods -> constructor([keySize], [noteStarts], [noteEnds])

               @param [keySize] specifies the search memory of the Markov chain
               @param [noteStarts] forces generation to begin at the start of a word
               @param [noteEnds] forces a halt, maybe. I can't remember.
    """
    def __init__(self, keySize=2, noteStarts=False, noteEnds=False):
        self.R = random.Random()
        self.dict = defaultdict(list)
        self.starting = []
        self.keySize = keySize
        self.noteStarts = noteStarts
        self.noteEnds = noteEnds
    def addKey(self, key, val):
        """Add a stub and value to the Markov dictionary.
        The key should be a tuple of length `keySize`, containing appropriate
        values.

        This is not enforced.
        """
        self.dict[key].append(val)
    def get(self, key):
        key = tuple(key)
        if key in self.dict:
            return self.dict[key]
        else:
            raise(IndexError)
    def get_by_argument(self, *arg):
        key = tuple(arg)
        return self.get(key)
    def parseText(self, molecules, sep=None):
        """Parse text and store in Markov dictionary.
        @param molecules is a list of `sentences`.
        @param sep separates complex molecules
        
        Note that sentences does not mean grammatical sentences,
        and instead form the "units" of the generator.

        For example, to generate individual words, the molecules would be
        words and the atoms would be letters. sep would be None.

        To generate phrases or prose, the molecules would be sentences and
        the atoms would be words. sep would be " ".
        """
        yieldEnd = ([i] for i in [endMarker])

        if sep is None:
            get_atom = lambda molecule: (i for i in molecule)
                #chain((i for i in molecule),yieldEnd)
        else:
            get_atom = lambda molecule: (i for i in molecule.split(sep))
                #chain((i for i in molecule.split(sep)),yieldEnd)#+[endMarker])
                #chain(yieldStart, (i for i in molecule.split(sep)),yieldEnd)
        if isinstance(molecules, str):
            molecules = [molecules]
        
        for molecule in molecules:
            if self.noteStarts:
                s = tuple(islice(get_atom(molecule),self.keySize))
                if len(s)==self.keySize:
                    self.starting.append(s)
            if self.noteEnds:
                loop_over = chain(get_atom(molecule),yieldEnd)
            else:
                loop_over = get_atom(molecule)
            for atoms in window(loop_over,self.keySize+1):
                self.addKey(atoms[:-1],atoms[-1])
    def set_seed(self, seed):
        self.seed=seed
        self.R.seed(seed)
    def makeSentence(self,maxlen=50, joinwith=None):
        if self.noteStarts:
            key = deque(self.R.choice(self.starting))
        else:
            key = deque(self.R.choice(list(self.dict.keys())))
        message = [i for i in key]
        i=0
        while i<maxlen:
            i+=1
            try:
                newWord = self.R.choice(self.get(key))
                message.append(newWord)
                key.popleft()
                key.append(newWord)
            except IndexError:
                continue
        if joinwith is not None:
            message = joinwith.join(message)
        return message

with open("corpus\\artofwar.txt") as f:
    text = f.read().lower().replace("\n","")
    G = Markov(5)
    G.parseText(text.split(". "))

with open("corpus\\russia.txt") as f:
    text = f.read().lower().split("\n")
    R = Markov(3, noteStarts=True)
    R.parseText(text)

with open("corpus\\stars.txt") as f:
    text = f.read().lower().split(", ")
    P = Markov(4)
    P.parseText(text)

with open("corpus\\greek.txt") as f:
    text = f.read().lower().split("\n")
##    text = [i.strip() for i in text]
    Q = Markov(3,noteStarts=True)
    Q.parseText(text)

with open("corpus\\dutch_town.txt") as f:
    text = f.read().lower().replace(" \n","\n").split("\n")
    D = Markov(3,noteStarts=True)
    D.parseText(text)

with open("corpus\\swedish.txt") as f:
    text = f.read().lower().replace(" \n","\n").split("\n")
    Sw = Markov(3,noteStarts=True)
    Sw.parseText(text)
##text = text.replace(". "," ")
##M = Markov(4)
##M.parseText(text.split(" "))
    
cr = """<<THIS ELECTRONIC VERSION OF THE COMPLETE WORKS OF WILLIAM
SHAKESPEARE IS COPYRIGHT 1990-1993 BY WORLD LIBRARY, INC., AND IS
PROVIDED BY PROJECT GUTENBERG ETEXT OF ILLINOIS BENEDICTINE COLLEGE
WITH PERMISSION.  ELECTRONIC AND MACHINE READABLE COPIES MAY BE
DISTRIBUTED SO LONG AS SUCH COPIES (1) ARE FOR YOUR OR OTHERS
PERSONAL USE ONLY, AND (2) ARE NOT DISTRIBUTED OR USED
COMMERCIALLY.  PROHIBITED COMMERCIAL DISTRIBUTION INCLUDES BY ANY
SERVICE THAT CHARGES FOR DOWNLOAD TIME OR FOR MEMBERSHIP.>>"""
with open("corpus\\shakespear.txt") as f:
    text = f.read().lower()
    text = text.replace(cr,"")
    lines = [i.strip() for i in text.split("\n")]
    S = Markov(5, noteStarts=True)
    S.parseText(lines)

    
####
####def test_getRandom():
####    k=random.choice(list(S.dict.keys()))
####
####def test_getElement():
####    k=S.dict.popitem()
####print(timeit("test_getRandom()", setup="from __main__ import test_getRandom", number=10000))
####print(timeit("test_getElement()", setup="from __main__ import test_getElement", number=10000))
##
##class Markov2(object):
##    def __init__(self, samples, order, minLength):
##        self.order = order
##        self.minLength = minLength
##        self.chains = {}
##        self.used = []
##        self.samples = [i.strip().upper() for i in samples if len(i) > order]
##        for word in self.samples:
##            for letter in xrange(len(word)-order):
##                token = word[letter:letter+order]
##                entries = self.chains.setdefault(token, list())
##                entries.append(word[letter + order])
##
##    def next(self):
##        s = ""; 
##        while True:
##            n = random.choice(self.samples)
##            i = random.randint(0, len(n) - self.order)
##            s = n[i:i+self.order]
##            while len(s) < len(n):
##                i = random.randint(0, len(s) - self.order)
##                token = s[i:i+self.order]
##                if token not in self.chains:
##                    break 
##                s += random.choice(self.chains[token])
##            s = s[0] + s[1:].lower()
##            if not (s in self.samples or s in self.used or len(s) < self.minLength):
##                break
##        self.used.append(s);
##        return s;
##
##    def reset(self):
##        self.used.Clear()
##
