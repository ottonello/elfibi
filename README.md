Create a `config.ini` file containing the oauth2 credentials:

```
[oauth2]
client_id=AA2JKL
client_secret=dd80a452f927bc3ee91104dc7d9dd9b3
```

Start the frontend:

```shell script
cd fe
npm start
```

Start the backend:

```shell script
./serve.sh
```

Start nginx(Docker)

````shell script
./nginx.sh
````

Start Riak(Docker)

```shell script

````shell script
./riak.sh
````
```
