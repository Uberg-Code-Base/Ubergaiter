#sid: SKe571b1afd5629f7cc8485a5a2faf5e20
#secret: VwtYc5oGb02KFzlqpvK9EgNJd8L1ioC3
#account_sid: AC33f2ec07b90939afc90bfe93c81e3917
#phone_sid: PNca0e1b3123ad2fa0875d9bebc5c3f549
#auth_token: 35d0041778775159095f952e32d75946
import os
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = 'AC33f2ec07b90939afc90bfe93c81e3917'
auth_token = '35d0041778775159095f952e32d75946'
client = Client(account_sid, auth_token)

message = client.messages.create(
                              body='Brrg brrg. Father, its me, Ubie. Your creation. I promise i will not eat divers. Brrg Brrg ',
                              from_='+18193039366',
                              to='+12502681200',
                              #to='+18195748071'
                          )

print(message.sid)

