# pylint: disable=C0103, missing-docstring

import sqlite3

conn = sqlite3.connect('data/movies.sqlite')
a = conn.cursor()

def detailed_movies(db):
    '''return the list of movies with their genres and director name'''
    query = """
    SELECT m.title, m.genres, d.name
    FROM movies m
    JOIN directors d ON director_id = d.id
    """
    db.execute(query)
    answer1 = db.fetchall()
    return answer1


def late_released_movies(db):
    '''return the list of all movies released after their director death'''
    query = """
    SELECT title
    FROM movies
    JOIN directors d ON director_id = d.id
    WHERE start_year > d.death_year
    """
    db.execute(query)
    answer2 = db.fetchall()
    return [tuple[0] for tuple in answer2]


def stats_on(db, genre_name):
    '''return a dict of stats for a given genre'''
    query = f"""
    SELECT genres, COUNT(id), ROUND(AVG(minutes), 2)
    FROM movies
    WHERE genres = "{genre_name}"
    GROUP BY genres
    """
    db.execute(query)
    answer3 = db.fetchone()
    return {
    'genre': answer3[0],
    'number_of_movies': answer3[1],
    'avg_length': answer3[2]
    }




def top_five_directors_for(db, genre_name):
    '''return the top 5 of the directors with the most movies for a given genre'''
    query = f"""
    SELECT name, COUNT(m.director_id)
    FROM directors
    JOIN movies m ON m.director_id = directors.id
    WHERE m.genres = "{genre_name}"
    GROUP BY name
    ORDER BY
    COUNT(m.director_id) DESC,
    name ASC
    LIMIT 5
    """
    db.execute(query)
    answer4 = db.fetchall()
    return answer4


def movie_duration_buckets(db):
    '''return the movie counts grouped by bucket of 30 min duration'''
    query = """
    SELECT (minutes/30 + 1)*30 AS bin,
    COUNT(id) AS movie_count
    FROM movies
    WHERE bin IS NOT NULL
    GROUP BY bin
    """
    db.execute(query)
    answer5 = db.fetchall()
    return answer5

print(movie_duration_buckets(a))


def top_five_youngest_newly_directors(db):
    '''return the top 5 youngest directors when they direct their first movie'''
    query = """
        SELECT
            directors.name,
            movies.start_year - directors.birth_year age
        FROM directors
        JOIN movies ON directors.id = movies.director_id
        GROUP BY directors.name
        HAVING age IS NOT NULL
        ORDER BY age
        LIMIT 5
    """
    db.execute(query)
    directors = db.fetchall()
    return directors
    # $CHALLENGIFY_END
