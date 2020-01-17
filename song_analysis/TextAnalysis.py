import csv

with open('songdata.csv') as song:
     songs = list(csv.reader(song))

@dataclass
class Song:
    artist: str
    title: str
    lyrics: str
    id: int

    def __hash__(self):
        return hash(self.artist, self.title, self.lyrics, self.id)

corpus = []
iden = 0

def createCorpus():
    for s in songs:
        newSong = Song()
        newSong.artist = s[0]
        newSong.title = s[1]
        newSong.lyrics = s[2]
        newSong.id = iden
        iden += 1
        corpus.append(newSong)

def tf-idf():
    idf = {}
    songCount = {}
    for song in corpus:
        count = {}
        currLyrics = song.lyrics.split(" ")
        for word in currLyrics:
            if word in idf:
                if song not in idf:
                    idf[word].add(song)
            else:
                idf[word] = Set()
                idf[word].add(song)
            if word in count:
                count[word] = curr[word] + 1
            else:
                count[word] = 1
        songCount[song.id] = count
    for sc in songCount:
        for curr in sc:
            
createCorpus()
textFrequency()
