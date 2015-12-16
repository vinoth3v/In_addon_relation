import relation

class RelationType(In.entity.Entity):
	'''RelationType Entity class.
	'''

	# controls whether this relation needs approval from other end
	approval_needed = True
	
	# one way or two way relation. eg: parent -> son, manager -> employee.
	# 1: oneway (teacher) 
	# 2: twoway (friend) 
	# 3: separate twoway (follow)
	
	flow = 2 # IN.relater.RELATION_FLOW_TWO_WAY # not available
	
	# reversed relation type id if this is oneway. 
	# teacher relation will create/request student relation.
	#reverse_type_id = 0
	
	# controls whether reverse relation can be created automatically.
	#reverse_auto_create = False
	
	# controls whether reverse relation needed approval.
	#reverse_approval_needed = True
	
	# controls whether system should ask before create/request.
	ask_on_confirm = False
	
	# maximum no. times a entity can request for this relation to a single entity.
	max_requests_to_entity = 1
	
	# maximum no. of pending reuests a entity allowed on this relation type
	max_pending_requests = 50
	
	# maximum no. of relations a entity can have on this relation type.
	# 0 : unlimitted
	#max_relations = 0
	
	# moved to data
	#add_text = 'Add'
	#remove_text = 'Remove'
	#cancel_text = 'Cancel'
	#accept_text = "Accept"
	#reject_text = 'Reject'
	
	#add_text_confirm = ''
	#remove_text_confirm = ''
	#cancel_text_confirm = ''
	#accept_text_confirm = ''
	#reject_text_confirm = ''
	
	data = {}
		
	def __init__(self, data = None, items = None, **args):

		
		super().__init__(data, items, **args)



@IN.register('RelationType', type = 'Entitier')
class RelationTypeEntitier(In.entity.EntityEntitier):
	'''Base RelationType Entitier'''

	# RelationType needs entity insert/update/delete hooks
	invoke_entity_hook = True

	# load all is very heavy
	entity_load_all = True
	
@IN.register('RelationType', type = 'Model')
class RelationTypeModel(In.entity.EntityModel):
	'''RelationType Model'''


@IN.hook
def entity_model():
	return {
		'RelationType' : {						# entity name
			'table' : {				# table
				'name' : 'relation_type',
				'columns' : {		# table columns / entity attributes
					'id' : {},
					'type' : {},
					'created' : {},
					'status' : {},
					'nabar_id' : {},
					'name' : {
						'type' : 'varchar', 'length' : 64, 'not null' : True,  'info' : 'human readable relation name. e.g Friend, Follow', 
					},
					'info' : {
						'type' : 'varchar', 'length' : 255, 'not null' : True,  'info' : 'relation type info.', 
					},
					'approval_needed' : {
						'type' : 'int', 'not null' : True, 'default' : 1, 'size' : 'smallint', 'info' : 'controls whether this relation needs approval from other end.', 
					},
					'flow' : {
						'type' : 'int',
						'not null' : True,
						'default' : 1, # 1: oneway (teacher}, 2: twoway (friend}, 3: separate twoway (follow)
						'size' : 'smallint',
						'info' : 'one way or two way relation. eg: parent -> son, manager -> employee.',
					},
					'ask_on_confirm' : {
						'type' : 'int',
						'not null' : True,
						'default' : 0,
						'size' : 'smallint',
						'info' : 'controls whether system should ask before create/request.',
					},
					'max_requests_to_entity' : {
						'type' : 'int', 'not null' : True, 'default' : 2, 'size' : 'smallint', 
						'info' : 'maximum no. times a entity can request for this relation to a single entity.', 
					},
					'max_pending_requests' : {
						'type' : 'int', 'not null' : True, 'default' : 2, 'size' : 'smallint', 
						'info' : 'maximum no. of pending reuests a entity allowed on this relation type', 
					},
					'max_relations' : {
						'type' : 'int', 'not null' : True, 'default' : 2, 'size' : 'smallint', 
						'info' : 'maximum no. of relations a entity can have on this relation type.', 
					},
					'data' : {
						'type' : 'json', 'not null' : True, 
						'info' : 'other data', 
					},
				},
				'keys' : {
					'primary' : 'id',
				},
			},
		},
	}

@IN.register('RelationType', type = 'Themer')
class RelationTypeThemer(In.entity.EntityThemer):
	'''RelationType themer'''
