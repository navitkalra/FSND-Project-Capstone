import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Actors, Movies

DATABASE_URL = 'postgres://postgres:12345678@localhost:5432/castagency'
ASSISTANT_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ikg2YlZOc0RTelUzMnNxOHhlTzRKeiJ9.eyJpc3MiOiJodHRwczovL2ZzbmRrYWxyYTEuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlZGQxNDA4MjI5ZGNlMDAxM2Q3Mjk5ZCIsImF1ZCI6ImNhZ2VuY3kiLCJpYXQiOjE1OTIyNTgwNDksImV4cCI6MTU5MjM0NDQ0OSwiYXpwIjoiWUR6SXVIeWFhR3hIcDhpZUVwUVV4S3BNeUNNUE4xakEiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.aTmqMMNUZneX5DPFGMc45zvBuyryYlbfSrChSdi-bvrXQE4S6ZWKAiJFNbRRq3QUandO6kpFZXGpjQz-4UbXHLrzLtCJ_sgOntAOk5UOx5v1AY2lUsiQUVJvUvd901kaYweL8GixnkYlDt_8wwfzdTacjDG3UMjiFhC3Eb_0S23pPzNSVrzV5CJxWiyfQwhBXYJluhhREA0K-4g-K2fgVTq3XQi9ko5tAMfIrUIhlobeTrS8XXv4rDT-yOLvZexuDHVG0KtYpxr59f7_jjPsb7YHbI4AN_KjI1Kek0F6T_C4r2bocLDi8TjYFbxPp2EJeLlMy6eaCCP3TLGg8kz46g'
DIRECTOR_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ikg2YlZOc0RTelUzMnNxOHhlTzRKeiJ9.eyJpc3MiOiJodHRwczovL2ZzbmRrYWxyYTEuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlZTUzYTA1ZTE4MzI3MDAxOTI3N2ZhMiIsImF1ZCI6ImNhZ2VuY3kiLCJpYXQiOjE1OTIyNTc5NzUsImV4cCI6MTU5MjM0NDM3NSwiYXpwIjoiWUR6SXVIeWFhR3hIcDhpZUVwUVV4S3BNeUNNUE4xakEiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.XZeQAeyR8sElZBOs5SpTeRzaBkeQfyV3AqzhOx9OHY4GlhjHHePyhkw6d3Xmov-lBa0atE2ibZfzY8Dp6x7cOm2IF4Bl9-bpXJkImRqHWP0fc-dibqC-er8ZKzZr76KnD4trrJTnZYNQ0cZAQ31fjuACHZE3Um_wkuGz98V6TOz_XDFrjn5GJj6hysDttGVk1nq5VOomeR0Bu6rmmF6xl44xT0Kqaa8EScNYwVE2FoDJmEkdQxx--xHploW9CpfJQ_8cJj__TAxEly7f4_yQJmAppPr_1zOd-E49wdohTmz3vGP2hfcSOvV3JEU9vA2XNLNlVvv_SygjjxS5h4v3FA'
PRODUCER_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ikg2YlZOc0RTelUzMnNxOHhlTzRKeiJ9.eyJpc3MiOiJodHRwczovL2ZzbmRrYWxyYTEuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlZDdmODAyMzQ3ZjNkMDAxM2ZiOWQ3NyIsImF1ZCI6ImNhZ2VuY3kiLCJpYXQiOjE1OTIyNTY5NTYsImV4cCI6MTU5MjM0MzM1NiwiYXpwIjoiWUR6SXVIeWFhR3hIcDhpZUVwUVV4S3BNeUNNUE4xakEiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.ZqzxHnojuU7x9YwNNMx4nNCRBni7cA-yPyqIKB7w8J_7omv8oUj9PlytGctv58iKL9-yakUDfDLjnxuLdkUOb_KR7OB9KIpAvIO3CjfBRVM4gRtugB14kixA72DsYJGDklrdxsgBnSZZ4mBnJA8NnWuOt-HDlaZMNh5ksTQVUJECieXoXS42XlWxCwxFyGw90tPIvXo91KR9xPRsytm4jkUAGnZkFDGGu1cYe0oJRkP8lwx9fGFDp0SOjA8dNRLU86FwiNypH5BwAv_pnE1vy7JUPpUZQEWMuApUbp7HlRridia95yLZUDse4Rp0m7hQUve_ShDduRquhEcNPDdLyQ'

# TEST CASE CLASS
class CastingAgencyTestCase(unittest.TestCase):

    def setUp(self):

