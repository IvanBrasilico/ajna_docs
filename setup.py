from setuptools import find_packages, setup

setup(
    name='ajna_docs',
    description='Visao computacional e Aprendizado de Maquina na Vigilancia Aduaneira',
    version='0.0.1',
    url='https://github.com/IvanBrasilico/ajna_docs',
    license='GPL',
    author='Ivan Brasilico',
    author_email='brasilico.ivan@gmail.com',
    packages=find_packages(),
    install_requires=[
        'Celery',
        'Flask',
        'Flask-BootStrap',
        'Flask-Login',
        'Flask-cors',
        'Flask-nav',
        'Flask-session',
        'Flask-wtf',
        'pandas',
        'pymongo',
        'redis',
        'sqlalchemy'
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite="tests",
    package_data={
    },
    extras_require={
        'dev': [
            'alembic',
            'bandit',
            'coverage',
            'flake8',
            'flake8-quotes',
            'flask-webtest',
            'isort',
            'pytest',
            'pytest-cov',
            'pytest-mock',
            'sphinx',
            'testfixtures',
            'tox'
        ],
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Topic :: Software Development :: User Interfaces',
        'Topic :: Utilities',
        'Programming Language :: Python :: 3.5',
    ],
)
