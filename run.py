from quack import qUAck

client = qUAck(filename = 'qUAckrc.sample')
messages = client.get_folder_messages('Private')

for message in messages:
  print message
  