name = "my name is khan"

s=name.split()
op=[]
op = [st[::-1] for st in s]
rev = " ".join(op)
print(rev)
