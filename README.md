# ContextForce SDK Documentation

## Overview

The `ContextForceClient` class provides a Python interface to interact with the ContextForce API. Below are the available methods, how to use them, and details on the headers automatically set by the SDK.

## Installation
```bash
pip install contextforce-python
```

## Initialization

### Example
```python
from contextforce_python import ContextForceClient

# api key is not required for free users. Get it when you want to have more free token and better rate limit
client = ContextForceClient(api_key='your_api_key')
```

## Methods

### 1. extract_content

Extracts content from a given page URL or list of URLs. The content can be returned in Markdown or JSON format.  

#### Parameters
- `urls`: A string (single URL) or a list of URLs.
- `result_format`: The format of the result, either `'markdown'` (default) or `'json'`.
- `include_links`: Boolean to include links in the output (default `False`).
- `include_images`: Boolean to include images in the output (default `False`).

#### Headers Set by SDK
- **Authorization**: Set to `Bearer {api_key}`.
- **Accept**: Set to `'application/json'` if `result_format` is `'json'`.
- **CF-Include-Links**: Set to `'true'` if `include_links` is `True`.
- **CF-Include-Images**: Set to `'true'` if `include_images` is `True`.

#### Example Usage
```python
# Convert an online article into markdown
result = client.extract_content("https://www.nbcnews.com/select/shopping/best-puppy-food-rcna151536")
```

### 2. extract_pdf

Extracts content from a PDF URL or file content. The content can be returned in Markdown or JSON format.

#### Parameters
- `pdf_source`: A string (PDF URL) or bytes (PDF file content).
- `result_format`: The format of the result, either `'markdown'` (default) or `'json'`.
- `page_number`: The pages to extract , either all (default) or given page number
- `mode`: The OCR mode to use: [`'auto'` (default), `'no-ocr'`, `'full-optimized-ocr'`, `'full-llm-ocr'`]
- `model`: Optional model to use: [`'gpt-4o'`, `'gpt-4o-mini'`, `'anthropic-sonnet-3.5'`]
- `openai_api_key`: Optional OpenAI API key if `model` is `'gpt-4o'` or `'gpt-4o-mini'`.
- `anthropic_api_key`: Optional Claude API key if `model` is `'anthropic-sonnet-3.5''`.

#### Headers Set by SDK
- **Authorization**: Set to `Bearer {api_key}`.
- **Accept**: Set to `'application/json'` if `result_format` is `'json'`.
- **CF-Mode**: Set to given mode if `mode` is specified
- **CF-Page-Number**: Set to given page number is `page_number` is specified
- **CF-Model**: Set to the model name if `model` is specified.
- **CF-OpenAI-API-Key**: Set to the OpenAI API key if `model` is `'gpt-4o-mini'`.
- **CF-Claude-API-Key**: Set to the Claude API key if `model` is `'claude-3.5'`.
- **Content-Type**: Set to `'multipart/form-data'` for file uploads.
- **CF-Content-Type**: Set to `'application/pdf'` when uploading PDF content.

#### Example Usage
```python
# Convert the PDF to markdown using Full LLM OCR mode
result = client.extract_pdf("https://arxiv.org/pdf/2210.05189")

# Convert the PDF to markdown and use gpt-4o-mini to handle the OCR for pages with special elements like formula, table and image
result = client.extract_pdf("https://arxiv.org/pdf/2210.05189", mode="full-llm-ocr", model="gpt-4o-mini", openai_api_key="sk-xxxxxx")
```

### 3. extract_product

Extracts product information from a given product page URL or list of URLs. The content is returned in JSON format by default.

#### Parameters
- `urls`: A string (single URL) or a list of URLs.
- `result_format`: The format of the result, either `'json'` (default) or `'markdown'`.
- `include_reviews`: Optional boolean to include product reviews in the output.

#### Headers Set by SDK
- **Authorization**: Set to `Bearer {api_key}`.
- **Accept**: Set to `'application/json'` if `result_format` is `'json'`.
- **CF-Include-Reviews**: Set to `'true'` if `include_reviews` is `True`.

#### Example Usage
```python
# Extract Amazon product info and return the result in json 
result = client.extract_product("https://www.amazon.com/dp/B001VIWHMY")
```

### 4. search_google

Performs a Google search based on a query.

#### Parameters
- `query`: The search query.
- `result_format`: The format of the result, either `'json'` (default) or `'markdown'`.
- `follow_links`: Optional boolean to follow links on the search results (default `True`).
- `top_n`: Optional integer to specify the number of top pages to crawl if `follow_links` is `True` (default `5`).

#### Headers Set by SDK
- **Authorization**: Set to `Bearer {api_key}`.
- **Accept**: Set to `'application/json'` if `result_format` is `'json'`.
- **CF-Follow-Links**: Set to `'true'` if `follow_links` is `True`.
- **CF-Top-N**: Set to the value of `top_n`.

#### Example Usage
```python
# Get Google SERP result only
result = client.search_google("best dog food")

# Get Google SERP result and convert the top N pages into markdown
result = client.search_google("best dog food", result_format="json", follow_links=True, top_n=5)
```

### 5. search_amazon

Performs an Amazon search based on a query.

#### Parameters
- `query`: The search query.
- `result_format`: The format of the result, either `'json'` (default) or `'markdown'`.
- `follow_links`: Optional boolean to follow links on the search results (default `True`).
- `top_n`: Optional integer to specify the number of top pages to crawl if `follow_links` is `True` (default `5`).

#### Headers Set by SDK
- **Authorization**: Set to `Bearer {api_key}`.
- **Accept**: Set to `'application/json'` if `result_format` is `'json'`.
- **CF-Follow-Links**: Set to `'true'` if `follow_links` is `True`.
- **CF-Top-N**: Set to the value of `top_n`.

#### Example Usage
```python
# Get the amazon search result
result = client.search_amazon("dog food")

# Get the amazon search result and follow the top N products to get the detail info in json
result = client.search_amazon("dog food", follow_links=True, top_n=5)
```

### 6. search_youtube

Performs a YouTube search based on a query.

#### Parameters
- `query`: The search query.
- `result_format`: The format of the result, either `'json'` (default) or `'markdown'`.
- `follow_links`: Optional boolean to follow links on the search results (default `True`).
- `top_n`: Optional integer to specify the number of top pages to crawl if `follow_links` is `True` (default `5`).

#### Headers Set by SDK
- **Authorization**: Set to `Bearer {api_key}`.
- **Accept**: Set to `'application/json'` if `result_format` is `'json'`.
- **CF-Follow-Links**: Set to `'true'` if `follow_links` is `True`.
- **CF-Top-N**: Set to the value of `top_n`.

#### Example Usage
```python
# Get the youtube search result based on the keyword
result = client.search_youtube("how to train my dog")

# Get the youtube search result and follow the top N links to get the video info
result = client.search_youtube("how to train my dog", follow_links=True, top_n=5)
```

---

This documentation provides detailed information on how to use each function within the `ContextForceClient` SDK and the headers automatically set by the SDK for each one of the functions.
