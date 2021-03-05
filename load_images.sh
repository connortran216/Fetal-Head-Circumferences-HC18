yourfilenames=`ls ./docker_images/*.tar`
for eachfile in $yourfilenames
do
    echo $eachfile
    docker load --input $eachfile
done