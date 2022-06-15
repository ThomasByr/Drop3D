pip uninstall drop3d -y
python setup.py sdist bdist_wheel
pip install .\dist\drop3d-0.0.1-py3-none-any.whl