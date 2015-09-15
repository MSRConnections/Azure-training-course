azure config mode arm
cd Images
for f in *.jpg
do
	azure storage blob upload -c "<Your Container Key Here>" "${f##*/}" input "${f##*/}"
done
cd ..
