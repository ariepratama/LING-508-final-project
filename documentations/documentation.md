# Search News By NE
## NE Search / Autocomplete
Retrieve all possible NE categories that has been stored in db, based on users input.

Api Url
```
GET localhost:5002/ner/related?query={query_string}
```

sample curl
```
   curl -X GET \
  'http://localhost:5002/ner/related?query=per' \
  -H 'cache-control: no-cache'
```
sample response
```json
{
    "data": [
        "PERCENT",
        "PERSON"
    ]
}
```


## News / Document search
Retrieve news articles based on NE category.

Api Url
```
POST localhost:5002/documents/search
```

Sample curl
```
curl -X POST \
  http://localhost:5002/documents/search \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/json' \
  -d '{
	"ner_category": "LAW"
}'
```

Sample Response
```json
{
    "data": [
        {
            "id": 4,
            "text": "Whether a sign of a good read; or..."
        },
        {
            "id": 5,
            "text": "The deaths of three American soldiers in Afghanistan this week are..."
        }
    ]
}
```