import csv

with open('songdata.csv') as song:
     songs = list(csv.reader(song))

@dataclass
class Song:
    artist: str
    title: str
    lyrics: str
    id: int

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
