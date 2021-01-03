---
title: "Rebalancing a docker swarm"
date: 2021-01-03
category:
- docker
featured: true
tags:
- raspberry-pi
- docker
slug: rebalancing-a-docker-swarm
---

Recently i started hosting the innernet.io blog on my home network, using a Swarm
of Raspberry Pi devices. This serves as an opportunity to explore more aspects of
Docker and Docker Swarms. 

A Docker Swarm is a collection of Docker hosts that work together as a manged unit.
A Docker Swarm basically allows for horizontal scaling, by using multiple hosts
to provide a service. 
The Swarm has one or more "manager" hosts and "worker" hosts. When a network
request hits any host within the Swarm, the Swarm delegates the request to one
of the hosts. The Swarm basically load balances the incoming request among the 
Docker containers that run within the Swarm.

This post explores how to deal with failing hosts within the Swarm, and how to
balance containers among hosts once the failing hosts recover, or when new hosts
join the Swarm.

Here is a quick video showing what happens when hosts within a Swarm fail, and
two approaches to rebalance containers among hosts in the Swarm.

<iframe width="560" height="315" src="https://www.youtube.com/embed/RVm2MXQBOao" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

# Swarms and container distribution

Docker Swarms can run one or more Docker Services.
Here's a `yml` file defining the innernet service:

```yml
version: '3.1'

services:
  innernet-blog:
    image: ds.innernet.io:5002/innernet-blog:latest
    deploy:
      replicas: 4
    ports:
      - "80:80"
```

According to this `yml` file, the `innernet-blog` service should run four
containers of the specified image. The Swarm will attempt to spread these four
containers accross the nodes (hosts) of the Swarm:

![balanced swarm containers](/extras/docker-swarm-balanced-containers.png)

When two of the Swarm nodes fail, the Swarm will spawn two new containers on the
remaining nodes:

![two nodes down](/extras/docker-swarm-down-nodes.png)

When the two failed Swarm nodes recover, the Swarm will not automatically spread
the four containers evenly among the nodes. This means the Swarm will appear to
be unbalanced. Some nodes run multiple containers while other nodes run no containers:

![unbalanced swarm containers](/extras/docker-swarm-unbalanced-containers.png)

# Detecting unbalanced Docker services

Detecting whether a Docker service is "unbalanced" is fairly easy.
We need to determine the following items for a given Docker service:

* A: The number of containers running in the Swarm
* B: The number of nodes that are running containers of the Docker service
* C: The number of nodes available in the Docker Swarm

If A > B, then we know that one or more of the nodes are running multiple containers of the image.

If C > B, then we know that some of the nodes are not running any containers of the image.

If both of these conditions are met, we know that the containers are not balanced across the available nodes in the Swarm

# Rebalancing the Docker Swarm

One way to rebalance the containers of a Swarm is to force-update the Swarm.
Here's an example `docker` command to accomplish this:

```bash
docker service update --force innernet_innernet-blog
```

This will take down all running containers and replace them. Once the command completes, the containers should be spread across all available nodes.
This does take a long time however to respawn all the containers. It is not necessary to respawn all containers - ideally we just want to respawn the containers that are "doubled-stacked" on nodes.

The following shell script tries to find unbalanced services, and then rebalances the containers by reducing the replication count to the number of active nodes that are running containers.
This will remove any double-stacked containers. Next, the script restores the replication count and this should spawn the containers among nodes that do not yet run containers.
This approach is much faster than force-updating the service.

```bash
for service in `docker service ls | awk '($2 != "viz" && $2 != "NAME") { print $1 }'`; do
  docker service ps ${service} | awk '($5 == "Running") { print $4 }' > container-nodes.txt
  container_node_count=`cat container-nodes.txt | sort | uniq | wc -l`
  container_count=`cat container-nodes.txt | wc -l`
  if [ $container_count -gt $container_node_count ]
  then
    available_node_count=`docker node ls | awk '($3 == "Ready" || $2 == "*" && $4 == "Ready") { print $1 }' | wc -l`
    if [ $available_node_count -gt $container_node_count ]
    then
      replicas="`docker service inspect ${service} --pretty | grep Replicas | awk '{ print $NF }'`"
      # Note: replicas should equal container_count, right?
      echo "service ${service} needs to be rebalanced to ${replicas} replicas"

      # Rebalance the containers by first scaling down, then up
      docker service scale ${service}=${container_node_count}
      docker service scale ${service}=${replicas}
    else
      echo "service ${service} can be rebalanced when adding a node"
    fi
  else
    echo "service ${service} does not need to be rebalanced"
  fi
done

```

This script can be downloaded from https://github.com/pythonquick/docker-admin/blob/main/docker-swarm-auto-rebalance.sh
