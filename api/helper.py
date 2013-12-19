import time

def compare_dictionaries(old_dict, new_dict):
    added_entries = {}  # new friends
    removed_entries = {}  # lost friends

    for key, value in new_dict.iteritems():
        try:
            old_dict[key]
        except KeyError:
            added_entries[key] = value

    for key, value in old_dict.iteritems():
        try:
            new_dict[key]
        except KeyError:
            removed_entries[key] = value

    return {
        'added_entries': added_entries,
        'removed_entries': removed_entries
    }


def add_entry_to_history(history, element_value, history_limit=20):
    today = time.strptime(time.strftime("%d/%m/%Y"), "%d/%m/%Y")
    timestamp = int(time.mktime(today))

    # Indices have to be string for django-nonrel
    history['%s' % timestamp] = element_value

    # Strip the history down to <limit> elements per user
    history_count = len(history)
    history_remove_keys = []

    counter = 0
    if history_count > history_limit:
        history_keys = history.keys()
        history_keys.sort(key=int)
        for key in history_keys:
            counter += 1
            if (history_count - history_limit) < counter:
                break

            history_remove_keys.append(key)

        for key in history_remove_keys:
            del history[key]