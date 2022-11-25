# Decode read-back bytes array into file
def decode(returned_bytes):
    bits_amount = len(returned_bytes) * 8
    high = 0
    i = 1
    for byte in returned_bytes:
        high = high | ( byte << bits_amount -8*i)
        i+=1
    
    return high

class Decode:

    def __init__(self):
        self.full_msg = ''

    def add(self, msg):
        msg = "{0:b}\n".format(decode(msg))
        if msg == '1011000000010000000':
            print("Reply is: Fatal writing (0x580 0x80)")
        elif msg == '101100000000110000001000000':
            print("Reply is: Successful writing (0x580 0x60 0x40)")
        elif msg == '1011000000110000000':
            print("Reply is: Fatal writing (0x581 0x80)")
        elif msg == '101100000010110000001000000':
            print("Reply is: Successful writing (0x580 0x60 0x40)")
        else:
            print("unknown feedback")

        self.full_msg += msg

    def save(self):
        with open('D:/My_projects/python_projects/engine/src/decode.txt', 'w') as file:  
            try: file.truncate(0)
            except Exception as file_error:
                print(file_error)

            file.write(self.full_msg)

