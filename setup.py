from setuptools import setup


setup(
    name='cldfbench_dogonlanguages',
    py_modules=['cldfbench_dogonlanguages'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'cldfbench.dataset': [
            'dogonlanguages=cldfbench_dogonlanguages:Dataset',
        ]
    },
    install_requires=[
        'cldfbench',
    ],
    extras_require={
        'test': [
            'pytest-cldf',
        ],
    },
)
