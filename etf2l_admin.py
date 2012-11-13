# encoding: utf-8

import xchat
import re
import exceptions

__module_name__ = 'ETF2L Admin'
__module_version__ = '1.0'
__module_description__ = '''
Easy admin-request handling for ETF2L admins.
When the bot announces a request, type `/g` to take care of it. The user will automatically be queried for you.
'''

ADMIN_CHANNEL = '#etf2l.admins'
ADMIN_CHANNEL = '#ntraum'
REGEX_BOT_REQUEST_MSG = r'Info: Admin requested in (?P<chan>#.+) by (?P<nick>.+), Request ID: (?P<id>\d+)'
DEBUG = False
DEBUG = True

requests = {}
latest_id = None

def debug(msg):
  if DEBUG:
    print('[{}] {}'.format(__module_name__, msg))

def on_msg(word, word_eol, userdata):
  msg = word[1]
  channel = xchat.get_context().get_info('channel')
  debug('Message: {}'.format(msg))
  debug('Channel: {}'.format(channel))
  if channel != ADMIN_CHANNEL:
    debug('Wrong channel, ignoring message...')
    return xchat.EAT_NONE

  m = re.match(REGEX_BOT_REQUEST_MSG, msg)
  if m:
    try:
      curr_user = m.group('nick')
      curr_id = int(m.group('id'))
      latest_id = curr_id
      requests[curr_id] = curr_user
      debug('Request added, Nick: {}, ID: {}'.format(curr_user, curr_id))
      return xchat.EAT_NONE
    except exceptions.ValueError:
      debug('Could not parse {} to integer'.format(m.group('id')))
      return xchat.EAT_NONE
  else:
    debug('Message did not match regex, ignoring...')
    return xchat.EAT_NONE

def r(word, word_eol, userdata):
  channel = xchat.get_context().get_info('channel')
  if 1 == len(word):
    debug('No ID specified')
    return xchat.EAT_XCHAT
  elif 2 == len(word):
    try:
      id = int(word[1])
      debug('ID specified: {}'.format(id))
      return xchat.EAT_XCHAT
    except exceptions.ValueError:
      debug('Could not parse {} to integer'.format(word[1]))
      return xchat.EAT_XCHAT
  else:
    debug('Too many arguments, ignoring...')
    return xchat.EAT_XCHAT

xchat.prnt('{} version {} loaded.'.format(__module_name__, __module_version__))
debug('Admin channel: {}'.format(ADMIN_CHANNEL))
debug('Regex: {}'.format(REGEX_BOT_REQUEST_MSG))

xchat.hook_print('Channel Message', on_msg)
xchat.hook_command('r', r)