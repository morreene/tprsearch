"# tprsearch" 


# build docker image
docker build -t searchtpr_app .
# run docker
docker run -p 8050:8050 --name my_searchtpr_app searchtpr_app

# TO ANOTHER COMPUTER
# copy docker to tar
docker save -o searchtpr_app.tar searchtpr_app
# copy tar to another computer
# load to another computer
docker load -i searchtpr_app.tar
