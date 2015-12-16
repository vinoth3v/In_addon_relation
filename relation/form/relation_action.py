import relation

class RelationAction(Form):
	'''RelationType Form'''
	
	def __init__(self, data = None, items = None, post = None, **args):

		super().__init__(data, items, post, **args)
		
		
		to_entity_type = args['to_entity_type']
		to_entity_id = args['to_entity_id']
		relation_type = args['relation_type']
		from_entity_type = args['from_entity_type']
		from_entity_id = args['from_entity_id']
		
		self.manager = relation.get_relation_manager(from_entity_type, from_entity_id, to_entity_type, to_entity_id)
		
		if relation_type != IN.relater.RELATION_TYPE_BAN and self.manager.banned():
			return
		
		if relation_type not in IN.relater.relation_type_entities:
			return
		
		set = self.add('TextDiv', {
			'id' : 'nabarset',
			'css' : ['i-grid i-grid-divider '], #  i-container-center i-text-center
		})
		
		from_entity =  self.manager.from_entity
		to_entity =  self.manager.to_entity
		
		set.add('TextDiv', {
			'value' : IN.themer.theme(from_entity, view_mode = 'teaser'),
			'css' : ['i-width-1-3 '],
		})
		
		set.add('TextDiv', {
			'value' : IN.themer.theme(to_entity, view_mode = 'teaser'),
			'css' : ['i-width-1-3 '],
		})
		
		set = self.add('FieldSet', {
			'id' : 'actionset',
			'css' : ['i-modal-footer i-text-right'],
			'weight' : 50, # last
		})
		
		relation_type_entity = IN.relater.relation_type_entities[relation_type]
		texts = relation_type_entity.data.get('text', {})
		
		existing_relation = self.manager.get_existing_relation(relation_type)
		
		if existing_relation:
			
			if existing_relation.relation_status == IN.relater.RELATION_STATUS_ACTIVE:
				
				set.add('Submit', {
					'id' : 'remove_relation',
					'value' : s(texts.get('remove_text', 'remove from ' + relation_type_entity.name)),
					'css' : ['i-button i-button-danger'],
					'attributes' : {
						'data-ajax_partial' : 1,
					},
				})

			elif existing_relation.relation_status == IN.relater.RELATION_STATUS_REQUESTED:
				
				# requested
				request = IN.relater.get_request(relation_type, from_entity_type, from_entity_id, to_entity_type, to_entity_id)
				if request and request.from_entity_type == from_entity_type and request.from_entity_id == from_entity_id:
					
					set.add('Submit', {
						'id' : 'cancel_relation_request',
						'value' : s(texts.get('cancel_request_text', 'Cancel ' + relation_type_entity.name + ' request')),
						'css' : ['i-button i-button-danger'],
						'attributes' : {
							'data-ajax_partial' : 1,
						},
					})
					
				else:
					
					set.add('Submit', {
						'id' : 'accept_relation_request',
						'value' : s(texts.get('accept_text', 'Accept as ' + relation_type_entity.name)),
						'css' : ['i-button i-button-primary'],
						'attributes' : {
							'data-ajax_partial' : 1,
						},
					})
					
					set.add('Submit', {
						'id' : 'reject_relation_request',
						'value' : s(texts.get('reject_request_text', 'Reject ' + relation_type_entity.name + ' request')),
						'css' : ['i-button i-button-danger'],
						'attributes' : {
							'data-ajax_partial' : 1,
						},
					})
			
				
		if not existing_relation or existing_relation.relation_status == IN.relater.RELATION_STATUS_INACTIVE:
			
			# TODO: check maximum number of requests
			
			set.add('Submit', {
				'id' : 'add_relation',
				'value' : s(texts.get('add_text', 'Add as ' + relation_type_entity.name)),
				'css' : ['i-button i-button-primary'],
				'attributes' : {
					'data-ajax_partial' : 1,
				},
			})

		if IN.context.request.ajax:
			set.add('Link', {
				'name' : 'cancel',
				'value' : s('Cancel'),
				'css' : ['i-button i-modal-close']
			})
		else:
			set.add('Link', {
				'name' : 'cancel',
				'value' : s('Cancel'),
				'css' : ['i-button'],
				'href' : '/nabar/' + str(to_entity_id)
			})
			
		self.css.append('i-panel')

