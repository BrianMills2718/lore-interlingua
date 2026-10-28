/* Lore Interlingua Visual–Semantic Encyclopedia, prototype v0.1.
 * The UI depicts a NAVIGATION ontology and non-authoritative visual hypotheses.
 * All prose comes from catalog.json via generated catalog.js; no third-party libs.
 */
(() => {
  'use strict';
  const DB = window.LORE_ENCYCLOPEDIA;
  if (!DB?.concepts?.length) throw new Error('Encyclopedia catalog missing');
  const byId = new Map(DB.concepts.map(x => [x.id, x]));
  const $ = id => document.getElementById(id);
  const S = { selected:'dependence', facet:'all', query:'', mode:'', value:.46, playing:false, demo:'dependence', notes:{}, last:0 };
  const facetNames = new Map(DB.facets.map(f => [f.id,f.label]));
  const canvas=$('demo'), ctx=canvas.getContext('2d');
  const W=canvas.width,H=canvas.height;
  const reduced = window.matchMedia?.('(prefers-reduced-motion: reduce)')?.matches ?? false;
  const palettes = {fundamental:'#b9d4c4',configuration:'#cbb0e6',relation:'#efce95',change:'#93cbcf',agent:'#e4a79d'};
  const labModes = {dependence:[['ground','Persistent grounding'],['transfer','Transient transfer']],identity:[['persist','Preserving identity']],composition:[['part','Constitutive parts'],['members','Group members']],time:[['reveal','Reveal a timeless link'],['event','Create a link (event)']]};
  const labNames = {dependence:'Grounding ≠ transfer',identity:'Identity through deformation',composition:'Constitution ≠ membership',time:'World time ≠ display time'};
  const labCautions={
    dependence:'This is a generic relation study; it does not identify Plotinian grounding with physical transport.',
    identity:'The marker A persists across drawings; that does not prove metaphysical identity in any particular theory.',
    composition:'Parts of one structure and members of a group are different relations.',
    time:'A change in the display is not automatically a change in the represented world.'
  };
  const modeCaption={
    'ground':'A and B remain in a specified grounding relation while their drawn positions change. No material packet travels.',
    'transfer':'A packet traverses from a source to a receiver. This is a separate hypothetical event, not the mechanics of grounding.',
    'persist':'One referent A retains its drawn identity marker while an attribute of the visible shape changes.',
    'part':'Four regions constitute a single drawn composite whole. This does not describe every kind of unity.',
    'members':'Four separate entities are members of a group. The dashed region indicates grouping, not physical constitution.',
    'reveal':'The relation exists throughout this hypothetical model. Only its visibility changes during presentation.',
    'event':'The relation is introduced in model time. This is a hypothetical temporal event—not how atemporal grounding works.'
  };
  const E=(tag,cl,txt)=>{const el=document.createElement(tag);if(cl)el.className=cl;if(txt!==undefined)el.textContent=txt;return el;};
  const add=(parent,child)=>{parent.appendChild(child);return child;};
  function choose(id,{focus=false}={}){
    if(!byId.has(id))return;
    const prev=S.selected;
    if(prev!==id){S.notes[prev]=$('note').value;S.selected=id;$('note').value=S.notes[id]||'';}
    S.value=.46;S.playing=false;
    S.demo=byId.get(id).demo_id||'dependence';S.mode=labModes[S.demo][0][0];
    $('note-status').textContent='';
    renderList();renderGraph();renderEntry();renderControls();drawDemo();
    if(focus)$('entry-heading').focus({preventScroll:true});
  }
  function renderFacets(){
    const wrap=$('facet-filters');wrap.replaceChildren();
    for (const facet of [{id:'all',label:'All'},...DB.facets]){
      const b=E('button','facet'+(S.facet===facet.id?' active':''),facet.label);
      b.type='button';b.setAttribute('aria-pressed',String(S.facet===facet.id));
      b.onclick=()=>{S.facet=facet.id;renderFacets();renderList();};
      wrap.appendChild(b);
    }
  }
  function matches(concept){
    const words=[concept.label,concept.definition,concept.kind,concept.facets.map(f=>facetNames.get(f)).join(' '),concept.examples.map(e=>e.statement).join(' ')].join(' ').toLowerCase();
    return (S.facet==='all'||concept.facets.includes(S.facet)) && words.includes(S.query);
  }
  function renderList(){
    const list=$('concept-list');list.replaceChildren();let found=DB.concepts.filter(matches);
    $('visible-count').textContent=`${found.length} of ${DB.concepts.length}`;
    if(!found.length){add(list,E('p','empty','No matching concepts. Try another term.'));return;}
    for(const c of found){
      const b=E('button','concept-btn'+(c.id===S.selected?' selected':''));b.type='button';b.setAttribute('aria-current',c.id===S.selected?'true':'false');
      add(b,E('span',null,c.label));add(b,E('small',null,c.facets.map(x=>facetNames.get(x)?.split(' ')[0]).join(' / ')));
      b.onclick=()=>choose(c.id,{focus:true});add(list,b);
    }
  }
  const SVG='http://www.w3.org/2000/svg';
  function sx(tag,attrs={},text){const x=document.createElementNS(SVG,tag);for(const [k,v] of Object.entries(attrs))x.setAttribute(k,String(v));if(text!==undefined)x.textContent=text;return x;}
  function renderGraph(){
    const svg=$('graph');svg.replaceChildren();const focus=byId.get(S.selected);
    const connected = new Map();
    for(const rel of focus.relations)connected.set(rel.target,{from:focus.id,to:rel.target,type:rel.type,why:rel.why});
    for(const c of DB.concepts)for(const rel of c.relations)if(rel.target===focus.id && !connected.has(c.id))connected.set(c.id,{from:c.id,to:focus.id,type:rel.type,why:rel.why});
    const layer=sx('g',{'aria-hidden':'true'});svg.appendChild(layer);
    for(const e of connected.values()){
      const a=byId.get(e.from).position,b=byId.get(e.to).position;
      const mx=(a.x+b.x)/2,my=(a.y+b.y)/2;
      const bend=(e.from<e.to?1:-1)*Math.min(15,Math.abs(a.y-b.y)*.10);
      const d=`M ${a.x} ${a.y} Q ${mx} ${my+bend} ${b.x} ${b.y}`;
      add(layer,sx('path',{d,fill:'none',stroke:'#729b91','stroke-width':2,'stroke-opacity':.65,'stroke-linecap':'round'}));
      const t=sx('text',{x:mx,y:my+bend-9,'text-anchor':'middle',fill:'#a2bfb6','font-size':10},e.type.replace('_',' '));layer.appendChild(t);
    }
    for(const [i,c] of DB.concepts.entries()){
      const kind=c.id===S.selected?'focus':connected.has(c.id)?'linked':'muted';
      const g=sx('g',{class:'graph-node '+kind,role:'button',tabindex:0,'aria-label':`Open ${c.label}`});
      const pos=c.position;
      add(g,sx('circle',{cx:pos.x,cy:pos.y,r:22,fill:kind==='muted'?'#13262b':'#22443e',stroke:kind==='focus'?'#a9dbb6':'#648e8c'}));
      add(g,sx('circle',{cx:pos.x,cy:pos.y,r:5,fill:palettes[c.facets[0]]||'#b0d1c8',stroke:'none'}));
      add(g,sx('text',{x:pos.x,y:pos.y+43},c.label));
      add(g,sx('title',{},`${c.label}: ${c.definition}`));
      g.addEventListener('click',()=>choose(c.id,{focus:true}));
      g.addEventListener('keydown',ev=>{if(ev.key==='Enter'||ev.key===' '){ev.preventDefault();choose(c.id,{focus:true})}});
      svg.appendChild(g);
    }
    $('graph-caption').textContent=`${focus.label} has ${connected.size} visible neighboring concepts · Layout is for navigation, not a picture of metaphysical space.`;
  }
  function renderEntry(){
    const c=byId.get(S.selected),root=$('entry-body');root.replaceChildren();
    $('entry-heading').textContent=c.label;
    $('entry-type').textContent=c.kind;
    add(root,E('div','kindline',c.facets.map(f=>facetNames.get(f)).join('  ·  ')));
    add(root,E('p','definition',c.definition));
    if(c.scope_note)add(root,E('p','sidenote',c.scope_note));
    const section=(name)=>{add(root,E('h3',null,name))};
    section('Important distinctions');let ul=add(root,E('ul'));
    for(const d of c.distinctions){const li=add(ul,E('li'));add(li,E('strong',null,d.name+' — '));li.append(document.createTextNode(d.note))}
    section('Connected concepts');let neighbors=add(root,E('div'));
    for(const r of c.relations){const b=E('button','relation-btn');b.type='button';b.title=r.why;add(b,E('span','relation-label',r.type));b.append(document.createTextNode(byId.get(r.target).label));b.onclick=()=>choose(r.target,{focus:true});neighbors.appendChild(b)}
    section('Examples within sources');
    for(const ex of c.examples){const src=DB.sources[ex.source],box=add(root,E('div','source-ref'));
      const head=add(box,E('div','ref-head'));add(head,E('strong',null,ex.ref+' · '+ex.scope));
      const a=add(head,E('a',null,'Open source'));a.href=src.path;a.title=`Open ${src.label}`;a.target='_blank';a.rel='noopener';
      add(box,E('blockquote',null,'“'+ex.statement+'”'));add(box,E('p',null,'Here: '+ex.relevance));
    }
    section('Visual hypotheses');
    for(const x of c.visual_candidates){const wrap=add(root,E('div','candidate'));add(wrap,E('strong',null,x.label));add(wrap,E('p',null,x.mapping));add(wrap,E('p','guard','Does not imply: '+x.does_not_assert));add(wrap,E('p','tags','Candidate primitives (experimental): '+x.primitives.join(' · ')));}
    section('Questions this could expose');ul=add(root,E('ul','question-list'));
    for(const x of c.questions)add(ul,E('li',null,x));
  }
  function renderControls(){
    const c=byId.get(S.selected),lab=S.demo;
    $('lab-context').textContent=(c.label+' · '+labNames[lab]+'. '+(c.id===lab?'Dedicated study. ':'Shared study, not a dedicated encoding. ')+labCautions[lab]);
    const root=$('demo-controls');root.replaceChildren();
    for(const [id,label] of labModes[lab]){
      const b=E('button','secondary',label);b.type='button';b.setAttribute('aria-pressed',String(S.mode===id));
      b.onclick=()=>{S.mode=id;S.value=.46;S.playing=false;renderControls();drawDemo()};root.appendChild(b);
    }
    const wrap=add(root,E('label','range-wrap'));add(wrap,E('span',null,lab==='dependence'?'Change view':lab==='composition'?'Rearrange':lab==='identity'?'Change form':'Inspect sequence'));
    const range=add(wrap,E('input'));range.type='range';range.id='study-range';range.min='0';range.max='100';range.step='1';range.value=Math.round(S.value*100);
    range.setAttribute('aria-label','Adjust displayed study parameter');range.oninput=()=>{S.value=Number(range.value)/100;S.playing=false;renderControls();drawDemo()};
    const play=E('button','secondary',S.playing?'Pause':'Animate');play.type='button';play.id='study-play';play.setAttribute('aria-pressed',String(S.playing));
    play.onclick=()=>{S.playing=!S.playing;play.textContent=S.playing?'Pause':'Animate';play.setAttribute('aria-pressed',String(S.playing))};root.appendChild(play);
    $('lab-overlay').textContent=modeCaption[S.mode];
  }
  function clear(){ctx.clearRect(0,0,W,H);ctx.fillStyle='#0c2024';ctx.fillRect(0,0,W,H);ctx.strokeStyle='#315254';ctx.lineWidth=1;ctx.strokeRect(28,24,W-56,H-48);}
  function label(s,x,y,size=14,color='#d8e3db',align='center'){ctx.textAlign=align;ctx.font=`${size}px system-ui`;ctx.fillStyle=color;ctx.fillText(s,x,y);}
  function circle(x,y,r,fill,stroke,width=2){ctx.beginPath();ctx.arc(x,y,r,0,Math.PI*2);if(fill){ctx.fillStyle=fill;ctx.fill()}if(stroke){ctx.lineWidth=width;ctx.strokeStyle=stroke;ctx.stroke()}}
  function link(a,b,color='#9ecbc3',width=4,dash=[]){ctx.save();ctx.beginPath();ctx.moveTo(...a);ctx.lineTo(...b);ctx.strokeStyle=color;ctx.lineWidth=width;ctx.setLineDash(dash);ctx.stroke();ctx.restore()}
  function roundedRect(x,y,w,h,r,fill,stroke){ctx.beginPath();ctx.roundRect(x,y,w,h,r);if(fill){ctx.fillStyle=fill;ctx.fill()}if(stroke){ctx.strokeStyle=stroke;ctx.lineWidth=2;ctx.stroke()}}
  function diamond(x,y,r,fill){ctx.beginPath();ctx.moveTo(x,y-r);ctx.lineTo(x+r,y);ctx.lineTo(x,y+r);ctx.lineTo(x-r,y);ctx.closePath();ctx.fillStyle=fill;ctx.fill()}
  function drawDependence(){
    const k=S.value,src=[251,155],dest=[575,105+105*k];
    circle(...src,53,'#193b3c','#a5d6bb');circle(...dest,53,'#273940','#b0c9d6');
    label('A',src[0],src[1]+8,26,'#e6f1e8');label(S.mode==='ground'?'Ground':'Source',src[0],src[1]+79,13,'#b1cdbf');
    label('B',dest[0],dest[1]+8,26,'#f2eee2');label(S.mode==='ground'?'Dependent':'Recipient',dest[0],dest[1]+79,13,'#b2c8ce');
    const a=[src[0]+53,src[1]],b=[dest[0]-53,dest[1]];
    if(S.mode==='ground'){
      link(a,b,'#a6d5b8',5);diamond((a[0]+b[0])/2,(a[1]+b[1])/2,10,'#f2c992');
      label('grounding remains',411,37,13,'#a9ccb8');
      label('no transferred object',411,294,12,'#c4b5a6');
    } else {
      link(a,b,'#5b8887',2,[5,8]);const x=a[0]+(b[0]-a[0])*k,y=a[1]+(b[1]-a[1])*k;
      circle(x,y,11,'#f3ca84','#ffe6b2');
      if(k>.85)circle(dest[0],dest[1],66,null,'#edc98b',2);
      label('packet position',410,36,13,'#e3c694');
      label('event with a moving marker',410,294,12,'#c4b5a6');
    }
  }
  function drawIdentity(){
    const k=S.value,cx=410,cy=161;
    const fill=ctx.createRadialGradient(cx,cy,0,cx,cy,150);fill.addColorStop(0,'#335e5a');fill.addColorStop(1,'#162b36');
    ctx.beginPath();for(let i=0;i<=120;i++){
      const a=i/120*Math.PI*2;
      const r=94*(1+k*.32*Math.sin(5*a+Math.PI*.2))+k*16*Math.sin(3*a);
      const x=cx+Math.cos(a)*r,y=cy+Math.sin(a)*r*.77;
      if(i===0)ctx.moveTo(x,y);else ctx.lineTo(x,y);
    }ctx.closePath();ctx.fillStyle=fill;ctx.fill();ctx.strokeStyle='#a6d5c0';ctx.lineWidth=3;ctx.stroke();
    diamond(cx,cy,17,'#f1d09e');label('A',cx,cy+7,17,'#142b2b');
    label('IDENTITY MARK A · HELD',410,42,13,'#ecd2a1');
    label('FORM · VARIABLE',410,296,13,'#a1caba');
  }
  function drawComposition(){
    const k=S.value,drift=33*k;
    if(S.mode==='part'){
      const colors=['#456f71','#618f83','#879d76','#c1a77b'];
      for(let i=0;i<4;i++){
        const a0=-Math.PI/2+i*Math.PI/2,a1=a0+Math.PI/2;
        ctx.beginPath();ctx.moveTo(410,160);ctx.arc(410,160,94,a0,a1);ctx.closePath();ctx.fillStyle=colors[i];ctx.fill();ctx.strokeStyle='#0d2024';ctx.lineWidth=4+drift/10;ctx.stroke();
        const a=(a0+a1)/2;label('P'+(i+1),410+Math.cos(a)*63,160+Math.sin(a)*63,14,'#0c2426');
      }
      circle(410,160,94,null,'#e4d3ab',3);label('ONE COMPOSITE WHOLE',410,47,14,'#e2d2ad');label('Constitutive regions',410,291,12,'#bdcabc');
    } else {
      ctx.save();ctx.setLineDash([8,7]);ctx.strokeStyle='#c5b0de';ctx.lineWidth=2.4;ctx.strokeRect(279,62,262,202);ctx.restore();
      const xy=[[351,116],[471,116],[351,210],[471,210]];
      xy.forEach(([x,y],i)=>{const jx=(i%2?1:-1)*drift*.32;circle(x+jx,y,25,['#456f71','#618f83','#879d76','#c1a77b'][i],'#d5daca');label('M'+(i+1),x+jx,y+5,12,'#0a2328')});
      label('ONE GROUP',410,44,14,'#d3b9e9');label('Membership is not physical constitution',410,294,12,'#bdcabc');
    }
  }
  function drawTime(){
    const k=S.value,a=[264,164],b=[563,164];
    circle(...a,51,'#203b3c','#a6d8ba');circle(...b,51,'#283b48','#a4c5d3');
    label('A',a[0],a[1]+8,24);label('B',b[0],b[1]+8,24);
    label(S.mode==='reveal'?'RELATION EXISTS THROUGHOUT':'RELATION FORMS IN THE MODEL',410,40,14,'#e5d6b5');
    const begin=[a[0]+52,a[1]],end=[b[0]-52,b[1]];
    if(S.mode==='reveal'){
      ctx.globalAlpha=.06+.94*k;link(begin,end,'#afddbb',6);diamond(411,164,9,'#f3ce95');ctx.globalAlpha=1;
      label('Presentation reveal: '+Math.round(k*100)+'%',410,286,13,'#aac9c1');
    } else {
      const pos=[begin[0]+(end[0]-begin[0])*k,begin[1]];
      link(begin,pos,'#afddbb',6);circle(...pos,6,'#f2c88d');
      label('Hypothetical event progress: '+Math.round(k*100)+'%',410,286,13,'#aac9c1');
    }
    label('A and B are not named metaphysical beings here.',410,304,11,'#8cb1aa');
  }
  function drawDemo(){
    clear();
    if(S.demo==='dependence')drawDependence();
    else if(S.demo==='identity')drawIdentity();
    else if(S.demo==='composition')drawComposition();
    else drawTime();
    $('lab-overlay').textContent=modeCaption[S.mode];
    const slider=$('study-range');if(slider)slider.value=Math.round(S.value*100);
  }
  function raf(ts){
    if(S.playing && !reduced){
      const dt=Math.min(.06,(ts-(S.last||ts))/1000);
      S.value=(S.value+dt*.18)%1;drawDemo();
    }else if(S.playing && reduced){S.playing=false;renderControls();}
    S.last=ts;window.requestAnimationFrame(raf);
  }
  $('search').addEventListener('input',e=>{S.query=e.target.value.trim().toLowerCase();renderList()});
  $('copy-note').onclick=async()=>{
    const c=byId.get(S.selected);
    const message=`Lore Interlingua research note\nConcept: ${c.label}\nStudy: ${labNames[S.demo]} / ${S.mode}, parameter ${Math.round(S.value*100)}%\nObservation: ${$('note').value.trim()||'(none entered)'}\nEpistemic status: exploratory visual hypothesis`;
    S.notes[S.selected]=$('note').value;
    try{await navigator.clipboard.writeText(message);$('note-status').textContent='Note copied. Nothing was uploaded.';}
    catch{ $('note').value=message;$('note').select();$('note-status').textContent='Clipboard unavailable: select and copy the prepared note manually.'; }
  };
  $('total-count').textContent=DB.concepts.length;
  renderFacets();choose('dependence');window.requestAnimationFrame(raf);
  // Stable read-only entry point used by automation / smoke tests.
  window.__encyclopedia={select:id=>choose(id), state:()=>({selected:S.selected,facet:S.facet,demo:S.demo,mode:S.mode,value:S.value}), catalog:DB};
})();