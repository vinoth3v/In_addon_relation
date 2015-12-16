#import In.entity

class Relation(In.entity.Entity):
	'''Relation Entity class.
	'''

	def __init__(self, data = None, items = None, **args):

		# default
		self.relation_status = 0
		self.parent_relation_id = 0
		self.top_relation_id = 0
		
		super().__init__(data, items, **args)

@IN.register('Relation', type = 'Entitier')
class RelationEntitier(In.entity.EntityEntitier):
	'''Base Relation Entitier'''

	# Relation needs entity insert/update/delete hooks
	invoke_entity_hook = True

	# load all is very heavy
	entity_load_all = False
	
@IN.register('Relation', type = 'Model')
class RelationModel(In.entity.EntityModel):
	'''Relation Model'''


@IN.hook
def entity_model():
	return {
		'Relation' : {						# entity name
			'table' : {				# table
				'name' : 'relation',
				'columns' : {		# table columns / entity attributes
					'id' : {},
					'type' : {},
					'created' : {},
					'status' : {},
					'nabar_id' : {},
					'relation_status': {
						'type' : 'int', 'unsigned' : True, 'not null' : True, 'default' : 0, 'size' : 'tiny'
					},
					'parent_relation_id' : {
						'type' : 'int', 'unsigned' : True, 'not null' : True, 'default' : 0, 
						'description' : 'Direct Parent relation Id',
					},
					'top_relation_id' : {
						'type' : 'int', 'unsigned' : True, 'not null' : True, 'default' : 0, 
						'description' : 'Top most Parent relation Id',
					},
				},
				'keys' : {
					'primary' : 'id',
				},
			},
		},
	}

@IN.register('Relation', type = 'Themer')
class RelationThemer(In.entity.EntityThemer):
	'''Relation themer'''
