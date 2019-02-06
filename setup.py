from setuptools import setup, find_packages

setup(
    name='k8sdeploy',
    version='0.1.0',
    author="Praveen D",
    author_email="praveend[dot]hac[at]gmail.com",
    description="Kubernetes deployment utility",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'click-plugins',
        'GitPython',
        'py',
        'colorlog',
    ],
    entry_points='''
        [console_scripts]
        k8sdeploy=src.k8s_deploy:deployment
    ''',
)
