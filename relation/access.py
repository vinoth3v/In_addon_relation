from collections import OrderedDict

@IN.hook
def access_keys():
	
	
	keys = {}

	group = 'Relation'
	keys[group] = OrderedDict()	# we may need order
	keys_entity_type = keys[group]

	# administer all entities
	keys_entity_type['admin_relation'] = {
		'title' : s('(Administer) Allow nabar to do ANY ACTION on Relation'),
		'flag' : 'danger',
	}
	
	for relation_type, relation_type_entity in IN.relater.relation_type_entities.items():
	
		#entity_type = entity_type.lower()			# lower case
		group = 'Relation_' + relation_type
		keys[group] = OrderedDict() 			# keep order
		
		keys_relation_type = keys[group]

		# view
		prefix = 'Relation_' + relation_type
		keys_relation_type['create_' + prefix] = {
			'title' : s('Allow nabar to create {relation_type} relation', {'relation_type' : relation_type})
		}
		keys_relation_type['accept_' + prefix] = {
			'title' : s('Allow nabar to accept {relation_type} relation request', {'relation_type' : relation_type})
		}
		keys_relation_type['reject_' + prefix] = {
			'title' : s('Allow nabar to reject {relation_type} relation request', {'relation_type' : relation_type})
		}
		keys_relation_type['remove_' + prefix] = {
			'title' : s('Allow nabar to remove from {relation_type} relation', {'relation_type' : relation_type})
		}
		keys_relation_type['cancel_request_' + prefix] = {
			'title' : s('Allow nabar to cancel {relation_type} relation request', {'relation_type' : relation_type})
		}

		# admin
		
		keys_entity_type['admin_' + prefix] = {
			'title' : s('(Administer) Allow nabar to do ANY ACTION on {relation_type} relation request', {'relation_type' : relation_type}),
			'flag' : 'danger',
		}
	
	return keys
