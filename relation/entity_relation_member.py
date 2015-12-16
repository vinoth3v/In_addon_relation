#import In.entity

class RelationMember(In.entity.Entity):
	'''RelationMember Entity class.
	'''

	def __init__(self, data = None, items = None, **args):

		# default
		self.relation_id = 0
		self.from_entity_type = ''
		self.from_entity_id = 0
		self.to_entity_type = ''
		self.to_entity_id = 0
		
		super().__init__(data, items, **args)

@IN.register('RelationMember', type = 'Entitier')
class RelationMemberEntitier(In.entity.EntityEntitier):
	'''Base RelationMember Entitier'''

	# RelationMember needs entity insert/update/delete hooks
	invoke_entity_hook = False

	# load all is very heavy
	entity_load_all = False
	
@IN.register('RelationMember', type = 'Model')
class RelationMemberModel(In.entity.EntityModel):
	'''RelationMember Model'''


@IN.hook
def entity_model():
	return {
		'RelationMember' : {						# entity name
			'table' : {				# table
				'name' : 'relation_member',
				'columns' : {		# table columns / entity attributes
					'id' : {},
					'type' : {},
					'created' : {},
					'status' : {},
					'nabar_id' : {},
					'relation_id' : {
						'type' : 'int', 'unsigned' : True, 'not null' : True, 
						'description' : 'RelationMember Id',
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

@IN.register('RelationMember', type = 'Themer')
class RelationMemberThemer(In.entity.EntityThemer):
	'''RelationMember themer'''

