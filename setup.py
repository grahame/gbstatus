from setuptools import setup, find_packages

dev_requires = ['flake8', 'nose']
install_requires = ['requests>=2.2']

setup(
    author = "Grahame Bowland",
    author_email = "grahame@angrygoats.net",
    description = "Drop-in alternative to i3status.",
    license = "GPL3",
    keywords = "i3status status",
    url = "https://github.com/grahame/gbstatus",
    name = "gbstatus",
    version = "1.0.0",
    packages = find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    extras_require = {
        'dev': dev_requires
    },
    install_requires = install_requires,
    entry_points = {
        'console_scripts': [
            'gbstatus = gbstatus.cli:main',
        ],
    }
)
