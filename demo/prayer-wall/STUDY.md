# Code the Word: Study Path

Every verse hidden in this codebase, in the order you meet it.

## 1. 1 Corinthians 12:12 (KJV)
> “For as the body is one, and hath many members, and all the members of that one body, being many, are one body: so also is Christ.”

*Many members, one body. Every method has its part.*

Found at `prayer_wall.py:14` above `class PrayerWall:`

## 2. Psalm 119:105 (KJV)
> “Thy word is a lamp unto my feet, and a light unto my path.”

*Reading the input lights the way for everything after.*

Found at `prayer_wall.py:25` above `def load(self):`

## 3. Psalm 119:11 (KJV)
> “Thy word have I hid in mine heart, that I might not sin against thee.”

*What is stored well is there when it is needed.*

Found at `prayer_wall.py:38` above `def save(self):`

## 4. John 10:9 (KJV)
> “I am the door: by me if any man enter in, he shall be saved, and shall go in and out, and find pasture.”

*There is one true door. Guard this one well.*

Found at `prayer_wall.py:45` above `def login(self, name, password):`

## 5. Revelation 3:20 (KJV)
> “Behold, I stand at the door, and knock: if any man hear my voice, and open the door, I will come in to him, and will sup with him, and he with me.”

*A request knocks. Someone has to answer.*

Found at `prayer_wall.py:54` above `def add_request(self, name, text):`

## 6. Matthew 7:7 (KJV)
> “Ask, and it shall be given you; seek, and ye shall find; knock, and it shall be opened unto you:”

*Every query is an asking.*

Found at `prayer_wall.py:72` above `def find_request(self, word):`

## 7. James 5:16 (KJV)
> “Confess your faults one to another, and pray one for another, that ye may be healed. The effectual fervent prayer of a righteous man availeth much.”

*Every tap here is someone praying for someone else.*

Found at `prayer_wall.py:83` above `def pray_for(self, request_id):`

## 8. Matthew 18:20 (KJV)
> “For where two or three are gathered together in my name, there am I in the midst of them.”

*Every connection is a gathering.*

Found at `prayer_wall.py:96` above `def mark_answered(self, request_id):`

## 9. Psalm 103:12 (KJV)
> “As far as the east is from the west, so far hath he removed our transgressions from us.”

*Removed completely, not just hidden.*

Found at `prayer_wall.py:108` above `def delete_request(self, request_id):`

## 10. Mark 16:15 (KJV)
> “And he said unto them, Go ye into all the world, and preach the gospel to every creature.”

*Every message sent out is a small going-forth.*

Found at `prayer_wall.py:116` above `def send_reminder(self, email):`

## 11. Genesis 1:1 (KJV)
> “In the beginning God created the heaven and the earth.”

*Everything that runs had a first line.*

Found at `prayer_wall.py:127` above `def main():`

## 12. Galatians 6:9 (KJV)
> “And let us not be weary in well doing: for in due season we shall reap, if we faint not.”

*The same faithful work, again and again, until the harvest.*

Found at `prayer_wall.py:136` above `for r in wall.find_request("healing"):`

## 13. Isaiah 65:24 (KJV)
> “And it shall come to pass, that before they call, I will answer; and while they are yet speaking, I will hear.”

*A good server listens before the call ends.*

Found at `wall.js:5` above `async function fetchRequests() {`

## 14. Matthew 5:16 (KJV)
> “Let your light so shine before men, that they may see your good works, and glorify your Father which is in heaven.”

*What is rendered here is seen by others.*

Found at `wall.js:19` above `function render(requests) {`

## 15. Philippians 4:6 (KJV)
> “Be careful for nothing; but in every thing by prayer and supplication with thanksgiving let your requests be made known unto God.”

*Every request, made known.*

Found at `wall.js:34` above `async function prayFor(id) {`

## 16. 1 John 1:9 (KJV)
> “If we confess our sins, he is faithful and just to forgive us our sins, and to cleanse us from all unrighteousness.”

*Errors caught and handled, not hidden. Confession is the catch block of the soul.*

Found at `wall.js:43` above `function showError(message) {`
