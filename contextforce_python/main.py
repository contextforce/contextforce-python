import requests
import os
import urllib.parse
from typing import Union, Optional, Dict, Any, List

class ContextForceClient:
    _BASE_URL = 'https://r.contextforce.com/'
    _SEARCH_BASE_URL = 'https://s.contextforce.com/'

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('CONTEXTFORCE_API_KEY')
        self.headers = {}
        if self.api_key:
            self.headers = {
                'Authorization': f'Bearer {self.api_key}'
            }

    def _get(self, url: str, headers: Dict[str, str]) -> Any:
        response = requests.get(url, headers={**self.headers, **headers})
        response.raise_for_status()
        if 'application/json' in response.headers.get('Content-Type', ''):
            return response.json()
        else:
            return response.text  # For Markdown or other text-based responses

    def _post(self, url: str, data: dict, headers: Dict[str, str]) -> Any:
        response = requests.post(url, json=data, headers={**self.headers, **headers})
        response.raise_for_status()
        if 'application/json' in response.headers.get('Content-Type', ''):
            return response.json()
        else:
            return response.text  # For Markdown or other text-based responses
    
    def _post_file(self, url: str, files: dict, headers: Optional[dict] = None) -> Any:
        headers = headers or {}
        response = requests.post(url, files=files, headers={**self.headers, **headers})
        response.raise_for_status()
        if 'application/json' in response.headers.get('content-type', ''):
            return response.json()
        else:
            return response.text  # For Markdown or other text-based responses
      
    # Extract content from page url
    def extract_content(self, urls: Union[str, List[str]], result_format: str = 'markdown',
                        include_links: bool = False, include_images: bool = False) -> Any:
        # Determine if headers are needed
        headers = {}        
        if result_format == 'json':
            headers['Accept'] = 'application/json'
        if include_links:
            headers['CF-Include-Links'] = 'true'
        if include_images:
            headers['CF-Include-Images'] = 'true'
        
        # If a single URL, use GET request
        if isinstance(urls, str):
            return self._get(f'{self._BASE_URL}{urls}', headers)
        else:
            # For multiple URLs, use POST request
            return self._post(f'{self._BASE_URL}', urls, headers)

    
    # Extract PDF (from URL or file content)
    def extract_pdf(self, pdf_source: str, result_format: str = 'markdown',
                    mode: str = 'no-ocr', page_number: Optional[str] = None,
                    model: Optional[str] = None, openai_api_key: Optional[str] = None,
                    anthropic_api_key: Optional[str] = None, gemini_api_key: Optional[str] = None) -> Any:
        
        """
            Extracts content from a PDF source and returns it in the specified format.

            Args:
                pdf_source (str): The source of the PDF, either a URL or local file path.
                result_format (str, optional): The format of the result. Defaults to 'markdown'.
                mode (str, optional): The mode of extraction, e.g., 'no-ocr'. Defaults to 'no-ocr'.
                page_number (Optional[str], optional): Specific page numbers to extract. Defaults to None.
                model (Optional[str], optional): The model to use for extraction. Defaults to None.
                openai_api_key (Optional[str], optional): API key for OpenAI models. Defaults to None.
                anthropic_api_key (Optional[str], optional): API key for Anthropic models. Defaults to None.
                gemini_api_key (Optional[str], optional): API key for Gemini models. Defaults to None.

            Returns:
                Any: The extracted content in the specified format.
        """
        # RAISE ERROR FOR INVALID INPUTS
        valid_formats = ["json", "markdown"]
        valid_modes = ['auto', 'no-ocr', 'full-llm-ocr']
        valid_models = ["gemini-1.5-flash-001", "gpt-4o-mini", "gpt-4o", "anthropic-sonnet-3.5"]

        if result_format not in valid_formats:
            raise ValueError(f"Invalid result format. Must be one of {valid_formats}.")

        if mode not in valid_modes:
            raise ValueError(f"Invalid mode. Must be one of {valid_modes}.")

        if mode == 'full-llm-ocr' or mode == 'auto':
            if not model or not (openai_api_key or anthropic_api_key or gemini_api_key):
                raise ValueError("LLM model and at least one API key must be provided for 'auto' or 'full-llm-ocr' modes.")
            if model not in valid_models:
                raise ValueError(f"Invalid LLM model. Must be one of {valid_models}.")

        # API key checks based on the chosen model
        api_key_requirements = {
            "anthropic-sonnet-3.5": anthropic_api_key,
            "gpt-4o-mini": openai_api_key,
            "gpt-4o": openai_api_key,
            "gemini-1.5-flash-001": gemini_api_key
        }

        if model in api_key_requirements and not api_key_requirements[model]:
            raise ValueError(f"{model.split('-')[0].capitalize()} API key must be provided for '{model}' LLM model.")
        
        # Construct headers
        headers = {}
        headers['CF-Result-Format'] = result_format

        if result_format == 'json':
            headers['Accept'] = 'application/json'
        if mode:
            headers['CF-Mode'] = mode
        if page_number:
            headers['CF-Page-Number'] = page_number
        if model:
            if model == 'gpt-4o-mini' or model == 'gpt-4o':
                headers['CF-OpenAI-Api-Key'] = openai_api_key or os.getenv('OPENAI_API_KEY')
            elif model == 'anthropic-sonnet-3.5':
                headers['CF-Anthropic-Api-Key'] = anthropic_api_key or os.getenv('ANTHROPIC_API_KEY')
            elif model == 'gemini-1.5-flash-001':
                headers['CF-Gemini-Api-Key'] = gemini_api_key or os.getenv('GEMINI_API_KEY')
            headers['CF-Model'] = model

        if (pdf_source.startswith('http://') or pdf_source.startswith('https://')):
            # If pdf_source is a URL
            return self._get(f'{self._BASE_URL}{pdf_source}', headers)
        else:
            # If pdf_source is file content (bytes)
            files=[
                ('file',('file.pdf',open(pdf_source,'rb'),'application/pdf'))
            ]
            return self._post_file(f'{self._BASE_URL}', files=files, headers=headers)

   
    # Extract content from page url
    def extract_product(self, urls: Union[str, List[str]], result_format: str = 'json', include_reviews: Optional[bool] = None) -> Any:
        # Construct headers
        headers = {}

        if result_format == 'json':
            headers['Accept'] = 'application/json'
        if include_reviews:
            headers['CF-Include-Reviews'] = 'true'

        if isinstance(urls, str):
            # Single URL case
            return self._get(f'{self._BASE_URL}{urls}', headers)
        else:
            # Multiple URLs case
            return self._post(f'{self._BASE_URL}', urls, headers)
        

    # Generic search function    
    def _search(self, search_url: str, result_format: str = 'json', follow_links: Optional[bool] = True, top_n: Optional[int] = 5) -> Any:
        # Construct headers
        headers = {}

        if result_format == 'json':
            headers['Accept'] = 'application/json'
        if follow_links:
            headers['CF-Follow-Links'] = 'true'
            headers['CF-Top-N'] = str(top_n)
        
        # Perform the GET request
        response = self._get(f'{self._SEARCH_BASE_URL}{search_url}', headers)
        return response
    
    # Google SERP
    def search_google(self, query: str, result_format: str = 'json', follow_links: Optional[bool] = True, top_n: Optional[int] = 5) -> Any:
        # URL encode the query
        encoded_query = urllib.parse.quote_plus(query)
        search_url = f'https://www.google.com/search?q={encoded_query}'
        return self._search(search_url, result_format, follow_links, top_n)

    # Amazon SERP
    def search_amazon(self, query: str, result_format: str = 'json', follow_links: Optional[bool] = True, top_n: Optional[int] = 5) -> Any:
        # URL encode the query
        encoded_query = urllib.parse.quote_plus(query)
        search_url = f'https://www.amazon.com/s?k={encoded_query}'
        return self._search(search_url, result_format, follow_links, top_n)

    # Youtube SERP   
    def search_youtube(self, query: str, result_format: str = 'json', follow_links: Optional[bool] = True, top_n: Optional[int] = 5) -> Any:
        # URL encode the query
        encoded_query = urllib.parse.quote_plus(query)
        search_url = f'https://www.youtube.com/results?search_query={encoded_query}'
        # For YouTube, we don’t need to append to the base URL as it’s a full URL
        return self._search(search_url, result_format, follow_links, top_n)
