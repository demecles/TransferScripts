#!/usr/env/ python3
# Creates a simple SMB share open to all connections for quickly transferring files, with user/pass authenication added
# Not intended for production use
# Tested on Python 3.11.4
# Author: Demecles
# Derived from: https://github.com/fortra/impacket/blob/master/examples/smbserver.py

import impacket, sys, threading
from impacket import smbserver
from impacket.ntlm import compute_lmhash, compute_nthash
from threading import Thread
from getpass import getpass

#Main
def main():

  #Check arguements or display help
  if(len(sys.argv)) != 5:
    print("Usage: python3 simpleSMB.py [shareName] [sharePath] [port] [username]")
    sys.exit()

  #Script variables
  share = sys.argv[1]
  folder = sys.argv[2]
  port = sys.argv[3]
  user = sys.argv[4]
  server = smbserver.SimpleSMBServer("0.0.0.0", int(port))
  server.addShare(share, folder)
  server.setSMB2Support(True)

  #Ask for user password
  password = getpass("Password:")

  #Convert passes to hashes
  lmhash = compute_lmhash(password)
  nthash = compute_nthash(password)
  server.addCredential(user, 0, lmhash, nthash)

  #Start daemonized impacket SMB thread using SMBv2
  thread = Thread(target=startSMB, args=(server,))
  thread.daemon = True
  thread.start()

  input("Press enter to stop SMB server")

  #Terminate thread
  stopSMB(server)

#SMB thread start function
def startSMB(serv):

  print("Starting SMB server...")
  try:
    serv.start()
    print("done")
  except Exception as e:
    print(e)
    sys.exit("Error starting SMB server. Check configuration.")

#SMB thread stop function
def stopSMB(serv):

  print("Stopping SMB server...")
  try:
    serv.stop()
    print("Stopped SMB server successfully")
  except Exception as e:
    print(e)
    sys.exit("Error stopping SMB server. Manually verify the port was closed.")
    
if __name__ == "__main__":
  main()
