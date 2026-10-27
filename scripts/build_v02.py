import json,copy,pathlib
from jsonschema import Draft202012Validator
ROOT=pathlib.Path(__file__).resolve().parents[1]
P=ROOT/'data'
v1=json.loads((P/'v0.1.json').read_text())

SOURCES=copy.deepcopy(v1['sources'])
SOURCES.update({
 'P-V': {'title':'Plotinus, Enneads V.3 (self-knowing intellect and self-awareness), MacKenna translation','url':'https://www.ccel.org/ccel/plotinus/enneads.v.iii.html'},
 'P-IV': {'title':'Plotinus, Enneads V.4 (contemplative experience)','url':'https://www.ccel.org/ccel/plotinus/enneads.v.iv.html'},
 'D-T': {'title':'Dennett Tower of Generate-and-Test, summarized in peer-reviewed discussion','url':'https://pmc.ncbi.nlm.nih.gov/articles/PMC8666905/'},
 'D-P': {'title':'Dennett, Conditions of Personhood (1976) as discussed in Cambridge journal article','url':'https://www.cambridge.org/core/journals/social-philosophy-and-policy/article/abs/connected-selfownership-and-our-obligations-to-others/3396A63EB50E94D89BC97091EAF9106E'},
 'D-O': {'title':'Dennett, Conditions of Personhood (original essay scan)','url':'https://philarchive.org/archive/DENCOP'},
 'B-S': {'title':'Alice Bailey, Esoteric Psychology I, question 1 (soul/personality distinctions)','url':'https://www.lucistrust.org/online_books/esoteric_psychology_volume_i/section_one_chapter_ii_certain_questions_and_their_answers/question_1_what_is_the_soul_can_we_define_it_what_is_its_nature_part2'},
 'B-T': {'title':'Lucis Trust, The Science of the Seven Rays, discussion of Bailey','url':'https://www.lucistrust.org/arcane_school/talks_and_articles/the_science_the_seven_rays'},
 'SEP-F': {'title':'Stanford Encyclopedia of Philosophy, Free Will','url':'https://plato.stanford.edu/entries/freewill/'},
 'SEP-M': {'title':'Stanford Encyclopedia of Philosophy, Moral Responsibility','url':'https://plato.stanford.edu/entries/moral-responsibility/'},
 'SEP-C': {'title':'Stanford Encyclopedia of Philosophy, Consciousness','url':'https://plato.stanford.edu/entries/consciousness/'}
})

# The typed *grammatical* signatures are neither claims about what actually exists nor philosophical stipulations.
# A symbol merely denotes something a tradition, example, or narrator talks about.
SORTS=['entity','episode','action','content','option','capacity','quality','norm','principle','world','collection','system','process','state','quantity']
SIG={
 'is_a':{'subject':'entity','kind':'quality'},
 'has_quality':{'bearer':'entity','quality':'quality'},
 'undergoes':{'subject':'entity','episode':'episode'},
 'experiences':{'subject':'entity','episode':'episode'},
 'aware_of':{'subject':'entity','target':'any'},
 'has_content':{'episode':'episode','content':'content'},
 'attends_to':{'subject':'entity','target':'any'},
 'available_for_use':{'content':'content','subject':'entity'},
 'represents':{'representation':'content','target':'any'},
 'evaluates':{'subject':'entity','option':'option'},
 'selects':{'subject':'entity','option':'option'},
 'performs':{'subject':'entity','action':'action'},
 'realizes_option':{'action':'action','option':'option'},
 'causes':{'source':'any','outcome':'any'},
 'agent_causes':{'agent':'entity','action':'action'},
 'precedes':{'before':'any','after':'any'},
 'cooccurs':{'left':'any','right':'any'},
 'has_capacity':{'subject':'entity','capacity':'capacity'},
 'offers_reason':{'content':'content','option':'option'},
 'responds_to_reason':{'subject':'entity','reason':'content'},
 'uses_tool':{'subject':'entity','tool':'entity'},
 'learns_by':{'subject':'entity','process':'process'},
 'envisages':{'subject':'entity','option':'option'},
 'governs':{'norm':'norm','action':'action'},
 'answerable_to':{'subject':'entity','norm':'norm'},
 'morally_responsible':{'subject':'entity','action':'action'},
 'attributes':{'observer':'entity','target':'entity','property':'quality'},
 'supports':{'support':'any','dependent':'any'},
 'part_of':{'part':'entity','whole':'entity'},
 'grounds':{'ground':'entity','dependent':'entity'},
 'transfers':{'origin':'entity','destination':'entity','carrier':'entity'},
 'mediates':{'source':'entity','mediator':'entity','recipient':'entity'},
 'differentiates':{'source':'entity','outputs':'list:entity'},
 'ranks':{'members':'list:entity'},
 'groups':{'whole':'collection','members':'list:entity'},
 'qualifies':{'influence':'entity','bearer':'entity','quality':'quality'},
 'transitions':{'subject':'entity','from':'state','to':'state'},
 'orients_to':{'subject':'entity','target':'entity'},
 'has_mode':{'subject':'entity','mode':'quality'},
}

