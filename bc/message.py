"""
BasicChat -- message.py
Author: Joshua Ibrom (sk3p7ic)

For messages.
"""

from enum import Enum

class MsgTypes(Enum):
  MSG_HEAD = 0
  MSG_NAME = 1
  MSG_NORM = 2
  MSG_CHID = 3

class Message:

  def __init__(self, user_id, msg_type, msg):
    self.user_id = str(user_id).zfill(4)
    if msg_type == MsgTypes.MSG_HEAD:
      raise Exception("Message cannot be of type MSG_HEAD")
    else:
      self.msg_type = msg_type
    self.msg = msg.encode()

  def getUserID(self):
    return self.user_id

  def getMsgType(self):
    return self.msg_type

  def getMsg(self):
    return self.msg

  def getMsgLength(self):
    return len(self.msg)
  
  def makeHeader(self):
    header =  f"User-ID: {self.user_id}\n"
    header += f"Msg-Type: {MsgTypes.MSG_HEAD.name}\n"
    header += f"Msg-Length: {str(len(self.msg)).zfill(4)}\n"
    if len(header) != 50:
      raise Exception(f"An error occurred generating the header (header " \
        f"length: {len(header)}")
    return header.encode()