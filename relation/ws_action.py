@IN.hook
def ws_action_relation_notification_count(context, message):
	
	try:
		
		nabar_id = context.nabar.id
		
		if not nabar_id:
			return
		
		count = IN.relater.get_relation_notification_count(nabar_id)
				
		context.send({
			'ws_command' : 'relation_notification_count',
			'count' : count
		})
		
	except Exception as e:
		IN.logger.debug()
