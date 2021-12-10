from datetime import datetime

COLOR = 0x5a3844

START_TIME = datetime.utcnow()


class Words:
    JOIN = "join vc!"
    LEAVE = "left!"

    NOW_PLAYING = "Now Playing..."
    ENQUEUED = "Enqueued"

    class Skip:
        NOT_PLAYING = "Not playing any music right now..."
        SUCCESS = "スキップ成功!"

    class Pause:
        NOT_PLAYING = "Not playing any music right now..."
        SUCCESS = "Paused"

    class Resume:
        SUCCESS = "Resumed"

    class Queue:
        EMPTY = "Queue is currently empty."
        CLEARED = "Queue cleared! 成功!"

    class Loop:
        ON = "looping is now on!"
        OFF = "looping is now off"

    class Reddit:
        R18 = "変態 バカ ボケナス 八幡\nhttps://c.tenor.com/qEW8kRsAFV8AAAAC/you-hachiman-oregairu.gif"


class Emoji:
    SKIP = "⏭"
    PAUSE_RESUME = "⏯"

    class Loop:
        # * Recommended by GitHub Copilot ✨✨✨
        ON = "🔁"
        OFF = "🔂"
