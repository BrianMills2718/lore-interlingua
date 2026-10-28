/* Applied-case explorer: combines existing ontology entries with source-scoped
   semantic casting, explicit image vocabulary and the original live study.
   This is an editorial cross-reference, not a theorem prover or video compiler. */
(() => {
  'use strict';
  const DB = window.LORE_CASES;
  const encyclopedia = window.__encyclopedia;
  if (!DB?.cases?.length || !encyclopedia?.select) {
    throw new Error('Case library or encyclopedia navigation is missing');
  }
  const $ = id => document.getElementById(id);
  const byId = new Map(DB.cases.map(c => [c.id, c]));
  const chosen = {caseId: DB.cases[DB.cases.length-1].id, claimId:'all', sceneLoaded:false};
  const node = (tag,cl,txt) => {
    const e = document.createElement(tag);
    if(cl)e.className = cl;
    if(txt !== undefined)e.textContent = txt;
    return e;
  };
  const add = (parent, child) => (parent.appendChild(child), child);
  const status = (claim) => claim.status === 'depicted' ? 'Depicted in the study' : 'Context only · not depicted';

  function openCase(id, claimId=null, {scroll=false}={}) {
    if(!byId.has(id)) return;
    const changed = chosen.caseId !== id;
    chosen.caseId = id;
    const c=byId.get(id);
    if(claimId && c.claims.some(x=>x.id===claimId))chosen.claimId=claimId;
    else if(changed)chosen.claimId='all';
    if(changed) { const frame=$('case-scene'); frame.removeAttribute('src'); $('case-frame-box').hidden=true; chosen.sceneLoaded=false; }
    renderCase();
    if(scroll) $('case-study').scrollIntoView({behavior:'smooth',block:'start'});
  }

  function renderCasePicker(){
    const root=$('case-picker'); root.replaceChildren();
    for(const c of DB.cases){
      const button=add(root,node('button','case-filter'+(chosen.caseId===c.id?' active':''),c.id.includes('010')?'010 · Living intermediary':'009 · Cosmic membrane'));
      button.type='button'; button.setAttribute('aria-pressed',String(chosen.caseId===c.id));
      button.onclick=()=>openCase(c.id,null,{scroll:false});
    }
  }
  function renderConceptCaseLinks(id) {
    const detail=$('entry-body');
    const old=detail.querySelector('[data-case-links]');
    if(old)old.remove();
    const matches=DB.cases.flatMap(c => c.related_concepts
      .filter(rel=>rel.id===id)
      .map(rel=>({c,rel})));
    if(!matches.length)return;
    const wrap=add(detail,node('div','applied-case-links'));
    wrap.dataset.caseLinks='true';
    add(wrap,node('h3',null,'Applied visual cases'));
    for(const {c,rel} of matches) {
      const b=add(wrap,node('button','applied-case-link',c.title));
      b.type='button';
      add(b,node('small',null,rel.role+' · '+rel.why));
      b.onclick=()=>openCase(c.id,rel.claim_id,{scroll:true});
    }
  }

  function paragraph(parent,text,cls=''){
    return add(parent,node('p',cls,text));
  }
  function link(parent,label,url,cls=''){
    const a=add(parent,node('a',cls,label));
    a.href=url;
    if(url.startsWith('https:')){a.target='_blank';a.rel='noopener noreferrer';}
    return a;
  }
  function renderClaimButtons(c){
    const root=$('case-claim-buttons');root.replaceChildren();
    const choices=[{id:'all',label:'All visual marks'},...c.claims.map(x=>({id:x.id,label:x.id+(x.status!=='depicted'?' · context':'' )}))];
    for(const item of choices) {
      const b=add(root,node('button','case-filter'+(chosen.claimId===item.id?' active':''),item.label));
      b.type='button';
      b.setAttribute('aria-pressed',String(chosen.claimId===item.id));
      b.onclick=()=>{chosen.claimId=item.id;renderCase();};
    }
  }
  function renderClaimDetails(c){
    const root=$('case-claim-details');root.replaceChildren();
    const selected=chosen.claimId==='all'?c.claims:c.claims.filter(x=>x.id===chosen.claimId);
    for(const claim of selected) {
      const item=add(root,node('article','case-claim'+(claim.status==='depicted'?'':' unshown')));
      const top=add(item,node('div','case-claim-top'));
      add(top,node('strong',null,claim.id+' · '+status(claim)));
      const url=c.source_documents.find(s=>s.id==='interlingua-claims')?.url;
      if(url)link(top,'Corpus source',url,'case-source-anchor');
      paragraph(item,claim.statement,'case-statement');
      paragraph(item,'Structure: '+claim.relation,'case-structure');
      paragraph(item,claim.reading,'case-reading');
      paragraph(item,'Not shown: '+claim.not_shown,'case-nonclaim');
    }
  }
  function renderMarks(c){
    const root=$('case-marks');root.replaceChildren();
    const selected=chosen.claimId==='all'?c.marks:c.marks.filter(x=>x.claim_ids.includes(chosen.claimId));
    $('case-mark-count').textContent=`${selected.length} of ${c.marks.length} documented visual elements`;
    if(!selected.length){paragraph(root,'No marks in this scene independently depict this stronger claim. That omission is intentional and documented.','case-empty');return;}
    for(const mark of selected){
      const card=add(root,node('article','case-mark'));
      const line=add(card,node('div','mark-head'));
      const icon=add(line,node('span','mark-swatch',mark.symbol));
      icon.style.color=mark.color;
      add(line,node('strong',null,mark.label));
      add(line,node('span','mark-type',mark.kind));
      paragraph(card,mark.mapping,'mark-mapping');
      paragraph(card,'Why included: '+mark.why,'mark-purpose');
      paragraph(card,'Does not assert: '+mark.does_not_assert,'mark-nonclaim');
      if(mark.visibility!=='shown')paragraph(card,'Display: '+mark.visibility,'mark-visibility');
    }
  }
  function renderConcepts(c){
    const root=$('case-concept-links');root.replaceChildren();
    const labels=new Map(encyclopedia.catalog.concepts.map(x=>[x.id,x.label]));
    for(const ref of c.related_concepts){
      const b=add(root,node('button','case-concept-chip',labels.get(ref.id)||ref.id));
      b.type='button';b.title=ref.role+': '+ref.why;
      b.onclick=()=>{encyclopedia.select(ref.id);$('entry-heading').scrollIntoView({behavior:'smooth',block:'start'});};
    }
  }
  function renderCase(){
    const c=byId.get(chosen.caseId);
    renderCasePicker();
    $('case-title').textContent=c.title;
    $('case-id-label').textContent=c.id.includes('010')?'Case 010 · Source linked':'Case 009 · Source linked';
    const so=$('case-source-observation'); so.textContent=c.source_observation?('Source-passage detail: '+c.source_observation.statement):''; so.hidden=!c.source_observation;
    $('case-subtitle').textContent=c.subtitle;
    $('case-overview').textContent=c.summary;
    $('case-scope').textContent=c.scope;
    $('case-status').textContent=c.status;
    renderConcepts(c);
    renderClaimButtons(c);renderClaimDetails(c);renderMarks(c);
    const docs=$('case-doc-links');docs.replaceChildren();
    if(c.artifact.encoding_audit) link(docs,'Inspect mark semantics · interactive audit',c.artifact.encoding_audit);
    link(docs,'Open interactive study',c.artifact.html);
    if(c.artifact.primary_treatment)link(docs,'Read study notes',c.artifact.primary_treatment);
    if(c.artifact.scene_contract)link(docs,'Visual semantics contract',c.artifact.scene_contract);
    if(c.id.includes('009')){link(docs,'Narration and symbol audit',c.artifact.narration_audit);link(docs,'Parsimony corrections',c.artifact.parsimony_audit);}
    const s=$('case-sources');s.replaceChildren();
    for(const src of c.source_documents){
      const row=add(s,node('div','case-source-item'));
      link(row,src.label,src.url);
      paragraph(row,src.locator,'case-source-locator');
    }
    const revisions=$('case-revisions');revisions.replaceChildren();
    c.decisions.forEach(x=>add(revisions,node('li',null,x)));
    const questions=$('case-questions');questions.replaceChildren();
    c.open_questions.forEach(x=>add(questions,node('li',null,x)));
  }
  const load=$('case-load-scene');
  load.addEventListener('click',()=>{
    const c=byId.get(chosen.caseId);
    const frame=$('case-scene');
    frame.src=c.artifact.html;
    $('case-frame-box').hidden=false;
    chosen.sceneLoaded=true;
    load.textContent='Reload interactive scene';
    $('case-scene').setAttribute('title',c.title+' — interactive study');
    $('case-scene-status').textContent=c.id.includes('010')?'Exploratory surface comparison loaded. The switch changes the modeled condition, not cosmological history.':'Interactive cosmic membrane scene loaded; diagnostic paths and key are optional.';
  });
  $('copy-case-note').addEventListener('click',async()=>{
    const c=byId.get(chosen.caseId);
    const note=`Lore Interlingua — applied case research note\nCase: ${c.title}\nSelected claim: ${chosen.claimId}\nObservation: ${$('case-note').value.trim()||'(none entered)'}\nStatus: art-directed, source-scoped research study; not an established visual grammar`;
    try {
      await navigator.clipboard.writeText(note);
      $('case-note-status').textContent='Note copied. Nothing was uploaded.';
    } catch {
      $('case-note').value=note;
      $('case-note').select();
      $('case-note-status').textContent='Clipboard unavailable; copy the selected note manually.';
    }
  });
  window.addEventListener('encyclopedia:select',e=>renderConceptCaseLinks(e.detail.id));
  renderCase();
  renderConceptCaseLinks(encyclopedia.state().selected);
  window.__caseExplorer = {
    select:(id,claimId)=>openCase(id,claimId),
    state:()=>({...chosen}),
    catalog:DB
  };
})();
