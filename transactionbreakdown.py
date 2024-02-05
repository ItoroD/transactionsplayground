
print("Hello World")

def deserialize_hex(hex_transaction):
    transaction = {}

    #fixed sized values
    transaction['version'] = hex_transaction[0:8]
    transaction['marker'] = int(hex_transaction[8:10], 16)
    transaction['flag'] = int(hex_transaction[10:12], 16)
    transaction['tx_in_count'] = int(hex_transaction[12:14], 16)
    transaction['tx_in'] = hex_transaction[14:96]
    transaction['tx_out_count'] = int(hex_transaction[96:98], 16)
    transaction['tx_out'] = hex_transaction[96:246]
    transaction['segwit'] = hex_transaction[246:378]
    transaction['lock_time'] = hex_transaction[378:386]

    hex_value = hex_transaction[0:8]
    # Reverse the byte order to convert to little endian
    little_endian_hex = "".join(reversed([hex_value[i:i+2] for i in range(0, len(hex_value), 2)]))
    # Convert the little endian hex to an integer
    dec_value = int(little_endian_hex, 16)

    print(dec_value)
    
    return transaction

hex_value = "e81c000000000000"
# Reverse the byte order to convert to little endian
little_endian_hex = "".join(reversed([hex_value[i:i+2] for i in range(0, len(hex_value), 2)]))
# Convert the little endian hex to an integer
dec_value = int(little_endian_hex, 16)

print(dec_value)

#this is input structure
    #previoustxid                                                   #outputnum  #sizeofUnlockscript    #sequence
#0ccc140e766b5dbc884ea2d780c5e91e4eb77597ae64288a42575228b79e2349   00000000        00                  00000000

#this is output structure
#numOfOutput        #amountToOuput0     #lockscriptSizeOutput0      #lockscriptForOutput0                                                   #amountToOuput1     #lockscriptSizeOutput0          #lockscriptForOutput01                     
#02                  bd37060000000000        22                    5120245091249f4f29d30820e5f36e1e5d477dc3386144220bd6f35839e94de4b9ca     e81c000000000000            16                  001416d31d7632aa17b3b316b813c0a3177f5b615020       

#witnessCount    #datalengthOfWitness                   witnessData
#    01              40                 838a1f0f1ee607b54abf0a3f55792f6f8d09c3eb7a9fa46cd4976f2137ca2e3f4a901e314e1b827c3332d7e1865ffe1d7ff5f5d7576a9000f354487a09de44cd


print(deserialize_hex("020000000001010ccc140e766b5dbc884ea2d780c5e91e4eb77597ae64288a42575228b79e234900000000000000000002bd37060000000000225120245091249f4f29d30820e5f36e1e5d477dc3386144220bd6f35839e94de4b9cae81c00000000000016001416d31d7632aa17b3b316b813c0a3177f5b6150200140838a1f0f1ee607b54abf0a3f55792f6f8d09c3eb7a9fa46cd4976f2137ca2e3f4a901e314e1b827c3332d7e1865ffe1d7ff5f5d7576a9000f354487a09de44cd00000000"))

