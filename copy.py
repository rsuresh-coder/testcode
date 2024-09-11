Decompose the 'Content' into clear and simple propositions, ensuring they are interpretable out of context. 1. Split compound sentence into simple sentences. Maintain the original phrasing from the input whenever possible. 2. For any named entity that is accompanied by additional descriptive information, separate this information into its own distinct proposition. 3. Decontextualize the proposition by adding necessary modifier to nouns or entire sentences and replacing pronouns (e.g., 'it', 'he', 'she', 'they', 'this', 'that') with the full name of the entities they refer to. 4. Present the results as a list of strings, formatted in JSON.

Content: Prior to restoration work performed between 1990 and 2001, Leaning Tower of Pisa leaned at an angle of 5.5 degrees, but the tower now leans at about 3.99 degrees. This means the top of the tower is displaced horizontally 3.9 meters (12 ft 10 in) from the center.


<|begin_of_text|><|start_header_id|>system<|end_header_id|>

Decompose the 'Content' into clear and simple propositions, ensuring they are interpretable out of context. 1. Split compound sentence into simple sentences. Maintain the original phrasing from the input whenever possible. 2. For any named entity that is accompanied by additional descriptive information, separate this information into its own distinct proposition. 3. Decontextualize the proposition by adding necessary modifier to nouns or entire sentences and replacing pronouns (e.g., 'it', 'he', 'she', 'they', 'this', 'that') with the full name of the entities they refer to. 4. Present the results as a list of strings, formatted in JSON.

Content: Prior to restoration work performed between 1990 and 2001, Leaning Tower of Pisa leaned at an angle of 5.5 degrees, but the tower now leans at about 3.99 degrees. This means the top of the tower is displaced horizontally 3.9 meters (12 ft 10 in) from the center.

<|eot_id|><|start_header_id|>assistant<|end_header_id|>



import fitz  # PyMuPDF

# Open the PDF
pdf_file = "/content/sample_data/wf_10k.pdf"  # Replace with your file path
doc = fitz.open(pdf_file)

# Initialize an empty variable to store the entire text
pdf_text = ""


# Function to split text into chunks of 400 words or newline characters
def split_text(text, word_limit=200):
    chunks = []
    current_chunk = []
    word_count = 0

    # Split the text by lines
    for line in text.splitlines():
        words = line.split()  # Split line into words
        word_count += len(words)
        current_chunk.append(line)

        # If word count exceeds the limit and line ends, append chunk
        if word_count >= word_limit:
            chunks.append("\n".join(current_chunk))
            current_chunk = []  # Reset for the next chunk
            word_count = 0  # Reset word count

    # Append the last chunk if any
    if current_chunk:
        chunks.append("\n".join(current_chunk))

    return chunks


# Iterate through each page of the PDF
for page_num in range(doc.page_count):
    page = doc.load_page(page_num)  # Load the current page
    pdf_text += page.get_text("text")  # Extract text from the page and add it to the variable

# Close the PDF document after reading
doc.close()

# Split the PDF text into 400-word or newline-separated chunks
text_chunks = split_text(pdf_text)

# Write the chunks to a text file
output_file = "/content/sample_data/wf_10k.txt"  # Output file name
with open(output_file, "w", encoding="utf-8") as f:
    for i, chunk in enumerate(  text_chunks):
        print(f"writing chunk {i}")
        f.write(get_sentences(chunk))
        f.write("\n\n###\n\n")  # Add a blank line between chunks
        if i > 10:
          break

print(f"Text has been written to {output_file}")

# Now pdf_text contains the entire text from the PDF
# print(pdf_text)
