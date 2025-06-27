from setuptools import setup, find_packages

setup(
    name="struk-generator",
    version="1.0.0",
    author="Your Name",
    description="Receipt generator GUI for Alfamart/Indomaret-style layout.",
    packages=find_packages(),
    install_requires=[
        "fpdf==1.7.2"
    ],
    include_package_data=True,
    entry_points={
        "gui_scripts": [
            "struk-generator=main:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
