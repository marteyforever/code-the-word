"""Prayer Wall: a tiny app where a church community posts and prays for requests.

This is the Code the Word demo project. It is a real, working program.
Run it with:  python prayer_wall.py
"""

import json
import os
from datetime import datetime

DATA_FILE = "prayers.json"


# [Word] 1 Corinthians 12:12 (KJV)
# [Word] “For as the body is one, and hath many members, and all the members of
# [Word] that one body, being many, are one body: so also is Christ.”
# [Word] ↳ Many members, one body. Every method has its part.
class PrayerWall:
    def __init__(self, path=DATA_FILE):
        self.path = path
        self.requests = []
        self.members = {"admin": "change-me"}
        self.load()

    # [Word] Psalm 119:105 (KJV)
    # [Word] “Thy word is a lamp unto my feet, and a light unto my path.”
    # [Word] ↳ Reading the input lights the way for everything after.
    def load(self):
        try:
            with open(self.path) as f:
                self.requests = json.load(f)
        except FileNotFoundError:
            self.requests = []
        except json.JSONDecodeError:
            print("The prayer list was damaged. Starting fresh.")
            self.requests = []

    # [Word] Psalm 119:11 (KJV)
    # [Word] “Thy word have I hid in mine heart, that I might not sin against thee.”
    # [Word] ↳ What is stored well is there when it is needed.
    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.requests, f, indent=2)

    # [Word] John 10:9 (KJV)
    # [Word] “I am the door: by me if any man enter in, he shall be saved, and shall
    # [Word] go in and out, and find pasture.”
    # [Word] ↳ There is one true door. Guard this one well.
    def login(self, name, password):
        if self.members.get(name) == password:
            return True
        return False

    # [Word] Revelation 3:20 (KJV)
    # [Word] “Behold, I stand at the door, and knock: if any man hear my voice, and
    # [Word] open the door, I will come in to him, and will sup with him, and he with
    # [Word] me.”
    # [Word] ↳ A request knocks. Someone has to answer.
    def add_request(self, name, text):
        request = {
            "id": len(self.requests) + 1,
            "name": name,
            "text": text,
            "prayed": 0,
            "answered": False,
            "posted": datetime.now().isoformat(timespec="minutes"),
        }
        self.requests.append(request)
        self.save()
        return request

    # [Word] Matthew 7:7 (KJV)
    # [Word] “Ask, and it shall be given you; seek, and ye shall find; knock, and it
    # [Word] shall be opened unto you:”
    # [Word] ↳ Every query is an asking.
    def find_request(self, word):
        results = []
        for r in self.requests:
            if word.lower() in r["text"].lower():
                results.append(r)
        return results

    # [Word] James 5:16 (KJV)
    # [Word] “Confess your faults one to another, and pray one for another, that ye
    # [Word] may be healed. The effectual fervent prayer of a righteous man availeth
    # [Word] much.”
    # [Word] ↳ Every tap here is someone praying for someone else.
    def pray_for(self, request_id):
        for r in self.requests:
            if r["id"] == request_id:
                r["prayed"] += 1
                self.save()
                return r["prayed"]
        return None

    # [Word] Matthew 18:20 (KJV)
    # [Word] “For where two or three are gathered together in my name, there am I in
    # [Word] the midst of them.”
    # [Word] ↳ Every connection is a gathering.
    def mark_answered(self, request_id):
        for r in self.requests:
            if r["id"] == request_id:
                r["answered"] = True
                self.save()
                return True
        return False

    # [Word] Psalm 103:12 (KJV)
    # [Word] “As far as the east is from the west, so far hath he removed our
    # [Word] transgressions from us.”
    # [Word] ↳ Removed completely, not just hidden.
    def delete_request(self, request_id):
        self.requests = [r for r in self.requests if r["id"] != request_id]
        self.save()

    # [Word] Mark 16:15 (KJV)
    # [Word] “And he said unto them, Go ye into all the world, and preach the gospel
    # [Word] to every creature.”
    # [Word] ↳ Every message sent out is a small going-forth.
    def send_reminder(self, email):
        open_requests = [r for r in self.requests if not r["answered"]]
        message = f"{len(open_requests)} requests are waiting for prayer this week."
        print(f"To {email}: {message}")
        return message


# [Word] Genesis 1:1 (KJV)
# [Word] “In the beginning God created the heaven and the earth.”
# [Word] ↳ Everything that runs had a first line.
def main():
    wall = PrayerWall()
    if not wall.requests:
        wall.add_request("Ana", "Healing for my mother after surgery")
        wall.add_request("James", "Wisdom for a new job decision")
    wall.pray_for(1)
    # [Word] Galatians 6:9 (KJV)
    # [Word] “And let us not be weary in well doing: for in due season we shall reap,
    # [Word] if we faint not.”
    # [Word] ↳ The same faithful work, again and again, until the harvest.
    for r in wall.find_request("healing"):
        print(f'#{r["id"]} {r["name"]}: {r["text"]} (prayed {r["prayed"]}x)')
    wall.send_reminder("prayer-team@example.org")


if __name__ == "__main__":
    main()