def A(predicate,**roles): return {'op':'atom','predicate':predicate,'roles':roles}
def AND(*items): return {'op':'and','items':list(items)}
def NEG(item):return {'op':'not','item':item}
def MOD(domain,mode,item,agent=None,background=None):
 r={'op':'modal','domain':domain,'mode':mode,'item':item}
 if agent:r['agent']=agent
 if background:r['background']=background
 return r

def EX(entity):return {'op':'exists','entity':entity}
def IMPL(a,b):return {'op':'implies','antecedent':a,'consequent':b}

def record(id,tradition,text,scope,symbols,expression,sources,locator,note='',kind='source_paraphrase'):
 return {'id':id,'tradition':tradition,'statement':text,'scope':scope,'symbols':symbols,'expression':expression,'evidence':{'kind':kind,'sources':sources,'locator':locator},'visual_guard':note}

claims=[]
# Migrate 12 legacy examples into one uniform formula shape. Literal parameters (numbers, axes, from/to states)
# remain parameters; identity-referents become typed symbols. No reinterpretation is implied by the migration.

def converted(c):
 symbols={}
 exprs=[]
 for p in c['operators']:
  op=p['op']; q={k:v for k,v in p.items() if k!='op'}
  if op=='rank':
   items=[str(x) for x in q['members']]
   symbols.update({x:'entity' for x in items})
   expr={'op':'atom','predicate':'ranks','roles':{'members':items},'parameters':{'axis':q['by'],'values':q['values'],'order':q['order']}}
  elif op=='mediate':
   items=[q['origin'],q['mediator'],q['destination']]
   symbols.update({x:'entity' for x in items})
   expr={'op':'atom','predicate':'mediates','roles':{'source':items[0],'mediator':items[1],'recipient':items[2]},'parameters':{'kind':q.get('kind'),'time':q.get('time')}}
  elif op=='differentiate':
   origin=q['origin'];outputs=q['outputs'];symbols[origin]='entity';symbols.update({x:'entity' for x in outputs})
   expr={'op':'atom','predicate':'differentiates','roles':{'source':origin,'outputs':outputs},'parameters':{'basis':q.get('basis')}}
  elif op=='transfer':
   for k in ['origin','destination','carrier']:symbols[q[k]]='entity'
   expr={'op':'atom','predicate':'transfers','roles':{k:q[k] for k in ['origin','destination','carrier']},'parameters':{k:v for k,v in q.items() if k not in ['origin','destination','carrier']}}
  elif op=='depend_on':
   for k in ['dependent','support']:symbols[q[k]]='entity'
   expr={'op':'atom','predicate':'supports','roles':{'support':q['support'],'dependent':q['dependent']},'parameters':{'dimension':q.get('dimension')}}
  elif op=='partition':
   whole='partitioned_set_'+c['id'];symbols[whole]='collection'
   members=[str(x) for x in q['whole']]
   symbols.update({x:'entity' for x in members})
   expr={'op':'atom','predicate':'groups','roles':{'whole':whole,'members':members},'parameters':{'original_groups':q['groups']}}
  elif op=='qualify':
   for k in ['influence','bearer']:symbols[q[k]]='entity'
   quality=q['quality'];symbols[quality]='quality'
   expr={'op':'atom','predicate':'qualifies','roles':{k:q[k] for k in ['influence','bearer','quality']},'parameters':{k:v for k,v in q.items() if k not in ['influence','bearer','quality']}}
  elif op=='change':
   symbols[q['subject']]='entity'
   for k in ['from','to']:symbols[q[k]]='state'
   expr={'op':'atom','predicate':'transitions','roles':{'subject':q['subject'],'from':q['from'],'to':q['to']},'parameters':{'time':q.get('time')}}
  elif op=='ground':
   symbols[q['ground']]='entity';symbols[q['dependent']]='entity'
   expr={'op':'atom','predicate':'grounds','roles':{k:q[k] for k in ['ground','dependent']},'parameters':{'time':q.get('time')}}
  elif op=='orient':
   symbols[q['subject']]='entity';symbols[q['target']]='entity'
   expr={'op':'atom','predicate':'orients_to','roles':{'subject':q['subject'],'target':q['target']},'parameters':{'dimension':q.get('dimension')}}
  else:raise ValueError(op)
  exprs.append(expr)
 return record(c['id'],c['tradition'],c['claim'],c['tradition'],symbols,AND(*exprs) if len(exprs)>1 else exprs[0],c['sources'],c['locator'],'; '.join(c['guardrails']),'migrated_v0_1')

