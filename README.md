## Prerequisites
1) Docker and docker-compose instaled
2) porst 8000-8003 are free
3) jq instaled (not mandatory, just to pritify the curl response)

## Build containers:
``cd replicated_log``
``docker-compose build``

## Run container
``docker-compose up -d``

## Check the status
``docker-compose ps``
Output example:
``
            Name                    Command         State            Ports          
------------------------------------------------------------------------------------
replicated_log_master_1        python -m app.main   Up      127.0.0.1:8000->8000/tcp
replicated_log_secondary-1_1   python -m app.main   Up      127.0.0.1:8001->8000/tcp
replicated_log_secondary-2_1   python -m app.main   Up      127.0.0.1:8002->8000/tcp
replicated_log_secondary-3_1   python -m app.main   Up      127.0.0.1:8003->8000/tcp
``

## Post a message:
``curl --request POST 'http://0.0.0.0:8000/append_msg' --data-raw '{"message": "some text of the message"}' | jq '.'``
Output example:
``
{
  "list size": 1 # count of messages in the list
}
``

## Get messages from a master node
``curl --location --request GET 'http://0.0.0.0:8000/list_msg' | jq '.'``
Output example:

``
[
  {
    "message": "some text of the message", # text of the message
    "created_at": "2020-11-11 17:06:19.117630" # the message creation timestamp
  }
]
``

To get the list of messages from secondary nodes, just use the curl from abou but replase the port with one of 8001-8003

## To stop and remove containers

``docker-compose stop && docker-compose rm -f``