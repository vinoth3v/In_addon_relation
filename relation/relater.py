import relation

class Relater:
	''''''
	
	# 1: oneway (teacher) 		
	RELATION_FLOW_ONE_WAY = 1 

	# 2: twoway (friend) 
	RELATION_FLOW_TWO_WAY = 2

	# 3: separate twoway (follow)
	RELATION_FLOW_TWO_WAY_SEPARATE = 3

	''' relation status '''

	RELATION_STATUS_INACTIVE = 0

	RELATION_STATUS_REQUESTED = 1

	RELATION_STATUS_ACTIVE = 2

	RELATION_STATUS_REJECTED = 3

	RELATION_TYPE_BAN = 'ban'

	relation_type_entities = {}
	
	def __init__(self):
		
		self.relation_type_entities = {}
		
		relation_types = IN.entitier.load_all('RelationType')
		if relation_types:
			for id, entity in relation_types.items():
				self.relation_type_entities[entity.type] = entity
	
	def get_relation_manager(self, from_entity_type, from_entity_id, to_entity_type, to_entity_id):
	
		manager = relation.RelationManager(from_entity_type, from_entity_id, to_entity_type, to_entity_id)
		
		return manager
	
	def hasActiveRelationBetween(self, relation_type, from_entity_type, from_entity_id, to_entity_type, to_entity_id):
		''''''
		
		try:
			
			relation_type_entity = self.relation_type_entities[relation_type]
			
			if not relation_type_entity:
				return False
			
			manager = self.get_relation_manager(from_entity_type, from_entity_id, to_entity_type, to_entity_id)
			
			relation_entity = manager.get_existing_relation(relation_type)
			
			if not relation_entity:
				return False
			
			if relation_entity.relation_status == self.RELATION_STATUS_ACTIVE:
				return True
			
		except Exception as e:
			IN.logger.debug()
		
		return False
	
	def add_relation_request(self, relation_type, from_entity_type, from_entity_id, to_entity_type, to_entity_id):
		''''''
		try:
			# TODO: add commit support
			
			
			relation_type_entity = self.relation_type_entities[relation_type]
			
			if not relation_type_entity:
				return False
				
			manager = self.get_relation_manager(from_entity_type, from_entity_id, to_entity_type, to_entity_id)
			
			relation_entity = manager.get_existing_relation(relation_type)
			
			if relation_entity:
				# change status to requested
				relation_entity.relation_status = self.RELATION_STATUS_REQUESTED
				relation_entity.save()
			else:
				
				# create relation if not exists
				relation_entity = Entity.new('Relation', {
					'nabar_id' : from_entity_id,
					'status' :  1,
					'relation_status' : self.RELATION_STATUS_REQUESTED,
					'type' : relation_type,
					'parent_relation_id' : 0,
					'top_relation_id' : 0
				})
			
				relation_entity.save()
				
				# create relation member
				Entity.new('RelationMember', {
					'relation_id' : relation_entity.id,
					'nabar_id' : from_entity_id,
					'status' :  1,
					'type' : 'member',
					'from_entity_type' : from_entity_type,
					'from_entity_id' : from_entity_id,
					'to_entity_type' : to_entity_type,
					'to_entity_id' : to_entity_id,
				}).save()
			
				# create reverse relation member if two way relation
				if relation_type_entity.flow == self.RELATION_FLOW_TWO_WAY:
					Entity.new('RelationMember', {
						'relation_id' : relation_entity.id,
						'nabar_id' : from_entity_id,
						'status' :  1,
						'type' : 'member',
						'from_entity_type' : to_entity_type,
						'from_entity_id' : to_entity_id,
						'to_entity_type' : from_entity_type,
						'to_entity_id' : from_entity_id,
					}).save()
				
			# create request
			request = Entity.new('RelationRequest', {
				'relation_id' : relation_entity.id,
				'nabar_id' : from_entity_id,
				'status' :  1,
				'type' : relation_type,
				'from_entity_type' : from_entity_type,
				'from_entity_id' : from_entity_id,
				'to_entity_type' : to_entity_type,
				'to_entity_id' : to_entity_id,
			})
			
			request.save()
			
			
			# create relation history
			Entity.new('RelationHistory', {
				'relation_id' : relation_entity.id,
				'type' : 'relation_request',
				'nabar_id' : from_entity_id,
				'status' :  1,
				'actor_entity_type' : from_entity_type,
				'actor_entity_id' : from_entity_id,
				'message' : ''
			}).save()
			
			
			args = {
				'from_entity_type' : from_entity_type,
				'from_entity_id' : from_entity_id,
				'to_entity_type' : to_entity_type,
				'to_entity_id' : to_entity_id,
				'manager' : manager,
				'relation_type_entity' : relation_type_entity, 
				'relation_entity' : relation_entity,
				'request' : request,
			}
			
			IN.hook_invoke('__relation_add_relation_request__', args)
			
			IN.hook_invoke('_'.join(('relation', relation_type, 'add_relation_request')), args)
			
			
			return True
		except Exception as e:
			IN.logger.debug()
			return False
		
	def add_relation(self, relation_type, from_entity_type, from_entity_id, to_entity_type, to_entity_id):
		''''''
		# TODO: add relation
		
		relation_type_entity = self.relation_type_entities[relation_type]
		
		if not relation_type_entity.approval_needed:
			pass
		return True
		
	def remove_relation(self, relation_type, from_entity_type, from_entity_id, to_entity_type, to_entity_id):
		'''remove from relation'''
		
		relation_type_entity = self.relation_type_entities[relation_type]
				
		manager = self.get_relation_manager(from_entity_type, from_entity_id, to_entity_type, to_entity_id)
		
		relation_entity = manager.get_existing_relation(relation_type)
		
		if relation_entity:
			# deactivate
			relation_entity.relation_status = self.RELATION_STATUS_INACTIVE
			relation_entity.save()
			
			args = {
				'from_entity_type' : from_entity_type,
				'from_entity_id' : from_entity_id,
				'to_entity_type' : to_entity_type,
				'to_entity_id' : to_entity_id,
				'manager' : manager,
				'relation_type_entity' : relation_type_entity, 
				'relation_entity' : relation_entity,
			}
			
			IN.hook_invoke('__relation_remove_relation__', args)
			
			IN.hook_invoke('_'.join(('relation', relation_type, 'remove_relation')), args)
			
			
		return True
		
	def reject_relation_request(self, relation_type, from_entity_type, from_entity_id, to_entity_type, to_entity_id):
		''''''
		try:
			
			request = self.get_request(relation_type, from_entity_type, from_entity_id, to_entity_type, to_entity_id)
			if not request:
				
				return False
			else:
				
				relation_type_entity = self.relation_type_entities[relation_type]
				
				manager = self.get_relation_manager(from_entity_type, from_entity_id, to_entity_type, to_entity_id)
				
				relation_entity = manager.get_existing_relation(relation_type)
				
				if relation_entity:
					# deactivate
					relation_entity.relation_status = self.RELATION_STATUS_INACTIVE
					relation_entity.save()
					
				# delete request
				request.delete()
				
				args = {
					'from_entity_type' : from_entity_type,
					'from_entity_id' : from_entity_id,
					'to_entity_type' : to_entity_type,
					'to_entity_id' : to_entity_id,
					'manager' : manager,
					'relation_type_entity' : relation_type_entity, 
					'relation_entity' : relation_entity,
					'request' : request,
				}
				
				IN.hook_invoke('__relation_reject_relation_request__', args)
				
				IN.hook_invoke('_'.join(('relation', relation_type, 'reject_relation_request')), args)
				
			return True
		except Exception as e:
			IN.logger.debug()			
			return
		
	def accept_relation_request(self, relation_type, from_entity_type, from_entity_id, to_entity_type, to_entity_id):
		''''''
		try:
			
			request = self.get_request(relation_type, from_entity_type, from_entity_id, to_entity_type, to_entity_id)
			if not request:
				return False
			else:
				
				relation_type_entity = self.relation_type_entities[relation_type]
				
				manager = self.get_relation_manager(from_entity_type, from_entity_id, to_entity_type, to_entity_id)
				
				relation_entity = manager.get_existing_relation(relation_type)
				
				if relation_entity:
					# deactivate
					relation_entity.relation_status = self.RELATION_STATUS_ACTIVE
					relation_entity.save()
				
				# delete request
				request.delete()
				
				args = {
					'from_entity_type' : from_entity_type,
					'from_entity_id' : from_entity_id,
					'to_entity_type' : to_entity_type,
					'to_entity_id' : to_entity_id,
					'manager' : manager,
					'relation_type_entity' : relation_type_entity, 
					'relation_entity' : relation_entity,
					'request' : request,
				}
				
				IN.hook_invoke('__relation_accept_relation_request__', args)
				
				IN.hook_invoke('_'.join(('relation', relation_type, 'accept_relation_request')), args)
				
			return True
		except Exception as e:
			IN.logger.debug()
			return
		
		
	def cancel_relation_request(self, relation_type, from_entity_type, from_entity_id, to_entity_type, to_entity_id):
		'''cancel the request made by from entity'''
		
		try:
			request = self.get_request(relation_type, from_entity_type, from_entity_id, to_entity_type, to_entity_id)
			if not request:				
				return False
			else:
				relation_type_entity = self.relation_type_entities[relation_type]
				
				manager = self.get_relation_manager(from_entity_type, from_entity_id, to_entity_type, to_entity_id)
				
				relation_entity = manager.get_existing_relation(relation_type)
				
				if relation_entity:
					# deactivate
					relation_entity.relation_status = self.RELATION_STATUS_INACTIVE
					relation_entity.save()
					
				# delete request
				request.delete()
			
			args = {
				'from_entity_type' : from_entity_type,
				'from_entity_id' : from_entity_id,
				'to_entity_type' : to_entity_type,
				'to_entity_id' : to_entity_id,
				'manager' : manager,
				'relation_type_entity' : relation_type_entity, 
				'relation_entity' : relation_entity,
				'request' : request,
			}
			
			IN.hook_invoke('__relation_cancel_relation_request__', args)
			
			IN.hook_invoke('_'.join(('relation', relation_type, 'cancel_relation_request')), args)
			

			return True
		except Exception as e:
			IN.logger.debug()
			return
		
	def get_request(self, relation_type, from_entity_type, from_entity_id, to_entity_type, to_entity_id):
		
		try:
			
			requests = IN.entitier.select('RelationRequest', [
				['type', relation_type],
				['from_entity_type', from_entity_type],
				['from_entity_id', from_entity_id],
				['to_entity_type', to_entity_type],
				['to_entity_id', to_entity_id],
			])
			
			if requests:
				return next(iter(requests.values()))
			
		except Exception as e:
			IN.logger.debug()
			return
	
	def get_relation_notification_count(self, nabar_id):
		
		try:
			
			cursor = IN.db.select({
				'table' : ['relation.relation', 'r'],
				'columns' : ['r.id', 'rr.from_entity_id', 'r.type'],
				'join' : [
					['inner join', 'relation.relation_request', 'rr', [
						['r.id = rr.relation_id']
					]]
				],
				'where' : [
					['r.relation_status', self.RELATION_STATUS_REQUESTED],
					['r.status', '>=', 1],
					['rr.to_entity_type', 'Nabar'],
					['rr.to_entity_id', nabar_id]
				]
			}).execute_count()
			
			if cursor.rowcount == 0:
				return 0
			
			return cursor.fetchone()[0]
			
		except Exception as e:
			IN.logger.debug()
	
		return 0
