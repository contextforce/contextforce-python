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
        headers['Content-Type'] = 'multipart/form-data'  # Set content type for file uploads
        response = requests.post(url, files=files, headers={**self.headers, **headers})
        response.raise_for_status()
        if 'application/json' in response.headers.get('Content-Type', ''):
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
    def extract_pdf(self, pdf_source: Union[str, bytes], result_format: str = 'markdown',
                    mode: str = 'auto', page_number: Optional[int] = None,
                    model: Optional[str] = None, openai_api_key: Optional[str] = None,
                    anthropic_api_key: Optional[str] = None) -> Any:
        
        # Construct headers
        headers = {}

        if result_format == 'json':
            headers['Accept'] = 'application/json'
        if mode:
            headers['CF-Mode'] = mode
        if page_number:
            headers['CF-Page-Number'] = str(page_number)
        if model:
            if model == 'gpt-4o-mini' or model == 'gpt-4o':
                headers['CF-OpenAI-API-Key'] = openai_api_key or os.getenv('OPENAI_API_KEY')
            elif model == 'anthropic-sonnet-3.5':
                headers['CF-Anthropic-API-Key'] = anthropic_api_key or os.getenv('ANTHROPIC_API_KEY')
            headers['CF-Model'] = model

        if isinstance(pdf_source, str):
            # If pdf_source is a URL
            return self._get(f'{self._BASE_URL}{pdf_source}', headers)
        else:
            # If pdf_source is file content (bytes)
            headers['CF-Content-Type'] = 'application/pdf'  # Custom header to indicate PDF content
            files = {'file': pdf_source}
            return self._post_file(f'{self._BASE_URL}', files, headers)

   
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
