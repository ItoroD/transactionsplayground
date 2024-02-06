import hashlib
import ecdsa
import base58

from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

def hash160(data: bytes):
    '''sha256 followed by ripemd160'''
    hash_1 = hashlib.sha256(data).digest()
    hash_2 = hashlib.new('ripemd160', hash_1).digest()
    return hash_2

def encode_base58_checksum(b: bytes):
    return base58.b58encode(b + hash256(b)[:4]).decode()

def decode_base58(s: str):
    return base58.b58decode(s)

def hash256(s):
    return hashlib.sha256(s).digest()

def hash256Two(s):
    return hashlib.sha256(hashlib.sha256(s).digest()).digest()

def generateRedeemScript(preImageHex):
    preImage = bytes.fromhex(preImageHex)
    preImageHash = hash256(preImage)
    #preImageHash[::-1].hex()
    redeemScript = bytes.fromhex("a8" + preImageHash.hex() + "88")
    print("redeemScript", redeemScript.hex())
    #print(preImageHash.hex())
    return redeemScript

def generateP2SHAddressFromScript(redeemScript, network):
    rs_hash = hash160(redeemScript)
    if network == "regtest" or network == "testnet":
        prefix = bytes.fromhex("c4")
    elif network == "mainnet":
        prefix = bytes.fromhex("05")
    else:
        return "Enter the network: tesnet/regtest/mainnet"
    return encode_base58_checksum(prefix + rs_hash)

def connect_to_node():
    """Connect to a Bitcoin node running on WSL."""
    try:
        # Replace 'user' and 'password' with your RPC user and password
        rpc_connection = AuthServiceProxy("http://%s:%s@localhost:18443" % ("itoro", "itoro"))
        return rpc_connection
    except JSONRPCException as json_exception:
        print(json_exception.error)

def privkey_to_pubkey(privkey: bytes):
    '''Converts a private key (bytes) to a compressed pubkey (bytes)'''
    privkey = ecdsa.SigningKey.from_string(privkey, curve=ecdsa.SECP256k1) # Don't forget to specify the curve
    uncompressed_pubkey = privkey.get_verifying_key()

    x_cor = bytes.fromhex(uncompressed_pubkey.to_string().hex())[:32] # The first 32 bytes are the x coordinate
    y_cor = bytes.fromhex(uncompressed_pubkey.to_string().hex())[32:] # The last 32 bytes are the y coordinate
    if int.from_bytes(y_cor, byteorder="big", signed=True) % 2 == 0: # We need to turn the y_cor into a number.
        compressed_pubkey = bytes.fromhex("02") + x_cor
    else:
        compressed_pubkey = bytes.fromhex("03") + x_cor
    return compressed_pubkey

def varint_len(data: bytes):
    '''returns the length of the input as a variable integer'''
    l = len(data)
    if l < int('fd',16):
        varint = l.to_bytes(1, byteorder="little", signed=False)
    elif l < int('ffff',16):
        varint = bytes.fromhex("fd") + l.to_bytes(2, byteorder="little", signed=False)
    else:
        raise Exception("This function only handles up to 0xffff bytes")
    return varint

def pushbytes(data: bytes):
    '''prepends the length of the input in bytes.
    Used for adding OP_PUSHBYTES in bitcoin script where stack items can be of arbitrary length.
    see BIP62
    '''
    l = len(data)
    if l <= 76:
        pushbytes = l.to_bytes(1, byteorder="little", signed=False)
    elif l <= 255:
        pushbytes = bytes.fromhex("4c") + l.to_bytes(1, byteorder="little", signed=False)
    elif l <= 520:
        pushbytes = bytes.fromhex("4d") + l.to_bytes(2, byteorder="little", signed=False)
    else:
        raise Exception("This function only handles up to 520 bytes")
    return pushbytes + data



def spendFunds(address, txid_to_spend, index_to_spend):
    receiver_spk = bytes.fromhex("76a9143bc28d6d92d9073fb5e3adf481795eaf446bceed88ac")

    # Set our outputs
    # Create a new pubkey to use as a change output.
    change_privkey = bytes.fromhex("4444444444444444444444444444444444444444444444444444444444444444")
    change_pubkey = privkey_to_pubkey(change_privkey)

    # Determine our output scriptPubkeys and amounts (in satoshis)
    output1_value_sat = int(float("1.5") * 100000000)
    output1_spk = receiver_spk
    output2_value_sat = int(float("0.5") * 100000000)
    output2_spk = bytes.fromhex("76a914") + hash160(change_pubkey) + bytes.fromhex("88ac")

    # VERSION
    # version '2' indicates that we may use relative timelocks (BIP68)
    version = bytes.fromhex("0200 0000")

    # INPUTS
    # We have just 1 input
    input_count = bytes.fromhex("01")

    # Convert txid and index to bytes (little endian)
    txid = (bytes.fromhex(txid_to_spend))[::-1]
    index = index_to_spend.to_bytes(4, byteorder="little", signed=False)

    # For the unsigned transaction we use an empty scriptSig
    scriptsig = bytes.fromhex("")

    # use 0xffffffff unless you are using OP_CHECKSEQUENCEVERIFY, locktime, or rbf
    sequence = bytes.fromhex("ffff ffff")

    inputs = (
        txid
        + index
        + varint_len(scriptsig)
        + scriptsig
        + sequence
    )

    # OUTPUTS
    # 0x02 for out two outputs
    output_count = bytes.fromhex("02")

    # OUTPUT 1 
    output1_value = output1_value_sat.to_bytes(8, byteorder="little", signed=True)
    # 'output1_spk' already defined at the start of the script

    # OUTPUT 2
    output2_value = output2_value_sat.to_bytes(8, byteorder="little", signed=True)
    # 'output2_spk' already defined at the start of the script

    outputs = (
        output1_value
        + pushbytes(output1_spk)
        + output2_value
        + pushbytes(output2_spk)
    )

    # LOCKTIME
    locktime = bytes.fromhex("0000 0000")

    unsigned_tx = (
        version
        + input_count
        + inputs
        + output_count
        + outputs
        + locktime
    )
    print("unsigned_tx: ", unsigned_tx.hex())




preimageHex = "427472757374204275696c64657273"
redeemScript = generateRedeemScript(preimageHex)
address = generateP2SHAddressFromScript(redeemScript,"regtest")
print("address:",address)

#node = connect_to_node()
#print(node.getblockchaininfo())

#node = setup_testshell()
#balance = node.getbalance()
#print(f"The balance of the wallet is {balance}")