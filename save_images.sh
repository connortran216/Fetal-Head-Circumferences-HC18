yourfilenames=`docker images --format "{{.Repository}}" --filter "reference=mask-rcnn-api_*"`
for eachfile in $yourfilenames
do
    echo "Download Image: " $eachfile
    docker save --output $PWD/docker_images/$eachfile.tar $eachfile
    echo "Finish Download <3"
done

