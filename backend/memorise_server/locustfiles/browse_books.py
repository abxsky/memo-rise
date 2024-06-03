from locust import HttpUser, task, between
from random import randint

#Stress Testing

class WebsiteUser(HttpUser):
    def on_start(self):
        response = self.client.post('/store/carts/')
        result = response.json()
        self.cart_id = result['id']
        
    wait_time = between(1,5)
    @task(2)
    def view_books(self):
        category_id = randint(1,5)
        self.client.get(f'/store/books/?category_id={category_id}', name='/store/books')

    @task(4)
    def view_book(self):
        book_id = randint(2,10)
        self.client.get(f'/store/books/{book_id}', name='/store/books/:id')
    
    @task(1)
    def add_to_cart(self):
        book_id = randint(2,10)
        self.client.post(
            f'/store/carts/{self.cart_id}/items/',
            name='/store/carts/items/',
            json={'book_id':book_id, 'quantity': 1}
        )

