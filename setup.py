from setuptools import setup

readme = open('README.rst', encoding='utf-8').read()

setup(
    name='django-softdel',
    version='0.1',
    description="""Provide a model that implements soft deletion (logical deletion).""",
    long_description=readme,
    author='lanfycode',
    author_email='614974213@qq.com',
    url='https://github.com/lanfycode/django-softdel.git/',
    keywords='django-softdel',
    packages=['softdel'],
    include_package_data=True,
    zip_safe=True,
    install_requires=['django>=2.2'],
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ]
)
