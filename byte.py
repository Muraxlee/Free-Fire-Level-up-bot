import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from protobuf_decoder.protobuf_decoder import Parser
import json

import base64
import time
from datetime import datetime

da = "f2212101"
dec = [
    "80",
    "81",
    "82",
    "83",
    "84",
    "85",
    "86",
    "87",
    "88",
    "89",
    "8a",
    "8b",
    "8c",
    "8d",
    "8e",
    "8f",
    "90",
    "91",
    "92",
    "93",
    "94",
    "95",
    "96",
    "97",
    "98",
    "99",
    "9a",
    "9b",
    "9c",
    "9d",
    "9e",
    "9f",
    "a0",
    "a1",
    "a2",
    "a3",
    "a4",
    "a5",
    "a6",
    "a7",
    "a8",
    "a9",
    "aa",
    "ab",
    "ac",
    "ad",
    "ae",
    "af",
    "b0",
    "b1",
    "b2",
    "b3",
    "b4",
    "b5",
    "b6",
    "b7",
    "b8",
    "b9",
    "ba",
    "bb",
    "bc",
    "bd",
    "be",
    "bf",
    "c0",
    "c1",
    "c2",
    "c3",
    "c4",
    "c5",
    "c6",
    "c7",
    "c8",
    "c9",
    "ca",
    "cb",
    "cc",
    "cd",
    "ce",
    "cf",
    "d0",
    "d1",
    "d2",
    "d3",
    "d4",
    "d5",
    "d6",
    "d7",
    "d8",
    "d9",
    "da",
    "db",
    "dc",
    "dd",
    "de",
    "df",
    "e0",
    "e1",
    "e2",
    "e3",
    "e4",
    "e5",
    "e6",
    "e7",
    "e8",
    "e9",
    "ea",
    "eb",
    "ec",
    "ed",
    "ee",
    "ef",
    "f0",
    "f1",
    "f2",
    "f3",
    "f4",
    "f5",
    "f6",
    "f7",
    "f8",
    "f9",
    "fa",
    "fb",
    "fc",
    "fd",
    "fe",
    "ff",
]
x = [
    "1",
    "01",
    "02",
    "03",
    "04",
    "05",
    "06",
    "07",
    "08",
    "09",
    "0a",
    "0b",
    "0c",
    "0d",
    "0e",
    "0f",
    "10",
    "11",
    "12",
    "13",
    "14",
    "15",
    "16",
    "17",
    "18",
    "19",
    "1a",
    "1b",
    "1c",
    "1d",
    "1e",
    "1f",
    "20",
    "21",
    "22",
    "23",
    "24",
    "25",
    "26",
    "27",
    "28",
    "29",
    "2a",
    "2b",
    "2c",
    "2d",
    "2e",
    "2f",
    "30",
    "31",
    "32",
    "33",
    "34",
    "35",
    "36",
    "37",
    "38",
    "39",
    "3a",
    "3b",
    "3c",
    "3d",
    "3e",
    "3f",
    "40",
    "41",
    "42",
    "43",
    "44",
    "45",
    "46",
    "47",
    "48",
    "49",
    "4a",
    "4b",
    "4c",
    "4d",
    "4e",
    "4f",
    "50",
    "51",
    "52",
    "53",
    "54",
    "55",
    "56",
    "57",
    "58",
    "59",
    "5a",
    "5b",
    "5c",
    "5d",
    "5e",
    "5f",
    "60",
    "61",
    "62",
    "63",
    "64",
    "65",
    "66",
    "67",
    "68",
    "69",
    "6a",
    "6b",
    "6c",
    "6d",
    "6e",
    "6f",
    "70",
    "71",
    "72",
    "73",
    "74",
    "75",
    "76",
    "77",
    "78",
    "79",
    "7a",
    "7b",
    "7c",
    "7d",
    "7e",
    "7f",
]


def generate_random_hex_color():
    # List of top 50 colors without #
    top_colors = [
    "902000156", "902000157", "902000172", "902000186", "902000191", 
    "902000231", "902000211", "902032018", "902032017", "902032014", 
    "902027016", "902033026", "902033027", "902042014", "902044006", 
    "902045005", "902045009", "902044003", "902042014"
]
    # Select a random color from the list
    random_color = random.choice(top_colors)
    return random_color




def encrypt_packet(plain_text, key, iv):
    plain_text = bytes.fromhex(plain_text)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    cipher_text = cipher.encrypt(pad(plain_text, AES.block_size))
    return cipher_text.hex()


def dec_to_hex(ask):
    ask_result = hex(ask)
    final_result = str(ask_result)[2:]
    if len(final_result) == 1:
        final_result = "0" + final_result
        return final_result
    else:
        return final_result


class ParsedResult:
    def __init__(self, field, wire_type, data):
        self.field = field
        self.wire_type = wire_type
        self.data = data


class ParsedResultEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ParsedResult):
            return {"field": obj.field, "wire_type": obj.wire_type, "data": obj.data}
        return super().default(obj)






def bunner_():
    bunner_1 = "902033001"
    bunner_2 = "902033013"
    bunner_3 = "902000172"
    bunner_4 = "902000271"
    bunner_5 = "902032014"
    bunner_6 = "902045004"
    bunner_7 = "902043009"
    bunner_8 = "902000003"
    bunner_9 = "902027027"
    bunner_10 = "902000306"
    bunner_11 = "902033017"
    
    # وضع كل البنرات في قائمة
    banners = [bunner_1, bunner_2, bunner_3, bunner_4, bunner_5,
               bunner_6, bunner_7, bunner_8, bunner_9, bunner_10, bunner_11]
    
    # اختيار بنر عشوائي من القائمة
    selected_bunner = random.choice(banners)
    
    # تحويل البنر إلى عدد صحيح إذا كان المطلوب نوع int
    selected_bunner_int = int(selected_bunner)  # تحويل إلى int
    
    return selected_bunner_int



def create_varint_field(field_number, value):
    field_header = (field_number << 3) | 0  # Varint wire type is 0
    return encode_varint(field_header) + encode_varint(value)


def create_length_delimited_field(field_number, value):
    field_header = (field_number << 3) | 2  # Length-delimited wire type is 2
    encoded_value = value.encode() if isinstance(value, str) else value
    return (
        encode_varint(field_header) + encode_varint(len(encoded_value)) + encoded_value
    )


