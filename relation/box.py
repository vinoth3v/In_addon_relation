from In.boxer.box import Box, BoxThemer

class BoxRelationActionList(Box):
	''''''
	title = s('Requests')

@IN.register('BoxRelationActionList', type = 'Themer')
class BoxRelationActionListThemer(BoxThemer):


	def theme_items(self, obj, format, view_mode, args):
		
		obj.css.append('i-overflow-container')
		
		data = {
			'lazy_args' : {
				'load_args' : {
					'data' : {
					},
				}
			},
		}
		
		obj.add('RelationActionListLazy', data)
		
		super().theme_items(obj, format, view_mode, args)
