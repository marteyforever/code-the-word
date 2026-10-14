# Code the Word

Scripture woven into source code, matched to what each block of code does.

A function that **searches** gets *"Seek, and ye shall find."*
Error handling gets *"If we confess our sins, he is faithful and just to forgive."*
A login gate gets *"I am the door."*

Anyone who reads the code reads the Word.

Learn more at [marteycornog.com](https://marteycornog.com). Every verse is also gathered into `STUDY.md`, a study path through the codebase in reading order.

## Example

```python
# [Word] Matthew 7:7 (KJV)
# [Word] "Ask, and it shall be given you; seek, and ye shall find; knock, and it
# [Word] shall be opened unto you:"
# [Word] ↳ Every query is an asking.
def find_user(self, name):
```

## Use it

You need Python 3 and nothing else. Put `codetheword.py` and `verses.json` in the same folder.

```
python codetheword.py my-project                 # preview, changes nothing
python codetheword.py my-project --write         # add the verses
python codetheword.py my-project --study         # build STUDY.md
python codetheword.py my-project --strip --write # remove every verse cleanly
python codetheword.py my-project --gap 4 --write # denser (default is 8)
```

It is safe to run more than once. Verses already in place are left alone.

## Languages

`#` comments: Python, Ruby, Shell, R, YAML, TOML
`//` comments: JavaScript, TypeScript, Java, Kotlin, Swift, Go, Rust, C, C++, C#, PHP, Dart, Scala
`--` comments: SQL, Lua, Haskell

## Curating the verses

Edit `verses.json`. Each category has:
- `starts_with`: the kind of statement (`try`, `for`, `class`)
- `keywords`: words found in function names (`fetch`, `delete`, `render`)
- `verses`: one or more, which rotate so a big codebase doesn't repeat

Add categories, swap verses, and write your own `note` reflections. The JSON is the heart of the project.

## Translation

All verses are from the KJV, which is public domain in the U.S. Modern translations like the NIV and ESV are copyrighted, so keep to the KJV, the WEB, or other public-domain texts if you plan to share or open-source this.
