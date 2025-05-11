import random
correct = [1]
wrong = [2,3,4,5,6,7]
select_3_wrong = random.sample(wrong, 3) + correct
print(select_3_wrong)
random.shuffle(select_3_wrong)
print(select_3_wrong)
# correct = [1]
# wrong = [2,3,4,5,6,7]
# select_3_wrong = random.sample(wrong, 3)
# print(select_3_wrong)
# an_all = correct + select_3_wrong
# random.shuffle(an_all)
# print(an_all)


if not False:
    print(1)