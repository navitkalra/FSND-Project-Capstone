import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Actors, Movies

# TEST CASE CLASS
class CastingAgencyTestCase(unittest.TestCase):

    def setUp(self):

        DATABASE_URL = 'postgres://postgres:12345678@localhost:5432/castagency'
        ASSISTANT_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ikg2YlZOc0RTelUzMnNxOHhlTzRKeiJ9.eyJpc3MiOiJodHRwczovL2ZzbmRrYWxyYTEuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlZGQxNDA4MjI5ZGNlMDAxM2Q3Mjk5ZCIsImF1ZCI6ImNhZ2VuY3kiLCJpYXQiOjE1OTIzMjMyNjksImV4cCI6MTU5MjQwOTY2OSwiYXpwIjoiWUR6SXVIeWFhR3hIcDhpZUVwUVV4S3BNeUNNUE4xakEiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.moRMR0jivAe5HAENj8yMoNR9WJHU7aVztyMAgMOpSYNg7iEGfp3Gbhlq-6DZu8YEHg5_RhtBcaX6hW-VVT9Y5zmZhfo-kf532swrV2A-ZNCM7O1_WP3jLlrasjBcl5hSouWx0rC8tR7esVPAazW8LmpstBnRYo3ietSlLgRkHRoYSIWar7yUW2eqCmnx9CM6qqfPpe2Bn8q7gy33I0RAiw5sRUUPlsa9RuAEcVRmdjO5USN2cmPPv85olQhVhMBL8bubx3lIGSPmrsqAaUwXBADCiuxakFu0nT3nksJiUfcBDbIEKfE7rmfiWnbIOkwEnJ3FFmNgeHXf-aGeJp8qAw'
        DIRECTOR_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ikg2YlZOc0RTelUzMnNxOHhlTzRKeiJ9.eyJpc3MiOiJodHRwczovL2ZzbmRrYWxyYTEuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlZTUzYTA1ZTE4MzI3MDAxOTI3N2ZhMiIsImF1ZCI6ImNhZ2VuY3kiLCJpYXQiOjE1OTIzMjMyMTUsImV4cCI6MTU5MjQwOTYxNSwiYXpwIjoiWUR6SXVIeWFhR3hIcDhpZUVwUVV4S3BNeUNNUE4xakEiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.JA6q9J75d-JKTwl8ZIQmTtWceLHVtJOYj4DzpOL8xE6EWCMtuaz-zbiokzAlI6Qyqi3CGgny-X8rjjOWwUEsXBOgGEjcYC75IBh2t_enEoJFb9nHYnwjOjMwNvW8F-9u3u4aGpB3ZWPNTzdqD1GybGbo3nm0k4ua4iAabOKeGcUrlpEtUp2mtowUceHry7B1Uhrd5ZQLITMG3JgMyJpBAkt1VP6mB_L1QIU1rIYhCafEfmLd3ZpxjF-pprKBIXvL5Z96q2mcXXVRtqK4Fgkct4ZPhAKiPqSk7ZkN_aH8jnp9Esqc40DdENaGHHLVcVj9dcSg3PKWswVsNhvGYfpPXA'
        PRODUCER_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ikg2YlZOc0RTelUzMnNxOHhlTzRKeiJ9.eyJpc3MiOiJodHRwczovL2ZzbmRrYWxyYTEuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlZDdmODAyMzQ3ZjNkMDAxM2ZiOWQ3NyIsImF1ZCI6ImNhZ2VuY3kiLCJpYXQiOjE1OTIzMjMxNjAsImV4cCI6MTU5MjQwOTU2MCwiYXpwIjoiWUR6SXVIeWFhR3hIcDhpZUVwUVV4S3BNeUNNUE4xakEiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.nHauEyCOdbhfQFjdK-uOjMb0lziMOD99eZaGON434NEIEZKfOZj6ojfUAACQDbZtroXdumOhsfD2EK4h2Xm38G-OiIWcPEkPTrYv0OrDTADvnXVFx500fM_0zwR1LoBlnWxNlWQy7g0KpU_C6BIRzxHuJ8u2sm9GJPbVnjMDIc3Cduvvm8Z8sl90KEF79uNlrN0xmlft1POwsKAd3oItDf8vlp_xIGdYCW2iT3nJg8e5E-pX351-KfApZPUZEJqVZW1yktCozz3o9pjwEKgVzNYr0S_7BUrQunVufPXwJ9Cl1g3yMNFxNWD8EZjwYtlAuZfEDTh2kvZ7Z7B95I70ZQ'

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
            'age' : 45,
            'gender': 'MALE'
        }

        self.post_actor1 = {
            'name' : "George",
            'age' : 28,
            'gender': 'MALE'
        }

        self.post_actor2 = {
            'name' : "Markus",
            'age' : 39,
            'gender': 'MALE'
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

# POST Positive case - Director Role
    def test_post_new_actor1(self):
        res = self.client().post('/actors',
                                 json=self.post_actor1,
                                 headers=self.director_auth_header)
        data = json.loads(res.data)

        actor = Actors.query.filter_by(id=data['actor-added']).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNotNone(actor)

# POST Positive case - Producer Role
    def test_post_new_actor2(self):
        res = self.client().post('/actors',
                                 json=self.post_actor2,
                                 headers=self.producer_auth_header)
        data = json.loads(res.data)

        actor = Actors.query.filter_by(id=data['actor-added']).one_or_none()

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
        self.assertEqual(data['message'], 'unprocessable')

# POST Negative Case - Add actor with missing gender - Director Role
    def test_post_new_actor_gender_missing(self):
        res = self.client().post('/actors',
                                 json=self.post_actor_gender_missing,
                                 headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'unprocessable')

# DELETE Positive Case - Deleting an existing actor - Director Role
    def test_delete_actor(self):
        res = self.client().post('/actors', json=self.post_actor,
                                 headers=self.director_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        actor_id = data['actor-added']

        res = self.client().delete('/actors/{}'.format(actor_id),
                                   headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['actor-deleted'], actor_id)

# DELETE Negative Case actor not found - Director Role
    def test_delete_actor_not_found(self):
        res = self.client().delete('/actors/999',
                                   headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Not found')

# PATCH Positive case - Update age of an existing
# actor - Director Role
    def test_patch_actor(self):
        res = self.client().patch('/actors/2',
                                  json=self.patch_actor_on_age,
                                  headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['actor-updated'], 2)

# PATCH Negative case - Update age for non-existent actor
# - Director Role
    def test_patch_actor_not_found(self):
        res = self.client().patch('/actors/99',
                                  json=self.patch_actor_on_age,
                                  headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Not found')

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
        self.assertEqual(data['message'], 'Permission not found.')

# RBAC DELETE Negative Case - Delete an existing actor
# without appropriate permission
    def test_delete_actor_wrong_auth(self):
        res = self.client().delete('/actors/10',
                                   headers=self.assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Permission not found.')


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

# POST Positive case - Producer Role
    def test_post_new_movie2(self):
        res = self.client().post('/movies', json=self.post_movie2,
                                 headers=self.producer_auth_header)
        data = json.loads(res.data)

        movie = Movies.query.filter_by(id=data['movie-added']).one_or_none()

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
        self.assertEqual(data['message'], 'unprocessable')

# POST Negative Case - Add movie with missing release date
# - Producer Role
    def test_post_new_movie_reldate_missing(self):
        res = self.client().post('/movies',
                                 json=self.post_movie_reldate_missing,
                                 headers=self.producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'unprocessable')

# DELETE Positive Case - Deleting an existing movie - Producer Role
    def test_delete_movie(self):
        res = self.client().post('/movies',
                                 json=self.post_movie,
                                 headers=self.producer_auth_header)
        data = json.loads(res.data)

        movie_id = data['movie-added']

        res = self.client().delete('/movies/{}'.format(movie_id),
                                   headers=self.producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['movie-deleted'], movie_id)

# DELETE Negative Case movie not found - Producer Role
    def test_delete_movie_not_found(self):
        res = self.client().delete('/movies/777',
                                   headers=self.producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Not found')

# PATCH Positive case - Update Release Date of
# an existing movie - Director Role
    def test_patch_movie(self):
        res = self.client().patch('/movies/2',
                                  json=self.patch_movie_on_reldate,
                                  headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['movie-updated'], 2)

# PATCH Negative case - Update Release Date for
# non-existent movie - Director Role
    def test_patch_movie_not_found(self):
        res = self.client().patch('/movies/99',
                                  json=self.patch_movie_on_reldate,
                                  headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Not found')

# RBAC - Test Cases:
# RBAC GET movies w/o Authorization header
    def test_get_movies_no_auth(self):
        res = self.client().get('/movies?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'],
                         'authorization_header_missing')

# RBAC POST movies with wrong Authorization header - Director Role
    def test_post_movie_wrong_auth(self):
        res = self.client().post('/movies', json=self.post_movie1,
                                 headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Permission not found')

# RBAC DELETE Negative Case - Delete an existing movie
# without appropriate permission
    def test_delete_movie_wrong_auth(self):
        res = self.client().delete('/movies/8',
                                   headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Permission not found')

# run 'python test_app.py' to start tests
if __name__ == "__main__":
    unittest.main()
