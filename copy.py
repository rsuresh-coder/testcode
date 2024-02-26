Customer (in Spanish): Hola, buenos días. Quiero depositar este cheque, por favor.
Banker (in English): Good morning! Let me help you with that. Do you have your account number?
Customer (in Spanish): Sí, aquí lo tengo. ¿Cuánto tiempo tomará para que el cheque se refleje en mi cuenta?
Banker (in English): It usually takes about 2 to 3 business days for the check to clear and the funds to be available in your account.
Customer (in Spanish): Entiendo, gracias. ¿Necesito algún recibo de esta transacción?
Banker (in English): Yes, I will give you a receipt with the transaction details and the expected date for the funds to be available.
Customer (in Spanish): Excelente, eso sería todo entonces. Muchas gracias por tu ayuda.
Banker (in English): You're welcome! If you have any other questions or need further assistance, feel free to ask. Have a great day!


import subprocess

def speak_line(line):
    """Speaks a line of text using the macOS 'say' command."""
    subprocess.call(['say', line])

def main(file_path):
    """Reads a file and speaks each line, waiting for user confirmation."""
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()  # Remove any leading/trailing whitespace
                if line:  # Check if line is not empty
                    line = line[ line.index(':'):  ]
                    speak_line(line)
                    input("Press [ENTER] to continue to the next line... or CTRL+C to exit.")
    except FileNotFoundError:
        print(f"The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    file_path = "/Users/sureshreddy/code/voiceversa/input.txt"
    main(file_path)

