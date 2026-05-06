"""

"""

import asyncio, json

# TODO: replace class methods pertaining to extracting data from JSON files throughout project with below function


def extract_data(json_file_path):
    try:
        with open(json_file_path) as raw_file:
            raw_dict = json.load(raw_file)
        return raw_dict
    except FileNotFoundError as fnf_error:
        # return empty dictionary, and print out error
        print(fnf_error)
        return {}


class EventBus:  # TODO: figure out how this works, and what it'll be used for
    def __init__(self):
        self._listeners = {}

    def subscribe(self, event_type, callback):
        self._listeners.setdefault(event_type, []).append(callback)

    async def emit(self, event_type, data = None):
        callbacks = self._listeners.get(event_type, [])
        await asyncio.gather(*[callback(data) for callback in callbacks])
