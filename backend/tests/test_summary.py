import unittest
from unittest.mock import patch, MagicMock
from ../summary import Summarizer

class SummarizerTests(unittest.TestCase):
    def setUp(self):
        self.summarizer = Summarizer()

    @patch('summary.PyPDF2.PdfReader')
    def test_read_pdf(self, MockPdfReader):
        # Mock the PDF reader to return specific text
        mock_pdf = MagicMock()
        mock_pdf.pages = [MagicMock(), MagicMock()]
        mock_pdf.pages[0].extract_text.return_value = "Page 1 text."
        mock_pdf.pages[1].extract_text.return_value = "Page 2 text."
        MockPdfReader.return_value = mock_pdf

        result = self.summarizer.read_pdf('fake_path.pdf')
        self.assertEqual(result, "Page 1 text. Page 2 text.")
    
    @patch('summary.BartForConditionalGeneration.generate')
    @patch('summary.BartTokenizer.batch_encode_plus')
    def test_text_summarizer_batch(self, mock_encode, mock_generate):
        # Mock the tokenizer and model generate function
        mock_encode.return_value = {'input_ids': [1, 2, 3]}
        mock_generate.return_value = [[1, 2, 3, 4]]
        mock_tokenizer = MagicMock()
        mock_tokenizer.decode.return_value = "This is a summary."
        self.summarizer.tokenizer = mock_tokenizer

        text = "This is a test text."
        summary = self.summarizer.text_summarizer_batch(text)
        self.assertIn("This is a summary.", summary)

    @patch('summary.Summarizer.openai_summarize')
    def test_summarize_pdf_parallel(self, mock_openai_summarize):
        # Mock the OpenAI summarize method
        mock_openai_summarize.return_value = "OpenAI summarized text."

        pdf_text = "This is a test PDF content."
        with patch.object(self.summarizer, 'read_pdf', return_value=pdf_text):
            with patch.object(self.summarizer, 'text_summarizer_batch', return_value="BART summarized text."):
                summary = self.summarizer.summarize_pdf_parallel('fake_path.pdf')
                self.assertIn("OpenAI summarized text.", summary)

if __name__ == '__main__':
    unittest.main()
