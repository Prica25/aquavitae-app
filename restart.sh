sudo docker-compose down
sudo docker rmi aquavitae_app
sudo docker-compose up -d
sudo docker logs aquavitae-app_app_1 -f
