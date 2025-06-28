from setuptools import setup, find_packages

setup(
    name="alfamart-indomaret-receipt",
    version="1.0.0",
    author="Farahat",
    description="Generate printable Alfamart/Indomaret-style receipts with a simple Python GUI and PDF output.",
    packages=find_packages(),
    install_requires=[
        "fpdf==1.7.2"
    ],
    include_package_data=True,
    entry_points={
        "gui_scripts": [
            "salfamart-indomaret-receipt=main:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
