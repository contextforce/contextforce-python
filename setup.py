from setuptools import setup, find_packages

setup(
    name='contextforce-python',
    version='0.1',
    description='Contextforce Client API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Danielle',
    author_email='contextforce01@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'requests'
    ],
    python_requires='>=3.6',
)
