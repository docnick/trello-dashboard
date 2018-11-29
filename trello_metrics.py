import numpy as np
import date_utils
import api


#
# Get due and late tasks
#
def get_tasks_with_due_date(cards):
    """
    Returns cards from the list which have a set due date
    :param cards:
    :return:
    """

    for card in cards:
        if card.get('due') is None:
            continue

        yield card


def get_tasks_due_on_date(cards, due_date=date_utils.get_today_date()):

    for card in get_tasks_with_due_date(cards):
        task_due_date = date_utils.get_date(card.get('due'))
        last_activity = date_utils.get_date(card.get('dateLastActivity'))

        if task_due_date == due_date:
            # task due date is equal to the given due_date parameter
            yield card
        elif task_due_date <= due_date and (last_activity >= due_date or not card.get('closed')):
            # task due date is in the past and the card is still open
            yield card


def get_past_due_tasks(cards, due_date=date_utils.get_today_date()):
    for card in get_tasks_due_on_date(cards, due_date):

        task_due_date = date_utils.get_date(card.get('due'))
        if date_utils.is_date_before_today(task_due_date) and not card.get('closed'):
            # task due in the past and the card is still open
            yield card
        elif date_utils.is_date_before_today(due_date):
            # due_date parameter is in the past
            last_activity = date_utils.get_date(card.get('dateLastActivity'))
            if last_activity > task_due_date or not card.get('closed'):
                # last activity is more recent than the task due date or the card is still open
                yield card
        elif date_utils.is_date_today(due_date) and not date_utils.is_before_close_business() and not card.get('closed'):
            # checking for today, if it's before close of business, don't count open cards as overdue
            yield card


def get_cards_open_on_date(cards, date):
    # TODO: this method is slow, needs to be optimized
    for card in cards:
        created_on = date_utils.get_created_on_date(card.get('id'))
        if created_on > date:
            continue

        last_activity = date_utils.get_date(card.get('dateLastActivity'))
        if not card.get('closed'):
            # if the card is still open then it was open on the given date
            yield card
        elif last_activity > date:
            # activity more recent than date
            yield card


def get_cards_closed_on_date(cards, date):

    for card in cards:
        created_on = date_utils.get_created_on_date(card.get('id'))
        if created_on > date:
            continue

        last_activity = date_utils.get_date(card.get('dateLastActivity'))
        if card.get('closed') and last_activity == date:
            # if the card is still open then it was open on the given date
            yield card


def get_card_ages(cards):
    card_open_ages = []
    for card in cards:
        opened_on_date = date_utils.get_created_on_date(card.get('id'))
        # date_diff_days(opened_on_date)
        card_open_ages.append(np.busday_count(opened_on_date, date_utils.get_today_date()))

    return card_open_ages


def get_x_oldest_cards(cards, x=5):

    card_ages = get_card_ages(cards)
    card_idx = np.argsort(card_ages)

    old_cards = []
    for i, idx in enumerate(reversed(card_idx)):
        old_cards.append((cards[idx], card_ages[idx]))

        if i > x:
            break

    return old_cards


# def get_cards_open_rng(cards):
#     CardOpenRng = namedtuple('CardOpenRng', ['card', 'open_date', 'close_date'])
#     card_rng = []
#     date_open = []
#     date_closed = []
#
#     for card in cards:
#         created_on = get_created_on_date(card.get('id'))
#         last_activity = get_date(card.get('dateLastActivity'))
#         is_closed = card.get('closed')
#
#         if not is_closed:
#             close_date = get_today_date()
#         else:
#             close_date = last_activity
#
#         card_rng.append(CardOpenRng(card, created_on, close_date))
#         date_open.append(created_on)
#         date_closed.append(close_date)
#
#     open_sorted_idx = np.argsort(date_open)
#     closed_sorted_idx = np.argsort(date_closed)
#
#     return card_rng, open_sorted_idx, closed_sorted_idx


if __name__ == '__main__':

    all_cards = api.get_all_cards(api.TRELLO_WAITING_FOR_LIST_ID)
    # tasks_due_today = get_tasks_due_on_date(all_cards)

    for card in all_cards:
        print(card)

    # get_trello_baords()
    # get_trello_lists(TRELLO_TODO_BOARD_ID)

    # Get creation time
    # for card in get_cards_from_list1(TRELLO_READ_REVIEW_LIST_ID):
    #     print(card.get('id'), card.get('name'))
    #     print('created on', datetime.date.fromtimestamp(int(card.get('id')[0:8], 16)))

    # show_past_due()

    # open_cards = get_all_open_cards(TRELLO_READ_REVIEW_LIST_ID)
    # card_ages = get_card_ages(open_cards)
    #
    # card_idx = np.argsort(card_ages)
    # for idx in reversed(card_idx):
    #     print(open_cards[idx].get('name'), card_ages[idx], sep='\t')
        #print(card.get('id'), card.get('name'), age)

    # all_cards = get_all_cards(TRELLO_WAITING_FOR_LIST_ID)
    # cards, open_idx, close_idx = get_cards_open_rng(all_cards)
    #
    # for cd, o, c in zip(cards, open_idx, close_idx):
    #     print('{:40.40}'.format(cd.card.get('name')), o, c, sep='\t')
    #
    # print('\n\n-------')
    # for card in cards:
    #     print('{:40.40}'.format(card.card.get('name')), card.open_date, card.close_date, sep='\t')

    # for day in get_date_range(50):
    #     item_count = len(list(get_cards_open_on_date(all_cards, day)))
    #     print('{} items open on {}'.format(item_count, day))