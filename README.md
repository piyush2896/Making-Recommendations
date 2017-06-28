# Recommendation System
This repository contains a simple recommendation system, made completely from scratch (no external libraries required).

## Usage
To *get recommendation*:
import recommendations.py and send a dictionary in format 
```
{
	"User 01": {
		"Product 01": Rating,
		"Product 02": Rating,
		"Product 03": Rating,
	},
	"User 02": {
		"Product 02": Rating,
		"Product 04": Rating,
		"Product 01": Rating,
	}...
}
```
along with a username to:
```
recommendations.getRecommendations(prefs, username)
```
<br/><br/>
To *transform preferences* from a dictionary like
{
	"User 01": {
		"Product 01": Rating,
		"Product 02": Rating,
		"Product 03": Rating,
	},
	"User 02": {
		"Product 02": Rating,
		"Product 04": Rating,
		"Product 01": Rating,
	}...
}

*to a dictionary like*
```
{
	"Product 01": {
		"User 01": Rating,
		"User 02": Rating
	},
	"Product 01": {
		"User 04": Rating,
		"User 02": Rating
	}...
}
```
send the preferences dictionary to:
```
recommendations.transformPrefs(prefs)
```