for c in v1['claims']:claims.append(converted(c))

claims.extend([
 record('G05','gurdjieff','Ordinary reactions may proceed mechanically, without a unified deliberate will.','gurdjieff',
        {'person':'entity','provocation':'episode','retaliation':'action','unified_will':'capacity'},
        AND(A('undergoes',subject='person',episode='provocation'), A('causes',source='provocation',outcome='retaliation'),A('performs',subject='person',action='retaliation'),NEG(A('has_capacity',subject='person',capacity='unified_will'))),
        ['G-O'],'chapters 3 and 6, mechanical man / lack of unity', 'Do not infer that no internal experience occurs.'),
 record('G06','gurdjieff','In self-remembering, attention is directed both toward an observed object and toward oneself.','gurdjieff',
        {'person':'entity','observed':'entity','attention_to_world':'episode','attention_to_self':'episode'},
        AND(A('attends_to',subject='person',target='observed'),A('attends_to',subject='person',target='person'),A('cooccurs',left='attention_to_world',right='attention_to_self')),
        ['G-O'],'chapter 7, Ouspensky’s divided-attention description','Overlapping attention is not a claim of two numerically distinct minds.'),
 record('B05','bailey','The personality comprises multiple lower vehicles or aspects rather than being identical to the soul.','bailey',
        {'personality':'entity','soul':'entity','physical_vehicle':'entity','emotional_vehicle':'entity','mental_vehicle':'entity','personality_composite':'quality'},
        AND(A('has_quality',bearer='personality',quality='personality_composite'),
            A('part_of',part='physical_vehicle',whole='personality'),A('part_of',part='emotional_vehicle',whole='personality'),A('part_of',part='mental_vehicle',whole='personality')),
        ['B-S'],'Question 1, discussion of personality as a sum of vehicles','Do not assume an empirical anatomical model.'),
 record('B06','bailey','In Bailey’s developmental account, a soul ray can increasingly dominate the expression of the personality.','bailey',
        {'person':'entity','soul_ray':'entity','personality_ray':'entity','integrated':'quality','soul_influence':'quality','personality_dominance':'state','soul_dominance':'state'},
        AND(A('qualifies',influence='soul_ray',bearer='person',quality='soul_influence'),A('has_quality',bearer='person',quality='integrated'),A('transitions',subject='person',**{'from':'personality_dominance','to':'soul_dominance'})),
        ['B-P','B-T'],'Question 4; Lucis Trust discussion of the rays','Qualifying influence is not automatically a physical substance transfer.'),
 record('P05','plotinus','Intellect can be understood as knowing itself in the act of intellection.','plotinus',
        {'intellect':'entity','intellection':'episode','self_as_content':'content'},
        AND(A('aware_of',subject='intellect',target='intellect'),A('represents',representation='self_as_content',target='intellect')),
        ['P-V'],'Enneads V.3, problems of self-knowledge','Representation is an analytic translation, not Plotinus’s own technical vocabulary.'),
 record('P06','plotinus','Plotinus distinguishes continuous inner intellection from its becoming explicitly available to ordinary human awareness.','plotinus',
        {'human_soul':'entity','person':'entity','intellection':'episode','thought_content':'content'},
        AND(A('undergoes',subject='human_soul',episode='intellection'),A('has_content',episode='intellection',content='thought_content'),NEG(A('aware_of',subject='person',target='intellection'))),
        ['P-V'],'Enneads V.3, discussion of intellection and perception','Simplified modeled episode: no universal assertion that such thoughts are always inaccessible.'),
 record('D01','dennett','At the intentional stance, an observer interprets a system by attributing intentional properties.','dennett',
        {'observer':'entity','system':'entity','belief_like':'quality'},
        A('attributes',observer='observer',target='system',property='belief_like'),
        ['D-O'],'Intentional stance discussed across Dennett’s work; essay on personhood','Attribution by observer is not logically identical to verified subjective experience.'),
 record('D02','dennett','A Popperian creature can evaluate a possible action through internal simulation before acting.','dennett',
        {'creature':'entity','refrain':'option','possible_attack':'option','imagined_outcome':'content'},
        AND(A('envisages',subject='creature',option='possible_attack'),A('envisages',subject='creature',option='refrain'),A('evaluates',subject='creature',option='refrain')),
        ['D-T'],'Tower of Generate-and-Test, Popperian level','Simulation of alternatives is not proof that alternatives are metaphysically open.'),
 record('D03','dennett','Moral personhood involves capacities and reciprocal normative relationships beyond basic intentional interpretation.','dennett',
        {'person':'entity','rationality':'capacity','communication':'capacity','reciprocity':'capacity','moral_norm':'norm'},
        AND(A('has_capacity',subject='person',capacity='rationality'),A('has_capacity',subject='person',capacity='communication'),A('has_capacity',subject='person',capacity='reciprocity'),A('answerable_to',subject='person',norm='moral_norm')),
        ['D-O','D-P'],'Conditions of Personhood (1976), six themes','Illustrative bundle of necessary-theme candidates, NOT Dennett proving sufficiency or a universal ladder.'),
 record('T01','constructed','An angry subject notices anger, compares alternatives, and chooses not to retaliate.','scenario_angry_person',
        {'person':'entity','anger':'episode','awareness_content':'content','attack':'option','refrain':'option','restraint':'action'},
        AND(A('experiences',subject='person',episode='anger'),A('aware_of',subject='person',target='anger'),A('has_content',episode='anger',content='awareness_content'),A('represents',representation='awareness_content',target='anger'),A('available_for_use',content='awareness_content',subject='person'),A('evaluates',subject='person',option='attack'),A('evaluates',subject='person',option='refrain'),A('selects',subject='person',option='refrain'),A('performs',subject='person',action='restraint'),A('realizes_option',action='restraint',option='refrain')),
        [],'constructed counterexample','Does not assert libertarian freedom or self-awareness merely from conscious choice.','constructed_case'),
 record('T02','constructed','A determinist model may allow deliberation but deny that the agent could have acted otherwise with the complete past and laws fixed.','scenario_determinism',
        {'person':'entity','refrain':'option','restraint':'action'},
        AND(A('selects',subject='person',option='refrain'),A('performs',subject='person',action='restraint'),NEG(MOD('agential','can',A('performs',subject='person',action='restraint'),agent='person'))),
        [],'constructed countermodel: final negation is a modeling placeholder for alternative ability','Careful: negating ability to perform actual action would be wrong; see explicit alternative-ability case T02b.','constructed_case'),
 record('T03','constructed','A compatibilist account can ascribe responsibility to an agent whose decision mechanism responds to reasons despite determinism.','scenario_compatibilism',
        {'person':'entity','reason':'content','restraint':'action'},
        AND(A('responds_to_reason',subject='person',reason='reason'),A('performs',subject='person',action='restraint'),A('morally_responsible',subject='person',action='restraint')),
        ['SEP-F','SEP-M'],'constructed example informed by reasons-responsiveness accounts','A school of responsibility, not the interlingua’s definition of agency.','constructed_case'),
 record('T04','constructed','A libertarian account can assert that the agent possessed genuine alternative possibilities at decision time.','scenario_libertarian',
        {'person':'entity','attack':'action','restraint':'action'},
        AND(MOD('agential','can',A('performs',subject='person',action='attack'),agent='person'),MOD('agential','can',A('performs',subject='person',action='restraint'),agent='person',background='same_complete_past_and_laws'),A('agent_causes',agent='person',action='restraint')),
        ['SEP-F'],'constructed example informed by agent-causal libertarianism','Do not equate merely imagining actions with being able to realize both.','constructed_case'),
 record('T05','constructed','A realm can be possible within a lore while not existing in its actual world.','scenario_modality',
        {'unrealized_realm':'entity'},
        AND(MOD('alethic','possible',EX('unrealized_realm')),NEG(EX('unrealized_realm'))),
        [],'constructed possible-vs-actual distinction','Scope possible to the tradition’s relevant modal space, not objective science.','constructed_case'),
 record('T06','constructed','A lore may posit an impersonal cosmic consciousness capable of experience but not deliberate selection.','scenario_impersonal_mind',
        {'cosmic_mind':'entity','experience':'capacity','selection':'capacity'},
        AND(A('has_capacity',subject='cosmic_mind',capacity='experience'),NEG(A('has_capacity',subject='cosmic_mind',capacity='selection'))),
        [],'constructed non-personal consciousness model','Neither denies that other traditions attribute agency to cosmic consciousness.','constructed_case'),
 record('T07','constructed','An obligation does not imply that the required action occurs; normative necessity is not causal inevitability.','scenario_obligation',
        {'person':'entity','help':'action','help_norm':'norm'},
        AND(A('governs',norm='help_norm',action='help'),MOD('deontic','obligatory',A('performs',subject='person',action='help')),NEG(A('performs',subject='person',action='help'))),
        ['SEP-M'],'constructed test of ought-versus-is','Do not render obligation as causal compulsion.','constructed_case'),
])
# Correction to the test T02: model absence of freedom to do OTHER action, not absence of capacity to perform action actually taken.
for c in claims:
 if c['id']=='T02':
  c['symbols']['attack']='action'
  c['expression']['items'][2]=NEG(MOD('agential','can',A('performs',subject='person',action='attack'),agent='person'))
  c['visual_guard']='Shows lack of alternative ability only; deliberation and a selected actual outcome remain representable.'
  c['evidence']['locator']='constructed determinist countermodel: cannot do otherwise with total prior conditions fixed'


