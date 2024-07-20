from setuptools import setup


setup(
    name='cldfbench_kogansemitic',
    py_modules=['cldfbench_kogansemitic'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'cldfbench.dataset': [
            'kogansemitic=cldfbench_kogansemitic:Dataset',
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
