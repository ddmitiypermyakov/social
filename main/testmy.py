def fetcher(x,i):
    return x[i]

a='spam'
try:
    print(fetcher(int(a), '10'))
except (IndexError, TypeError, ValueError):
    print('Hi,luser')
finally:
    print('Hi,hegklwsjglsgkl=', a )


print('print')

print('a' + '1')

a=[1,2,3,4,5][::-2]
print(a)

def foo(extra):
    def bar(func):
        def wrap(a:str):
            return '|'.join([extra,func(a)])
        return wrap
    return bar
@foo('wrap')
def spam(x):
    return x

print(spam('zoo'))

try:
    1/0
except Exception as X:
    print(X)
    Sav=X
print(type(Sav),Sav)
