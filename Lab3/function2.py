movies = [
{
"name": "Usual Suspects", 
"imdb": 7.0,
"category": "Thriller"
},
{
"name": "Hitman",
"imdb": 6.3,
"category": "Action"
},
{
"name": "Dark Knight",
"imdb": 9.0,
"category": "Adventure"
},
{
"name": "The Help",
"imdb": 8.0,
"category": "Drama"
},
{
"name": "The Choice",
"imdb": 6.2,
"category": "Romance"
},
{
"name": "Colonia",
"imdb": 7.4,
"category": "Romance"
},
{
"name": "Love",
"imdb": 6.0,
"category": "Romance"
},
{
"name": "Bride Wars",
"imdb": 5.4,
"category": "Romance"
},
{
"name": "AlphaJet",
"imdb": 3.2,
"category": "War"
},
{
"name": "Ringing Crime",
"imdb": 4.0,
"category": "Crime"
},
{
"name": "Joking muck",
"imdb": 7.2,
"category": "Comedy"
},
{
"name": "What is the name",
"imdb": 9.2,
"category": "Suspense"
},
{
"name": "Detective",
"imdb": 7.0,
"category": "Suspense"
},
{
"name": "Exam",
"imdb": 4.2,
"category": "Thriller"
},
{
"name": "We Two",
"imdb": 7.2,
"category": "Romance"
}
]

def is_it_higher_than(movie):
    return movie["imdb"] > 5.5


def score_above (movies):
    filtered_movies = []   
    for movie in movies:   
        if movie["imdb"] > 5.5:   
            filtered_movies.append(movie)   
    return filtered_movies   


def movies_by_category(movies, category):
    filtered_by_category_movies = []   
    for movie in movies:   
        if movie["category"] == category:   
            filtered_by_category_movies.append(movie)   
    return filtered_by_category_movies
 
 
def average_imdb(movies):
    av_imdb = 0   
    for movie in movies:  
        av_imdb += movie["imdb"]   
    return av_imdb / len(movies)   

 
def average_imdb_by_category(movies, category):
    category_movies = movies_by_category(movies, category)
    return average_imdb(category_movies)

 
print(is_it_higher_than(movies[0]))  
print(score_above(movies))   
print(movies_by_category(movies,"Romance"))   
print(average_imdb(movies))   
print(average_imdb_by_category(movies, "Romance"))   