#    self.assistant_auth_header= {'Authorization' : 'Bearer ' + os.environ['assistant_token']}
#    self.director_auth_header = {'Authorization' : 'Bearer ' + os.environ['director_token']}
#    self.producer_auth_header = {'Authorization' : 'Bearer ' + os.environ['producer_token']}
#    self.database_path = os.environ['DATABASE_URL']

        self.assistant_auth_header = {'Authorization' :
                                      'Bearer ' + ASSISTANT_TOKEN}
        self.director_auth_header = {'Authorization' :
                                     'Bearer ' + DIRECTOR_TOKEN}
        self.producer_auth_header = {'Authorization' :
                                     'Bearer ' + PRODUCER_TOKEN}
        self.database_path = DATABASE_URL

        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app, self.database_path)



#Test data set-up for all tests down under

        self.post_actor = {
            'name' : "Michael",
            'age' : 45
        }

        self.post_actor1 = {
            'name' : "George",
            'age' : 28
        }

        self.post_actor2 = {
            'name' : "Markus",
            'age' : 39
        }

        self.post_actor_name_missing = {
            'age' : 34,
            'gender': "MALE"
        }

        self.post_actor_gender_missing = {
            'age' : 34,
            'name': "John"
        }

        self.patch_actor_on_age = {
            'age' : 55
        }

        self.post_movie = {
            'title' : "SAMPLE MOVIE",
            'release_date' : "2090-10-10"
        }

        self.post_movie1 = {
            'title' : "MAHABHARATA",
            'release_date' : "2030-10-10"
        }

        self.post_movie2 = {
            'title' : "MAHABHARATA - 2",
            'release_date' : "2032-10-10"
        }

        self.post_movie_title_missing = {
            'release_date' : "2030-10-10"
        }

        self.post_movie_reldate_missing = {
            'title' : "RAMAYANA"
        }

        self.patch_movie_on_reldate = {
            'release_date' : "2035-10-10"
        }

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()


    def tearDown(self):
        pass



