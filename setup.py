from setuptools import setup, find_packages


setup(
    name="SocialMedia",
    version="0.1.0",
    author="Lena Ai team",
    author_email="mahmoud.hammam@lenaai.net",
    description="social media integrations module",
    packages=find_packages(),
    install_requires=["requests", "facebook-business"],
    python_requires=">=3.7",
)