claims.append(record('T08','constructed',
 'An implication can describe a rule without asserting that the antecedent causes the consequent.',
 'scenario_logical_rule',
 {'soul':'entity','soul_kind':'quality','immortal':'quality'},
 IMPL(A('is_a',subject='soul',kind='soul_kind'),A('has_quality',bearer='soul',quality='immortal')),
 [],'constructed conditional illustration',
 'This formula states a conditional within a hypothetical system; it neither causes immortality nor asserts the antecedent.',
 'constructed_case'))

SCHEMA={
 '$schema':'https://json-schema.org/draft/2020-12/schema',
 'title':'Comparative Cosmology Interlingua v0.2 Corpus','type':'object',
 'required':['version','sorts','predicates','claims','sources'],
 'properties':{
   'version':{'const':'0.2.0'},'sorts':{'type':'array','items':{'type':'string'}},
   'predicates':{'type':'object'},'sources':{'type':'object'},
   'claims':{'type':'array','minItems':1,'items':{'$ref':'#/$defs/claim'}},
   'principles':{'type':'array','items':{'type':'string'}},
   'translation_stages':{'type':'array','items':{'type':'string'}}},
 'additionalProperties':False,
 '$defs':{
 'expr':{'oneOf':[
   {'type':'object','required':['op','predicate','roles'],'properties':{'op':{'const':'atom'},'predicate':{'type':'string'},'roles':{'type':'object'},'parameters':{'type':'object'}},'additionalProperties':False},
   {'type':'object','required':['op','items'],'properties':{'op':{'enum':['and','or']},'items':{'type':'array','minItems':1,'items':{'$ref':'#/$defs/expr'}}},'additionalProperties':False},
   {'type':'object','required':['op','item'],'properties':{'op':{'const':'not'},'item':{'$ref':'#/$defs/expr'}},'additionalProperties':False},
   {'type':'object','required':['op','item','domain','mode'],'properties':{'op':{'const':'modal'},'item':{'$ref':'#/$defs/expr'},'domain':{'enum':['alethic','deontic','epistemic','agential']},'mode':{'enum':['possible','necessary','obligatory','permitted','known','believed','can']},'agent':{'type':'string'},'background':{'type':'string'}},'additionalProperties':False},
   {'type':'object','required':['op','entity'],'properties':{'op':{'const':'exists'},'entity':{'type':'string'}},'additionalProperties':False},
   {'type':'object','required':['op','antecedent','consequent'],'properties':{'op':{'const':'implies'},'antecedent':{'$ref':'#/$defs/expr'},'consequent':{'$ref':'#/$defs/expr'}},'additionalProperties':False}
 ]},
 'claim':{'type':'object','required':['id','tradition','statement','scope','symbols','expression','evidence','visual_guard'],
 'properties':{'id':{'type':'string'},'tradition':{'type':'string'},'statement':{'type':'string'},'scope':{'type':'string'},'symbols':{'type':'object','additionalProperties':{'enum':SORTS}},'expression':{'$ref':'#/$defs/expr'},'evidence':{'type':'object','required':['kind','sources','locator'],'properties':{'kind':{'enum':['migrated_v0_1','source_paraphrase','constructed_case']},'sources':{'type':'array','items':{'type':'string'}},'locator':{'type':'string'}},'additionalProperties':False},'visual_guard':{'type':'string'}},'additionalProperties':False}
 }
}

