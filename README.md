# README.md for the Trend Analysis training

Author: Martijn Zwennes <martijn.zwennes@incentro.com>

Pre-requisites:
- Google Cloud account with a credit card
- UNIX based OS (Fedora, Ubuntu, CentOS)

Get a instagram access token and client secret
    
    http://jelled.com/instagram/access-token
    
    https://www.instagram.com/oauth/authorize?client_id=CLIENTID
        &redirect_uri=REDIR_URL
        &response_type=token
        &scope=basic+public_content+follower_list+comments+relationships+likes
    
        
Setup datalab Docker image
    
    docker run -it -p "127.0.0.1:8081:8080" -v "${HOME}:/content" \
    -e "PROJECT_ID=incentro-sam-1070" \
    gcr.io/cloud-datalab/datalab:local
        
Creating a dataproc cluster

    gcloud dataproc clusters create <cluster-name> \
    --project <project-id> \
    --bucket <bucket-name>
    --initialization-actions \
        gs://dataproc-initialization-actions/jupyter/jupyter.sh
        
        
SSH tunnel into the server
    
    gcloud compute ssh \ 
    --zone=europe-west1-c \
    --ssh-flag="-D" \
    --ssh-flag="10000" \
    --ssh-flag="-N" "zwennes-training-cluster-m"
    
    /usr/bin/google-chrome "http://zwennes-training-cluster-m:8123" \
    --proxy-server="socks5://localhost:10000" \
    --host-resolver-rules="MAP * 0.0.0.0 , EXCLUDE localhost"  \
    --user-data-dir=/tmp/
    

SQL

    SELECT 
      keyword, 
      avg(sentiment_polarity) as polarity, 
      avg(sentiment_magnitude) as magnitude,
      count(*) as tweet_count
    FROM [incentro-sam-1070:zwennes.tweets] 
    GROUP BY keyword;
    
    SELECT 
      keyword, 
      count(*) as tweet_count 
    FROM zwennes.tweets
    GROUP BY keyword;