def create_protobuf_packet(fields):
    packet = bytearray()    
    for field, value in fields.items():
        if isinstance(value, dict):
            nested_packet = create_protobuf_packet(value)
            packet.extend(create_length_delimited_field(field, nested_packet))
        elif isinstance(value, int):
            packet.extend(create_varint_field(field, value))
        elif isinstance(value, str) or isinstance(value, bytes):
            packet.extend(create_length_delimited_field(field, value))
    
    return packet        


def encode_varint(number):
    # Ensure the number is non-negative
    if number < 0:
        raise ValueError("Number must be non-negative")

    # Initialize an empty list to store the varint bytes
    encoded_bytes = []

    # Continuously divide the number by 128 and store the remainder,
    # and add 128 to the remainder if there are still higher bits set
    while True:
        byte = number & 0x7F
        number >>= 7
        if number:
            byte |= 0x80
        encoded_bytes.append(byte)
        if not number:
            break

    # Return the varint bytes as bytes object
    return bytes(encoded_bytes)


# Example usage
numbers = [902000208, 902000209, 902000210, 902000211]


def Encrypt_ID(number):
    number = int(number)
    encoded_bytes = []
    while True:
        byte = number & 0x7F
        number >>= 7
        if number:
            byte |= 0x80
        encoded_bytes.append(byte)
        if not number:
            break
    return bytes(encoded_bytes).hex()


def Encrypt(number):
    number = int(number)
    encoded_bytes = []

    while True:
        byte = number & 0x7F
        number >>= 7
        if number:
            byte |= 0x80

        encoded_bytes.append(byte)
        if not number:
            break
    return bytes(encoded_bytes).hex()


print(Encrypt(11057708226))


def Decrypt(encoded_bytes):
    encoded_bytes = bytes.fromhex(encoded_bytes)
    number = 0
    shift = 0
    for byte in encoded_bytes:
        value = byte & 0x7F
        number |= value << shift
        shift += 7
        if not byte & 0x80:
            break
    return number


def Decrypt_ID(da):
    if da != None and len(da) == 10:
        w = 128
        xxx = len(da) / 2 - 1
        xxx = str(xxx)[:1]
        for i in range(int(xxx) - 1):
            w = w * 128
        x1 = da[:2]
        x2 = da[2:4]
        x3 = da[4:6]
        x4 = da[6:8]
        x5 = da[8:10]
        return str(
            w * x.index(x5)
            + (dec.index(x2) * 128)
            + dec.index(x1)
            + (dec.index(x3) * 128 * 128)
            + (dec.index(x4) * 128 * 128 * 128)
        )

    if da != None and len(da) == 8:
        w = 128
        xxx = len(da) / 2 - 1
        xxx = str(xxx)[:1]
        for i in range(int(xxx) - 1):
            w = w * 128
        x1 = da[:2]
        x2 = da[2:4]
        x3 = da[4:6]
        x4 = da[6:8]
        return str(
            w * x.index(x4)
            + (dec.index(x2) * 128)
            + dec.index(x1)
            + (dec.index(x3) * 128 * 128)
        )

    return None


def parse_results(parsed_results):
    result_dict = {}
    for result in parsed_results:
        field_data = {}
        field_data["wire_type"] = result.wire_type
        if result.wire_type == "varint":
            field_data["data"] = result.data
        if result.wire_type == "string":
            field_data["data"] = result.data
        if result.wire_type == "bytes":
            field_data["data"] = result.data
        elif result.wire_type == "length_delimited":
            field_data["data"] = parse_results(result.data.results)
        result_dict[result.field] = field_data
    return result_dict


def get_available_room(input_text):
    try:
        parsed_results = Parser().parse(input_text)
        parsed_results_objects = parsed_results
        parsed_results_dict = parse_results(parsed_results_objects)
        json_data = json.dumps(parsed_results_dict)
        return json_data
    except Exception as e:
        print(f"error {e}")
        return None


def get_leader(packet):
    json_result = get_available_room(packet)
    parsed_data = json.loads(json_result)
    json_data = parsed_data["5"]["data"]["1"]["data"]["8"]["data"]
    return str(json_data)


def get_target(packet):
    json_result = get_available_room(packet)
    parsed_data = json.loads(json_result)
    json_data = parsed_data["5"]["data"]["1"]["data"]["1"]["data"]
    return str(json_data)


def get_player_status(packet):
    json_result = get_available_room(packet)
    parsed_data = json.loads(json_result)
    json_data = parsed_data["5"]
    keys = list(json_data.keys())
    data = keys[1]
    keys = list(json_data[data].keys())
    
    try:
        data = json_data[data]
        data = data["1"]
        data = data["data"]
        data = data["3"]
    except KeyError:
        return ["غير متصل", packet]

    if data["data"] == 1:
        target = get_target(packet)
        return ["في وضع اللعب الفردي (Solo)", target]

    if data["data"] == 2:
        target = get_target(packet)
        leader = get_leader(packet)
        group_count = parsed_data["5"]["data"]["1"]["data"]["9"]["data"]
        return ["في مجموعة داخل اللعبة (Squad)", target, leader, group_count]

    if data["data"] == 3:
        target = get_target(packet)
        return ["على وشك دخول المباراة (On the verge of joining the game)", target]

    if data["data"] == 5:
        target = get_target(packet)
        return ["على وشك دخول المباراة (On the verge of joining the game)", target]

    if data["data"] == 7 or data["data"] == 6:
        target = get_target(packet)
        return ["في جزيرة الصداقة (Friendship Island Mode)", target]
    
    return "غير موجود (Not Found)"