CORPUS={
 'version':'0.2.0','sorts':SORTS,'predicates':SIG,'sources':SOURCES,'claims':claims,
 'principles':[
  'Referent declaration is not existence assertion; a lore may describe possibilities or fictional narrators.',
  'Assertions are scoped to named worldview/model. Models can disagree without inconsistency in the interlingua.',
  'Experiencing, being aware of, making content available for reasoning, attending, and reflecting are distinct predicates; equivalences must be asserted inside a model.',
  'Choosing, reasons-responsiveness, moral accountability and libertarian alternative possibilities are independent predicates.',
  'Causation is not implication; obligation is not inevitability; existential grounding is not material transfer.',
  'An observer attributing a belief is distinct from establishing that the observed entity has experience.',
  'Visualization temporal ordering is not necessarily the depicted world’s temporal ordering.',
  'Default absence of a proposition is unknown, never false: use explicit negation only for claimed denials.',
  'Presentation-specific colors/icons must not change conceptual source meanings.',
  'Tradition-specific definitions and qualifying assumptions must remain inspectable in research even when omitted from narration.'
 ],
 'translation_stages':['source assertion + locator','scope within worldview','declare referents as typed placeholders','construct propositions with argument roles','qualify modality, time and implicit assumptions','render using compositional grammar / iconic and conventional lexicon']
}

