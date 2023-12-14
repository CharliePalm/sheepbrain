from model import RequestType
class Handler:
    def __init__(self):
        self.function_map = {
            '/get_test': (self.get_test, RequestType.get),
            '/start': (self.start, RequestType.post) # returns player hand and turns up until player turn
        }
    
    def test(self, args):
        print('test called')

    def handle(self, path, request_type, args=None):
        self.function_map[path]()