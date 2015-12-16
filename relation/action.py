from .page import *

@IN.hook
def actions():
	actns = {}

	actns['relation/action/{relation_type}/{to_entity_type}/{to_entity_id}'] = {
		'title' : 'relation action popup',
		'handler' : action_handler_relation_action_popup,
	}

	return actns
