# test file for search.py
from search import Search

search = Search(None)

def test_sort():
    assert search.sort([3,2,1,6]) == [1,2,3,6]
    assert search.sort([1,2,3,4]) == [1,2,3,4]
    assert search.sort([1,1,1,1,2,1,1,1,1,1]) == [1,1,1,1,1,1,1,1,1,2]
    assert search.sort(["a","b","c"]) == ["a","b","c"]
    assert search.sort(["c","b","a"]) == ["a","b","c"]

def test_search():
    pass