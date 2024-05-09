import pandas as pd

def find_words_in_sentence(sentence, words_to_check):
    # Convert the sentence to lowercase to ensure case-insensitive matching
    sentence = sentence.lower()
    # Find and return the list of words that are present in the sentence
    found_words = [word for word in words_to_check if word.lower() in sentence]
    return found_words

# Load the Excel file into a DataFrame
df = pd.read_excel('input.xlsx')

# Define the list of words to check for
words_to_check = ["apple", "banana", "cherry"]

# Apply the find_words_in_sentence function to the 'sentence' column
df['Found Words'] = df['sentence'].apply(find_words_in_sentence, words_to_check=words_to_check)

# Create a new column to show whether any words were found
df['Words Found'] = df['Found Words'].apply(lambda x: bool(x))

# Save the modified DataFrame back to an Excel file
df.to_excel('output.xlsx', index=False)

print("Processing complete. Modified file saved.")