def send_spam_invites(inv, key, iv, id):


        packet = f"080112e90108fff3f5bd0610{Encrypt(id)}180228ffc7afa02542337b22537469636b6572537472223a225b313d313230303030303030312d31325d222c2274797065223a22537469636b6572227d4a440a2dc3aac2a7c281c3a0c2bcc2ba48545f4dc383c298c3a2c282c2b4c3a2c282c2b3c3a2c282c2a62ac3aac2a7c28210ecdd8dae0318e4efd2ad0320e401288bfff5b103520261726a520a4c68747470733a2f2f67726170682e66616365626f6f6b2e636f6d2f76392e302f3130363230353531303932343336302f706963747572653f77696474683d313630266865696768743d313630100118017200"



        print(packet)

        encrypted_packet = nmnmmmmn(packet, key, iv)
        header_length = len(encrypted_packet) // 2
        print(f" send_spam_invites {header_length}")

        header_length_hex = dec_to_hex(header_length)
        print(f" send_spam_invites {header_length_hex}")

        if len(header_length_hex) == 2:
            final_packet = "1215000000" + header_length_hex + encrypted_packet
        elif len(header_length_hex) == 3:
            final_packet = "121500000" + header_length_hex + encrypted_packet
        elif len(header_length_hex) == 4:
            final_packet = "12150000" + header_length_hex + encrypted_packet
        elif len(header_length_hex) == 5:
            final_packet = "12150000" + header_length_hex + encrypted_packet
        else:
            raise ValueError("eororr 505 🐜")

        inv.send(bytes.fromhex(final_packet))


def SendRopen(inv, key, iv, uid):
    uid = {Encrypt(uid)}
    uid_hex = next(iter(uid))
    packet = f"080112e8010ae301afadaea327bfbd809829a8fe89db07eda4c5f818f8a485850eefb3a39e06{uid_hex}ecb79fd623e4b3c0f506c6bdc48007d4efbc7ce688be8709c99ef7bc02e0a8bcd607d6ebe8e406dcc9a6ae07bfdab0e90a8792c28d08b58486f528cfeff0c61b95fcee8b088f96da8903effce2b726b684fbe10abfe984db28bbfebca528febd8dba28ecb98cb00baeb08de90583f28a9317a5ced6ab01d3de8c71d3a1b1be01ede292e907e5ecd0b903b2cafeae04c098fae5048cfcc0cd18d798b5f401cd9cbb61e8dce3c00299b895de1184e9c9ee11c28ed0d803f8b7ffec02a482babd011001"
    

    encrypted_packet = nmnmmmmn(packet, key, iv)
    header_length = len(encrypted_packet) // 2  
    print(f" smpa > {header_length}")
    

    header_length_hex = dec_to_hex(header_length)
    print(f"sapm > {header_length_hex}")
    

    if len(header_length_hex) == 2:
        final_packet = "0f15000000" + header_length_hex + encrypted_packet
    elif len(header_length_hex) == 3:
        final_packet = "0f1500000" + header_length_hex + encrypted_packet
    elif len(header_length_hex) == 4:
        final_packet = "0f150000" + header_length_hex + encrypted_packet
    elif len(header_length_hex) == 5:
        final_packet = "0f150000" + header_length_hex + encrypted_packet
    else:
        raise ValueError("eororr 505 🐜")
    
    # DONE 
    inv.send(bytes.fromhex(final_packet))



def SendRopen4(inv, key, iv):
    packet = "080112f5040a010110013a0d0a044944433110a3011a024d453a0d0a04494443321085011a024d453a150a044944433310ffffffffffffffffff011a024d4540014a0601090a121920580162ac040a8001303830453830383137374445454236353032303130313030303030303030304130303042303030313030303030303030313831323544413730393030303032333431373232393134303030303030303030303030303030303030303030303030303030303030303030303030303066663030303030303030663939613032653810441a850376595a551205004a020c085301025405060850035a0e0107535200055650550c0a045501060105091500084508040e0201065106040f0e0506520304005401540c0a0802550252000502020d1a01024a5c5202026572697a6063526264435e447670507e510e64525704060c1a084c745959435c786e7d48097b7e0052696658555b697a0476556255430d15000a457749516a1e654a4f647e6b695b4c59021b796667695d766a71404209130e4d684f575f445363785471624840717d0158734c6540560a6d475b060d1205084a487a5f7d435e566404735463534d424a5b1f5c4742025f6f0856470b1302485e597b760c097f5c440952520545517552404e7e00625d6e7b4b740d13044c5c7145617e5c535d405559605945785b720f715b04600573007109041a094c655a457b7c195f504c7d5c41587c46630f7a75725d476c65490d610b120c455606426a697d435b767d407103605f487d68577f695271617b5d520913024d515c0175757203460579736b685164707553647d65647d726a686f0d22047e5f5855300a3a0812797b7f7e6212144207312e3130382e3848035001"

    encrypted_packet = nmnmmmmn(packet, key, iv)
    header_length = len(encrypted_packet) // 2
    print(f"in 5 > {header_length}")

    header_length_hex = dec_to_hex(header_length)
    print(f"in 5 > {header_length_hex}")

    if len(header_length_hex) == 2:
        final_packet = "0315000000" + header_length_hex + encrypted_packet
    elif len(header_length_hex) == 3:
        final_packet = "031500000" + header_length_hex + encrypted_packet
    elif len(header_length_hex) == 4:
        final_packet = "03150000" + header_length_hex + encrypted_packet
    elif len(header_length_hex) == 5:
        final_packet = "03150000" + header_length_hex + encrypted_packet
    else:
        raise ValueError("eororr 505 🐜")

    inv.send(bytes.fromhex(final_packet))

def Sendexit(inv, key, iv, uid):
    packet = "0807120608da89d98d27"

    encrypted_packet = nmnmmmmn(packet, key, iv)
    if encrypted_packet is None:
        return None

    header_length = len(encrypted_packet) // 2
    header_length_hex = dec_to_hex(header_length)

    if len(header_length_hex) == 2:
        final_packet = "0515000000" + header_length_hex + encrypted_packet
        inv.send(bytes.fromhex(final_packet))
    elif len(header_length_hex) == 3:
        final_packet = "051500000" + header_length_hex + encrypted_packet
        inv.send(bytes.fromhex(final_packet))
    elif len(header_length_hex) == 4:
        final_packet = "05150000" + header_length_hex + encrypted_packet
        inv.send(bytes.fromhex(final_packet))
    elif len(header_length_hex) == 5:
        final_packet = "05150000" + header_length_hex + encrypted_packet
        inv.send(bytes.fromhex(final_packet))





def nmnmmmmn(plain_text, key, iv):
    plain_text = bytes.fromhex(plain_text)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    cipher_text = cipher.encrypt(pad(plain_text, AES.block_size))
    return cipher_text.hex()