# JSON Schema validation + a separate semantic type, link, and modal discipline checker.
Draft202012Validator.check_schema(SCHEMA)
Draft202012Validator(SCHEMA).validate(CORPUS)
errors=[]
seen=set()
def chkexpr(ex,symbols,claim):
 op=ex['op']
 if op=='atom':
  pred=ex['predicate']; sig=SIG.get(pred)
  if sig is None: errors.append((claim,'unknown predicate',pred));return
  if set(ex['roles'])!=set(sig):errors.append((claim,'role mismatch',pred,set(ex['roles'])^set(sig)))
  for role,expected in sig.items():
   value=ex['roles'].get(role)
   if value is None:continue
   if expected.startswith('list:'):
    if not isinstance(value,list):errors.append((claim,'list required',pred,role));continue
    e=expected.split(':')[1];vs=value
   else:e=expected;vs=[value]
   for v in vs:
    if not isinstance(v,str) or v not in symbols:errors.append((claim,'undeclared symbol',v));continue
    if e!='any' and symbols[v]!=e:errors.append((claim,'sort mismatch',pred,role,v,symbols[v],e))
 elif op in ['and','or']:
  for child in ex['items']:chkexpr(child,symbols,claim)
 elif op=='not':chkexpr(ex['item'],symbols,claim)
 elif op=='modal':
  good={'alethic':{'possible','necessary'},'deontic':{'obligatory','permitted'},'epistemic':{'known','believed'},'agential':{'can'}}
  if ex['mode'] not in good[ex['domain']]:errors.append((claim,'invalid modal combination',ex['domain'],ex['mode']))
  if ex['domain']=='agential' and symbols.get(ex.get('agent'))!='entity':errors.append((claim,'agential modal needs entity agent'))
  if ex['domain']!='agential' and ex.get('agent'):errors.append((claim,'extraneous agent'))
  chkexpr(ex['item'],symbols,claim)
 elif op=='exists':
  if symbols.get(ex['entity'])!='entity':errors.append((claim,'exists expects entity'))
 elif op=='implies':
  chkexpr(ex['antecedent'],symbols,claim);chkexpr(ex['consequent'],symbols,claim)

