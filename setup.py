from distutils.core import setup

from setuptools import setup

setup(
    name='django-ses-analytics',
    version='0.1dev',
    author='Sergey Kopylov',
    author_email='sergkop@gmail.com',
    packages=['ses_analytics'],
    package_data={'ses_analytics': ['static/img/1x1.gif']},
    platforms=['any'],
    url='https://github.com/startup-guide/django-ses-analytics',
    license='MIT',
    description='Send emails and collect analytics in Django with Amazon SES',
    long_description=open('README.md').read(),
    install_requires=[
        'django>=1.5',
        'lxml>=3.2.3',
        'beautifulsoup4>=4.3.1',
        'boto>=2.10.0',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
        'Topic :: Communications :: Email',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
