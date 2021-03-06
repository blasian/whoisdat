from projectoxford.Client import Client

#Face ID
faceClient = Client().face('9defe6b7bd8045eea6cccb8e4b8d5ddd')

personGroup = 'mlb'
cano = 'http://mlb.mlb.com/mlb/images/players/head_shot/429664.jpg'
canoswing = 'http://cdn.rsvlts.com/wp-content/uploads/2013/08/Robinson-Cano.jpg'
arod = 'http://cdn.blackenterprise.com/wp-content/blogs.dir/1/files/2013/04/Alex-Rodriguez-major-league-highest-salaried-players-black-enterprise.jpg'
pedro = 'http://i278.photobucket.com/albums/kk100/sillysyclone/Memorabilia_and_Sports_Cards/JorgeBonifacioandMe.jpg'

# detect faces in a second photo
detectResults = faceClient.detect({'url': pedro})
faceIds = []
for result in detectResults:
    faceIds.append(result['faceId'])

# identify any known faces from the second photo
identifyResults = faceClient.identify(personGroup, faceIds)
for result in identifyResults:
    for candidate in result['candidates']:
        confidence = candidate['confidence']
        personData = faceClient.person.get(personGroup, candidate['personId'])
        name = personData['name']
        print('identified {0} with {1}% confidence'.format(name, str(float(confidence) * 100)))

# READ BEFORE UNCOMMENTING
# removes the example person group from your subscription
# faceClient.personGroup.delete(personGroup)