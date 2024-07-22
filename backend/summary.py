from concurrent.futures import ThreadPoolExecutor
from transformers import BartForConditionalGeneration, BartTokenizer
import textwrap
import PyPDF2
from openai import OpenAI
import torch
import re

class Summarizer:
    """
    Class to summarize text from a PDF using BART model and refine using OpenAI.

    Attributes:
        pdf_path (str): Path to the PDF file to be summarized.
        model_name (str): Name of the BART model to use for summarization.
        openai_base_url (str): Base URL for OpenAI API.
        openai_api_key (str): API key for accessing OpenAI API.
        model (BartForConditionalGeneration): BART model instance.
        tokenizer (BartTokenizer): BART tokenizer instance.
        openai_client (OpenAI): OpenAI client instance.
    """

    def __init__(self):
        """
        Initializes the Summarizer with necessary parameters and sets up BART and OpenAI.

        Args:
            pdf_path (str): Path to the PDF file to be summarized.
            model_name (str, optional): Name of the BART model to use. Defaults to "facebook/bart-large-cnn".
            openai_base_url (str, optional): Base URL for OpenAI API. Defaults to "http://localhost:8080/v1".
            openai_api_key (str, optional): API key for accessing OpenAI API. Defaults to "sk-no-key-required".
        """
        self.pdf_path = ""
        self.model_name = "facebook/bart-large-cnn"
        self.openai_base_url = "http://localhost:8080/v1"
        self.openai_api_key = "sk-no-key-required"
        # Initialize BART model and tokenizer on GPU
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = BartForConditionalGeneration.from_pretrained(self.model_name).to(self.device)
        # Initialize BART model and tokenizer
        # self.model = BartForConditionalGeneration.from_pretrained(self.model_name).cuda()
        self.tokenizer = BartTokenizer.from_pretrained(self.model_name)
        
        # Initialize OpenAI client
        self.openai_client = OpenAI(base_url=self.openai_base_url, api_key=self.openai_api_key)
        print("Initialized BART & OpenAI")
    
    def read_pdf(self, pdf_path):
        """
        Reads a PDF file and extracts text from each page.

        Returns:
            str: Extracted text from the PDF.
        """
        self.pdf_path = pdf_path
        with open(self.pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            num_pages = len(pdf_reader.pages)
            text = ""
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()

        sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)

        # Initialize a list to store sentences to keep
        filtered_sentences = []

        # Iterate through the sentences in chunks of 2, skipping alternate chunks
        for i in range(0, len(sentences), 4):
            filtered_sentences.extend(sentences[i:i+3])

        # Join the filtered sentences back into a single string
        filtered_text = ' '.join(filtered_sentences)
        print("Read the PDF")
        return filtered_text
    
    def text_summarizer_batch(self, text, batch_size=4, max_chunk_size=1000):
        """
        Summarizes the given text using the BART model with batch processing.

        Args:
            text (str): Text to be summarized.
            batch_size (int, optional): Number of chunks to process in parallel. Defaults to 4.
            max_chunk_size (int, optional): Maximum size of each chunk. Defaults to 1000.

        Returns:
            str: Summarized text.
        """
        formatted_summary = ""
        chunks = [text[i:i+max_chunk_size] for i in range(0, len(text), max_chunk_size)]
        
        for batch_start in range(0, len(chunks), batch_size):
            batch_texts = chunks[batch_start:batch_start+batch_size]
            inputs = self.tokenizer.batch_encode_plus(["summarize: " + chunk for chunk in batch_texts], return_tensors="pt", max_length=1024, truncation=True, padding=True).to(self.device)
            summary_ids = self.model.generate(inputs['input_ids'], max_length=250, min_length=50, length_penalty=2.0, num_beams=4, early_stopping=True)
            summaries = [self.tokenizer.decode(summary_id, skip_special_tokens=True) for summary_id in summary_ids]
            formatted_summary += "\n".join(textwrap.wrap("\n".join(summaries), width=80))

        return formatted_summary

    def summarize_pdf_parallel(self, pdf_path):
        """
        Summarizes the entire PDF content in parallel using threads, refines using OpenAI, and returns the final summary.

        Returns:
            str: Final summarized text.
        """
        pdf_text = self.read_pdf(pdf_path)
        pdf_text = pdf_text.replace("\t", "").replace("\n", "").split("1 – ")[1:]
        pdf_text = " ".join(pdf_text)
        
        total_length = len(pdf_text)
        present_summary = self.text_summarizer_batch(pdf_text)
        print("First BART Summarization")
        while len(present_summary) > total_length/5:
            present_summary = self.text_summarizer_batch(present_summary, max_chunk_size = 800)
            print("Second BART Summarization")
        
        # Using ThreadPoolExecutor for OpenAI interactions
        step = 9000
        sum_text = ""
        with ThreadPoolExecutor(max_workers=4) as executor:  # Adjust max_workers based on your system's capabilities
            futures = []
            for i in range(0, len(present_summary), step):
                user_text = present_summary[i:i+step]
                futures.append(executor.submit(self.openai_summarize, user_text))
            
            for future in futures:
                sum_text += future.result()
        return sum_text.replace("Here is a summary of the key events:", "").replace("<|eot_id|>", "")

    def openai_summarize(self, user_text):
        """
        Utilizes OpenAI to refine the summary for a chunk of text.

        Args:
            user_text (str): Chunk of text to summarize.

        Returns:
            str: Summarized text.
        """
        completion = self.openai_client.chat.completions.create(
            model="LLaMa_CPP",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that provides concise summaries of text. Focus on summarizing the key events without listing quotes."},
                {"role": "user", "content": f"Please summarize the following text:\n\n{user_text}\n\nSummarize the key events only, to the point, and do not include any direct quotes or specific lines from the text."}
            ]
        )
        return completion.choices[0].message.content.replace("Here are the key events summarized:", "").replace("", "")