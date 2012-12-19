from distutils.core import setup

setup(
    name='django-ses-analytics',
    version='0.1dev',
    author='Sergey Kopylov',
    author_email='sergkop@gmail.com',
    packages=['ses_analytics'],
    platforms=['any'],
    url='https://github.com/startup-guide/django-ses-analytics',
    license='MIT',
    description='Send emails and collect analytics in Django with Amazon SES',
    long_description=open('README.md').read(),
    install_requires=[
        'django>=1.4.3',
        'lxml>=3.0.2',
        'beautifulsoup4>=4.1.3',
        'boto>=2.6.0',
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
