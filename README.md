# sjson (WIP)
Python: Stream JSON parser/merger, designed to work for large/many JSON files.


## Stream Merging Large JSON Files



Steps:

1. Define a JSON structure (no actual value) with merging patterns
2. Generate independent files (cache) to store each merging pattern (list or dict)
3. Read an actual JSON file, according to the pattern(path), stream output into the cache files
4. Iterate each JSON file to repeat the above step
5. Reading each cache file (in stream), find the corresponding pattern position, write the content (in stream) to override the "pattern symbole"



Assumption:

1. We must know the exact JSON structure before merging
2. If we don't know the structure, it will always override



Structure example (`struct.json`):

```json
{
    "code": 200,
    "report": "Person Profile",
    "name": "<replace-by-str-override>",
    "age": "<replace-by-int-max>",
    "count": "<replace-by-int-sum>",
    "products": "<replace-by-list>",
    "properties": "<replace-by-dict>",
    "subsets": {
    	"deep-nest": "<replace-by-dict>"
	}
}
```



Input file examples (`a.json` and `b.json`):

```json
# a.json
{
    "code": 200,
    "report": "Person Profile",
    "name": "Jason",
    "age": 30,
    "count": 2,
    "products": [
        {"name": "a", "price": 1},
        {"name": "b", "price": 2}
    ],
    "properties": {
        "books": ["a", "b", "c"],
        "games": [1, 2, 3]
    },
    "subsets": {
        "deep-nest": {
            "students": ["a", "b", "c"]
        }
    },
    "override": [
        "a": "a",
        "b": "b"
    ]
}

# b.json
{
    "code": 200,
    "report": "Person Profile",
    "name": "Sam",
    "age": 40,
    "count": 3,
    "products": [
        {"name": "c", "price": 3},
        {"name": "d", "price": 4}
    ],
    "properties": {
        "books": ["d", "e", "f"],
        "games": [4, 5, 6]
    },
    "subsets": {
        "deep-nest": {
            "friends": ["d", "e", "f"]
        }
    },
    "override": [
        "c": "c",
        "d": "d"
    ]
}
```





Result example (`result.json`):

```json
{
    "code": 200,
    "report": "Person Profile",
    "name": "Sam",
    "age": 40,
    "count": 5,
    "products": [
        {"name": "a", "price": 1},
        {"name": "b", "price": 2},
        {"name": "c", "price": 3},
        {"name": "d", "price": 4}
    ],
    "properties": {
        "books": ["a", "b", "c", "d", "e", "f"],
        "games": [1, 2, 3, 4, 5, 6]
    },
    "subsets": {
        "deep-nest": {
            "students": ["a", "b", "c"],
            "friends": ["d", "e", "f"]
        }
    },
    "override": [
        "c": "c",
        "d": "d"
    ]
}
```



Python code:

```python
import sjson

struct = open('struct.json').read()  # It can also be an empty {}
stream = sjson.Stream(struct=struct)

d1 = stream.loads(path='data-from-csv-1.json')  # ==> write content into different cache files
d2 = stream.loads(path='data-from-csv-2.json')  # ==> write content into different cache files

stream.dumps(path='final.json')  # ==> Merge cache files
```



Algorithm:

1. Flatten the `structure.json` into 1-level
2. Generate "command" for each key in the flattened JSON
3. Generate tmp names/files for each command
4. Use the original structure JSON as the "base data"
5. Traverse the k/v of each input JSON
6. Compare the current k/v with flattened-json to see if there's a command
7. Follow the command for current key, write current value into corresponding cache
8. Continue traversal until the file is finished
9. Repeating same operations to each file until all files are finished
10. Replace each "command/pattern" with the content from cache file
