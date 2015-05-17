#!/usr/bin/python
import imaplib, email

import imaplib
import re
import os
import sys
import string
import csv

ATT_NONE = 0
ATT_ALL  = 1
ATT_POINTS    = 2
ATT_ALLOWANCE = 3
attLkup = ['none','all','points','allowance']

TGT_NONE = 0
TGT_CHILD3 = 1
TGT_CHILD2= 2
TGT_CHILD1 = 3 
targetLkup = ['none','child1','child2','child3']

EMAIL_ACCT = "someemail@gmail.com"
EMAIL_PASSWD = "somepassword"

# note that if you want to get text content (body) and the email contains
# multiple payloads (plaintext/ html), you must parse each message separately.
# use something like the following: (taken from a stackoverflow post)
def get_first_text_block(email_message_instance):
    maintype = email_message_instance.get_content_maintype()
    if maintype == 'multipart':
        for part in email_message_instance.get_payload():
            if part.get_content_maintype() == 'text':
                return part.get_payload()
    elif maintype == 'text':
        return email_message_instance.get_payload()

# gets the latest mail message and parses to see if it is from me or Mom
# and if so, deletes the email from the server and returns the txt
## RETURNS: emailTxt, goodToGo
def get_mail():
  mail = imaplib.IMAP4_SSL('imap.gmail.com')
  mail.login(EMAIL_ACCT, EMAIL_PASSWD)
  mail.list()
  # Out: list of "folders" aka labels in gmail.
  mail.select("inbox") # connect to inbox.
  
  result, data = mail.search(None, "ALL")
   
  ids = data[0] # data is a list.
  id_list = ids.split() # ids is a space separated string
  latest_email_id = id_list[-1] # get the latest
   
  result, data = mail.fetch(latest_email_id, "(RFC822)") # fetch the email body (RFC822) for the given ID
   
  raw_email = data[0][1] # here's the body, which is raw text of the whole email
  # including headers and alternate payloads
  
  # print raw_email
  
  email_message = email.message_from_string(raw_email)
   
  toAddr = email_message['To']
  print toAddr
   
  fromAddr = email.utils.parseaddr(email_message['From'])
  sender = ""
  if len(fromAddr) > 1:
    sender = fromAddr[1]
  else:
    sender = fromAddr[0]
  print sender
  isFromDad = re.match('.*dademail|.*dad',sender)
  isFromMom  = re.match('.*momemail|.*mom',sender)
  
  emailTxt = get_first_text_block(email_message)
  goodToGo = False 
  if isFromDad or isFromMom:
    print "From Mom or Dad!"
    goodToGo = True
   
  # print email_message.items() # print all headers
  
  print emailTxt

   
  # Delete the message if the parse was successful
  if goodToGo:
    print "Deleting Email!"
    mail.store(latest_email_id, '+FLAGS', '\\Deleted')
    mail.expunge()
  
  mail.close()
  mail.logout()
  return emailTxt, goodToGo

def parseCommand(emailTxt):
  target = TGT_NONE
  attribute = ATT_NONE
  value = 0

  # First lower the case
  lwrTxt = emailTxt.lower()

  # Next, get the attribute 
  if re.match('.*allowance|.*alw', lwrTxt):
    attribute = ATT_ALLOWANCE
    print "Command allowance!"
  elif re.match('.*points|.*pnt|.*pnts', lwrTxt):
    attribute = ATT_POINTS
    print "Command points!"
  elif re.match('.*all', lwrTxt):
    attribute = ATT_ALL
    print "Command all!"
  else:
    print "Unsupported attribute: " + lwrTxt

  # Then, get the target: child1|c1, child2|c2, child3|c3
  if re.match('.*child1|.*c1', lwrTxt):
    target = TGT_CHILD1
    print "Target child1!"
  elif re.match('.*child2|.*c2', lwrTxt):
    target = TGT_CHILD2
    print "Target child2!"
  elif re.match('.*child3|.*c3', lwrTxt):
    target = TGT_CHILD3
    print "Target child3!"
  else:
    print "Unsupported target: " + lwrTxt

  # Finally, get modifier value
  strNum = re.findall('[+-]?\d+(?:\.\d+)?', lwrTxt)
  print strNum
  num = 0
  if strNum:
    num = float(strNum[0])
  value = num

  print 'The Target = {0}, attribute = {1}, value = {2}.'.format(target,attribute,value)
  return target, attribute, value

# Line format: {target},{attribute},{value}
#     example: child1,allowance,20
#              child1,points,10
#              child3,points,20
#              child2,allowance,10
fname = '/home/root/scripts/database.txt'

# Parse the CSV database and update the new value
# RETURN: newValue
def updateDb(attribute, target, value):
  theList = []
  # First, open database file and load values
  # Also, update the appropriate value
  csvfile = open(fname, 'rb')
  reader = csv.reader(csvfile)
  newVal = 0
  for row in reader:
    if len(row) != 3: 
      continue
    newVal = float(row[2])
    if (int(row[0]) == target) and (int(row[1]) == attribute):
      newVal += value
      print 'Updating {0}\'s {1} to {2}'.format(targetLkup[int(row[0])],attLkup[int(row[1])],newVal)
    theList.append((int(row[0]),int(row[1]),newVal))
  csvfile.close()

  # Then, rewrite the database
  csvfile = open(fname, 'wb')
  writer = csv.writer(csvfile)
  for row in theList:
    writer.writerow(row)
  csvfile.close()

  return newVal
 

target = TGT_NONE
attribute = ATT_NONE
value = 0.0

emailTxt, goodToGo = get_mail()
if goodToGo:
  commandList = emailTxt.split(",")
  for command in commandList: 
    target, attribute, value = parseCommand(command)
    if target != TGT_NONE:
      print updateDb(attribute, target, value)
