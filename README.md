### Quickstart

```sh
docker-compose up --build
```

### How it works

###### REST API microservice

 - Receives calculation requests which will be *asynchronously* processed by `RPC microservice`.
 - Provides access to calculation's results and status.

###### task WORKER

 - Receives calculation task and run the calculation `REST API microservice` sent.
 - Persists the calculation result, so `REST API microservice` can retrieve and respond it.

### How to (lazily) use it

```sh
sh calculate.sh
```

This will request the `REST API microservice` to schedule an calculation. Then, retrieves and displays it.  
### Notes

From another solution's point of view other than an `RPC API`, a `REST API` also is a option.
It's way better tested!
```sh
# Run tests with
python -m doctest arithmetic.py
pytest tests -v
```

Scale at your will by instantiating more `web` and/or `worker` containers

It's also good to remember that there are no mounted volumes, so all the calculations will be lost in the `void` once the containers stop.
