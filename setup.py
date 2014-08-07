from setuptools import setup, find_packages


setup(
    name = "django-netpromoterscore",
    version = '0.0.1',
    description = "Model, Tests, and API for collecting promoter score from users.",
    author = "Austin Brennan",
    author_email = "ab@epantry.com",
    url = "https://github.com/epantry/django-netpromoterscore",
    keywords = ["promoter score", "net promoter score", "django"],
    install_requires = [],
    packages = find_packages(),
    include_package_data=True,
    )