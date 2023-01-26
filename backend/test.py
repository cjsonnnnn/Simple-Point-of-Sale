import bcrypt

msg = "ASSD"
ep = bcrypt.hashpw(msg.encode(), bcrypt.gensalt())
print(ep)
print(bcrypt.checkpw(msg.encode(), ep))