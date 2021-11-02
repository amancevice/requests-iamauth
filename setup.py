from setuptools import (find_packages, setup)

with open('README.md', 'r') as readme:
    long_description = readme.read()

setup(
    author='amancevice',
    author_email='smallweirdnum@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Utilities',
    ],
    description='SigV4 authorizer for requests',
    install_requires=[
        'boto3',
        'requests',
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    name='requests-iamauth',
    packages=find_packages(exclude=['tests']),
    python_requires='>= 3.6',
    setup_requires=['setuptools_scm'],
    url='https://github.com/amancevice/requests-iamauth',
    use_scm_version=True,
)
