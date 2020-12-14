#!/usr/bin/env bash
DOCS_FOLDER="/home/test/docs_auto"

echo "Activate venv"
source $DOCS_FOLDER/venv_for_auto/bin/activate

echo "Go to git-folder with code"
cd $DOCS_FOLDER/repo
git checkout develop

echo "Pull changes from git"
git pull

echo "Install requirements from requirements.txt"
pip install -r requirements.txt

echo "Go to docs folder"
cd  $DOCS_FOLDER/docs_sphinx

echo "Rebuild documentation"
rm -rf tools*.rst framework.*rst

sphinx-apidoc -o . ../repo

rm -rf tests.*rst

make clean

make html

echo "Restart apache container"
docker restart sp_docs_apache