@IN.register('RelationType', type = 'EntityAddForm')
class RelationTypeAddForm(In.entity.EntityAddForm):
	'''RelationType Form'''
	
	def __init__(self, data = None, items = None, post = None, **args):

		super().__init__(data, items, post, **args)
		
		# TODO: early validate: one flag type per flag bundle
		
		set = self.add('FieldSet', {
			'id' : 'configset',
			'css' : ['i-form-row'],
			'weight' : 0,
		})
		
		entity_type = args['entity_type']
		entity_bundle = args['entity_bundle']
		
		
		set = self.add('FieldSet', {
			'id' : 'actionset',
			'css' : ['i-form-row i-text-primary'],
			'weight' : 50, # last
		})
		
		set.add('Submit', {
			'id' : 'submit',
			'value' : s('Save'),
			'css' : ['i-button i-button-primary i-button-large']
		})

		self.css.append('ajax i-panel i-panel-box i-margin-large')

@IN.register('RelationTypeAddForm', type = 'Former')
class RelationTypeAddFormFormer(In.entity.EntityAddFormFormer):
	'''RelationType Form Former'''
	
	#def validate(self, form, post):
		#if form.has_errors:
			#return
		
	#def submit_partial(self, form, post):
		
		#super().submit_prepare(form, post)
		
		
	#def submit_prepare(self, form, post):
		
		#super().submit_prepare(form, post)
		
		#if form.has_errors:
			#return
		
		#entity_type = form.args['entity_type']
		
		#flag_type_entity = form.processed_data['entity']
		
	#def submit(self, form, post):
		
		#super().submit(form, post)
		
		#if form.has_errors:
			#return
		
		