def invite1(inv, key, iv):
    packet = "080112b905120101180120032a026172420d0a04494443311085011a024d45420c0a044944433210781a024d45420d0a044944433310d7011a024d454801520601090a1219205801680172e8040a8001303830453832383139414630333736453032303130313030303030303030313230303133303030313030303030303032454636383242463430393030303031343431373232393134303030303030303030303030303030303030303030303030303030303030303030303030303066663030303030303030663939613032653810111abf0375505f5c1b00014d00040a000b005a085703570d030a525a025f0b090252090402050a020f0050041208064e0a5f565c5c550801090154030f0a0d000850010d0550045b55080b530155580f11020b4f555b0703627a6771636a576b6d465f437e7e5b7d580b6d5b5205010414515c5755505f1e43544a545d5d5f5c494c585e5f585b53515d524d594d57017a0e547a545a555366095e6b6f000a7405784c6373504e795d0e1a02457c5e5843517f6a7f480372760753696b5f515969700d7e5263554e0a11020a4f615e0162024f41555154604c520177037b446a407806774b5f1e6804140a4f68455e5743526375537560484a7875065973416244540a674e53010c120b4b667e7142685d7643576d186755011c08017645767c6104745f54740512084d6004780b416a7c41014b78516e4a726060486b7c47037c465804520e1a09094d034e43447740076b1748485d08460518715a7f4e7b567d5e53580b04100a445f5e7b76020b7c5347015e530245517b5043417d086e5c697b4b7a0f100d4f515d0074727b05400676716b695065777c55627e6a667d736b69680414074f5f054d626978425470764a78006f574878695879625878627455520c220477575f54300b3a091378796f796b6115154208312e3130382e3134480350019801e301aa01024f52"
    encrypted_packet = nmnmmmmn(packet, key, iv)
    if encrypted_packet is None:
        return None

    header_length = len(encrypted_packet) // 2
    header_length_hex = dec_to_hex(header_length)

    if len(header_length_hex) == 2:
        final_packet = "0515000000" + header_length_hex + encrypted_packet
        inv.send(bytes.fromhex(final_packet))
    elif len(header_length_hex) == 3:
        final_packet = "051500000" + header_length_hex + encrypted_packet
        inv.send(bytes.fromhex(final_packet))
    elif len(header_length_hex) == 4:
        final_packet = "05150000" + header_length_hex + encrypted_packet
        inv.send(bytes.fromhex(final_packet))
    elif len(header_length_hex) == 5:
        final_packet = "05150000" + header_length_hex + encrypted_packet
        inv.send(bytes.fromhex(final_packet))

def bbb1(inv, key, iv):
    packet = "08311289010801100f1803221fe28094cd9ecd9fcd9ee29d80e385a4ca9fc9aae29d80c9b4e1b480277320722a063131313132333008381e4001480150b58486f5285801600268c092d151720c0a0449444331106d1a024d45720d0a04494443321086011a024d45720d0a044944433310e2011a024d457a0701090a0b1219208801c8c89001d00101fa01020001"
    encrypted_packet = nmnmmmmn(packet, key, iv)
    if encrypted_packet is None:
        return None

    header_length = len(encrypted_packet) // 2
    header_length_hex = dec_to_hex(header_length)

    if len(header_length_hex) == 2:
        final_packet = "0515000000" + header_length_hex + encrypted_packet
        inv.send(bytes.fromhex(final_packet))
    elif len(header_length_hex) == 3:
        final_packet = "051500000" + header_length_hex + encrypted_packet
        inv.send(bytes.fromhex(final_packet))
    elif len(header_length_hex) == 4:
        final_packet = "05150000" + header_length_hex + encrypted_packet
        inv.send(bytes.fromhex(final_packet))
    elif len(header_length_hex) == 5:
        final_packet = "05150000" + header_length_hex + encrypted_packet
        inv.send(bytes.fromhex(final_packet))


def ope_gwt(inv, key, iv):

    packet = "08 1f 12 06 08 da 89 d9 8d 27"

    print(packet)
    encrypted_packet = nmnmmmmn(packet, key, iv)
    header_length = len(encrypted_packet) // 2
    print(f"in 5 > {header_length}")

    header_length_hex = dec_to_hex(header_length)
    print(f"in 5 > {header_length_hex}")

    if len(header_length_hex) == 2:
        final_packet = "0514000000" + header_length_hex + encrypted_packet
    elif len(header_length_hex) == 3:
        final_packet = "051400000" + header_length_hex + encrypted_packet
    elif len(header_length_hex) == 4:
        final_packet = "05140000" + header_length_hex + encrypted_packet
    elif len(header_length_hex) == 5:
        final_packet = "05140000" + header_length_hex + encrypted_packet
    else:
        raise ValueError("eororr 505 🐜")

    inv.send(bytes.fromhex(final_packet))

def kelly(inv, key, iv):
    bot_mode = bot_mode_pb2.BotMode()
    bot_mode.key1 = 17
    bot_mode.key2.uid = 7802788212
    bot_mode.key2.key2 = 1
    bot_mode.key2.key3 = 4
    bot_mode.key2.key4 = 62
    bot_mode.key2.byte = base64.b64decode("Gg==")
    bot_mode.key2.key8 = 5
    bot_mode.key2.key13 = 227
    binary_data = bot_mode.SerializeToString()
    packet = binary_data.hex()

    encrypted_packet = nmnmmmmn(packet, key, iv)
    header_length = len(encrypted_packet) // 2
    header_length_hex = dec_to_hex(header_length)
    
    if len(header_length_hex) == 2:
        final_packet = "0515000000" + header_length_hex + encrypted_packet
    elif len(header_length_hex) == 3:
        final_packet = "051500000" + header_length_hex + encrypted_packet
    elif len(header_length_hex) == 4:
        final_packet = "05150000" + header_length_hex + encrypted_packet
    elif len(header_length_hex) == 5:
        final_packet = "05150000" + header_length_hex + encrypted_packet
    else:
        raise ValueError("eororr 505 🐜")

    inv.send(bytes.fromhex(final_packet))



