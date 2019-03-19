from setuptools import setup, find_packages

setup(
    name = 'ecce',
    author = 'Christian Di Lorenzo',
    author_email = 'rcddeveloper@icloud.com',
    setup_requires = ['pytest-runner'],
    tests_require = ['pytest', 'pytest-describe'],
    packages = find_packages(),
    entry_points = {
        'console_scripts': [
            # 'ecce = ecce.__main__:main'
        ]
    }
)
