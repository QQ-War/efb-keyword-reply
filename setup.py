from setuptools import setup, find_packages

setup(
    name='efb-keyword-reply',
    packages=find_packages(),
    version='0.1.0',
    description='keyword reply',
    author='QQ-War',
    author_email="undefined@example.com",
    url='https://github.com/QQ_War/efb-keyword-reply.git',
    include_package_data=True,
    install_requires=[
        "ehforwarderbot"
    ],
    entry_points={
        "ehforwarderbot.middleware":"QQ_War.keyword_reply=efb_keyword_reply:KeywordReplyMiddleware",
    }
    )