@IN.register('RelationAction', type = 'Former')
class RelationActionFormer(FormFormer):
	'''RelationType Form Former'''
	
	#def validate(self, form, post):
		#if form.has_errors:
			#return
		
	def submit_partial(self, form, post):
		
		super().submit_partial(form, post)
		
		if 'element_id' not in post:
			return
		
		if form.has_errors:
			return
		
		args = form.args
		
		to_entity_type = args['to_entity_type']
		to_entity_id = args['to_entity_id']
		relation_type = args['relation_type']
		from_entity_type = args['from_entity_type']
		from_entity_id = args['from_entity_id']
		
		relation_type_entity = IN.relater.relation_type_entities[relation_type]
		
		element_id = post['element_id']
		
		relater = IN.relater
		
		if element_id == 'add_relation':
			
			# if approval_needed, create request
			if relation_type_entity.approval_needed:
				
				result = relater.add_relation_request(relation_type, from_entity_type, from_entity_id, to_entity_type, to_entity_id)
				
				if result:
					form.result_commands = [{
						'method' : 'closeAjaxModal',
						'args' : [],
					}]
					
					form.result_commands.append({
						'method' : 'notify',
						'args' : [{
							'message' : s('{type} request sent!', {'type' :  relation_type_entity.name}),
							'status'  : 'info',
							'timeout' : 5000,
							'pos'     : 'bottom-left'			
						}]
					})
			
			else:
				# no approval needed, create relation
				result = relater.add_relation(relation_type, from_entity_type, from_entity_id, to_entity_type, to_entity_id)
				
				if result:
					form.result_commands = [{
						'method' : 'closeAjaxModal',
						'args' : [],
					}]
					
					form.result_commands.append({
						'method' : 'notify',
						'args' : [{
							'message' : s('Relation {type} added!', {'type' :  relation_type_entity.name}),
							'status'  : 'info',
							'timeout' : 5000,
							'pos'     : 'bottom-left'			
						}]
					})
			
		elif element_id == 'accept_relation_request':
			
			if from_entity_id == IN.context.nabar.id:
				# if current user accepting, request is by to_entity
				result = relater.accept_relation_request(relation_type, to_entity_type, to_entity_id, from_entity_type, from_entity_id)
			else:
				result = relater.accept_relation_request(relation_type, from_entity_type, from_entity_id, to_entity_type, to_entity_id)
			
			if result:
				form.result_commands = [{
					'method' : 'closeAjaxModal',
					'args' : [],
				}]
				
				form.result_commands.append({
					'method' : 'notify',
					'args' : [{
						'message' : s('{type} relation created!', {'type' :  relation_type_entity.name}),
						'status'  : 'info',
						'timeout' : 5000,
						'pos'     : 'bottom-left'			
					}]
				})
			
		elif element_id == 'reject_relation_request':
			
			if from_entity_id == IN.context.nabar.id:
				# if current user accepting, request is by to_entity
				result = relater.reject_relation_request(relation_type, to_entity_type, to_entity_id, from_entity_type, from_entity_id)
			else:
				result = relater.reject_relation_request(relation_type, from_entity_type, from_entity_id, to_entity_type, to_entity_id)
			if result:
				form.result_commands = [{
					'method' : 'closeAjaxModal',
					'args' : [],
				}]
				
				form.result_commands.append({
					'method' : 'notify',
					'args' : [{
						'message' : s('{type} request rejected!', {'type' :  relation_type_entity.name}),
						'status'  : 'info',
						'timeout' : 5000,
						'pos'     : 'bottom-left'			
					}]
				})
		
		elif element_id == 'cancel_relation_request':
			'''cancel the request made by from entity'''
			
			result = relater.cancel_relation_request(relation_type, from_entity_type, from_entity_id, to_entity_type, to_entity_id)
			if result:
				form.result_commands = [{
					'method' : 'closeAjaxModal',
					'args' : [],
				}]
				
				form.result_commands.append({
					'method' : 'notify',
					'args' : [{
						'message' : s('{type} request cancelled!', {'type' :  relation_type_entity.name}),
						'status'  : 'info',
						'timeout' : 5000,
						'pos'     : 'bottom-left'			
					}]
				})
			
		elif element_id == 'remove_relation':
			
			result = relater.remove_relation(relation_type, from_entity_type, from_entity_id, to_entity_type, to_entity_id)
			
			if result:
				form.result_commands = [{
					'method' : 'closeAjaxModal',
					'args' : [],
				}]
				
				form.result_commands.append({
					'method' : 'notify',
					'args' : [{
						'message' : s('{type} relation removed!', {'type' :  relation_type_entity.name}),
						'status'  : 'info',
						'timeout' : 5000,
						'pos'     : 'bottom-left'			
					}]
				})
			
		
