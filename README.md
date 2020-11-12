## Prerequisites
1) Docker and docker-compose installed
2) ports 8000-8003 are free
3) jq installed (not mandatory, just to prettify the curl response)

## Build containers:
``cd replicated_log``
``docker-compose build``

## Run container
``docker-compose up -d``

## Check the status
``docker-compose ps``

Output example:

```
            Name                    Command         State            Ports          
------------------------------------------------------------------------------------
replicated_log_master_1        python -m app.main   Up      127.0.0.1:8000->8000/tcp
replicated_log_secondary-1_1   python -m app.main   Up      127.0.0.1:8001->8000/tcp
replicated_log_secondary-2_1   python -m app.main   Up      127.0.0.1:8002->8000/tcp
replicated_log_secondary-3_1   python -m app.main   Up      127.0.0.1:8003->8000/tcp
```

# Use the Swagger ui 

## Post a message:
* Open in browser the following link:
``http://127.0.0.1:8000/docs#/default/append_msg_append_msg_post``
* Click on the '**Try it out**' button
* insert in the body section the following body:
``
{
"message" : "some message text"
}
``
## Get messages from a master node:
``http://127.0.0.1:8000/docs#/default/list_msg_list_msg_get``

To get the list of messages from secondary nodes, just use the curl from above but replace the port with one of 8001-8003

# Use a terminal 

## Post a message:
``curl --request POST 'http://0.0.0.0:8000/append_msg' --data-raw '{"message": "some text of the message"}' | jq '.'``

Output example:

```
  {
    "message": "some text of the message", # text of the message
    "created_at": "2020-11-11 17:06:19.117630" # the message creation timestamp
  }
```

## Get messages from a master node
``curl --location --request GET 'http://0.0.0.0:8000/list_msg' | jq '.'``
Output example:

```
[
  {
    "message": "some text of the message", # text of the message
    "created_at": "2020-11-11 17:06:19.117630" # the message creation timestamp
  }
]
```

To get the list of messages from secondary nodes, just use the curl from above but replace the port with one of 8001-8003

## To stop and remove containers

``docker-compose stop && docker-compose rm -f``
