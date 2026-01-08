from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
from protobuf_decoder.protobuf_decoder import Parser
import json
key = b'Yg&tc%DEuh6%Zc^8'  # 16-byte AES key
iv = b'6oyZDr22E3ychjM%'   # 16-byte IV

def parse_results(parsed_results):
    result_dict = {}
    for result in parsed_results:
        if result.wire_type == "varint":
            result_dict[int(result.field)] = result.data
        elif result.wire_type == "string" or result.wire_type == "bytes":
            result_dict[int(result.field)] = result.data
        elif result.wire_type == "length_delimited":
            nested_data = parse_results(result.data.results)
            result_dict[int(result.field)] = nested_data
    return result_dict


def zitado_get_proto(input_text):
    try:
        parsed_results = Parser().parse(input_text)
        parsed_results_objects = parsed_results
        parsed_results_dict = parse_results(parsed_results_objects)
        json_data = json.dumps(parsed_results_dict)
        return json_data
    except Exception as e:
        print(f"error {e}")
        return None
    
def encrypt_packet(plain_text,key,iv):
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
def encode_varint(number):
    if number < 0:
        raise ValueError("Number must be non-negative")
    encoded_bytes = []
    while True:
        byte = number & 0x7F
        number >>= 7
        if number:
            byte |= 0x80
        encoded_bytes.append(byte)
        if not number:
            break
    return bytes(encoded_bytes)

def create_varint_field(field_number, value):
    field_header = (field_number << 3) | 0  
    return encode_varint(field_header) + encode_varint(value)

def create_length_delimited_field(field_number, value):
    field_header = (field_number << 3) | 2
    encoded_value = value.encode() if isinstance(value, str) else value
    return encode_varint(field_header) + encode_varint(len(encoded_value)) + encoded_value

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