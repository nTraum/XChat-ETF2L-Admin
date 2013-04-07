# encoding: utf-8

import xchat
import re
import exceptions

__module_name__ = 'ETF2L Admin'
__module_version__ = '1.2'
__module_description__ = '''Easy admin-request handling for ETF2L admins.
When the bot announces a request, type `/g` to take care of it. The user will automatically be queried for you.
'''

HELP_MSG='''/g <ID> takes request with specified ID.
/g takes latest request.'''
ADMIN_CHANNEL = '#etf2l.admins'
REGEX_BOT_REQUEST_MSG = r'Info: Admin requested in (?P<chan>#.+) by (?P<nick>.+), Request ID: (?P<id>\d+)'
REGEX_BOT_REMINDER_MSG = r'Open admin request by (?P<nick>.+) ID: (?P<id>\d+)'
DEBUG = False

class RequestHandler:
  def __init__(self):
    self.requests = {}
    self.latest_id = None

  def handle_latest_request(self, context):
    if None == self.latest_id:
      say('Request queue is empty.')
      return xchat.EAT_XCHAT 
    return self.handle_request(self.latest_id, context)

  def handle_request(self, id, context):
   if id in self.requests:
    say('Taking request #{}'.format(id))
    nick = self.requests.pop(id)
    context.command('say !got {}'.format(id))
    context.command('query {}'.format(nick))
    context.command('msg {} Hi {}, how can I help you?'.format(nick, nick))
    if len(self.requests) != 0:
     self.latest_id = self.requests.iterkeys().next
    else:
     debug('Request queue is now empty.')
     self.latest_id = None
   else:
    say('Unknown ID: #{}'.format(id))
   return xchat.EAT_XCHAT

  def add_request(self, id, nick):
   self.latest_id = id
   self.requests[id] = nick
   debug('Added request to queue: #{} by {}'.format(id,nick))

def say(msg):
  print('[{}] {}'.format(__module_name__, msg))

def debug(msg):
  if DEBUG:
    say(msg)

def on_msg(word, word_eol, handler):
  colorRe = re.compile(r"(||[0-9]{1,2}(,[0-9]{1,2}|))")
  msg = colorRe.sub("",word[1])
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
   m = re.match(REGEX_BOT_REMINDER_MSG, msg)
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
   debug('Message did not match regex, ignoring...')
   return xchat.EAT_NONE

def g(word, word_eol, handler):
  channel = xchat.get_context().get_info('channel')
  if channel != ADMIN_CHANNEL:
    say('This command can be used in {} only.'.format(ADMIN_CHANNEL))
    return xchat.EAT_XCHAT
  if len(word) > 2:
    say('Too many arguments, type \'/help g\' to get help.')
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
debug('Request Regex: {}'.format(REGEX_BOT_REQUEST_MSG))
debug('Reminder Regex: {}'.format(REGEX_BOT_REMINDER_MSG))
h = RequestHandler()

xchat.hook_print('Channel Message', on_msg, h)
xchat.hook_print('Channel Msg Hilight', on_msg, h)
xchat.hook_command('g', g, h,help=HELP_MSG)