### What is this

A webapp which fetches your Fitbit heart rate data and plots it in your browser.
Oauth2 tokens are stored in Postgres, data is stored in Riak TS. 

### What this isn't

Proper software: This piece of software doesn't have any tests, misses some error handling, isn't properly commented. Use or reuse
under your own risk. 

### What do you need

A Fitbit account and data, an app in https://dev.fitbit.com/.
To access detailed heart rate data, you'll need a 'Personal' Application type.

Set your callback URLs to local:
```shell script
http://localhost:8080/auth_callback
http://localhost:8000/api/auth_callback
```

Create a `config.ini` file containing the oauth2 credentials:

```
[oauth2]
client_id=AA2JKL
client_secret=dd80a452f927bc3ee91104dc7d9dd9b3
```

# Running locally

All you need is Docker, NPM and a Poetry env.

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
