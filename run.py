from quack import qUAck

client = qUAck(filename = 'qUAckrc')
#client.get_folders(subscribed_only = True)

#client.post_message(folder = 'Private', subject = 'quackjson Test', body = 'Hello', to = 'pwaring')

messages = client.get_folder_messages('Private')
#print messages

for message in messages:
  print message
  #full_msg = client.get_message(message['id'])
  
  #print full_msg