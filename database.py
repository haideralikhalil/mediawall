# Access Firebase database
from google.cloud import firestore

# Add a new user to the database
db = firestore.Client.from_service_account_json('key.json')
doc_ref = db.collection('channels').document('muhammad@gmail.com')
doc_ref.set({
    'name': 'Aljaheera',
    'url': 'https://www.youtube.com/watch?v=gCNeDWCI0vo',
   
})

# Then query to list all users
users_ref = db.collection('channels')

for doc in users_ref.stream():
    print('{} => {}'.format(doc.id, doc.to_dict()))