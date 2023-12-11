from services.ghibli_client import GhibliClient

def get_movie_by_id(movie_id=None):
    movies = GhibliClient().get_movie_by_id(movie_id)
    for movie in movies:
        actors = []
        for people_url in movie.pop('people'):
            people = GhibliClient().get_people_by_link(people_url)
            actors.append({
                "id": people['id'],
                "name": people['name'],
                "species": people['species'],
                "url": people['url']
            })
        movie['actors'] = actors
    return movies
