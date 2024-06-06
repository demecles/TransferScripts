#!/usr/env/ python3
# Creates an unauthenticated simple SMB share open to all connections for quickly transferring files.
# May be blocked on some versions of Windows
# Not intended for production use
# Tested on Python 3.11.4
# Author: Demecles

import impacket, sys, threading
from impacket import smbserver
from threading import Thread

#Main
def main():

  #Check arguements or display help
  if(len(sys.argv)) != 4:
    print("Usage: python3 simpleSMB.py [shareName] [sharePath] [port]")
    sys.exit()

  #Script variables
  share = sys.argv[1]
  folder = sys.argv[2]
  port = sys.argv[3]
  server = smbserver.SimpleSMBServer("0.0.0.0", int(port))
  server.addShare(share, folder)
  server.setSMB2Support(True)


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
