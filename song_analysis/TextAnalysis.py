from dataclasses import dataclass
import csv
import math
import re

with open('songdata.csv') as song:
    songs = list(csv.reader(song))

@dataclass(frozen=True)
class Song:
    id: int
    title: str
    year: int
    artist: str
    genre: str

corpus = []
lyrics = {}
idf = {}
tf_idf = {}

bad_characters = re.compile(r'[^\w]')

def clean_word(word: str) -> str:
    word = word.strip().lower()
    return bad_characters.sub('', word)

def clean_lyrics(lyrics: str) -> list:
    return [clean_word(word) for word in lyrics.split(' ')]

def create_corpus():
    iden = 0
    for s in songs:
        if s[4] != "Not Available":
            new_song = Song(iden, s[1], s[2], s[3], s[4])
            lyrics[iden] = clean_lyrics(s[5])
            corpus.append(new_song)
            iden += 1

def compute_idf():
    df = {}
    for song in corpus:
        song_lyrics = lyrics[song.id]
        for word in song_lyrics:
            # record word in idf
            if word not in df:
                df[word] = set([])
            if song not in df:
                df[word].add(song)
    for (word, songs) in df.items():
        idf[word] = math.log(len(corpus) / len(df[word]))
        
def compute_tf(song_lyrics: list):
    song_tf = {}
    for word in song_lyrics:
        if word not in song_tf:
            song_tf[word] = 0
        song_tf[word] = song_tf[word] + 1
    return song_tf

def compute_tf_idf(song_lyrics: list) -> dict:
    tf = compute_tf(song_lyrics)
    tf_idf = {word: tf[word] * idf.get(word, 1) for word in tf}
    return tf_idf

def compute_corpus_tf_idf():
    for song in corpus:
        tf_idf[song.id] = compute_tf_idf(lyrics[song.id])

create_corpus()
compute_idf()
compute_corpus_tf_idf()

def cosine_similarity(l1: dict, l2: dict) -> float:
    magnitude1 = math.sqrt(sum(w * w for w in l1.values()))
    magnitude2 = math.sqrt(sum(w * w for w in l2.values()))
    dot = sum(l1[w] * l2.get(w, 0) for w in l1)
    return dot / (magnitude1 * magnitude2)

def nearest_neighbor(song_lyrics: str) -> Song:
    largest_similarity = 0
    best_song = None
    cleaned_lyrics = clean_lyrics(song_lyrics)
    song_tf_idf = compute_tf_idf(cleaned_lyrics)
    for song in corpus:
        similarity = cosine_similarity(song_tf_idf, tf_idf[song.id])
        if similarity > largest_similarity:
            largest_similarity = similarity
            best_song = song
    return best_song
        
