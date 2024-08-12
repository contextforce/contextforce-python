import pytest
from contextforce_python import ContextForceClient

def test_extract_content():
    client = ContextForceClient()
    result = client.extract_content("https://www.nbcnews.com/select/shopping/best-puppy-food-rcna151536")
    print(result)

# def test_extract_pdf():
#     api_key = 'your_api_key_here'
#     client = ContextForceClient(api_key=api_key)

#     pdf_file_path = '2210.05189v3.pdf'
    
#     with open(pdf_file_path, 'rb') as file:
#         pdf_content = file.read()

#     result = client.extract_pdf(
#         pdf_source=pdf_content,
#         result_format='markdown',
#         model='gpt-4o-mini',
#         openai_api_key='your_openai_api_key'
#     )

# def test_api_call_failure(validator, requests_mock):
#     requests_mock.get(validator.api_url, status_code=500)
#     with pytest.raises(Exception):
#         validator.validate(INVALID_PHONE_NUMBER)
        
# def test_phone_number_with_unsupported_country_code(validator, requests_mock):
#     requests_mock.get(validator.api_url, status_code=400)
#     with pytest.raises(Exception):
#         validator.validate(VALID_PHONE_NUMBER, country_code="ZZ")