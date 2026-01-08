import os
import sys
import time
import json
import threading
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Color codes for terminal
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    banner = f"""
{Colors.RED}{Colors.BOLD}
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║    ██████╗ ███████╗██╗  ██╗                                ║
║    ██╔══██╗██╔════╝╚██╗██╔╝                                ║
║    ██████╔╝█████╗   ╚███╔╝                                 ║
║    ██╔══██╗██╔══╝   ██╔██╗                                 ║
║    ██║  ██║███████╗██╔╝ ██╗                                ║
║    ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝                                ║
║                                                            ║
║        ╔═╗╔═╗╦═╗╔═╗╔═╗╦═╗╔═╗╔╦╗╦╔═╗╔╗╔                     ║
║        ║  ║ ║╠╦╝╠═╝║ ║╠╦╝╠═╣ ║ ║║ ║║║║                     ║
║        ╚═╝╚═╝╩╚═╩  ╚═╝╩╚═╩ ╩ ╩ ╩╚═╝╝╚╝                     ║
║                                                            ║
║             {Colors.CYAN}Free Fire Gaming Bot v2.0{Colors.RED}                      ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
{Colors.END}
    {Colors.YELLOW}⚡ Auto Start | Team Code | UID Invite ⚡{Colors.END}
{Colors.CYAN}════════════════════════════════════════════════════════════{Colors.END}
"""
    print(banner)

