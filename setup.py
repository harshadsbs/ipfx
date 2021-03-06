from setuptools import setup, find_packages


with open('requirements.txt', 'r') as f:
    required = f.read().splitlines()

setup(
    name = 'ipfx',
    version = '0.1.0',
    description = """intrinsic physiology feature extractor""",
    author = "David Feng",
    author_email = "davidf@alleninstitute.org",
    url = 'https://github.com/AllenInstitute/ipfx',
    packages = find_packages(),
    install_requires = required,
    include_package_data=True,
#    entry_points={
#          'console_scripts': [
#              'allensdk.ipfx = allensdk.ipfx.__main__:main'
#        ]
#    },
    setup_requires=['pytest-runner'],
)
