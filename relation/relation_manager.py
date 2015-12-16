
class RelationManager:
	'''instance per relation'''

	def __init__(self, from_entity_type, from_entity_id, to_entity_type, to_entity_id):
		
		self.from_entity_type = from_entity_type
		self.from_entity_id = from_entity_id
		self.to_entity_type = to_entity_type
		self.to_entity_id = to_entity_id
		
		entitier = IN.entitier
		
		self.from_entity = entitier.load_single(from_entity_type, from_entity_id)
		if not self.from_entity:
			raise In.entity.InvalidEntityException()
			
		self.to_entity  = entitier.load_single(to_entity_type, to_entity_id)
		if not self.to_entity:
			raise In.entity.InvalidEntityException()
		
		self.existing_relations = {}

		self.no_permission_message = s('Sorry! But you have no permission to do this action!')
		self.no_relation_message = s('Sorry! There is no relation exists!')
		self.relation_exists_message = s('Relation already exists!')
		self.request_already_sent_message = s('Request already sent!')


	def get_existing_relation(self, relation_type):
		if relation_type in self.existing_relations:
			return self.existing_relations[relation_type]
		
		relation_type_entity = relation_type
		
		existing_relation = None
		
		#if relation_type_entity.is_one_way():
			#where = [
				#['OR', [
					#['AND', [
						#['from_entity_type', self.from_entity_type],
						#['from_entity_id', self.from_entity_id],
						#['to_entity_type', self.to_entity_type],
						#['to_entity_id', self.to_entity_id],
					#]],
					#['AND', [
						#['from_entity_type', self.to_entity_type],
						#['from_entity_id', self.to_entity_id],
						#['to_entity_type', self.from_entity_type],
						#['to_entity_id', self.from_entity_id],
					#]],
				#],
				#['type', relation_type]
			#]
		#else:
		where = [
			['from_entity_type', self.from_entity_type],
			['from_entity_id', self.from_entity_id],
			['to_entity_type', self.to_entity_type],
			['to_entity_id', self.to_entity_id],
			['relation.type', relation_type]
		]
		
		cursor = IN.db.select({
			'table' : 'relation.relation_member',
			'join' : [
				['join', 'relation.relation', 'relation', [['relation_member.relation_id = relation.id']]],
			],
			'columns' : ['relation.id'],
			'where' : where,
		}).execute()
		
		if cursor.rowcount > 0:
			relation_id = cursor.fetchone()['id']
			
			existing_relation = IN.entitier.load_single('Relation', relation_id)
		
		self.existing_relations[relation_type] = existing_relation
		
		if existing_relation:
			return existing_relation
	
	def banned(self):
		# TODO: ban entity
		return False
	