def kelly1(inv, key, iv):
    bot_mode = bot_mode_pb2.BotMode()
    bot_mode.key1 = 17
    bot_mode.key2.uid = 7802788212
    bot_mode.key2.key2 = 1
    bot_mode.key2.key3 = 5
    bot_mode.key2.key4 = 62
    bot_mode.key2.byte = base64.b64decode("Gg==")
    bot_mode.key2.key8 = 2
    bot_mode.key2.key13 = 227
    binary_data = bot_mode.SerializeToString()
    packet = binary_data.hex()
    print(packet)
    encrypted_packet = nmnmmmmn(packet, key, iv)
    header_length = len(encrypted_packet) // 2
    header_length_hex = dec_to_hex(header_length)
    
    if len(header_length_hex) == 2:
        final_packet = "0515000000" + header_length_hex + encrypted_packet
    elif len(header_length_hex) == 3:
        final_packet = "051500000" + header_length_hex + encrypted_packet
    elif len(header_length_hex) == 4:
        final_packet = "05150000" + header_length_hex + encrypted_packet
    elif len(header_length_hex) == 5:
        final_packet = "05150000" + header_length_hex + encrypted_packet
    else:
        raise ValueError("eororr 505 🐜")

    inv.send(bytes.fromhex(final_packet))


def started(inv, key, iv):

    packet = "0809123308b58486f5283a0d0a04494443311097011a024d453a0d0a04494443321080011a024d453a0d0a04494443331080011a024d45"

    encrypted_packet = nmnmmmmn(packet, key, iv)
    header_length = len(encrypted_packet) // 2
    print(f"strats > {header_length}")

    header_length_hex = dec_to_hex(header_length)
    print(f"moll> {header_length_hex}")

    if len(header_length_hex) == 2:
        final_packet = "0515000000" + header_length_hex + encrypted_packet
    elif len(header_length_hex) == 3:
        final_packet = "051500000" + header_length_hex + encrypted_packet
    elif len(header_length_hex) == 4:
        final_packet = "05150000" + header_length_hex + encrypted_packet
    elif len(header_length_hex) == 5:
        final_packet = "05150000" + header_length_hex + encrypted_packet
    else:
        raise ValueError("eororr 505 🐜")

    inv.send(bytes.fromhex(final_packet))

#def send_Anonymous(inv, key, iv):




def inv_opst(inv, key, iv):
    root = get_bot_pb2.Root()
    root.field1 = 1
    root.field2.field1 = 10982883893
    root.field2.field2 = 3067679507
    root.field2.field3 = 1
    
    # تحديد الوقت الحالي بتوقيت UTC
    current_time = datetime.now(pytz.utc)  # الحصول على الوقت الحالي بتوقيت UTC
    timestamp = int(current_time.timestamp())  # تحويل الوقت إلى طابع زمني (Unix timestamp)

    # تعيين الوقت في الحقل field5
    root.field2.field5 = timestamp  # تعيين الوقت الحالي بتوقيت UTC كطابع زمني
    
    root.field2.field7 = 1
    root.field2.field8 = '{"GroupID":3161100693,"Group":3,"Map":[1],"Game":1,"Match":2,"MemberNum":1,"RequireRankMin":219,"RequireRankMax":220,"CSSpecialModeEventId":0,"GroupTag":"0;0","SecretCode":"1740128473793558578_55fbsg66g6","RecruitCode":"1740128474885500781_uqi94qmebq","showGameBuf":0,"hasLuckyBuf":false,"hasMapBonus":false,"type":"group"}'
    root.field2.field10 = "en"
    root.field2.field9.field1 = "[00FF00]Anonymous"
    root.field2.field9.field2 = 902038028
    root.field2.field9.field3 = 901033004
    root.field2.field9.field4 = 219
    root.field2.field9.field8 = "[00FF00]Anonymous"
    root.field2.field13.field1 = "https://graph.facebook.com/v9.0/111802521083341/picture?width=160&height=160"
    root.field2.field13.field2 = 1
    root.field2.field13.field3 = 1
    root.field2.field14.SetInParent()

    binary_data = root.SerializeToString()
    packet = binary_data.hex()

    # تأكد من أن nmnmmmmn موجودة أو استخدم تشفير مناسب
    encrypted_packet = nmnmmmmn(packet, key, iv)
    header_length = len(encrypted_packet) // 2
    print(f" send_spam_invites {header_length}")

    def dec_to_hex(value):
        return hex(value)[2:]  # تحويل العدد إلى قيمة hex بدون "0x"

    header_length_hex = dec_to_hex(header_length)
    print(f" send_spam_invites {header_length_hex}")

    if len(header_length_hex) == 2:
        final_packet = "1215000000" + header_length_hex + encrypted_packet
    elif len(header_length_hex) == 3:
        final_packet = "121500000" + header_length_hex + encrypted_packet
    elif len(header_length_hex) == 4:
        final_packet = "12150000" + header_length_hex + encrypted_packet
    elif len(header_length_hex) == 5:
        final_packet = "12150000" + header_length_hex + encrypted_packet
    else:
        raise ValueError("eororr 505 🐜")

    inv.send(bytes.fromhex(final_packet))
        
def Opening(inv, key, iv, id):
    invite = bot_invite_pb2.invite_uid()
    invite.num = 2#2
    invite.Func.uid = int(id)
    invite.Func.region = "ME"
    invite.Func.number = 1
    encoded_data = invite.SerializeToString()
    packet = encoded_data.hex()
    encrypted_packet = nmnmmmmn(packet, key, iv)
    header_length = len(encrypted_packet) // 2
    header_length_hex = dec_to_hex(header_length)

    if len(header_length_hex) == 2:
        final_packet = "0515000000" + header_length_hex + encrypted_packet
    elif len(header_length_hex) == 3:
        final_packet = "051500000" + header_length_hex + encrypted_packet
    elif len(header_length_hex) == 4:
        final_packet = "05150000" + header_length_hex + encrypted_packet
    elif len(header_length_hex) == 5:
        final_packet = "05150000" + header_length_hex + encrypted_packet
    else:
        raise ValueError("eororr 505 🐜")

    inv.send(bytes.fromhex(final_packet))



