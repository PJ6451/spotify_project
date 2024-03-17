# Motivation and Questions
The motivation behind this project was very simple. First, I wanted to mess around with Airflow and Tableau. Since these tools can be somewhat linked, I figured it might not hurt to combine them into a single project. Secondly, I love music and have been playing guitar for a long time, and I wanted to incorporate that knowledge into this project.

To that end, I decided on an easy problem. On a fundamental level, there's differences between different countries musical preferences. For example, US pop music usually is composed of chord progressions compossed of 4 chords; however, Japanese pop is noted for having much longer, much more complex chord progressions (both of these statements obviously reflect average behavior and are not hard rules). I knew Spotify had audio feature metadata built into their API , and so my question became:

### Do Spotify's audio features reflect any differnce between different countries' music?

To create some variability, I chose three countries: USA, Japan, and El Salvador. The simple reason behind adding El Salvador was my wife's family is from there, so we listen to a lot of Latin music. I told my wife about the project and how one of the audio features is danceability, so a second question arose:

### Is the music of El Salvador more danceable than other countries?

I was informated that Spotify would probably be wrong otherwise. To see more about the audio features meta data offered by Spotify, see [here](https://developer.spotify.com/documentation/web-api/reference/get-audio-features).

# Methodology

In order to answer these questions, I decided to use the daily Top 50 playlists that Spotify creates based on user habits in a specific country. This seamed like the easiest way to not only understand what most users in a country liked, but also see if anything changed based on events in music (such as a new album being released by a global artist). These reportedly get recalibrated each day, so I figured it might show a good amount of change in that time.

From a technical perspective, I used the following software:

- postgres, for storage of the data locally,
- airflow, to run a docker container which would execute my ETL pipeline,
- Tableau, to show off the results and do some analysis.

I decided to let airflow run locally for 2 weeks, which seemed like a good amount of time to collect data.

# Results

I was able to collect a little over 200 records in 2 weeks time, much less than I expected. Since these are Top 50 lists, I expected to at least have 150 records, indicating no change in 2 weeks. The graph below in fact indicates that a good percentage of that change was due to the release of Kanye West's most recent album.

![Country/Artist Counts](<images/Spotify Records Counts.png>)

To answer my first question, the following graphs below provide somewhat of a compelling answer. Based on both the questions I was asking and a correllation analysis I did in [this](https://github.com/PJ6451/spotify_project/blob/main/genre_correllation_study.ipynb) notebook, I decided to focus on 4 specific features:

- danceability: a measure from 0 to 1 on how danceable a track is, 0 being sit and 1 being dance
- valence: a measure from 0 to 1 describing how positive a track is, 0 being sad and 1 being happy
- mode: a value of 0 or 1 describing the key of a song, 0 being that the song is minor (typically sad) and 1 being major (typically happy)
- energy: a value from 0 to 1 describing the "intensity and activity" of a song. The API doc describes 0 as being like a classical piece, while a 1 might be metal music.

From a real world perspective, the only measure I'm familiar with measuring is the mode. Telling a minor song from a major song is pretty easy to do in most cases. The other measures are very subjective, and are based probably on some combination of subjectiveness and AI (like any good classification system). My reasoning for choosing them is that they scored fairly high (in terms of absolute value) on the correclation matrix.

![alt text](<images/Spotify Records Average Feature Value by Country.png>)

Using these graphs, I'm making the following generalizations:

- Japaense pop music is on average in a major key, and much more energetic and positive than the other countries
- Pop music in El Salvador is much more danceable (my wife was happy to hear this); while pop music there is more energetic and positive than the US pop music, it is also more often in a minor key
- US pop music is very middle of the road in terms of key and danceability, but is less positive and more low energy than the other countries.

In conclusion, we can answer yes to both of my questions, at least from this small sample. These playlists probably change quite a bit in a given year, and it could be that I chose a bad time to collect data. There's also the question of Kanye's new album skewing the data (after some fiddling with Tableau, the answer's remain the same), but it was very cool to see how a cultural event could influence collected data. To see these and other dashboards in Tableau Public, see [here](https://public.tableau.com/app/profile/michael.johnson5530/vizzes). 

From a technical perspective, getting airflow and docker running on a Mac was interesting. There's some memory leackage somewhere, although I was never able to pinpoint exactly where. Getting refamiarized with postgres is always fun, and never a chore (looking at my data provided in the csv, you can see I forgot how to do bigserial right). Tableau seems very similar to other visualization software I've used in previous roles. It is much more user friendly, which I really loved.

If I did this again, I'd maybe try and find a more dynamic source and be a little cleaner with my postgres. I'd also consider dropping psycopg2 for the loading phase, since I found out later that airflow has its own postgres operators. Overall this was a lot of fun, and I'm currently considering what my next project will be.