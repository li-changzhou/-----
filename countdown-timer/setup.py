from setuptools import setup, find_packages

setup(
    name="countdown-timer",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.11",
    install_requires=[
        "click>=8.1.0",
        "pytest>=7.4.0",
        "pytest-cov>=4.1.0",
    ],
    extras_require={
        "dev": [
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "isort>=5.12.0",
        ],
        "p2": [
            "fastapi>=0.100.0",
            "sqlalchemy>=2.0.0",
            "uvicorn>=0.23.0",
        ],
        "p3": [
            "redis>=5.0.0",
            "celery>=5.3.0",
            "pytz>=2023.3",
        ],
    },
    entry_points={
        "console_scripts": [
            "countdown=countdown_timer.cli:cli",
        ],
    },
)
