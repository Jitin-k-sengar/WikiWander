import os
import threading
from colorama import Fore
from wikipedia import wikipedia, PageError
from logo import display_logo
import keyboard

# Constants for content types
FULL_CONTENT = 1
SUMMARY = 2

def clear_screen():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_interface():
    """Displays the logo and clears the screen."""
    clear_screen()
    display_logo()

def options():
    """Displays the available options for content types."""
    print(Fore.MAGENTA + '''
    1.  Get Full Content
    2.  Get Summary
    ''')
    print("\n")

def listen_for_escape(stop_event):
    """Listens for the escape key to stop the program."""
    while not stop_event.is_set():
        if keyboard.is_pressed('esc'):
            stop_event.set()
            print("\n" + Fore.RED + "Thank you!  Goodbye!")

def get_valid_input(prompt, valid_range):
    """Gets valid input from the user."""
    while True:
        try:
            choice = int(input(prompt))
            if choice in valid_range:
                return choice
            else:
                print(Fore.RED + "Please choose a valid option!")
        except ValueError:
            print(Fore.RED + "Invalid input. Please enter a number.")

def wiki():
    """Main function to handle the Wikipedia search and content retrieval."""
    stop_event = threading.Event()
    
    # Start the escape key listener in a separate thread
    escape_thread = threading.Thread(target=listen_for_escape, args=(stop_event,))
    escape_thread.daemon = True  # Daemonize thread
    escape_thread.start()

    while not stop_event.is_set():
        try:
            display_interface()
            
            search = input(Fore.YELLOW + "Search: ")
            
            display_interface()
            
            topics = wikipedia.search(search)
            topic_count = len(topics)

            for index, topic in enumerate(topics, start=1):
                print(Fore.MAGENTA + f"{index}.   {topic}")
                
            print("\n")
            
            if topic_count == 0:
                print(Fore.RED + "No topics found.")
                continue
            
            choose = get_valid_input(Fore.YELLOW + "Select Topic: ", range(1, topic_count + 1))

            display_interface()
            options()
            
            selection = get_valid_input(Fore.YELLOW + "Choose Content Type: ", [FULL_CONTENT, SUMMARY])

            display_interface()

            if selection == FULL_CONTENT:
                try:
                    content = wikipedia.page(topics[choose - 1]).content
                    print(Fore.GREEN + f"{content}")
                except PageError:
                    print(Fore.RED + "The requested page does not exist. Please try another topic.")
            elif selection == SUMMARY:
                try:
                    summary = wikipedia.summary(topics[choose - 1])
                    print(Fore.GREEN + f"{summary}")
                except PageError:
                    print(Fore.RED + "The requested summary could not be found. Please try another topic.")

            print("\n")
            input(Fore.RED + "Press Enter to continue...")

        except Exception as e:
            print(Fore.RED + f"An error occurred: {e}")

# Start the Wiki function
wiki()