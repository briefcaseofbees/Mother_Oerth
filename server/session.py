"""
    for handling active game sessions
"""

from game_assets import GameTime


class Session:
    def __init__(self):
        """
        Session is a class that stores information about the state of a game session
        """
        self.session_title = None
        self.session_id = None
        self.current_time = GameTime()      # current time in the session (i.e. in-universe time)
        self.involved_players = set()       # players that are required for session to run

    def save_session_details(self):
        # save session details to correct database/file entry based on session_id
        pass

    def load_session_details(self):
        # poll database or collection of files for session details based on session_id
        pass

    def start_session(self):
        # check that all involved_players are connected
        pass

    def halt_session(self):
        # freeze the current session and save the details of the session in a database (or file)
        pass


