docker run -d -P -v $(pwd)/data:/var/lib/riak -v $(pwd)/logs:/var/log/riak -v $(pwd)/riak/schemas:/etc/riak/schemas --name=riakts --rm -d -p 8087:8087 -p 8098:8098 basho/riak-ts