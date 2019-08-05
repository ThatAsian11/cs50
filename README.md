# Anubis

This app uses the TheMovieDB API to fetch movie and tv show data for various uses

The app can do the following:
- **Search**: The user can search for any movie or TV show and the app will fetch the response from the API
- **Trending**: The app will display the trending movies or TV shows of the week
- **Content**: Additional data about a particular movie or show can viewed by clicking on it
- **Watchlist**: The user can add any content to their watchlist
    - They can see all of the content in their watchlist to keep track of what to watch
    - Items can be marked as "watched" 

The API sometimes fails to return a response so the page may need to be reloaded if `Search` or `Trending` fail