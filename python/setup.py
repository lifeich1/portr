import setuptools

setuptools.setup(
    name="portr-act-lifeich0",
    version="0.0.1",
    author="lifeich0",
    description="tiny heartbeat package",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=[
        'web.py>=0.40',
        'python-socketio',
    ],
)
