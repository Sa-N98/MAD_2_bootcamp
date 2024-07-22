popular_music_artists = [
    "Taylor Swift", "Drake", "Ariana Grande", "Billie Eilish", "Post Malone",
    "Ed Sheeran", "The Weeknd", "Beyoncé", "Rihanna", "Justin Bieber",
    "Kanye West", "Dua Lipa", "Bruno Mars", "Lady Gaga", "Travis Scott",
    "Cardi B", "Selena Gomez", "Harry Styles", "Khalid", "Shawn Mendes",
    "Adele", "Megan Thee Stallion", "Olivia Rodrigo", "Bad Bunny", "Doja Cat",
    "Lil Nas X", "J Balvin", "Halsey", "Lil Baby", "Lizzo",
    "Nicki Minaj", "Camila Cabello", "Imagine Dragons", "Chris Brown", "Maroon 5",
    "Future", "SZA", "Sam Smith", "Demi Lovato", "Katy Perry",
    "J. Cole", "Juice WRLD", "Lana Del Rey", "Anuel AA", "Rosalía",
    "Shakira", "Maluma", "Karol G", "BLACKPINK", "BTS",
    "Miley Cyrus", "Luke Combs", "The Chainsmokers", "Marshmello", "John Legend",
    "Lil Uzi Vert", "21 Savage", "DJ Khaled", "Cardi B", "Kendrick Lamar",
    "Zayn", "Alicia Keys", "Kane Brown", "Jason Derulo", "Enrique Iglesias",
    "Nicky Jam", "Tove Lo", "Jennifer Lopez", "A Boogie wit da Hoodie", "YG",
    "Roddy Ricch", "Giveon", "Sia", "Charlie Puth", "G-Eazy",
    "Young Thug", "Bryson Tiller", "Tyga", "Normani", "Bazzi",
    "Tinashe", "Rita Ora", "Summer Walker", "Tory Lanez", "Anderson .Paak",
    "Saweetie", "Maren Morris", "Dan + Shay", "Florida Georgia Line", "Thomas Rhett",
    "Kacey Musgraves", "Lil Wayne", "Pitbull", "Jonas Brothers", "Ellie Goulding",
    "Kelly Clarkson", "Panic! At The Disco", "H.E.R.", "Shakira"
]


output=[]



for x in popular_music_artists:
    y = x.split(" ")[0]
    sql_template= f"insert into user (username, email, password, user_type) values ('{x}', '{y}@email.org', 1234, 'artist')"
    output.append(sql_template)

# for  i in output:
#     print(i,';')


import musicbrainzngs
musicbrainzngs.set_useragent("Example music app", "0.1", "http://example.com/music")


# for x in popular_music_artists:
result = musicbrainzngs.search_artists(artist='Taylor Swift')
print(result['artist-list'][0]['name'])
print(result['artist-list'][0]['id'])
artist_id = result['artist-list'][0]['id']
print()

releases = musicbrainzngs.get_artist_by_id(id=artist_id, includes=["release-groups"], release_type=["album", "ep"])
print(releases)
