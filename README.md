Very simple audio monitor docker container.
Pulls from an RTSP(s) stream (such as a unifi protect camera), takes readings every 5 seconds, then presents an update every 1 minute.
<img width="2870" height="1557" alt="image" src="https://github.com/user-attachments/assets/1f477003-3e9d-419b-b0da-add25fb47f4b" />


To deploy. Either clone this repository and build it by using the build-docker-compose.yml and renaming the example.env file to .env, or, copy the example.env file to .env and use the regular docker-compose.yml to pull the image from gchr.io. Note, the ghcr.io image is only build for x86_64
