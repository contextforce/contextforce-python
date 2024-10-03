# import pytest
from main import ContextForceClient

# def test_extract_content():
#     client = ContextForceClient()
#     result = client.extract_content("https://www.nbcnews.com/select/shopping/best-puppy-food-rcna151536")
#     print(result)

def test_extract_pdf():
    client = ContextForceClient()

    pdf_file_path = 'tests/2210.05189v3.pdf'  
    # pdf_file_url = 'https://arxiv.org/pdf/2210.05189v3'  

    result = client.extract_pdf(
        pdf_source=pdf_file_path,
        result_format='json',
        mode='auto',
        page_number='1, 2',
        model = 'gpt-4o-mini',
        openai_api_key='sk-xxx'
    )
    print(result)

test_extract_pdf()

# def test_api_call_failure(validator, requests_mock):
#     requests_mock.get(validator.api_url, status_code=500)
#     with pytest.raises(Exception):
#         validator.validate(INVALID_PHONE_NUMBER)
        
# def test_phone_number_with_unsupported_country_code(validator, requests_mock):
#     requests_mock.get(validator.api_url, status_code=400)
#     with pytest.raises(Exception):
#         validator.validate(VALID_PHONE_NUMBER, country_code="ZZ")