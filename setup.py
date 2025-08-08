from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="simulate-to-survive",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A text-based survival simulation game with emotional storytelling",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/simulate-to-survive",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "black>=23.7.0",
            "flake8>=6.0.0",
            "mypy>=1.5.1",
        ],
    },
    entry_points={
        "console_scripts": [
            "simulate-to-survive=simulate_to_survive.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "simulate_to_survive": ["assets/**/*", "config/**/*"],
    },
)
