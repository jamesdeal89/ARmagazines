# test file for search.py
from search import Search

def test_sort():
    search = Search(None,[3,2,1,6])
    assert search.sort() == [1,2,3,6]
    search = Search(None,[1,2,3,4])
    assert search.sort() == [1,2,3,4]
    search = Search(None,[1,1,1,1,2,1,1,1,1,1])
    assert search.sort() == [1,1,1,1,1,1,1,1,1,2]
    search = Search(None,["a","b","c"])
    assert search.sort() == ["a","b","c"]
    search = Search(None,["c","b","a"])
    assert search.sort() == ["a","b","c"]

def test_search():
    search = Search("a-file", ["c-file","b-file","a-file"])
    search.sort()
    assert search.search() == True
    search = Search("a-file", ["a-file","b-file","c-file"])
    search.sort()
    assert search.search() == True
    search = Search("a-file", ["c-file","a-file","b-file"])
    search.sort()
    assert search.search() == True
    search = Search("a-file", ["b-file","c-file","d-file"])
    search.sort()
    assert search.search() == False