def join_teamcode(inv, room_id, key, iv):
    room_id_hex = ''.join(format(ord(c), 'x') for c in room_id)
    packet = f"080412b705220701090a0b1219202a07{room_id_hex}300640014ae9040a8001303946454133424438453839323231443032303331423031313131313030303230303239303030323030323530303032353442383542303530393030303033423431373232393134323230313034303631343034376462626236636163626536363734373436356530303030303066663037303930353065313262636665363810dd011abf03755154571b08004d000c0950090c560c0b0857015a0f020f5d5009085657570c0b075d0f04080809120208440b0c0000080b5101060f0f060e5c010d0d5406560c0b0b0a5b005b0d0505000d1b020a445e5b0f026270697b636b5c606d4e5e437470517d5900665b5a04010e1a094f7c575b4a5178697f480878760e50606b585259697b077e5b605c4e0d12020a446b5e08610b4f465651546b465208740a7b436940780d7d4b561d610413094f684e54574a516a75547660484172750f5a7a416547540a6c4453080f1b08084d014e4c457c41066a1649485f08490413705b7e4f7a567f5e5c590005110b455e5e79760d0a775246005f52024751745148407c096f5d69794b750e1b0a4e6c747840625c7f415e6c1d6d5f081e02007f477f7d640e7e56567e041b50575654515e1f43564a5b5c565e5d484d595e5d5854525a5c534c584c57037a015571555b545267095c6b6001017504794d6273524e765c051b0b4460037b0b4161764108487151694972606b426b75440a7c415b045205100d44540e4d6a697a4a55747c41730b6f5f487a61597d68537369745d520e1a0c4f505d037d7a7203410c77716a69536c7f755363746b667c736860600d22047c575755300b3a091d6d647370687a1d144208312e3130382e3134480350015a0c0a044944433110761a024d455a0d0a04494443321084011a024d455a0d0a044944433310d7011a024d456a02656e8201024f52"
    encrypted_packet = nmnmmmmn(packet, key, iv)
    header_length = len(encrypted_packet) // 2
    print(f" goo > {header_length}")

    header_length_hex = dec_to_hex(header_length)
    print(f" goo > {header_length_hex}")

    if len(header_length_hex) == 2:
        final_packet = "0515000000" + header_length_hex + encrypted_packet
    elif len(header_length_hex) == 3:
        final_packet = "051500000" + header_length_hex + encrypted_packet
    elif len(header_length_hex) == 4:
        final_packet = "05150000" + header_length_hex + encrypted_packet
    elif len(header_length_hex) == 5:
        final_packet = "05150000" + header_length_hex + encrypted_packet
    else:
        raise ValueError("eororr 505 🐜")

    inv.send(bytes.fromhex(final_packet))

def xxx1(inv, key, iv):
    packet = "0803125c089cc2b6b929420c0a0449444331105d1a024d45420d0a04494443321091011a024d45420d0a044944433310ea011a024d454a0701090a0b12192050016214ffffffffffffffffff01ffffffffffffffffff0168037003820102656e"

    encrypted_packet = nmnmmmmn(packet, key, iv)
    if encrypted_packet is None:
        return None

    header_length = len(encrypted_packet) // 2
    header_length_hex = dec_to_hex(header_length)

    if len(header_length_hex) == 2:
        final_packet = "0e15000000" + header_length_hex + encrypted_packet
        inv.send(bytes.fromhex(final_packet))
    elif len(header_length_hex) == 3:
        final_packet = "0e1500000" + header_length_hex + encrypted_packet
        inv.send(bytes.fromhex(final_packet))
    elif len(header_length_hex) == 4:
        final_packet = "0e150000" + header_length_hex + encrypted_packet
        inv.send(bytes.fromhex(final_packet))
    elif len(header_length_hex) == 5:
        final_packet = "0e150000" + header_length_hex + encrypted_packet
    else:
        raise ValueError("eororr 505 🐜")
        
    print (final_packet)
    inv.send(bytes.fromhex(final_packet))

import threading

# متغير لحفظ الحزم المرسلة سابقًا
sent_packets = []

# دالة لإرسال الحزم في الخلفية
def send_packet(inv, final_packet):
    inv.send(bytes.fromhex(final_packet))

