# Yubin

Converts Japanese address in raw string to structured object.

Usage
====

```python
>>> from yubin import Postman
>>> pm = Postman()

# Returns structured object.
>>> pm.tokenize('〒158-0094東京都世田谷区玉川一丁目14番1号')
Address(to=['東京都'], kai=[], ku=['世田谷区'], mune=[], chome=['一丁目'], ban=['14番'], go=['1号'], postal=['〒158-0094'], endgo=[],
        tokens=['〒158-0094', '東京都', '世田谷区', '玉川', '一丁目', '14番', '1号'])

# Return tokenized string, split by space.
>>> pm.tokenize('〒158-0094東京都世田谷区玉川一丁目14番1号', return_str=True)
'〒158-0094 東京都 世田谷区 玉川 一丁目 14番 1号'
```
