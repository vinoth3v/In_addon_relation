import os

@IN.hook
def asset_prepare(context):
	
	if context.nabar.id and not context.request.ajax:
		
		context.asset.add_js('''
			require(['In', 'In_ws', 'In_relation'], function(relation){
				//IN.trigger('dom', true);
			});
			''', 'relation.js', 'inline', weight = 11)
		
		#context.asset.add_css('/files/assets-relation/css/relation.css', 'relation.css', weight = 11)
		
@IN.hook
def public_file_paths():
	
	return {
		'assets-relation' : {
			'base_path' : os.path.join(IN.APP.app_path, 'addons/relation/assets'),
		}
	}

@IN.hook
def notification_count(context):
	
	try:
		nabar_id = context.nabar.id
		
		if not nabar_id:
			return
		
		count = IN.relater.get_relation_notification_count(nabar_id)
		
		return {
			'relation_count' : count
		}
	except Exception as e:
		IN.logger.debug()
		