def xxx23(inv, key, iv, id):
    threads = []  # لتخزين الـ threads
    for _ in range(100):  # إرسال 100 حزمة
        hardest = hardest_pb2.hardest()
        hardest.field1 = 33
        hardest.field2.uid = int(id)
        hardest.field2.region = "ME"
        hardest.field2.field3 = 1
        hardest.field2.field4 = 1
        hardest.field2.field5 = base64.b64decode("AQkKEhYZIA==")
        hardest.field2.name = "—͟͞͞❀ㅤʟɪ❀ɴᴀ"
        hardest.field2.field7 = 228
        hardest.field2.field8 = 3210
        hardest.field2.field10 = "JO"
        hardest.field2.field11 = "7428b253defc164018c604a1ebbfebdf"
        hardest.field2.field12 = 1
        hardest.field2.field13 = int(id)
        hardest.field2.field16 = 1
        hardest.field2.field17.field1 = "098F82B99672C9EC02010200000000000036000200340002DE9E55D20900002541722914000000018bcf932db6cacbe667b5b9a3000000ff00000100835d80aa"
        hardest.field2.field17.field2 = 113
        hardest.field2.field17.filed3 = base64.b64decode("d1pfXBUBAE0GUwNXCgkGAABSVAZXCwEAAVMFAQZSBwZSXFQGVVcEDxICAkUAVVYJAQBSUQUOAAVVCQZQAFdSXFIDAwgABwIAVw9XARMAA0pdUAULZXNgcmFlVWFmTlhCd3hYeFALZ1pVBAAMEgdNd1xQRFh4aX1HAXh9D1RoYllSXGFwB39VYlRGDBUAAE9OXHVpSAZzdgEGTWFpclwCA0ReUHsGf1QIewYMEAtFZ0ZXXkNVY39XfmVBSXB8AVlxS2xAVwNlRl0BDhAMSn5UUmRBHl0KflVlZUdjAFlCXlFxA2NddFNgCw4aBExDHlVTWQpGbmBTXUIaY3AcQEFRQ1lFWllQRQcEFQlMA2JYYVJSY38IdWR/eGlwa2xHf3pQBUwaAnxKCxMBCU0Oc0tfbwJoY2IITHp3BX0ZA0ZSXkxTZ0Z8QmENEgJKfnh4Q1VeBRp7YWhyBFcCfFJ2d2ZIZldqWAdbDBICTXphYA9IH1xEBH5gVFBRd3deXA94UkN7b31qBQwVAwNPAGZZZlxFbgkCZl5VB1JoeW5QfAVzHVJHW0NRDA==")
        hardest.field2.field17.filed4 = base64.b64decode("f15YVA==")
        hardest.field2.field17.field6 = 11
        hardest.field2.field17.field7 = base64.b64decode("F38AUnFzZBIV")
        hardest.field2.field17.version = "1.109.4"
        hardest.field2.field17.field9 = 3
        hardest.field2.field17.field10 = 1
        hardest.field2.field18 = 214
        hardest.field2.field19 = 53
        
        entry1 = hardest.field2.field20.add()
        entry1.field1 = "IDC1"
        entry1.field2 = 75
        entry1.region = "ME"
        
        entry2 = hardest.field2.field20.add()
        entry2.field1 = "IDC2"
        entry2.field2 = 71
        entry2.region = "ME"
        
        entry3 = hardest.field2.field20.add()
        entry3.field1 = "IDC3"
        entry3.field2 = 283
        entry3.region = "ME"
        
        hardest.field2.field23.field2 = 1
        hardest.field2.field23.field3 = 1
        hardest.field2.avatar = bunner_()  # تغيير البنر مع كل حزمة
        hardest.field2.field26.SetInParent()
        hardest.field2.field28.SetInParent()
        
        encoded_data = hardest.SerializeToString()
        packet = encoded_data.hex()

        print(packet)

        encrypted_packet = nmnmmmmn(packet, key, iv)
        header_length = len(encrypted_packet) // 2
        print(f"inv > {header_length}")

        header_length_hex = dec_to_hex(header_length)
        print(f"inv > {header_length_hex}")

        if len(header_length_hex) == 2:
            final_packet = "0515000000" + header_length_hex + encrypted_packet
        elif len(header_length_hex) == 3:
            final_packet = "051500000" + header_length_hex + encrypted_packet
        elif len(header_length_hex) == 4:
            final_packet = "05150000" + header_length_hex + encrypted_packet
        elif len(header_length_hex) == 5:
            final_packet = "05150000" + header_length_hex + encrypted_packet
        else:
            raise ValueError("eororr 505 🐜")
        
        # استخدام threading لإرسال الحزم بشكل متوازي
        thread = threading.Thread(target=send_packet, args=(inv, final_packet))
        thread.start()
        threads.append(thread)

    # انتظار اكتمال جميع الحزم المرسلة
    for thread in threads:
        thread.join()

# استدعاء الدالة
# xxx23(inv, key, iv, id)