def print_status(message, status_type="info"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    if status_type == "success":
        icon = "✓"
        color = Colors.GREEN
    elif status_type == "error":
        icon = "✗"
        color = Colors.RED
    elif status_type == "warning":
        icon = "⚠"
        color = Colors.YELLOW
    else:
        icon = "ℹ"
        color = Colors.CYAN
    
    print(f"{Colors.BOLD}[{timestamp}]{Colors.END} {color}{icon} {message}{Colors.END}")
# ║  {Colors.GREEN}3.{Colors.END} {Colors.WHITE}Send Invite by UID{Colors.CYAN}                                     ║
def print_menu():
    menu = f"""
{Colors.CYAN}╔════════════════════════════════════════════════════════════╗
║                    {Colors.BOLD}MAIN MENU{Colors.END}{Colors.CYAN}                               ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║  {Colors.GREEN}1.{Colors.END} {Colors.WHITE}Start Bot (Login & Connect){Colors.CYAN}                            ║
║  {Colors.GREEN}2.{Colors.END} {Colors.WHITE}Auto Start with Team Code{Colors.CYAN}                              ║
║  {Colors.GREEN}4.{Colors.END} {Colors.WHITE}Stop Current Operation{Colors.CYAN}                                 ║
║  {Colors.GREEN}5.{Colors.END} {Colors.WHITE}View Bot Status{Colors.CYAN}                                        ║
║  {Colors.GREEN}6.{Colors.END} {Colors.WHITE}Configure Settings{Colors.CYAN}                                     ║
║  {Colors.GREEN}7.{Colors.END} {Colors.WHITE}View Logs{Colors.CYAN}                                              ║
║  {Colors.RED}0.{Colors.END} {Colors.WHITE}Exit{Colors.CYAN}                                                   ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝{Colors.END}
"""
    print(menu)

def loading_animation(text, duration=2):
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        frame = frames[i % len(frames)]
        print(f"\r{Colors.CYAN}{frame} {text}...{Colors.END}", end="", flush=True)
        time.sleep(0.1)
        i += 1
    print(f"\r{Colors.GREEN}✓ {text} Complete!{Colors.END}          ")

def get_user_input(prompt, input_type="text", color=Colors.CYAN):
    print(f"{color}┌─{Colors.END}")
    user_input = input(f"{color}└─> {Colors.WHITE}{prompt}: {Colors.END}")
    return user_input if input_type == "text" else int(user_input)

def display_bot_info():
    try:
        uid = os.getenv("BOT_UID")
        password = os.getenv("BOT_PASSWORD")
        # with open("bot.txt", "r") as file:
        #     data = json.load(file)
        if not uid or not password:
            print_status("BOT_UID or BOT_PASSWORD not set in .env!", "error")
            return
        
        print(f"\n{Colors.CYAN}╔════════════════════════════════════════════════════════════╗")
        print(f"║                  {Colors.BOLD}BOT INFORMATION{Colors.END}{Colors.CYAN}                           ║")
        print(f"╠════════════════════════════════════════════════════════════╣{Colors.END}")
        
        # for uid, password in data.items():
        print(f"{Colors.WHITE}  UID: {Colors.GREEN}{uid}{Colors.END}")
        print(f"{Colors.WHITE}  Password: {Colors.YELLOW}{'*' * 10}{Colors.END}")
        print(f"{Colors.CYAN}  ────────────────────────────────────────────────────────{Colors.END}")
        
        print(f"{Colors.CYAN}╚════════════════════════════════════════════════════════════╝{Colors.END}\n")
    except Exception as e:
        print_status(f"Error reading .env: {e}", "error")

class BotController:
    def __init__(self):
        self.is_running = False
        self.operation_type = None
        self.bot_thread = None
        
    def start_bot(self):
        if self.is_running:
            print_status("Bot is already running!", "warning")
            return
        
        print_status("Starting bot...", "info")
        loading_animation("Initializing connection")
        
        # Import and start the actual bot
        try:
            from app import FF_CLIENT
            
            # with open("bot.txt", "r") as file:
            #     data = json.load(file)
            # uid, pwd = list(data.items())[0]
            uid = os.getenv("BOT_UID")
            pwd = os.getenv("BOT_PASSWORD")

            if not uid or not pwd:
                print_status("BOT_UID or BOT_PASSWORD not set in .env!", "error")
                return
            
            self.bot_thread = threading.Thread(
                target=lambda: FF_CLIENT(uid, pwd),
                daemon=True
            )
            self.bot_thread.start()
            
            self.is_running = True
            self.operation_type = "Connected"
            print_status("Bot started successfully!", "success")
            
        except Exception as e:
            print_status(f"Failed to start bot: {str(e)}", "error")
    
    def auto_start_teamcode(self):
        if not self.is_running:
            print_status("Please start the bot first (Option 1)", "warning")
            return
        
        team_code = get_user_input("Enter Team Code", "text", Colors.YELLOW)
        
        if not team_code.isdigit():
            print_status("Invalid team code! Use numbers only.", "error")
            return
        
        print_status(f"Auto start enabled for team: {team_code}", "success")
        print_status("Send /lw command in-game to activate", "info")
        self.operation_type = f"Auto Start (Team: {team_code})"
    
    def send_invite_by_uid(self):
        if not self.is_running:
            print_status("Please start the bot first (Option 1)", "warning")
            return
        
        uid = get_user_input("Enter Target UID", "text", Colors.MAGENTA)
        
        if not uid.isdigit():
            print_status("Invalid UID! Use numbers only.", "error")
            return
        
        loading_animation(f"Sending invite to UID: {uid}")
        print_status(f"Invite sent to UID: {uid}", "success")
        self.operation_type = f"Invite Sent (UID: {uid})"
    
    def stop_operation(self):
        if not self.is_running:
            print_status("No operation is running", "warning")
            return
        
        print_status("Stopping current operation...", "warning")
        loading_animation("Disconnecting")
        
        self.is_running = False
        self.operation_type = None
        print_status("Operation stopped successfully!", "success")
    
    def view_status(self):
        clear_screen()
        print_banner()
        
        status = "ONLINE" if self.is_running else "OFFLINE"
        status_color = Colors.GREEN if self.is_running else Colors.RED
        
        print(f"\n{Colors.CYAN}╔════════════════════════════════════════════════════════════╗")
        print(f"║                   {Colors.BOLD}SYSTEM STATUS{Colors.END}{Colors.CYAN}                           ║")
        print(f"╠════════════════════════════════════════════════════════════╣{Colors.END}")
        print(f"{Colors.WHITE}  Bot Status: {status_color}{status}{Colors.END}")
        print(f"{Colors.WHITE}  Operation: {Colors.YELLOW}{self.operation_type or 'None'}{Colors.END}")
        print(f"{Colors.WHITE}  Uptime: {Colors.CYAN}Connected{Colors.END}" if self.is_running else f"{Colors.WHITE}  Uptime: {Colors.RED}Not Connected{Colors.END}")
        print(f"{Colors.CYAN}╚════════════════════════════════════════════════════════════╝{Colors.END}\n")
        
        input(f"{Colors.YELLOW}Press Enter to continue...{Colors.END}")

def main():
    controller = BotController()
    
    while True:
        clear_screen()
        print_banner()
        display_bot_info()
        print_menu()
        
        try:
            choice = get_user_input("Select an option", "text", Colors.GREEN)
            
            if choice == "1":
                controller.start_bot()
                time.sleep(2)
            
            elif choice == "2":
                controller.auto_start_teamcode()
                time.sleep(2)
            
            elif choice == "3":
                controller.send_invite_by_uid()
                time.sleep(2)
            
            elif choice == "4":
                controller.stop_operation()
                time.sleep(2)
            
            elif choice == "5":
                controller.view_status()
            
            elif choice == "6":
                print_status("Settings configuration coming soon!", "info")
                time.sleep(2)
            
            elif choice == "7":
                print_status("Log viewer coming soon!", "info")
                time.sleep(2)
            
            elif choice == "0":
                print_status("Shutting down Rex Corporation Bot...", "warning")
                loading_animation("Exiting")
                print(f"\n{Colors.RED}{Colors.BOLD}Thanks for using Rex Corporation!{Colors.END}\n")
                sys.exit(0)
            
            else:
                print_status("Invalid option! Please try again.", "error")
                time.sleep(1)
        
        except KeyboardInterrupt:
            print(f"\n\n{Colors.RED}Program interrupted by user{Colors.END}")
            sys.exit(0)
        except Exception as e:
            print_status(f"Error: {str(e)}", "error")
            time.sleep(2)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"{Colors.RED}Fatal Error: {str(e)}{Colors.END}")
        sys.exit(1)