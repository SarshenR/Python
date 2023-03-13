import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='packageOwnPay',
    version='0.0.1',
    author='Sarshen Ramsamy',
    author_email='sarshenr@hollywoodbets.net',
    description='Testing installation of Package',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/SarshenR/Python',
    project_urls = {
        "Bug Tracker": "https://github.com/SarshenR/Python"
    },
    license='MIT',
    packages=['packageOwnPay'],
    install_requires=['requests'],
)