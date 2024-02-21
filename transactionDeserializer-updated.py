def deserialize_hex(hex_transaction):
    transaction = {}


def convertEndian(hexString):
    hex_value = "e81c000000000000"
    # Reverse the byte order to convert to little endian
    little_endian_hex = "".join(reversed([hex_value[i:i+2] for i in range(0, len(hex_value), 2)]))
    # Convert the little endian hex to an integer
    #dec_value = int(little_endian_hex, 16)
    #print(dec_value)
    return little_endian_hex

def convertFixedLength(hexValue):
    bigEdianHex = convertEndian(hexValue)
    dec_value = int(bigEdianHex, 16)
    return [dec_value, len(hexValue)]

def decodeCompactSize(hexValue):
    firstByte = int(hexValue[0:2],16)
    hexLength = 2

    if(firstByte < 253):
        return [firstByte, hexLength]
    elif(firstByte == 253):
        hexLength = 4
        decodedValue = convertFixedLength(hexValue[2:6])[0]
        return [decodedValue, hexLength]
    elif(firstByte == 254):
        hexLength = 8
        decodedValue = convertFixedLength(hexValue[2:10])[0]
        return [decodedValue, hexLength]
    elif(firstByte == 255):
        hexLength = 16
        decodedValue = convertFixedLength(hexValue[2:18])[0]
        return [decodedValue, hexLength]
    
def decodeField(startIdx, length, decodeFunction, rawTransaction):
        hexValue = rawTransaction[startIdx: startIdx + length]
        decodedData = decodeFunction(hexValue)
        return decodedData
    
    # version has first 4 bytes
def getVersion(rawTransaction):
        version = decodeField(0, 8, convertFixedLength, rawTransaction)
        return version
    
def isSegWit(rawTransaction):
    version = getVersion(rawTransaction)[0]
    #version = decodeField(0, 8, convertFixedLength, rawTransaction)
    if(version < 2):
        return False 

    #now we check that marker and flag are in the format 0001
    marker = int(rawTransaction[8:10],16)
    flag = int(rawTransaction[10:12],16)
    return marker == 0 and flag == 1

def getInputCount(rawTransaction, isSegWit):
    nextOffset = getVersion(rawTransaction)[1]
    #print(nextOffset)
    #here we want to skip marker and flag if it is a segwit transaction
    nextOffset =  nextOffset + 4 if isSegWit else nextOffset
    [inputCount, hexToSkip] = decodeField(nextOffset, 2, decodeCompactSize, rawTransaction)
    #return [inputCount, hexToSkip + nextOffset]
    return [inputCount,  hexToSkip + nextOffset]


def getInputs(rawTransaction):
    inputs = []
    [inputCount, nextOffset] = getInputCount(rawTransaction, isSegWit)    

    for i in range(inputCount):
        [txid, hexToSkip] = decodeField(currentOffset, 64, convertEndian, rawTransaction)
        currentOffset += hexToSkip
    

rawHex = "020000000001010ccc140e766b5dbc884ea2d780c5e91e4eb77597ae64288a42575228b79e234900000000000000000002bd37060000000000225120245091249f4f29d30820e5f36e1e5d477dc3386144220bd6f35839e94de4b9cae81c00000000000016001416d31d7632aa17b3b316b813c0a3177f5b6150200140838a1f0f1ee607b54abf0a3f55792f6f8d09c3eb7a9fa46cd4976f2137ca2e3f4a901e314e1b827c3332d7e1865ffe1d7ff5f5d7576a9000f354487a09de44cd00000000"
isSegwitTx = isSegWit(rawHex)
print(isSegwitTx)
inputCount = getInputCount(rawHex, isSegwitTx)
print(inputCount)
