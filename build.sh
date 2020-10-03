# build the static site in hugo/public directory"
(cd hugo && hugo -D)

# The following builds and publishes the image to a private repository at ds.innernet.io:5002
# Note: enable Docker Desktop to use experimental features for buildx command to work:
docker buildx build --platform linux/amd64,linux/arm64,linux/arm/v7 -t ds.innernet.io:5002/innernet-blog:latest --push .