# Test cases for the Endpoints related to /actors
#------------------------------------------------
# GET Positive case - Assistant Role
    def test_get_actors1(self):
        res = self.client().get('/actors?page=1',
                                headers=self.assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actors']) > 0)

# GET Positive case - Director Role
    def test_get_actors2(self):
        res = self.client().get('/actors?page=1',
                                headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actors']) > 0)

# GET Positive case - Producer Role
    def test_get_actors3(self):
        res = self.client().get('/actors?page=1',
                                headers=self.producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actors']) > 0)

# GET Negative case - Invalid Page No. - Assistant Role
    def test_get_actors_not_found(self):
        res = self.client().get('/actors?page=99',
                                headers=self.assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Actors Not Found')

# POST Positive case - Director Role
    def test_post_new_actor1(self):
        res = self.client().post('/actors',
                                 json=self.post_actor1,
                                 headers=self.director_auth_header)
        data = json.loads(res.data)

        actor = Actors.query.filter_by(id=data['created']).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNotNone(actor)

# POST Positive case - Producer Role
    def test_post_new_actor2(self):
        res = self.client().post('/actors',
                                 json=self.post_actor2,
                                 headers=self.producer_auth_header)
        data = json.loads(res.data)

        actor = Actors.query.filter_by(id=data['created']).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNotNone(actor)

# POST Negative Case - Add actor with missing name
# - Director Role
    def test_post_new_actor_name_missing(self):
        res = self.client().post('/actors',
                                 json=self.post_actor_name_missing,
                                 headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'],
                         'Name is missing in request.')

# POST Negative Case - Add actor with missing gender - Director Role
    def test_post_new_actor_gender_missing(self):
        res = self.client().post('/actors',
                                 json=self.post_actor_gender_missing,
                                 headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'],
                         'Gender is missing in request.')

# DELETE Positive Case - Deleting an existing actor - Director Role
    def test_delete_actor(self):
        res = self.client().post('/actors', json=self.post_actor,
                                 headers=self.director_auth_header)
        data = json.loads(res.data)

        actor_id = data['created']
        res = self.client().delete('/actors/{}'.format(actor_id),
                                   headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], format(actor_id))

# DELETE Negative Case actor not found - Director Role
    def test_delete_actor_not_found(self):
        res = self.client().delete('/actors/999',
                                   headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'],
                         'Actor id 999 not found in database.')

# PATCH Positive case - Update age of an existing
# actor - Director Role
    def test_patch_actor1(self):
        res = self.client().patch('/actors/1',
                                  json=self.patch_actor_on_age,
                                  headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actor']) > 0)
        self.assertEqual(data['updated'], 1)

# PATCH Negative case - Update age for non-existent actor
# - Director Role
    def test_patch_actor_not_found(self):
        res = self.client().patch('/actors/99',
                                  json=self.patch_actor_on_age,
                                  headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Actor id 99 not found.')

# RBAC - Test Cases:
# RBAC GET actors w/o Authorization header
    def test_get_actors_no_auth(self):
        res = self.client().get('/actors?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'],
                         'Authorization header is expected.')

# RBAC POST actors with wrong Authorization header - Assistant Role
    def test_post_actor_wrong_auth(self):
        res = self.client().post('/actors',
                                 json=self.post_actor1,
                                 headers=self.assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'],
                         'Permission not found to add actor.')

# RBAC DELETE Negative Case - Delete an existing actor
# without appropriate permission
    def test_delete_actor_wrong_auth(self):
        res = self.client().delete('/actors/1',
                                   headers=self.assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'],
                         'Permission not found to delete actor.')


# Test cases for the Endpoints related to /movies
#------------------------------------------------
# GET Positive case - Assistant Role
    def test_get_movies1(self):
        res = self.client().get('/movies?page=1',
                                headers=self.assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['movies']) > 0)

# GET Positive case - Director Role
    def test_get_movies2(self):
        res = self.client().get('/movies?page=1',
                                headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['movies']) > 0)

# GET Positive case - Producer Role
    def test_get_movies3(self):
        res = self.client().get('/movies?page=1',
                                headers=self.producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['movies']) > 0)

# GET Negative case - Invalid Page No. - Assistant Role
    def test_get_movies_not_found(self):
        res = self.client().get('/movies?page=99',
                                headers=self.assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Movies Not Found')


# POST Positive case - Director Role
    def test_post_new_movie1(self):
        res = self.client().post('/movies', json=self.post_movie1,
                                 headers=self.director_auth_header)
        data = json.loads(res.data)

        movie = Movies.query.filter_by(id=data['created']).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNotNone(movie)

# POST Positive case - Producer Role
    def test_post_new_movie2(self):
        res = self.client().post('/movies', json=self.post_movie2,
                                 headers=self.producer_auth_header)
        data = json.loads(res.data)

        movie = Movies.query.filter_by(id=data['created']).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNotNone(movie)

# POST Negative Case - Add movie with missing title
# - Producer Role
    def test_post_new_movie_title_missing(self):
        res = self.client().post('/movies',
                                 json=self.post_movie_title_missing,
                                 headers=self.producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'],
                         'Title of Movie is missing in request.')

# POST Negative Case - Add movie with missing release date
# - Producer Role
    def test_post_new_movie_reldate_missing(self):
        res = self.client().post('/movies',
                                 json=self.post_movie_reldate_missing,
                                 headers=self.producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'],
                         'Release Date of Movie is missing in \
                         request.')

# DELETE Positive Case - Deleting an existing movie - Producer Role
    def test_delete_movie(self):
        res = self.client().post('/movies',
                                 json=self.post_movie,
                                 headers=self.producer_auth_header)
        data = json.loads(res.data)

        movie_id = data['created']
        res = self.client().delete('/movies/{}'.format(movie_id),
                                   headers=self.producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], format(movie_id))

# DELETE Negative Case movie not found - Producer Role
    def test_delete_movie_not_found(self):
        res = self.client().delete('/movies/777',
                                   headers=self.producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'],
                         'Movie id 777 not found in database.')

# PATCH Positive case - Update Release Date of
# an existing movie - Director Role
    def test_patch_movie(self):
        res = self.client().patch('/movies/1',
                                  json=self.patch_movie_on_reldate,
                                  headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['movie']) > 0)
        self.assertEqual(data['updated'], 1)

# PATCH Negative case - Update Release Date for
# non-existent movie - Director Role
    def test_patch_movie_not_found(self):
        res = self.client().patch('/movies/99',
                                  json=self.patch_movie_on_reldate,
                                  headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Movie id 99 not found.')

# RBAC - Test Cases:
# RBAC GET movies w/o Authorization header
    def test_get_movies_no_auth(self):
        res = self.client().get('/movies?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'],
                         'Authorization header is expected.')

# RBAC POST movies with wrong Authorization header - Director Role
    def test_post_movie_wrong_auth(self):
        res = self.client().post('/movies', json=self.post_movie1,
                                 headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'],
                         'Permission not found to add movie.')

# RBAC DELETE Negative Case - Delete an existing movie
# without appropriate permission
    def test_delete_movie_wrong_auth(self):
        res = self.client().delete('/actors/1',
                                   headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'],
                         'Permission not found to delete movie.')


# run 'python test_app.py' to start tests
if __name__ == "__main__":
    unittest.main()
