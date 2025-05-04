import random

correct = [1]
wrong = [2,3,4,5,6,7]
select_3_wrong = random.sample(wrong, 3)
print(select_3_wrong)
an_all = correct + select_3_wrong
random.shuffle(an_all)
print(an_all)


def gg(r, args):
    print(r)
    print(*args)

gg('r', ['1', '3', '3'])