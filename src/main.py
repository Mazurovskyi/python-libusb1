import usb1
import sys
import time
from . decoder import Decode



def processReceivedData(transfer):
    if transfer.getStatus() != usb1.TRANSFER_COMPLETED:
        # Transfer did not complete successfully, there is no data to read.
        # This example does not resubmit transfers on errors. You may want
        # to resubmit in some cases (timeout, ...).
        return
    data = transfer.getBuffer()[:transfer.getActualLength()]
    print("data: ",data)
    # Process data...
    # Resubmit transfer once data is processed.
    transfer.submit()

def show(reading_bytes):
    returned_value = []
    for byte in reading_bytes:
        returned_value.append(byte)

    print("reading_bytes: [",end=' ')
    for el in returned_value:
        print(hex(el), end=' ')

    print("] \n")






#initialization_start = (0x01, 0x00)	#01 h Start network node
#initialization_oper =  (0x80, 0x00)	#02 h Stop network node
                                        #80 h Go to “Pre-operational”
                                        #81 h Reset node
                                        #82 h Reset communication

initialization_start = [0x03, 0x00, 0x82, 0x01, 0x00]   #0x03 0x00 0x82
initialization_oper = [0x03, 0x00, 0x82, 0x80, 0x00]
control_word_0F = [0x03, 0x00, 0x86, 0x2B, 0x40, 0x60, 0x00, 0x0F, 0x00]
work_mode = [0x03, 0x00, 0x85, 0x2F, 0x60, 0x60, 0x00, 0x01]
actual_position = [0x03, 0x00, 0x84, 0x40, 0x64, 0x60, 0x00]
speed = [ 0x03, 0x00, 0x88, 0x23, 0x81, 0x60, 0x00, 0xE8, 0x03, 0x00, 0x00 ]
acceleration = [0x03, 0x00, 0x88, 0x23, 0x83, 0x60, 0x00, 0x20, 0x4E, 0x00, 0x00]
control_word_2F = [0x03, 0x00, 0x86, 0x2B, 0x40, 0x60, 0x00, 0x2F, 0x00]
location_cash = [0x03, 0x00, 0x88, 0x23, 0x7A, 0x60, 0x00, 0xE0, 0x93, 0x04, 0x00]
status = [0x03, 0x00, 0x84, 0x40, 0x41, 0x60, 00]

dataframe = [control_word_0F, work_mode, actual_position, speed, acceleration, control_word_2F, location_cash, status]


control_word_rev = [0xC0, 0x21, 0x8A, 0xD0, 0x18, 0x00, 0x0B, 0xC0, 0x00]
location_cash_rev = [0xC0, 0x22, 0x08, 0xDE, 0x98, 0x00, 0x38, 0x24, 0xC1, 0x00, 0x00]

dataframe_rev = [control_word_rev,location_cash_rev]



returned_msg = Decode()

with usb1.USBContext() as context:
    handle = context.openByVendorIDAndProductID(0x5555,0x5710)
    if handle is None:
        print("Device not found")
        sys.exit(0)
        
    handle.claimInterface(0)

    print("Interface is claimed \n")


    for data in dataframe:

        #data.reverse()

        #invert_can_dataframe = []
        #for byte in data:
        #	invert_can_dataframe.append( ~byte & 0xFF)
        
        #data = bytes(invert_can_dataframe)

        transfared_bytes = handle.bulkWrite(0x01,data)
        print("transfared_bytes: ",transfared_bytes)

        time.sleep(0.5)

        reading_bytes = handle.bulkRead(0x83,15)
        print("reading_bytes: ",reading_bytes)
        returned_msg.add(reading_bytes)

        show(reading_bytes)
 
    returned_msg.save()


