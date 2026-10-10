from pathlib import Path

from setuptools import find_packages, setup


ROOT = Path(__file__).parent


def read_text(filename: str) -> str:
    return (ROOT / filename).read_text(encoding="utf-8")


INSTALL_REQUIRES = [
    "matplotlib>=3.8",
    "networkx>=3.2",
    "numpy>=1.26",
]


if __name__ == "__main__":
    setup(
        name="electrify",
        version="0.0.1",
        description="Electronics math, quantity parsing, plotting, and circuit-network helpers.",
        long_description=read_text("README.md"),
        long_description_content_type="text/markdown",
        packages=find_packages(exclude=("deprecated", "deprecated.*")),
        package_data={"electrify": ["py.typed"]},
        python_requires=">=3.11",
        install_requires=INSTALL_REQUIRES,
        extras_require={
            "dev": ["mypy>=1.10"],
        },
    )
