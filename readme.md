# Motivation and Questions
The motivation behind this project was very simple. First, I wanted to experiment with Airflow and Tableau. Since these tools can be somewhat linked, I knew I could use them in a single project. Secondly, I love music and have been playing guitar for a long time, and I wanted to incorporate that in some way.

To that end, I decided on the following problem. On a fundamental level, there's differences between different countries' musical preferences. For example, US pop music usually is composed of chord progressions composed of 4 chords; however, Japanese pop is noted for having much longer, much more complex chord progressions (both of these statements obviously reflect average behavior and are not hard rules). [This](https://www.youtube.com/watch?v=QtPx6WdNM30) is a short video that shows this exact concept. I knew Spotify had audio feature metadata built into their API , and so my question became:

### Do Spotify's audio features reflect differences between different countries' user preferences?

To create some variability, I chose three countries: USA, Japan, and El Salvador. I chose the US as its pop scene is arguably the most influential in the world. I'm from the US, so I'm also most familiar with this range of music. Japan was chosen a) because I like Japanese music, and b) because Japanese culture is very much in style globally. Japanese media is much more globally consumed than ever before, and Japanese tourism is exploding (see [here](https://www.tourism.jp/en/tourism-database/stats/)). The simple reason behind adding El Salvador is my wife's family is from there, so we listen to a lot of Latin music. I told my wife about the project and that one of the audio features is danceability, so a second question arose:

### Do users in El Salvador prefer more danceable tracks than other countries?

One issue is that the Spotify doesn't provide user counts per country, so I'm assuming that at the very least the samples will be representative of the population, if not that the users sampled will have the same size.

To see more about the audio features meta data offered by Spotify, see [here](https://developer.spotify.com/documentation/web-api/reference/get-audio-features).

# Methodology

In order to answer these questions, I decided to use the daily Top 50 playlists that Spotify creates based on user habits in a specific country. These playlists provide a great way to understand what most users in a country like at a given time, and also document any major changes such as a new album being released by a popular artist. These reportedly get recalibrated each day, so it might show a good amount of change depending on how long I ran the program.

From a technical perspective, my stack included the following software:

- postgres, for storage of the data locally,
- airflow, to run a docker container which would execute my ETL pipeline,
- Tableau, to show off the results and do some analysis.

I decided to let airflow run daily for 2 weeks. During the extract phase, I did some null-checking to make sure I was only pulling in actual values. Trying to accommodate for null values in the audio features meta data would be very difficult, and would probably rely on some form of clustering of individual artist's music. Considering the scope, I decided to focus on making sure the artist and spotify uri's were filled, so that I could at least get that data at a later date if possible. As far as any transformations, I made sure the data was in the right order for easy loading and debugging. 

# Results

I was able to collect 213 records in 2 weeks time. The graph below in fact indicates that a good percentage of that change was due to the release of Kanye West's most recent album. Another interesting takeaway from this graph is music preferences in El Salvador: unlike the US and Japan, the artists with the top tracks are not "from" the country they are associated with. Both Karol G and Feid are from Columbia, while Bad Bunny is from Puerto Rico.

![Country/Artist Counts](<images/Spotify Records Counts.png>)

To answer my questions from above, the following graphs below provide somewhat of a compelling answer. Based on both the questions I was asking and a correlation analysis I did in [this](https://github.com/PJ6451/spotify_project/blob/main/genre_correllation_study.ipynb) notebook, I decided to focus on 4 specific features:

- danceability: a measure from 0 to 1 on how danceable a track is, 0 being sit and 1 being dance
- valence: a measure from 0 to 1 describing how positive a track is, 0 being sad and 1 being happy
- mode: a value of 0 or 1 describing the key of a song, 0 being that the song is minor (typically sad) and 1 being major (typically happy)
- energy: a value from 0 to 1 describing the "intensity and activity" of a song. The API doc describes 0 as being like a classical piece, while a 1 might be metal music.

From a real world perspective, the only measure I'm familiar with measuring is the mode. Telling a minor song from a major song is pretty easy to do in most cases. The other measures are potentially very subjective, and are based probably on some combination of programmer logic and AI (like any good classification system). Energy and Valence do have some strong correlation in this sample, so there also might be some overlap in terms of what's being measured. My reasoning for choosing both is that they scored fairly high (in terms of absolute value) on the correlation matrix.

![alt text](<images/Spotify Records Average Feature Value by Country.png>)

Using these graphs, I made the following generalizations:

- Japanese users prefer more energetic and positive music in a major key, but also don't care as much about danceability as users in the US and El Salvador.
- Users in El Salvador prefer their music to be more danceable (my wife was happy to hear this); while users have a stronger preference for more energetic and positive tracks than the US, users also show a preference for songs in a minor key.
- US user preferences are very middle of the road in terms of key and danceability, but also like less positive and low energy tracks than the other countries.

# Conclusion

Let's return to my questions. First,

### Do Spotify's audio features reflect any differences between different countries' music preferences?

Secondly,

### Do users in El Salvador prefer more danceable tracks than other countries?

From the graphs above showing average values per country, the answer to both is yes, at least from this sample. These playlists probably change quite a bit in a given year, and it could be that different times would reflect different preferences. One way to test this would be collecting all the data for a given year, or even looking at YoY trends. One question that could change this is if there's any bias in the way Spotify measures these values. There's also the question of Kanye's new album skewing the data, but filtering out those values yielded very similar results in terms of the average values (it was also cool that a real world event influenced my project). To see these and other dashboards I made for this project, see [here](https://public.tableau.com/app/profile/michael.johnson5530/vizzes). 

From a technical perspective, getting airflow and docker running on a Mac was both fun and complicated. There was some memory leackage somewhere, although I was never able to pinpoint exactly where. Some forums suggested this was an issue with Docker and the new Apple chips, others suggested it might be an issue with Docker Desktop. Regardless, I solved this by just restarting Docker once a week. Airflow is extremely easy to use, and in the future I'd try dropping the psycopg2 requirement for the loading phase and just use airflow's postgres operators.

In regards to Tableau, it is extremely user friendly. This is unfortunately not the case for other viz software I've used, and I can see why it's maintained it's user base even with other software like PowerBI and Looker gaining more popularity.

Overall this was a lot of fun, and I'm currently considering what my next project will be.
