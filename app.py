import threading
import json
import time
import logging
import socket
import sys
import os
import base64
import binascii
import requests
import jwt
import psutil
import re

from dotenv import load_dotenv
# load environment variables from .env file
load_dotenv()

from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp
from google.protobuf.json_format import MessageToJson

import jwt_generator_pb2
import MajorLoginRes_pb2

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from protobuf_decoder.protobuf_decoder import Parser
from important_zitado import *
from byte import *

# ================== CONFIG ==================
START_SPAM_DURATION = 18       # start spam kitni der chale
WAIT_AFTER_MATCH_SECONDS = 20  # match khatam + lobby wapas approx time
START_SPAM_DELAY = 0.2         # start packets ke beech delay

PROMO_TEXT = "Tg @lsahilxx | Ig @lsahilxx"

# ================== LOGGING ==================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("start_teamcode_bot.log"),
        logging.StreamHandler(sys.stdout),
    ],
)

threads = []
socket_client = None
clients = None
g_token = None


def restart_program():
    logging.warning("Initiating bot restart...")
    try:
        p = psutil.Process(os.getpid())
        # Deprecation warning aati hai, par abhi ignore kar sakte ho
        for handler in p.open_files() + p.connections():
            try:
                os.close(handler.fd)
            except Exception as e:
                logging.error(f"Failed to close handler {handler.fd}: {e}")
    except Exception as e:
        logging.error(f"Error during pre-restart cleanup: {e}")

    python = sys.executable
    os.execl(python, python, *sys.argv)


def encrypt_packet(plain_text, key, iv):
    if isinstance(key, str):
        key = bytes.fromhex(key)
    if isinstance(iv, str):
        iv = bytes.fromhex(iv)
    plain_text = bytes.fromhex(plain_text)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    cipher_text = cipher.encrypt(pad(plain_text, AES.block_size))
    return cipher_text.hex()


def encrypt_api(plain_text):
    plain_text = bytes.fromhex(plain_text)
    key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
    iv = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
    cipher = AES.new(key, AES.MODE_CBC, iv)
    cipher_text = cipher.encrypt(pad(plain_text, AES.block_size))
    return cipher_text.hex()


def parse_results(parsed_results):
    result_dict = {}
    for result in parsed_results:
        field_data = {"wire_type": result.wire_type}
        if result.wire_type in ("varint", "string", "bytes"):
            field_data["data"] = result.data
        elif result.wire_type == "length_delimited":
            field_data["data"] = parse_results(result.data.results)
        result_dict[result.field] = field_data
    return result_dict


def get_available_room(input_text):
    try:
        parsed_results = Parser().parse(input_text)
        parsed_results_dict = parse_results(parsed_results)
        json_data = json.dumps(parsed_results_dict)
        return json_data
    except Exception as e:
        logging.error(f"error in get_available_room: {e}")
        return None


def dec_to_hex(ask: int) -> str:
    ask_result = hex(ask)
    final_result = str(ask_result)[2:]
    if len(final_result) == 1:
        final_result = "0" + final_result
    return final_result


def extract_jwt_from_hex(hex_str):
    byte_data = binascii.unhexlify(hex_str)
    message = jwt_generator_pb2.Garena_420()
    message.ParseFromString(byte_data)
    json_output = MessageToJson(message)
    token_data = json.loads(json_output)
    return token_data


