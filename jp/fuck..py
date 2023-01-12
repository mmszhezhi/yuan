
class F:
    def __init__(self):
        self.name = 'fuck'


f = F()
for k,v in f.__dict__.items():
    if isinstance(v, (str, int, float, dict)):
        # t[k] = v
        print(k,v)

