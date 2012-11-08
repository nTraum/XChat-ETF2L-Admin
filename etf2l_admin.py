# encoding: utf-8

import xchat
import re

__module_name__ = 'ETF2L Admin'
__module_version__ = '1.0'
__module_description__ = '''
Easy admin-request handling for ETF2L admins.
When the bot announces a request, type `/g` to take care of it. The user will automatically be queried for you.
'''

ADMIN_CHANNEL = '#etf2l.admins'
REGEX_BOT_REQUEST_MSG = r'Info: Admin requested in (?P<chan>#.+) by (?P<nick>.+), Request ID: (?P<id>\d+)'
curr_id = None
curr_user = None

def on_msg(word, word_eol, userdata):
  if chan != ADMIN_CHANNEL:
    return xchat.EAT_NONE

  m = re.match(REGEX_BOT_REQUEST_MSG, msg)
  if m:
    curr_user = m.group('nick')
    curr_id = m.group('id')
  return xchat.EAT_NONE

def r():
  if curr_id is None or curr_user is None:
    return
  pass 

xchat.hook_command('r', r)