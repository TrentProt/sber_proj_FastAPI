import bcrypt
pas = b'gggdfg'

hashed = bcrypt.hashpw(pas, bcrypt.gensalt(rounds=4))

if bcrypt.checkpw(pas, hashed):
        print("It Matches!")
else:
    print("It Does not Match :(")

print(hashed)