from projectoxford.Client import Client
client = Client()
faceClient = client.face('9defe6b7bd8045eea6cccb8e4b8d5ddd')

group = 'mlb'

print faceClient.person.list(group)