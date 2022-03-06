import json


class Stream:
    def __init__(self, struct: dict):
        # TODO: STREAM LOAD
        self.struct = struct

    def loads(self, path: str = None) -> dict:
        # TODO: STREAM READ
        with open(path, 'r') as f:
            d = json.loads(f.read())

        # TODO: PARSE JSON & WRITE TO CACHE FILES
        # ...
        return d

    def dumps(self, path: str) -> bool:
        # TODO: WRITE CACHE INTO FINAL JSON FILE
        # with open(path, 'a') as f:
        #     f.write()
        return True


def main():
    struct = json.loads(open('struct.json').read())
    stream = Stream(struct=struct)
    stream.loads(path='a.json')
    stream.loads(path='b.json')
    stream.dumps(path='/tmp/final.json')


if __name__ == '__main__':
    main()
