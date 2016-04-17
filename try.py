from alchemyapi import AlchemyAPI
def try():
	alchemyapi = AlchemyAPI()
	myText = "I am liking  this hackathon"
	response = alchemyapi.sentiment("text", myText)
	if(response["docSentiment"]["type"]=="positive"):
		return "blue"
	else:
		return "gray"