def Clan(id,code,key,iv):
    fields = {1: 3, 2: {1: int(id), 2: 1, 4: str(code)}}
    packet = create_protobuf_packet(fields).hex()
    packet_encrypt = encrypt_packet(packet,key,iv)
    package = dec_to_hex(int(len(packet_encrypt) // 2))
    if len(package) == 2: header = "1201000000"
    if len(package) == 3: header = "120100000"
    if len(package) == 4: header = "12010000"
    if len(package) == 5: header = "1201000"
    packet = header + package + packet_encrypt
    return packet
        
def gen_msgv2_clan(msg, key, iv):
    root = clan_msg_pb2.clan_msg(
        field_1=1,
        field_2=clan_msg_pb2.clan_msg.Nested2(
            field_1=10982883893,
            field_2=3067679507,
            field_3=1,
            field_4=msg,
            field_5=int(time.time()),
            field_9=clan_msg_pb2.clan_msg.Nested2.Nested9(
                field_1="ⒶℕⓉⒾⒷⒶℕ 𝐵𝒪𝒯 𝗞𝗜𝗠𝗟𝗘𝗧 𝗔𝗛𝗠𝗘𝗗",
                field_2=902044014,#
                field_3=901000041,
                field_4=238,#
                field_7=2,
                field_8="ⒶℕⓉⒾⒷⒶℕ 𝐵𝒪𝒯 𝗞𝗜𝗠𝗟𝗘𝗧 𝗔𝗛𝗠𝗘𝗗"
            ),
            field_10="en",
            field_13=clan_msg_pb2.clan_msg.Nested2.Nested13(
                link="https://graph.facebook.com/v9.0/111802521083341/picture?width=160&height=160",
                field_2=1,
                field_3=1
            ),
            field_14=clan_msg_pb2.clan_msg.Nested2.Nested14()
        )
    )

    binary_data = root.SerializeToString()
    packet = binary_data.hex()
    encrypted_packet = nmnmmmmn(packet, key, iv)
    header_length = len(encrypted_packet) // 2
    header_length_hex = dec_to_hex(header_length)

    if len(header_length_hex) == 2:
        final_packet = "1215000000" + header_length_hex + nmnmmmmn(packet, key, iv)
    elif len(header_length_hex) == 3:
        final_packet = "121500000" + header_length_hex + nmnmmmmn(packet, key, iv)
    elif len(header_length_hex) == 4:
        final_packet = "12150000" + header_length_hex + nmnmmmmn(packet, key, iv)
    elif len(header_length_hex) == 5:
        final_packet = "1215000" + header_length_hex + nmnmmmmn(packet, key, iv)
    return bytes.fromhex(final_packet)






def generate_name_with_color():
    # قائمة بالأسماء
    names = [
    "Anonymou1", "Anonymou2", "Anonymou3", "Anonymou4", "Anonymou5",
    "Anonymo22", "Anonymo23", "Anonymo24", "Anonymo25"
]
    
    # قائمة بالألوان المذهلة بصيغة HTML
    colors = [
    "[C][b][00FF00]",  # أخضر قوي (يدل على الهكر)
    "[C][b][00FF00]",  # أخضر قوي (يدل على الهكر)
    "[C][b][00FF00]",  # أخضر قوي (يدل على الهكر)
    "[C][b][00FF00]",  # أخضر قوي (يدل على الهكر)
    "[C][b][00FF00]",  # أخضر قوي (يدل على الهكر)
    "[C][b][00FF00]",  # أخضر قوي (يدل على الهكر)
    "[C][b][00FF00]",  # أخضر قوي (يدل على الهكر)
    "[C][b][00FF00]",  # أخضر قوي (يدل على الهكر)
    "[C][b][00FF00]",  # أخضر قوي (يدل على الهكر)
    "[C][b][00FF00]",  # أخضر قوي (يدل على الهكر)
    "[C][b][00FF00]",  # أخضر قوي (يدل على الهكر)
    "[C][b][00FF00]",  # أخضر قوي (يدل على الهكر)
    "[C][b][00FF00]",  # أخضر قوي (يدل على الهكر)
    "[C][b][00FF00]",  # أخضر قوي (يدل على الهكر)
    "[C][b][00FF00]",  # أخضر قوي (يدل على الهكر)
    "[C][b][00FF00]"   # أخضر قوي (يدل على الهكر)
]
    
    # توليد اسم عشوائي مع لون عشوائي
    name = random.choice(names)
    color = random.choice(colors)
    
    # إعادة الاسم مع اللون
    return color + name


def generate_numbers(start, end):

    numbers = [i for i in range(start, end+1)]
    return numbers






# دالة join_team
def join_team(ne, inv, room_id, uid, key, iv):
    threads = []  # لتخزين الـ threads

    for _ in range(100):  # إرسال 100 حزمة
        root = spam_join_pb2.spam_join()
        root.field_1 = 78
        root.field_2.field_1 = int(room_id)

        # استدعاء دالة توليد الاسم مع اللون
        root.field_2.name = f"[C][b][00FF00]{ne}"

        root.field_2.field_3.field_2 = 1
        root.field_2.field_3.field_3 = 1
        root.field_2.field_4 = 0  # تصحيح الرقم
        root.field_2.field_5 = 2280
        root.field_2.field_6 = 208
        root.field_2.field_11 = int(uid)
        root.field_2.field_12 = 1

        # سيريالايز للبيانات
        data = root.SerializeToString()
        packet = data.hex()
        packet_encrypt = nmnmmmmn(packet, key, iv)
        _ = dec_to_hex(int(len(packet_encrypt) // 2))    

        # حساب حجم الحزمة
        if len(_) == 2:
            header = "0e15000000"
        elif len(_) == 3:
            header = "0e1500000"
        elif len(_) == 4:
            header = "0e150000"
        elif len(_) == 5:
            header = "0e15000"   

        # توليد الحزمة النهائية
        final_packet = header + _ + packet_encrypt

        # تشغيل العملية في Thread منفصل
        thread = threading.Thread(target=send_packet, args=(inv, final_packet))
        thread.start()
        threads.append(thread)

    # انتظار اكتمال جميع الحزم المرسلة
    for thread in threads:
        thread.join()
        
def decrypt_api(cipher_text):
    key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
    iv = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plain_text = unpad(cipher.decrypt(bytes.fromhex(cipher_text)), AES.block_size)
    return plain_text.hex()


def encrypt_api(plain_text):
    plain_text = bytes.fromhex(plain_text)
    key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
    iv = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
    cipher = AES.new(key, AES.MODE_CBC, iv)
    cipher_text = cipher.encrypt(pad(plain_text, AES.block_size))
    return cipher_text.hex()

def get_squad_leader(packet):
    json_result = get_available_room(packet)
    parsed_data = json.loads(json_result)
    return parsed_data["5"]["data"]["1"]["data"]


def send_msg_in_room(Msg, room_id, key, iv):
    fields = {
        1: 1,
        2: {
            1: int(room_id),
            2: int(room_id),
            3: 3,
            4: f"{Msg}",
            5: int(datetime.now().timestamp()),
            7: 2,
            9: {
                1: "byte bot",
                2: bunner_(),
                4: 228,
                7: 1,
            },
            10: "ar",
            13: {2: 1, 3: 1},
        },
    }

    # إنشاء حزمة بروتوكول (protobuf)
    packet = create_protobuf_packet(fields)

    # تحويل الحزمة إلى تمثيل سداسي عشري وإضافة قيمة ثابتة "7200"
    packet = packet.hex() + "7200"

    # حساب طول رأس الحزمة بعد التشفير
    header_length = len(encrypt_packet(packet, key, iv)) // 2
    header_length = dec_to_hex(header_length)

    # تحديد تنسيق الحزمة بناءً على طول الرأس
    if len(header_length) == 2:
        final_packet = "1215000000" + header_length + encrypt_packet(packet, key, iv)
        return bytes.fromhex(final_packet)

    elif len(header_length) == 3:
        final_packet = "121500000" + header_length + encrypt_packet(packet, key, iv)
        return bytes.fromhex(final_packet)

    elif len(header_length) == 4:
        final_packet = "12150000" + header_length + encrypt_packet(packet, key, iv)
        return bytes.fromhex(final_packet)

    elif len(header_length) == 5:
        final_packet = "12150000" + header_length + encrypt_packet(packet, key, iv)
        return bytes.fromhex(final_packet)


def join_room_chanel(room_id, key, iv):
    fields = {
        1: 3,
        2: {
            1: int(room_id),
            2: 3,
            3: "ar",
        },
    }
    packet = create_protobuf_packet(fields)
    packet = packet.hex() + "7200"
    header_lenth = len(encrypt_packet(packet, key, iv)) // 2
    header_lenth = dec_to_hex(header_lenth)
    if len(header_lenth) == 2:
        # print(header_lenth)
        # print('len of headr == 2')
        final_packet = "1215000000" + header_lenth + encrypt_packet(packet, key, iv)
        # print(final_packet)
        return bytes.fromhex(final_packet)

    if len(header_lenth) == 3:
        #  print(header_lenth)
        #  print('len of headr == 3')
        final_packet = "121500000" + header_lenth + encrypt_packet(packet, key, iv)
        # print("121500000"+header_lenth)
        return bytes.fromhex(final_packet)
    if len(header_lenth) == 4:
        #  print('len of headr == 4')
        final_packet = "12150000" + header_lenth + encrypt_packet(packet, key, iv)
        return bytes.fromhex(final_packet)
    if len(header_lenth) == 5:
        final_packet = "12150000" + header_lenth + encrypt_packet(packet, key, iv)
        return bytes.fromhex(final_packet)


    
