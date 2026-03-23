## Implementation: The Recusrive Agent

from google import genai
from google.genai import types
import json


def run_living_harvest_agent(brand_name, depth=0, max_depth=2):
	client = genai.Client()


	# 1. Structured Output with an added 'reasoning' and 'next_step' field

	harvest_schema = {
		"type": "OBJECT",
		"properties": {

			"brand": {},
			"harvest_found": {},
			"harvest_date": {},
			"confidence_score": {},
			"reasoning": {},
			"suggested_action": {}
		},

		"required": ["brand","harvest_found","reasoning"]
	}


	# 2. Tools
	# The advantage of using the google search tool here is you have
	# access to live information 


	## <TBD gets all the different information and complete this code here> 

	