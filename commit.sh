TOKEN="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"
USERNAME="Bececrazy"
REPO="SAP1-Computer"

git init
git add -A
git commit -m "new commit"
git branch -M main
git remote remove origin
git remote add origin https://$TOKEN@github.com/$USERNAME/$REPO.git
git push -u origin main