# Automated Trading Bot API (In Progress)

## Usage

All responses will have the form

```json
{
	"data": "Mixed type holding the content of the response",
	"message": "Description of what happened"
}
```

Subsequent response definitions will only represent the content of the "data" field

### Get all Bots

`Get /bots`

**Response**

- `200 OK` on success
```json
[
	{
		"id": "123",
		"name": "bot1",
		"buy_behaviors": {
				   "group_conditional":"or",
				   "group":[
				   		{
                                     			"group_conditional":"and", <*>
                                     			"group":[
				     					{
				       						"function":"momentum",
				       						"inputs":{
				  	          					"interval":200
					        				},
				       						"conditional":"greater_than", <**>
				       						"target":"0.1" <***>
			             					},
				     					{
				       						"function":"moving_average",
				       						"inputs":{
					        					  "interval":200
					        				},
				       						"conditional":"greater_than", <**>
				       						"target":"current_price" <***>
			             					}
				  				]
				  		},
				  		{
				     			"group_conditional":"or", <*>
                                     			"behaviors":[
				     					{
				       						"function":"momentum",
				       						"inputs":{
				  	          					"interval":200
					        				},
				       						"conditional":"greater_than", <**>
				       						"target":"0.1" <***>
			             					},
				     					{
				       						"function":"moving_average",
				       						"inputs":{
					        			  		"interval":200
					        				},
				       						"conditional":"greater_than", <**>
				       						"target":"current_price" <***>
			             					}
				  				]
						}
					]
				}
		"sell_behaviors": [
				   {
				     "function":"momentum",
				     "inputs":{
					        "interval":200
					      },
				     "conditional":"less_than",
				     "target":"-0.1" <*>
			           }
				]
	}
]
<*> conditional enum ("greater_than", "equal_to", "less_than", "greater_than_or_equal_to", "less_than_or_equal_to")
<**> target will be parsed into either a number or an enum ("current_price")
```
