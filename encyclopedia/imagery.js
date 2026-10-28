/* Curated film/imagery comparison. Canonical source is imagery.json. No network or storage. */
(()=>{
'use strict';
const D=window.LORE_IMAGERY;
if(!D?.motifs || !D?.terms || !D?.works) throw Error('Imagery data not loaded');
const $=id=>document.getElementById(id);
const make=(tag,cls,content)=>{const e=document.createElement(tag);if(cls)e.className=cls;if(content!==undefined)e.textContent=content;return e;};
const add=(to,el)=>to.appendChild(el);
D.works.forEach(w=>{
  const wrap=make('article','work');
  const img=add(wrap,make('img'));img.src=w.storyboard;img.alt='Storyboard montage from '+w.title;img.loading='lazy';
  const inner=add(wrap,make('div','work-inner'));
  add(inner,make('div','eyebrow','FILM '+w.id));add(inner,make('h3','',w.title));add(inner,make('p','',w.focus));
  const vid=add(inner,make('video'));vid.controls=true;vid.preload='metadata';vid.playsInline=true;vid.src=w.source;vid.setAttribute('aria-label',w.title+' video preview');
  const meta=add(inner,make('div','meta'));add(meta,make('span','',w.id==='011'?'Organic mediation':w.id==='012'?'Seven-world hierarchy':'Cumulative cosmology'));
  const link=add(meta,make('a','', 'Open video file'));link.href=w.source;
  add($('film-comparison'),wrap);
});
D.terms.forEach(t=>{
  const card=make('article','term');add(card,make('h3','',t.term));add(card,make('div','question',t.question));
  add(card,make('p','',t.source_meaning));
  add(card,make('div','smallcaps','What Films 011 and 012 communicated'));
  add(card,make('p','',t.explained_now));
  add(card,make('div','smallcaps','What Film 013 adds'));
  add(card,make('p','',t.after013||''));
  add(card,make('div','smallcaps','Still open'));
  add(card,make('p','gap',t.missing));
  add($('term-grid'),card);
});
function status(card,film,code,note){
 const box=add(card,make('div','status '+code));
 add(box,make('strong','',film));add(box,make('div','label',code==='present'?'Visible':code==='partial'?'Only partial':'Not depicted'));
 add(box,make('div','',note));
}
function matchFilter(m,filter){
 if(filter==='reduced')return m.film011==='present' && m.film012!=='present';
 if(filter==='restored')return m.film011==='present'&&m.film012!=='present'&&m.film013==='present';
 if(filter==='new')return m.film011==='absent' && m.film012!=='absent';
 if(filter==='missing')return m.film011==='absent' && m.film012==='absent';
 return true;
}
function render(){
 const q=$('search').value.trim().toLowerCase(),filter=$('filter').value;
 const root=$('motifs');root.replaceChildren();let n=0;
 for(const m of D.motifs){
  const combined=[m.label,m.kind,m.meaning,m.next,...m.ontology].join(' ').toLowerCase();
  if(!combined.includes(q)||!matchFilter(m,filter))continue;
  n++;
  const card=add(root,make('article','motif'));
  add(card,make('h3','',m.label));add(card,make('div','kind',m.kind+' · '+m.source_ref.join(', ')));
  add(card,make('p','meaning',m.meaning));
  const row=add(card,make('div','statuses'));
  status(row,'FILM 011',m.film011,m.film011_note);status(row,'FILM 012',m.film012,m.film012_note);status(row,'FILM 013',m.film013,m.film013_note);
  const details=add(card,make('details'));add(details,make('summary','', 'Why keep it? What does it not claim?'));
  add(details,make('p','', 'Next: '+m.next));
  add(details,make('p','', 'Lost if removed: '+m.what_lost));
  add(details,make('p','', 'Does NOT assert: '+m.non_claim));
  add(details,make('p','', 'Related ontology categories: '+m.ontology.join(', ')));
 }
 $('count').textContent=n+' / '+D.motifs.length+' motifs';
 if(n===0)add(root,make('p','', 'No motifs matched. Clear the search or change the filter.'));
}
$('search').addEventListener('input',render);$('filter').addEventListener('change',render);render();
for(const s of Object.values(D.source_documents)){
 const a=add($('sources'),make('a','citation',s.label));a.href=s.url;a.rel='noopener noreferrer';a.target='_blank';
}
})();