for c in claims:
 if c['id'] in seen:errors.append((c['id'],'duplicate id'))
 seen.add(c['id'])
 chkexpr(c['expression'],c['symbols'],c['id'])
 for s in c['evidence']['sources']:
  if s not in SOURCES:errors.append((c['id'],'missing source',s))
 if c['evidence']['kind']=='source_paraphrase' and not c['evidence']['sources']:errors.append((c['id'],'unattributed primary claim'))

# Test that schema / checker actually reject corrupt structure and bad modal combinations.
assert not errors,errors
neg_good=copy.deepcopy(CORPUS);neg_good['claims'][0]['expression']={'op':'modal','domain':'deontic','mode':'necessary','item':EX('Absolute')}
semantic_bad=[]
chkexpr(neg_good['claims'][0]['expression'],neg_good['claims'][0]['symbols'],'INTENTIONAL_NEGATIVE_TEST')
# negative checker appends to `errors`
assert errors and errors[-1][1]=='invalid modal combination',errors
negative_test_count=len(errors)
errors.clear()

schema_file=ROOT/'schemas'/'v0.2.schema.json'
corpus_file=P/'v0.2.json'
schema_file.write_text(json.dumps(SCHEMA,indent=2,ensure_ascii=False)+'\n')
corpus_file.write_text(json.dumps(CORPUS,indent=2,ensure_ascii=False)+'\n')
counts={s:sum(c['tradition']==s for c in claims) for s in sorted(set(c['tradition'] for c in claims))}
report={'status':'passed','version':'0.2.0','claims':len(claims),'claims_by_tradition':counts,'legacy_migrated':len(v1['claims']),'new_records':len(claims)-len(v1['claims']),'schema_errors':0,'semantic_errors':0,'negative_validator_test':'passed','distinct_predicates':len(SIG),'limitations':['The semantics are typed and structurally validated, not mathematically verified against the source texts.','Ambiguity/undertranslation can survive machine validation.','Compositional minimality and visual comprehension have not yet been established.']}
(ROOT/'reports'/'v0.2.validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
