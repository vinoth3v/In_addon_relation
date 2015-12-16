#import In.entity

class RelationRequest(In.entity.Entity):
	'''RelationRequest Entity class.
	'''

	def __init__(self, data = None, items = None, **args):

		# default
		self.relation_id = 0
		self.from_entity_type = ''
		self.from_entity_id = 0
		self.to_entity_type = ''
		self.to_entity_id = 0
		
		super().__init__(data, items, **args)

@IN.register('RelationRequest', type = 'Entitier')
class RelationRequestEntitier(In.entity.EntityEntitier):
	'''Base RelationRequest Entitier'''

	# RelationRequest needs entity insert/update/delete hooks
	invoke_entity_hook = False

	# load all is very heavy
	entity_load_all = False
	
@IN.register('RelationRequest', type = 'Model')
class RelationRequestModel(In.entity.EntityModel):
	'''RelationRequest Model'''


@IN.hook
def entity_model():
	return {
		'RelationRequest' : {						# entity name
			'table' : {				# table
				'name' : 'relation_request',
				'columns' : {		# table columns / entity attributes
					'id' : {},
					'type' : {},
					'created' : {},
					'status' : {},
					'nabar_id' : {},
					'relation_id' : {
						'type' : 'int', 'unsigned' : True, 'not null' : True, 
						'description' : 'RelationRequest Id',
					},
					'from_entity_type' : {
						'type' : 'varchar', 'length' : 32, 'not null' : True, 'default' : 'nabar', 
						'description' : 'Entity type. eg: nabar',
					},
					'from_entity_id' : {
						'type' : 'int', 'unsigned' : True, 'not null' : True, 'default' : 0
					},
					'to_entity_type' : {
						'type' : 'varchar', 'length' : 32, 'not null' : True, 'default' : 'nabar', 
						'description' : 'Entity type. eg: nabar', 
					},
					'to_entity_id' : {
						'type' : 'int', 'unsigned' : True, 'not null' : True, 'default' : 0
					},
				},
				'keys' : {
					'primary' : 'id',
				},
			},
		},
	}

@IN.register('RelationRequest', type = 'Themer')
class RelationRequestThemer(In.entity.EntityThemer):
	'''RelationRequest themer'''
