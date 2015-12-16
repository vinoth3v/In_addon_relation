import json

class RelationActionListLazy(In.core.lazy.HTMLObjectLazy):
	'''list of comments'''

	def __init__(self, data = None, items = None, **args):

		super().__init__(data, items, **args)

		# always set new id
		self.id = 'RelationActionListLazy'
		
		context = IN.context
		if context.request.ajax_lazy:
			
			db = IN.db
			connection = db.connection

			nabar_id = context.nabar.id
			
			if not nabar_id:
				return
				
			query = IN.db.select({
				'table' : ['relation.relation', 'r'],
				'columns' : ['r.id', 'rr.from_entity_id', 'r.type'],
				'join' : [
					#['inner join', 'relation.relation_member', 'rm', [
					#	['r.id = rm.relation_id']
					#]],
					['inner join', 'relation.relation_request', 'rr', [
						['r.id = rr.relation_id']
					]]
				],
				'where' : [
					['r.relation_status', IN.relater.RELATION_STATUS_REQUESTED],
					['r.status', '>=', 1],
					['rr.to_entity_type', 'Nabar'],
					['rr.to_entity_id', nabar_id]
				],
				'order' : {'rr.created' : 'desc'}
			})
			
			cursor = query.execute()
			
			__form_load = IN.former.load
			
			if cursor.rowcount > 0:
				
				for row in cursor:
					
					from_entity_id = row['from_entity_id']
					
					form = __form_load('RelationActionDirect', args = {
						'from_entity_type' : 'Nabar',
						'from_entity_id' : nabar_id,	# viewer
						'to_entity_type' : 'Nabar',
						'to_entity_id' : from_entity_id,# page
						'relation_type' : row['type']	
					})
					
					self.add(form)
				
					#remaining = total - limit
					#if remaining > 0 and  last_id > 0:
						#self.add('TextDiv', {
							#'id' : '_'.join(('more-commens', parent_entity_type, str(parent_entity_id), str(self.parent_id))),
							#'value' : str(remaining) + ' more comments',
							#'css' : ['ajax i-text-center pointer i-panel-box i-panel-box-primary'],
							#'attributes' : {
								#'data-href' : ''.join(('/comment/more/!Content/', str(parent_entity_id), '/', str(last_id), '/', str(self.parent_id)))
							#},
							#'weight' : -1
						#})

		

@IN.register('RelationActionListLazy', type = 'Themer')
class RelationActionListLazyThemer(In.core.lazy.HTMLObjectLazyThemer):
	'''lazy themer'''

	def theme_attributes(self, obj, format, view_mode, args):
		
		obj.lazy_args['type'] = obj.__type__
		
		json_args = ''
		try:
			json_args = json.dumps(obj.lazy_args, skipkeys = True, ensure_ascii = False)
		except Exception as e:
			print(9999999999, obj.lazy_args, obj.__type__)
			raise e
			
		obj.attributes['data-args'] = json_args
		return super().theme_attributes(obj, format, view_mode, args)

