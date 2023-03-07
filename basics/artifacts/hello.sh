for i in {000..100}
do
    sleep 1
    echo $i > "output/${i}.txt"
    echo "Wrote output/${i}.txt"
done