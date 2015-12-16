import relation

class RelationLink(HTMLObjectLazy):
	''''''	
	
	from_entity_type = 'Nabar'
	from_entity_id = 0
	to_entity_type = 'Nabar'
	to_entity_id = 0
	relation_type = ''
	
	_manager = None
	
	def __init__(self, data = None, items = None, **args):
		super().__init__(data, items, **args)
		
	@property
	def manager(self):
		if self._manager is None:
			self._manager = relation.get_relation_manager(self.from_entity_type, self.from_entity_id, self.to_entity_type, self.to_entity_id)
		return self._manager
		
@IN.register('RelationLink', type = 'Themer')
class RelationLinkThemer(HTMLObjectLazyThemer):
	''''''
	
	def theme_items(self, obj, format, view_mode, args):
		
		if view_mode != 'lazy':
		
			# return if has active ban
			if obj.relation_type != IN.relater.RELATION_TYPE_BAN and obj.manager.banned():
				return
			
			if obj.relation_type not in IN.relater.relation_type_entities:
				return
			
			relation_type_entity = IN.relater.relation_type_entities[obj.relation_type]
			text = ''
			
			existing_relation = obj.manager.get_existing_relation(obj.relation_type)
			
			texts = relation_type_entity.data.get('text', {})
			
			if existing_relation:
				
				if existing_relation.relation_status == IN.relater.RELATION_STATUS_ACTIVE:
					#text = s(texts.get('cancel_text', 'Cancel'))
					# TODO: different name for one way relationship
					text = '<i class="i-icon-check-circle"></i> ' + s(relation_type_entity.name)
				elif existing_relation.relation_status == IN.relater.RELATION_STATUS_INACTIVE:
					
					text = s(texts.get('add_text', 'Add'))
					
				elif existing_relation.relation_status == IN.relater.RELATION_STATUS_REQUESTED:
					
					# requested
					request = IN.relater.get_request(obj.relation_type, obj.from_entity_type, obj.from_entity_id, obj.to_entity_type, obj.to_entity_id)
					
					if request and request.from_entity_type == obj.from_entity_type and int(request.from_entity_id) == int(obj.from_entity_id):
						text = s(texts.get('cancel_request_text', 'Cancel request'))
					else:
						text = s(texts.get('accept_text', 'Accept'))
			
			# defaul to add text
			if text == '':
				text = s(texts.get('add_text', 'Add'))
			
			obj.add('Link', {
				'value' : text,
				'href' : ''.join(('/relation/action/!' + obj.relation_type + '/!' + obj.to_entity_type, '/' + str(obj.to_entity_id))),
				'css' : [
					'ajax-modal no-ajax', 
					obj.relation_type + '-link',
					'i-button i-button-primary'
				]
			})
			
			super().theme_items(obj, format, view_mode, args)
