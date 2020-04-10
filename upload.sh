for i in {1..30}
do if [ $i -lt 10 ]
then
    git add "0$i"
    git commit -m "Maintain Historical Dataset"
    git push
fi 
if [ $i -ge 10 ]
then
    git add "$i"
    git commit -m "Maintain Historical Dataset"
    git push
fi
done