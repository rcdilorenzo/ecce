from setuptools import setup, find_packages

setup(
    name = 'ecce',
    author = 'Christian Di Lorenzo',
    author_email = 'rcddeveloper@icloud.com',
    setup_requires = ['pytest-runner'],
    tests_require = ['pytest', 'pytest-describe'],
    packages = find_packages(),
    include_package_data=True,
    package_data={'ecce': ['data/**/*', 'data/ESV.json']},
    entry_points = {
        'console_scripts': [
            'ecce = ecce.__main__:main'
        ]
    }
)
