mkdir /tmp/work
cd /tmp/work

mkdir foo
touch foo/hello.txt
echo "---- 1st copy..."
cp -r foo bar
find .

echo "---- 2nd copy..."
cp -r foo bar
find .

cd ..
rm -rf /tmp/work