class FF_CLIENT(threading.Thread):
    def __init__(self, uid, password):
        super().__init__()
        self.id = uid
        self.password = password
        self.key = None
        self.iv = None
        self.auto_start_running = False
        self.auto_start_teamcode = None
        self.stop_auto = False
        self.get_tok()

    # ------------- LOGIN PART -------------
    def parse_my_message(self, serialized_data):
        MajorLogRes = MajorLoginRes_pb2.MajorLoginRes()
        MajorLogRes.ParseFromString(serialized_data)

        timestamp = MajorLogRes.kts
        key = MajorLogRes.ak
        iv = MajorLogRes.aiv
        BASE64_TOKEN = MajorLogRes.token
        timestamp_obj = Timestamp()
        timestamp_obj.FromNanoseconds(timestamp)
        timestamp_seconds = timestamp_obj.seconds
        timestamp_nanos = timestamp_obj.nanos
        combined_timestamp = timestamp_seconds * 1_000_000_000 + timestamp_nanos
        return combined_timestamp, key, iv, BASE64_TOKEN

    def GET_PAYLOAD_BY_DATA(self, JWT_TOKEN, NEW_ACCESS_TOKEN, date):
        token_payload_base64 = JWT_TOKEN.split(".")[1]
        token_payload_base64 += "=" * ((4 - len(token_payload_base64) % 4) % 4)
        decoded_payload = base64.urlsafe_b64decode(token_payload_base64).decode(
            "utf-8"
        )
        decoded_payload = json.loads(decoded_payload)
        NEW_EXTERNAL_ID = decoded_payload["external_id"]
        SIGNATURE_MD5 = decoded_payload["signature_md5"]

        now = datetime.now()
        now = str(now)[: len(str(now)) - 7]

        payload = bytes.fromhex(
            "1a13323032352d30372d33302031313a30323a3531220966726565206669726528013a07312e3131382e31422c416e64726f6964204f5320372e312e32202f204150492d323320284e32473438482f373030323530323234294a0848616e6468656c645207416e64726f69645a045749464960c00c68840772033332307a1f41524d7637205646507633204e454f4e20564d48207c2032343635207c203480019a1b8a010f416472656e6f2028544d292036343092010d4f70656e474c20455320332e319a012b476f6f676c657c31663361643662372d636562342d343934622d383730622d623164616364373230393131a2010c3139372e312e31322e313335aa0102656eb201203939366136323964626364623339363462653662363937386635643831346462ba010134c2010848616e6468656c64ca011073616d73756e6720534d2d473935354eea014066663930633037656239383135616633306134336234613966363031393531366530653463373033623434303932353136643064656661346365663531663261f00101ca0207416e64726f6964d2020457494649ca03203734323862323533646566633136343031386336303461316562626665626466e003daa907e803899b07f003bf0ff803ae088004999b078804daa9079004999b079804daa907c80403d204262f646174612f6170702f636f6d2e6474732e667265656669726574682d312f6c69622f61726de00401ea044832303837663631633139663537663261663465376665666630623234643964397c2f646174612f6170702f636f6d2e6474732e667265656669726574682d312f626173652e61706bf00403f804018a050233329a050a32303139313138363933a80503b205094f70656e474c455332b805ff7fc00504e005dac901ea0507616e64726f6964f2055c4b71734854394748625876574c6668437950416c52526873626d43676542557562555551317375746d525536634e30524f3751453141486e496474385963784d614c575437636d4851322b7374745279377830663935542b6456593d8806019006019a060134a2060134b2061e40001147550d0c074f530b4d5c584d57416657545a065f2a091d6a0d5033"
        )
        payload = payload.replace(b"2025-07-30 11:02:51", str(now).encode())
        payload = payload.replace(
            b"ff90c07eb9815af30a43b4a9f6019516e0e4c703b44092516d0defa4cef51f2a",
            NEW_ACCESS_TOKEN.encode("UTF-8"),
        )
        payload = payload.replace(
            b"996a629dbcdb3964be6b6978f5d814db",
            NEW_EXTERNAL_ID.encode("UTF-8"),
        )
        payload = payload.replace(
            b"7428b253defc164018c604a1ebbfebdf",
            SIGNATURE_MD5.encode("UTF-8"),
        )
        PAYLOAD = payload.hex()
        PAYLOAD = encrypt_api(PAYLOAD)
        PAYLOAD = bytes.fromhex(PAYLOAD)
        whisper_ip, whisper_port, online_ip, online_port = self.GET_LOGIN_DATA(
            JWT_TOKEN, PAYLOAD
        )
        return whisper_ip, whisper_port, online_ip, online_port

    def GET_LOGIN_DATA(self, JWT_TOKEN, PAYLOAD):
        url = "https://client.ind.freefiremobile.com/GetLoginData"
        headers = {
            "Expect": "100-continue",
            "Authorization": f"Bearer {JWT_TOKEN}",
            "X-Unity-Version": "2018.4.11f1",
            "X-GA": "v1 1",
            "ReleaseVersion": "Ob51",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; G011A Build/PI)",
            "Host": "clientbp.common.ggbluefox.com",
            "Connection": "close",
            "Accept-Encoding": "gzip, deflate, br",
        }

        max_retries = 3
        attempt = 0

        while attempt < max_retries:
            try:
                response = requests.post(
                    url, headers=headers, data=PAYLOAD, verify=False
                )
                response.raise_for_status()
                x = response.content.hex()
                json_result = get_available_room(x)
                if not json_result:
                    raise ValueError("Empty json_result from get_available_room()")
                parsed_data = json.loads(json_result)

                whisper_address = parsed_data["32"]["data"]
                online_address = parsed_data["14"]["data"]

                # ✅ original logic jaisa hona chahiye
                online_ip = online_address[: len(online_address) - 6]
                whisper_ip = whisper_address[: len(whisper_address) - 6]

                online_port = int(online_address[len(online_address) - 5 :])
                whisper_port = int(whisper_address[len(whisper_address) - 5 :])

                return whisper_ip, whisper_port, online_ip, online_port


            except Exception as e:
                logging.error(
                    f"Request failed in GET_LOGIN_DATA: {e}. Attempt {attempt + 1} of {max_retries}. Retrying..."
                )
                attempt += 1
                time.sleep(2)

        logging.critical("Failed to get login data after multiple attempts. Restarting.")
        restart_program()
        return None, None, None, None

    def guest_token(self, uid, password):
        url = "https://100067.connect.garena.com/oauth/guest/token/grant"
        headers = {
            "Host": "100067.connect.garena.com",
            "User-Agent": "GarenaMSDK/4.0.19P4(G011A ;Android 10;en;EN;)",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "close",
        }
        data = {
            "uid": f"{uid}",
            "password": f"{password}",
            "response_type": "token",
            "client_type": "2",
            "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
            "client_id": "100067",
        }
        response = requests.post(url, headers=headers, data=data)
        data = response.json()
        NEW_ACCESS_TOKEN = data["access_token"]
        NEW_OPEN_ID = data["open_id"]
        OLD_ACCESS_TOKEN = (
            "ff90c07eb9815af30a43b4a9f6019516e0e4c703b44092516d0defa4cef51f2a"
        )
        OLD_OPEN_ID = "996a629dbcdb3964be6b6978f5d814db"
        time.sleep(0.2)
        data = self.TOKEN_MAKER(
            OLD_ACCESS_TOKEN, NEW_ACCESS_TOKEN, OLD_OPEN_ID, NEW_OPEN_ID, uid
        )
        return data

    def TOKEN_MAKER(
        self, OLD_ACCESS_TOKEN, NEW_ACCESS_TOKEN, OLD_OPEN_ID, NEW_OPEN_ID, id
    ):
        headers = {
            "X-Unity-Version": "2018.4.11f1",
            "ReleaseVersion": "Ob51",
            "Content-Type": "application/x-www-form-urlencoded",
            "X-GA": "v1 1",
            "Content-Length": "928",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; ASUS_Z01QD Build/QKQ1.190825.002)",
            "Host": "loginbp.ggblueshark.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
        }
        data = bytes.fromhex(
            "1a13323032352d30372d33302031313a30323a3531220966726565206669726528013a07312e3131382e31422c416e64726f6964204f5320372e312e32202f204150492d323320284e32473438482f373030323530323234294a0848616e6468656c645207416e64726f69645a045749464960c00c68840772033332307a1f41524d7637205646507633204e454f4e20564d48207c2032343635207c203480019a1b8a010f416472656e6f2028544d292036343092010d4f70656e474c20455320332e319a012b476f6f676c657c31663361643662372d636562342d343934622d383730622d623164616364373230393131a2010c3139372e312e31322e313335aa0102656eb201203939366136323964626364623339363462653662363937386635643831346462ba010134c2010848616e6468656c64ca011073616d73756e6720534d2d473935354eea014066663930633037656239383135616633306134336234613966363031393531366530653463373033623434303932353136643064656661346365663531663261f00101ca0207416e64726f6964d2020457494649ca03203734323862323533646566633136343031386336303461316562626665626466e003daa907e803899b07f003bf0ff803ae088004999b078804daa9079004999b079804daa907c80403d204262f646174612f6170702f636f6d2e6474732e667265656669726574682d312f6c69622f61726de00401ea044832303837663631633139663537663261663465376665666630623234643964397c2f646174612f6170702f636f6d2e6474732e667265656669726574682d312f626173652e61706bf00403f804018a050233329a050a32303139313138363933a80503b205094f70656e474c455332b805ff7fc00504e005dac901ea0507616e64726f6964f2055c4b71734854394748625876574c6668437950416c52526873626d43676542557562555551317375746d525536634e30524f3751453141486e496474385963784d614c575437636d4851322b7374745279377830663935542b6456593d8806019006019a060134a2060134b2061e40001147550d0c074f530b4d5c584d57416657545a065f2a091d6a0d5033"
        )
        data = data.replace(OLD_OPEN_ID.encode(), NEW_OPEN_ID.encode())
        data = data.replace(OLD_ACCESS_TOKEN.encode(), NEW_ACCESS_TOKEN.encode())
        hex_data = data.hex()
        d = encrypt_api(hex_data)
        Final_Payload = bytes.fromhex(d)
        URL = "https://loginbp.ggblueshark.com/MajorLogin"

        RESPONSE = requests.post(URL, headers=headers, data=Final_Payload, verify=False)

        combined_timestamp, key, iv, BASE64_TOKEN = self.parse_my_message(
            RESPONSE.content
        )
        if RESPONSE.status_code == 200:
            if len(RESPONSE.text) < 10:
                return False
            whisper_ip, whisper_port, online_ip, online_port = self.GET_PAYLOAD_BY_DATA(
                BASE64_TOKEN, NEW_ACCESS_TOKEN, 1
            )
            self.key = key
            self.iv = iv
            return (
                BASE64_TOKEN,
                key,
                iv,
                combined_timestamp,
                whisper_ip,
                whisper_port,
                online_ip,
                online_port,
            )
        else:
            return False

    def nmnmmmmn(self, data_hex):
        key, iv = self.key, self.iv
        try:
            key = key if isinstance(key, bytes) else bytes.fromhex(key)
            iv = iv if isinstance(iv, bytes) else bytes.fromhex(iv)
            data = bytes.fromhex(data_hex)
            cipher = AES.new(key, AES.MODE_CBC, iv)
            cipher_text = cipher.encrypt(pad(data, AES.block_size))
            return cipher_text.hex()
        except Exception as e:
            logging.error(f"Error in nmnmmmmn: {e}")

    # ------------- BASIC PACKETS -------------
    def start_autooo(self):
        fields = {
            1: 9,
            2: {
                1: 12480598706,
            },
        }
        packet = create_protobuf_packet(fields).hex()
        header_length = len(encrypt_packet(packet, self.key, self.iv)) // 2
        header_length_final = dec_to_hex(header_length)
        if len(header_length_final) == 2:
            final_packet = "0515000000" + header_length_final + self.nmnmmmmn(packet)
        elif len(header_length_final) == 3:
            final_packet = "051500000" + header_length_final + self.nmnmmmmn(packet)
        elif len(header_length_final) == 4:
            final_packet = "05150000" + header_length_final + self.nmnmmmmn(packet)
        elif len(header_length_final) == 5:
            final_packet = "0515000" + header_length_final + self.nmnmmmmn(packet)
        return bytes.fromhex(final_packet)

    def leave_s(self):
        fields = {
            1: 7,
            2: {
                1: 12480598706,
            },
        }
        packet = create_protobuf_packet(fields).hex()
        header_length = len(encrypt_packet(packet, self.key, self.iv)) // 2
        header_length_final = dec_to_hex(header_length)
        if len(header_length_final) == 2:
            final_packet = "0515000000" + header_length_final + self.nmnmmmmn(packet)
        elif len(header_length_final) == 3:
            final_packet = "051500000" + header_length_final + self.nmnmmmmn(packet)
        elif len(header_length_final) == 4:
            final_packet = "05150000" + header_length_final + self.nmnmmmmn(packet)
        elif len(header_length_final) == 5:
            final_packet = "0515000" + header_length_final + self.nmnmmmmn(packet)
        return bytes.fromhex(final_packet)

    def GenResponsMsg(self, Msg, Enc_Id):
        fields = {
            1: 1,
            2: {
                1: 12947146032,
                2: Enc_Id,
                3: 2,
                4: str(Msg),
                5: int(datetime.now().timestamp()),
                7: 2,
                9: {
                    1: "SHAZZ",
                    2: 902050001,
                    3: 901049014,
                    4: 330,
                    5: 801040108,
                    8: "Friend",
                    10: 1,
                    11: 1,
                },
                10: "IND",
            },
        }
        packet = create_protobuf_packet(fields).hex()
        header_length = len(encrypt_packet(packet, self.key, self.iv)) // 2
        header_length_final = dec_to_hex(header_length)
        if len(header_length_final) == 2:
            final_packet = "1215000000" + header_length_final + self.nmnmmmmn(packet)
        elif len(header_length_final) == 3:
            final_packet = "121500000" + header_length_final + self.nmnmmmmn(packet)
        elif len(header_length_final) == 4:
            final_packet = "12150000" + header_length_final + self.nmnmmmmn(packet)
        elif len(header_length_final) == 5:
            final_packet = "1215000" + header_length_final + self.nmnmmmmn(packet)
        return bytes.fromhex(final_packet)

    # ------------- AUTO LOOP -------------
    def auto_start_loop(self, team_code, uid):
        global socket_client, clients
        logging.info(f"[AUTO] Auto start loop started for team {team_code}")

        while not self.stop_auto:
            try:
                # join
                join_teamcode(socket_client, team_code, self.key, self.iv)
                time.sleep(2)

                if clients:
                    msg = f"[C][B][FFA500]Team {team_code} joined. Starting match..."
                    msg += f"\n{PROMO_TEXT}"
                    clients.send(self.GenResponsMsg(msg, uid))

                # start spam
                start_packet = self.start_autooo()
                end_time = time.time() + START_SPAM_DURATION
                while time.time() < end_time and not self.stop_auto:
                    socket_client.send(start_packet)
                    time.sleep(START_SPAM_DELAY)

                if self.stop_auto:
                    break

                # wait
                if clients:
                    msg = (
                        f"[C][B][00FF00]Match started. Bot lobby me wait karega "
                        f"{WAIT_AFTER_MATCH_SECONDS} sec..."
                    )
                    msg += f"\n{PROMO_TEXT}"
                    clients.send(self.GenResponsMsg(msg, uid))

                waited = 0
                while waited < WAIT_AFTER_MATCH_SECONDS and not self.stop_auto:
                    time.sleep(1)
                    waited += 1

                if self.stop_auto:
                    break

                # leave
                leave_packet = self.leave_s()
                socket_client.send(leave_packet)
                logging.info(f"[AUTO] Left team {team_code} to rejoin again.")
                time.sleep(2)

                if clients:
                    msg = (
                        f"[C][B][FF0000]Leaving team {team_code} and rejoining to force start again..."
                    )
                    msg += f"\n{PROMO_TEXT}"
                    clients.send(self.GenResponsMsg(msg, uid))


            except Exception as e:
                logging.error(f"[AUTO] Error in auto_start_loop: {e}", exc_info=True)
                # yahan network/socket ka issue hoga to restart sahi rahega
                self.stop_auto = True
                self.auto_start_running = False
                restart_program()
                break


        logging.info(f"[AUTO] Auto start loop stopped for team {team_code}")

    # ------------- SOCKETS -------------



    def sockf1(self, tok, online_ip, online_port):
        global socket_client
        socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        online_port = int(online_port)

        try:
            socket_client.settimeout(10)
            socket_client.connect((online_ip, online_port))
        except Exception as e:
            logging.error(
                f"[ONLINE] Failed to connect to {online_ip}:{online_port}: {e}. Restarting."
            )
            restart_program()
            return

        socket_client.settimeout(None)
        socket_client.send(bytes.fromhex(tok))
        logging.info(f"[ONLINE] Connected to {online_ip}:{online_port}")

        while True:
            try:
                data2 = socket_client.recv(4096)
                if data2 == b"":
                    logging.error("Online socket closed by remote host. Restarting.")
                    restart_program()
                    break
            except Exception as e:
                logging.critical(f"Unhandled error in sockf1 loop: {e}. Restarting.")
                restart_program()
                break


    def connect(self, tok, whisper_ip, whisper_port, online_ip, online_port):
        global clients
        global socket_client

        clients = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        whisper_port = int(whisper_port)
        clients.connect((whisper_ip, whisper_port))
        clients.send(bytes.fromhex(tok))
        logging.info(f"[WHISPER] Connected to {whisper_ip}:{whisper_port}")

        thread = threading.Thread(
            target=self.sockf1, args=(tok, online_ip, online_port)
        )
        threads.append(thread)
        thread.start()

        while True:
            try:
                data = clients.recv(9999)
                if data == b"":
                    logging.error("Whisper socket closed by remote host. Restarting.")
                    restart_program()
                    break

                # ------- /lw -------
                if b"/lw" in data:
                    try:
                        json_result = get_available_room(data.hex()[10:])
                        if not json_result:
                            logging.warning("get_available_room returned None for /lw")
                            continue

                        parsed_data = json.loads(json_result)
                        uid = (
                            parsed_data.get("5", {})
                            .get("data", {})
                            .get("1", {})
                            .get("data", None)
                        )
                        if uid is None:
                            logging.warning("UID not found in parsed_data for /lw")
                            continue

                        split_data = re.split(rb"/lw", data, maxsplit=1)
                        if len(split_data) < 2:
                            msg = "[C][B][FF0000]Please provide a team code after /lw."
                            msg += f"\n{PROMO_TEXT}"
                            clients.send(self.GenResponsMsg(msg, uid))
                            continue

                        # text after /lw, before '(' and newline
                        cmd_text = (
                            split_data[1]
                            .split(b"(")[0]
                            .decode(errors="ignore")
                            .strip()
                        )

                        # split by whitespace
                        command_parts = cmd_text.split()
                        if not command_parts:
                            msg = "[C][B][FF0000]Please provide a team code."
                            msg += f"\n{PROMO_TEXT}"
                            clients.send(self.GenResponsMsg(msg, uid))
                            continue

                        team_code = command_parts[0]

                        # numeric validation
                        if not team_code.isdigit():
                            msg = (
                                "[C][B][FF0000]Invalid team code! "
                                "Please use like /lw123456 (only numbers)."
                            )
                            msg += f"\n{PROMO_TEXT}"
                            clients.send(self.GenResponsMsg(msg, uid))
                            continue

                        if self.auto_start_running:
                            msg = (
                                f"[C][B][00FFFF]Auto start already running for team "
                                f"{self.auto_start_teamcode}. Use /stop to disable."
                            )
                            msg += f"\n{PROMO_TEXT}"
                            clients.send(self.GenResponsMsg(msg, uid))
                            continue

                        self.auto_start_running = True
                        self.auto_start_teamcode = team_code
                        self.stop_auto = False

                        msg = (
                            f"[C][B][FFA500]Auto start enabled for team {team_code}. "
                            f"Bot join → start → wait → leave → rejoin 24x7."
                        )
                        msg += f"\n{PROMO_TEXT}"
                        clients.send(self.GenResponsMsg(msg, uid))

                        t = threading.Thread(
                            target=self.auto_start_loop,
                            args=(team_code, uid),
                            daemon=True,
                        )
                        t.start()

                    except Exception as e:
                        logging.error(f"An error occurred in /lw command: {e}", exc_info=True)
                        # yahan bot restart nahi karega, sirf error log karega
                        try:
                            json_result = get_available_room(data.hex()[10:])
                            if json_result:
                                parsed_data = json.loads(json_result)
                                uid = (
                                    parsed_data.get("5", {})
                                    .get("data", {})
                                    .get("1", {})
                                    .get("data", None)
                                )
                                if uid:
                                    msg = (
                                        "[C][B][FF0000]Something went wrong in /lw. "
                                        "Please use format: /lw123456 (numbers only)."
                                    )
                                    msg += f"\n{PROMO_TEXT}"
                                    clients.send(self.GenResponsMsg(msg, uid))
                        except Exception:
                            pass
                        continue

                # ------- /stop -------
                if b"/stop" in data:
                    try:
                        json_result = get_available_room(data.hex()[10:])
                        if not json_result:
                            logging.warning("get_available_room returned None for /stop")
                            continue

                        parsed_data = json.loads(json_result)
                        uid = (
                            parsed_data.get("5", {})
                            .get("data", {})
                            .get("1", {})
                            .get("data", None)
                        )
                        if uid is None:
                            logging.warning("UID not found in parsed_data for /stop")
                            continue

                        if not self.auto_start_running:
                            msg = "[C][B][FF0000]Auto start already stopped."
                            msg += f"\n{PROMO_TEXT}"
                            clients.send(self.GenResponsMsg(msg, uid))
                            continue

                        self.stop_auto = True
                        self.auto_start_running = False

                        msg = (
                            f"[C][B][00FF00]Auto start stopped for team {self.auto_start_teamcode}."
                        )
                        msg += f"\n{PROMO_TEXT}"
                        clients.send(self.GenResponsMsg(msg, uid))
                        self.auto_start_teamcode = None

                    except Exception as e:
                        logging.error(f"An error occurred in /stop command: {e}", exc_info=True)
                        # yahan bhi restart nahi
                        continue

                # ------- /help -------
                if b"/help" in data:
                    try:
                        json_result = get_available_room(data.hex()[10:])
                        if not json_result:
                            logging.warning("get_available_room returned None for /help")
                            continue

                        parsed_data = json.loads(json_result)
                        uid = (
                            parsed_data.get("5", {})
                            .get("data", {})
                            .get("1", {})
                            .get("data", None)
                        )
                        if uid is None:
                            logging.warning("UID not found in parsed_data for /help")
                            continue

                        msg = (
                            "[C][B][00FFFF]Choose Lone Wolf map and select 1v1 mode "
                            "then use command /lw{teamcode}\n"
                            "Example: /lw123456"
                        )
                        msg += f"\n{PROMO_TEXT}"

                        clients.send(self.GenResponsMsg(msg, uid))

                    except Exception as e:
                        logging.error(f"An error occurred in /help command: {e}", exc_info=True)
                        # no restart
                        continue

            except Exception as e:
                logging.critical(
                    f"A critical unhandled error occurred in connect loop: {e}. Restarting."
                )
                restart_program()

    def get_tok(self):
        global g_token
        token_data = self.guest_token(self.id, self.password)
        if not token_data:
            logging.critical("Failed to get token data from guest_token. Restarting.")
            restart_program()

        (
            token,
            key,
            iv,
            Timestamp,
            whisper_ip,
            whisper_port,
            online_ip,
            online_port,
        ) = token_data
        g_token = token

        try:
            decoded = jwt.decode(token, options={"verify_signature": False})
            account_id = decoded.get("account_id")
            encoded_acc = hex(account_id)[2:]
            hex_value = dec_to_hex(Timestamp)
            time_hex = hex_value
            BASE64_TOKEN_ = token.encode().hex()
            logging.info(f"Token decoded. Account ID: {account_id}")
        except Exception as e:
            logging.error(f"Error processing token: {e}. Restarting.")
            restart_program()

        try:
            head_len = len(encrypt_packet(BASE64_TOKEN_, key, iv)) // 2
            head_len_hex = hex(head_len)[2:]

            length = len(encoded_acc)
            zeros = "00000000"
            if length == 9:
                zeros = "0000000"
            elif length == 8:
                zeros = "00000000"
            elif length == 10:
                zeros = "000000"
            elif length == 7:
                zeros = "000000000"
            else:
                logging.warning("Unexpected length encountered")

            head = f"0115{zeros}{encoded_acc}{time_hex}00000{head_len_hex}"
            final_token = head + encrypt_packet(BASE64_TOKEN_, key, iv)
            logging.info("Final token constructed successfully.")
        except Exception as e:
            logging.error(f"Error constructing final token: {e}. Restarting.")
            restart_program()

        self.key = key
        self.iv = iv
        self.connect(final_token, whisper_ip, whisper_port, online_ip, online_port)


# ================== MAIN ==================
if __name__ == "__main__":
    # with open("bot.txt", "r") as file:
    #     data = json.load(file)
    uid = os.getenv("BOT_UID")
    pwd = os.getenv("BOT_PASSWORD")

    if not uid or not pwd:
        logging.critical("BOT_UID or BOT_PASSWORD not set in .env!")
        sys.exit(1)

    # ids_passwords = list(data.items())
    # num_clients = len(ids_passwords)
    num_threads = 1  # sirf 1 client

    while True:
        try:
            logging.info("Main execution block started (/lw, /stop, /help bot).")

            for i in range(num_threads):
                # uid, pwd = ids_passwords[i % num_clients]
                logging.info(f"Starting client for ID: {uid}")
                FF_CLIENT(uid, pwd)
                time.sleep(3)

            logging.info(
                f"All {len(threads)} online threads initiated. Main thread will now wait."
            )
            for thread in threads:
                thread.join()

        except KeyboardInterrupt:
            logging.info("Shutdown signal received. Exiting.")
            break
        except Exception as e:
            logging.critical(f"A critical error occurred in the main block: {e}")
            logging.info("Restarting the entire application in 5 seconds...")
            time.sleep(5)
            restart_program()
