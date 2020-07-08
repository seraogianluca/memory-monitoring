# Memory Monitoring

## What is this repository?
It is a project for the Cloud Computing course of the MSc Artificial Intelligence and Data Engineering at University of Pisa.

## What does this project is supposed to do?
The project should periodically retrieve the memory usage of remote machines and save the data into an instance of [Gnocchi](https://github.com/gnocchixyz/gnocchi) database, moreover it should retrieve and show such values from the database.

The project is composed by a producer and a consumer. The producer reads the data from the machines using ssh connections and save the data retreived on Gnocchi. The consumer reads and show the data retreived from Gnocchi.

![Architecture](/doc/architecture.png)

## Run our paramount project by yourself!
To run this project, first you need a cloud infrastructure with Openstack and Gnocchi installed on top. Then, you need Docker to run both producer and consumer in containers.

Copy the consumer and producer direcotries to the machine where docker is installed and connect to it. Directories must have the following structure:

```sh
root@host-name:~# ls
consumer  producer 
```

**producer/** directory:
```sh
root@host-name:~/producer# ls
config.json  producer.py  Dockerfile requirements.txt
```

**consumer/** directory:
```sh
root@host-name:~/consumer# ls
config.json  consumer.py  Dockerfile requirements.txt
```

The `config.json`file is the same and must be in both the directories.

### Producer
Build the customized image using the Dockerfile. Run the following commands inside the producer directory.

```sh
docker build -t producer .
```

Run the container in background with the **-d** option:
```sh
 docker run -d producer
```

or if you want to see the producer output in realtime run the container in foreground with the **-it** option:
```sh
 docker run -it producer
```

Every 30 seconds, for every machine, the producer makes three requests, one every 4 seconds.

### Consumer
Build the customized image of the consumer using the Dockerfile. Run the following commands inside the producer directory.

```sh
docker build -t consumer .
```

Since the consumer is an interactive script it must run in foreground to choose the aggregation method and granularity to show. The consumer will read the periodic updates of the producer every 30 seconds.

```sh
docker run -it consumer
```

**Example of execution:**
```sh
root@G2LT74AKPEAN2NI:~/consumer# docker run -it consumer
Please, chose a kind of aggregation:

1) Mean
2) Min
3) Max
1
Please, chose a granularity:

1) Minute
2) Hour
1

Host: 172.0.0.1

+---------------------------+-------------+--------------------+
|         Timestamp         | Granularity |        MEAN        |
+---------------------------+-------------+--------------------+
| 2020-07-07T19:20:00+00:00 |     60.0    |       35.89        |
| 2020-07-07T19:21:00+00:00 |     60.0    |       35.87        |
| 2020-07-07T19:22:00+00:00 |     60.0    |       35.88        |
| 2020-07-07T19:23:00+00:00 |     60.0    |       35.88        |
| 2020-07-07T19:24:00+00:00 |     60.0    |       36.16        |
+---------------------------+-------------+--------------------+

# ... other machines results
```

### Useful commands:
List all the containers:
```sh
docker ps -a
```

Stop all the containers:
```sh
docker stop $(docker ps -a -q)
```

Remove all the containers:
```sh
docker rm $(docker ps -a -q)
```

List all the images:
```sh
docker images -a
```

Remove all the images (add `-f` option to force the action):
```sh
docker rmi $(docker images -a -q)
```

## One more thing...
We use one metric for each machine on Gnocchi. For each metric use the `medium` archive policy that aggregates the data with two different granularities:
- 1 minute granularity over 7 days
- 1 hour granularity over 365 days

We don't use a specific aggregation because our consumer retrieves the data using mean, min and max.

To let the application work the `config.json` should be properly filled. The config file should include a list of the hosts for which the memory monitoring is performed with the respective `metric-id` on Gnocchi.

```json
{
    "hosts": [
        {
            "ip": "machine-ip",
            "user": "machine-user",
            "password": "machine-password",
            "metric": "gnocchi-metric-id"
        }
    ]
}
```