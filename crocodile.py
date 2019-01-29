import vk_api
from setting import *


def correct(text):
    return text[::-1]


def reformat(lst):
    res = ''
    for i in lst:
        res += ',' + str(i['type']) + str(i[i['type']]['owner_id']) + '_' + str(i[i['type']]['id'])
    return res[1:]


vk_session = vk_api.VkApi(EMAIL, PASSWORD, scope='messages')
vk_session.auth()

vk = vk_session.get_api()

connect = vk.messages.getLongPollServer()

while True:
    q = vk.messages.getLongPollHistory(ts=connect['ts'])
    if q['messages']['count']:
        for item in q['messages']['items']:
            if item['out']:
                newText = correct(item['text'])
                if newText != item['text']:
                    vk.messages.edit(peer_id=item['peer_id'], message=newText, message_id=item['id'],
                                     attachment=reformat(item['attachments']), keep_forward_messages=1, keep_snippets=1)
        connect = vk.messages.getLongPollServer()
