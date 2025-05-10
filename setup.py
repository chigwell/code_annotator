from setuptools import setup, find_packages

setup(
    name='code_annotator',  # Name of the package
    version='2025.05.100925',  # Version of the package
    author='Eugene Evstafev',  # Author's name
    author_email='chigwel@gmail.com',  # Contact email for the author
    description='A tool to annotate code using the LLM7.io',  # Short description of the package
    long_description=open('README.md').read(),  # Long description read from README.md
    long_description_content_type='text/markdown',  # Content type of the long description
    url='https://github.com/chigwell/code_annotator',  # URL of the project repository
    packages=find_packages(),  # Automatically find and include all packages
    install_requires=[
        'requests',  # Requests library for HTTP requests
        'llmatch_messages',  # Additional library used by the package
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',  # License classification
        'Development Status :: 3 - Alpha',  # Development status indicator
        'Intended Audience :: Developers',  # Target audience
        'Programming Language :: Python :: 3',  # Python 3 compatibility
        'Operating System :: OS Independent',  # OS independent
    ],
    python_requires='>=3.6',  # Minimum Python version required
    entry_points={
        'console_scripts': [
            'code-annotator=code_annotator.annotator:main',  # Command line script entry point
        ],
    },
)