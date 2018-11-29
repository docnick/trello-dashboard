import requests
import json
from secrets import API_KEY, API_TOKEN

API_BASE = 'https://api.trello.com/1'

TRELLO_NEXT_STEPS_LIST_ID = '5b3ce1bbceeaefac9ebe04bb'
TRELLO_WAITING_FOR_LIST_ID = '5b3ce1c6acf705468bcd9070'
TRELLO_READ_REVIEW_LIST_ID = '5b3ce252016382d11454f3ff'
TRELLO_SOMEDAY_LIST_ID = '5b3ce1d0b7d106dc15ac379e'
TRELLO_TODO_BOARD_ID = '5b3ce1b3f79757810c477371'


def get_cards_from_list(list_id, fields=None, filters=None):

    if fields is None:
        fields = 'id,name,due,dateLastActivity,closed'

    if filters is None:
        filters = 'open'

    r = requests.get('{}/lists/{}/cards?key={}&token={}&fields={}&filter={}'.format(API_BASE,
                                                                                    list_id,
                                                                                    API_KEY,
                                                                                    API_TOKEN,
                                                                                    fields,
                                                                                    filters))
    return json.loads(r.content)


def get_all_archived_cards(list_id):
    # simplified helper function for getting just the archived cards
    archived_cards = get_cards_from_list(list_id, filters='closed')
    return archived_cards


def get_all_open_cards(list_id):
    # simplified helper function for getting just the open cards
    open_cards = get_cards_from_list(list_id, filters='open')
    return open_cards


def get_all_cards(list_id):
    open_cards = get_cards_from_list(list_id, filters='open')
    archived_cards = get_cards_from_list(list_id, filters='closed')
    return open_cards + archived_cards


def get_cards_moved_out_of_list(list_id):
    """
    Returns a set of card IDs that have been removed from the given list
    :param list_id: Trello ListID
    :return: set of card IDs
    """
    r = requests.get('{}/lists/{}/actions?key={}&token={}'.format(API_BASE, list_id,
                                                                    API_KEY, API_TOKEN))

    if r.status_code != 200:
        raise Exception('API call failed: {}'.format(r.reason))

    cards = json.loads(r.content)
    card_ids = []
    for card in cards:
        data = card.get('data')

        if data.get('listAfter'):
            card_ids.append(data.get('card').get('id'))

    return set(card_ids)


def get_trello_boards(trello_user):
    """
    Return the set of boards owned by the given Trello user
    :param trello_user: Trello username
    :return: list of json board objects returned from the trello api
    """
    r = requests.get('{}/members/{}/boards?key={}&token={}'.format(API_BASE, trello_user,
                                                                   API_KEY, API_TOKEN))
    if r.status_code != 200:
        raise Exception('API call failed: {}'.format(r.reason))

    return json.loads(r.content)


def get_trello_lists(board_id):
    r = requests.get('{}/boards/{}/lists?key={}&token={}'.format(API_BASE, board_id,
                                                                 API_KEY, API_TOKEN))
    if r.status_code != 200:
        raise Exception('API call failed: {}'.format(r.reason))

    return json.loads(r.content)