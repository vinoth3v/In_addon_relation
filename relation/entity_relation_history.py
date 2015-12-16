#import In.entity

class RelationHistory(In.entity.Entity):
	'''RelationHistory Entity class.
	'''

	def __init__(self, data = None, items = None, **args):

		# default
		self.relation_id = 0
		self.action = ''
		self.actor_entity_type = ''
		self.actor_entity_id = 0
		self.message = ''
		
		super().__init__(data, items, **args)

@IN.register('RelationHistory', type = 'Entitier')
class RelationHistoryEntitier(In.entity.EntityEntitier):
	'''Base RelationHistory Entitier'''

	# RelationHistory needs entity insert/update/delete hooks
	invoke_entity_hook = False

	# load all is very heavy
	entity_load_all = False
	
@IN.register('RelationHistory', type = 'Model')
class RelationHistoryModel(In.entity.EntityModel):
	'''RelationHistory Model'''


@IN.hook
def entity_model():
	return {
		'RelationHistory' : {						# entity name
			'table' : {				# table
				'name' : 'relation_history',
				'columns' : {		# table columns / entity attributes
					'id' : {},
					'type' : {},
					'created' : {},
					'status' : {},
					'nabar_id' : {},
					'relation_id' : {
						'type' : 'int', 'unsigned' : True, 'not null' : True, 
						'description' : 'RelationHistory Id',
					},
					'actor_entity_type' : {
						'type' : 'varchar', 'length' : 32, 'not null' : True,
					},
					'actor_entity_id' : {
						'type' : 'varchar', 'int' : 32, 'not null' : True, 'default' : 'nabar',
					},
					'message' : {
						'type' : 'varchar', 'length' : 32, 'not null' : True,
					},
				},
				'keys' : {
					'primary' : 'id',
				},
			},
		},
	}

@IN.register('RelationHistory', type = 'Themer')
class RelationHistoryThemer(In.entity.EntityThemer):
	'''RelationHistory themer'''

