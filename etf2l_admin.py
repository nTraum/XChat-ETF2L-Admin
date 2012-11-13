# encoding: utf-8

import xchat
import re
import exceptions

__module_name__ = 'ETF2L Admin'
__module_version__ = '1.0'
__module_description__ = '''Easy admin-request handling for ETF2L admins.
When the bot announces a request, type `/g` to take care of it. The user will automatically be queried for you.
'''

HELP_MSG='''/r <ID> takes request with specified ID.
/r takes latest request.'''
ADMIN_CHANNEL = '#etf2l.admins'
REGEX_BOT_REQUEST_MSG = r'Info: Admin requested in (?P<chan>#.+) by (?P<nick>.+), Request ID: (?P<id>\d+)'
DEBUG = False

class RequestHandler:
  def __init__(self):
    self.requests = {}
    self.latest_id = None

  def handle_latest_request(self, context):
    if None == self.latest_id:
      say('Latest request unknown.')
      return xchat.EAT_XCHAT
    return self.handle_request(self.latest_id, context)

  def handle_request(self, id, context):
    if id in self.requests:
      say('Taking request #{}'.format(id))
      nick = self.requests.pop(id)
      context.command('say !got {}'.format(id))
      context.command('query {}'.format(nick))
      context.command('msg {} Hi {}, how can I help you?'.format(nick, nick))
    else:
      say('Unknown ID: #{}'.format(id))
    return xchat.EAT_XCHAT

  def add_request(self, id, nick):
    self.latest_id = id
    self.requests[id] = nick


def say(msg):
  print('[{}] {}'.format(__module_name__, msg))

def debug(msg):
  if DEBUG:
    say(msg)

def on_msg(word, word_eol, handler):
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
      h.add_request(curr_id, curr_user)
      debug('Request added, Nick: {}, ID: #{}'.format(curr_user, curr_id))
      return xchat.EAT_NONE
    except exceptions.ValueError:
      debug('Could not parse {} to integer'.format(m.group('id')))
      return xchat.EAT_NONE
  else:
    debug('Message did not match regex, ignoring...')
    return xchat.EAT_NONE

def r(word, word_eol, handler):
  channel = xchat.get_context().get_info('channel')
  if channel != ADMIN_CHANNEL:
    say('This command can be used in {} only.'.format(ADMIN_CHANNEL))
    return xchat.EAT_XCHAT
  if len(word) > 2:
    say('Too many arguments, type \'/help r\' to get help.')
    return xchat.EAT_XCHAT

  if 1 == len(word):
    debug('No ID specified.')
    return h.handle_latest_request(xchat.get_context())
  elif 2 == len(word):
    try:
      id = int(word[1])
      debug('ID specified: #{}.'.format(id))
      return h.handle_request(id, xchat.get_context())
    except exceptions.ValueError:
      say('\'{}\' is no valid ID.'.format(word[1]))
      return xchat.EAT_XCHAT

say('{} version {} loaded.'.format(__module_name__, __module_version__))
debug('Admin channel: {}'.format(ADMIN_CHANNEL))
debug('Regex: {}'.format(REGEX_BOT_REQUEST_MSG))

h = RequestHandler()
xchat.hook_print('Channel Message', on_msg, h)
xchat.hook_print('Channel Msg Hilight', on_msg, h)
xchat.hook_command('r', r, h,help=HELP_MSG)