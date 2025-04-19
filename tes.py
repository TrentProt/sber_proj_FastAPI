from datetime import datetime

current_time = datetime.utcnow().timestamp()
p = 123
if current_time > p:
    print(True)