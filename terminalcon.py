import time
import sys
from colorama import Fore, Style
import atexit
from groq import Groq
from rich.markdown import Markdown
from rich.console import Console
import os

GROQ_KEY = "" # Your Groq API key here
console = Console()
client = Groq(api_key=GROQ_KEY)

messages_memory = []

def groq_completion(messages):
    reasoning = ""
    response = ""

    completion_args = {
        "model": "compound-beta-mini",
        "messages": messages,
        "temperature": 0.7,
        "max_completion_tokens": 1024,
        "stream": True,
    }

    completion = client.chat.completions.create(**completion_args)

    for chunk in completion:
        delta = chunk.choices[0].delta
        if delta.content:
            response += delta.content
        if delta.reasoning:
            reasoning += delta.reasoning

    return response, reasoning

def reset_terminal():
    # Reset color and show the cursor when the program exits
    print(Style.RESET_ALL)
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()

# Register the reset function to be called on exit
atexit.register(reset_terminal)

def main():
    while True:
        try:
            # Show the cursor again
            sys.stdout.write("\033[?25h")
            sys.stdout.flush()

            # Display the prompt in yellow color on the same line
            print(Fore.YELLOW + ">> ", end='', flush=True)

            # Get user input (same line)
            prompt = input()

            # Hide the cursor
            sys.stdout.write("\033[?25l")
            sys.stdout.flush()

            messages = [
                {"role": "system", "content": "You are Qubicon, a silly assistant devloped by Franko"},
                *messages_memory,
                {"role": "user", "content": prompt}
            ]

            response, reasoning = groq_completion(messages)

            messages_memory.append({"role": "user", "content": prompt})
            messages_memory.append({"role": "assistant", "content": response})

            if reasoning:
                # Display the reasoning in blue color on the same line
                print(Fore.BLUE + f"[Reasoning] {reasoning}")
            if response:
                # Display the response in green color on the same line
                print(Fore.GREEN + "[Response]")
                console.print(Markdown(response))

            time.sleep(1)

        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            reset_terminal()
            print("Program terminated.")
            break

        except Exception as e:
            reset_terminal()
            print(Fore.RED + f"An error occurred: {e}")
            break

if __name__ == "__main__":
    main()
