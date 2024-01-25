from setuptools import setup, find_packages

setup(
    name='code_annotator',
    version='0.0.1',
    author='Eugene Evstafev',
    author_email='chigwel@gmail.com',
    description='A tool to annotate code using the Mistral API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/chigwell/code_annotator',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'code-annotator=code_annotator.annotator:main',
        ],
    },
)