
def action_handler_relation_action_popup(context, action, relation_type, to_entity_type, to_entity_id, **args):
	
	try:
		
		form_args = {
			'to_entity_type' : to_entity_type,
			'to_entity_id' : to_entity_id,
			'relation_type' : relation_type,
			'from_entity_type' : 'Nabar',
			'from_entity_id' : context.nabar.id,
		}
		form = IN.former.load('RelationAction', args = form_args)
		
		if context.request.ajax_modal:
			
			element_id = 'i-ajax-modal'
			element_id = element_id + ' .modal-content'
			
			relation_type_entity = IN.relater.relation_type_entities[relation_type]
			
			modal = Object.new(type = "HTMLModalPopup", data = {
				'title' : s(relation_type_entity.name),
			})
			modal.add(form)
			
			output = {
				element_id : modal,
			}
			context.response = In.core.response.PartialResponse(output = output)
		else:
			context.response.output.add(form)
			
	except:
		IN.logger.debug()
