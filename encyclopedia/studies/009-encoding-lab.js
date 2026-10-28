/* Experimental visual study of mark semantics — not a claim of cosmological dynamics. */
(() => {
  'use strict';
  const D = window.LORE_ENCODING_AUDIT;
  if (!D?.encoding?.outgoing?.channels?.length) throw new Error('Encoding audit source data missing');
  const $ = id => document.getElementById(id);
  const c = $('comparison'), g = c.getContext('2d');
  const width = c.width, height = c.height;
  const channels = D.encoding.outgoing.channels;
  const state = { mode:'original', equalize:false, labels:true, g02:true, time:4, playing:true, last:performance.now() };
  const E=[440,293], R=87;
  const targets={
    sun:{at:[143,133], cp:[215,225], start:[380,235]},
    planets:{at:[550,99], cp:[544,165], start:[468,208]},
    moon:{at:[816,350], cp:[641,419], start:[528,317]}
  };
  const at=(a,b,ctrl,t)=>{const u=1-t; return [u*u*a[0]+2*u*t*ctrl[0]+t*t*b[0],u*u*a[1]+2*u*t*ctrl[1]+t*t*b[1]]};
  function line(a,b,color='#36535a',w=1){g.strokeStyle=color;g.lineWidth=w;g.beginPath();g.moveTo(...a);g.lineTo(...b);g.stroke()}
  function dot(x,y,r,col){g.fillStyle=col;g.beginPath();g.arc(x,y,r,0,Math.PI*2);g.fill()}
  function circle(x,y,r,col,w=1){g.strokeStyle=col;g.lineWidth=w;g.beginPath();g.arc(x,y,r,0,Math.PI*2);g.stroke()}
  function label(s,x,y,size=15,color='#cbd8d2'){if(!state.labels)return;g.font=`${size}px system-ui`;g.textAlign='center';g.fillStyle=color;g.fillText(s,x,y)}
  function mark(x,y,shape,color,phase){
    g.save();g.translate(x,y);g.fillStyle=color;g.strokeStyle=color;g.lineWidth=2;
    if(shape==='dot'){dot(0,0,3.5,color)}
    else if(shape==='square'){g.rotate(.25+phase*.04);g.fillRect(-4,-4,8,8)}
    else if(shape==='ring'){circle(0,0,5.3,color,2)}
    g.restore();
  }
  function assign(ch,i){
    if(state.mode==='uniform')return {shape:'dot',color:'#d6e1d9'};
    if(state.mode==='permuted'){const to=channels[(i+1)%channels.length];return {shape:to.shape,color:to.color};}
    return {shape:ch.shape,color:ch.color};
  }
  function render(t=state.time){
    state.time=t;g.clearRect(0,0,width,height);
    const bg=g.createLinearGradient(0,0,width,height);bg.addColorStop(0,'#06111d');bg.addColorStop(1,'#102535');g.fillStyle=bg;g.fillRect(0,0,width,height);
    // Stable identifiable participants (no fictional cosmic orbits or four unexplained levels).
    dot(...E,69,'#194858');dot(E[0]-14,E[1]-21,31,'#2c676b');dot(E[0]+23,E[1]+28,27,'#305b4b');dot(E[0]+1,E[1]-7,25,'#406f5e');circle(...E,69,'#91b8ae',1.4);
    circle(...E,R,'#78ccb4',1.6);
    for(let j=0;j<24;j++){let a=j*2*Math.PI/24;let x=E[0]+R*Math.cos(a),y=E[1]+R*Math.sin(a);
      dot(x,y,j%4===0?3.8:2,'#9fdec5');
      if(j%4===0){line([x,y],[x+10*Math.cos(a),y+10*Math.sin(a)],'#79baa0',1.1)}
    }
    dot(...targets.sun.at,34,'#ebbd78');circle(...targets.sun.at,42,'#e1c590',1.2);
    dot(...targets.moon.at,29,'#a7bec9');circle(targets.moon.at[0]-7,targets.moon.at[1]-5,5,'#7e9dac');
    const planetPositions=[[506,94],[550,72],[592,105]];
    for(let i=0;i<planetPositions.length;i++){const p=planetPositions[i];dot(...p,8+i,'#40818c');circle(...p,8+i,'#9bcfd2',1)}
    label('SUN',143,67);label('PLANETARY WORLD',550,41);label('ORGANIC LIFE',E[0],172,16,'#a7e6c9');label('EARTH',E[0],300,16);label('MOON',816,411);
    if(state.g02){
      for(let i=0;i<planetPositions.length;i++){
        let src=planetPositions[i],dst=[E[0]+R*Math.cos(-2.55+i*.48),E[1]+R*Math.sin(-2.55+i*.48)];
        let cp=[(src[0]+dst[0])/2-20+i*24,(src[1]+dst[1])/2-18];
        for(let k=0;k<7;k++){const u=(t*.11+k/7+i*.13)%1;const p=at(src,dst,cp,u);mark(...p,'dot','#77e2d7',t);}
      }
      for(let i=0;i<10;i++){const angle=i*2*Math.PI/10+t*.025,outer=[E[0]+R*Math.cos(angle),E[1]+R*Math.sin(angle)],inner=[E[0]+63*Math.cos(angle),E[1]+63*Math.sin(angle)];const u=(t*.18+i*.27)%1;const p=[outer[0]+u*(inner[0]-outer[0]),outer[1]+u*(inner[1]-outer[1])];mark(...p,'dot','#c5eaba',t);}
    }
    // All three G03 outputs use the *same* rendering operation; distinct glyphs are category cues.
    channels.forEach((ch,i)=>{
      const target=targets[ch.id];const shown=assign(ch,i);
      const rate=state.equalize ? .081 : ch.rate;
      for(let k=0;k<9;k++){const u=(t*rate+k/9+i*.07)%1;const p=at(target.start,target.at,target.cp,u);mark(...p,shown.shape,shown.color,t);}
    });
    $('clock').textContent='0:'+String(Math.floor(t)).padStart(2,'0');
  }
  function updateText(){
    const mode = D.operations.find(x=>x.id===state.mode);
    $('what-changes').textContent=mode.changes+(state.equalize?' All three animation rates have also been normalized.':' The original unequal rates remain as implementation parameters.');
    const interpretations={
      original:'The original scene distinguishes recipient-linked categories through color and shape. It still uses the same propagation operation for all three.',
      uniform:'Recipient directions persist, but the outgoing marks no longer distinguish their kinds. A statement or icon key must supply the difference asserted by G03.',
      permuted:'The colors and glyphs change recipients, yet the lore claim stays the same. The mapping is a convention, not a discovered physical identity.'
    };
    $('interpretation').textContent=interpretations[state.mode]+(state.equalize?' Equalizing rates loses no source-specified speed information.':'');
    for(const operation of D.operations){const b=$('mode-'+operation.id);const active=operation.id===state.mode;b.classList.toggle('active',active);b.setAttribute('aria-pressed',String(active));}
    const root=$('legend');root.replaceChildren();
    channels.forEach((ch,i)=>{const appearance=assign(ch,i);const item=document.createElement('span');item.className='legend-item';const glyph=document.createElement('span');glyph.className='glyph';glyph.textContent=appearance.shape==='square'?'■':appearance.shape==='ring'?'◎':'●';glyph.style.color=appearance.color;item.appendChild(glyph);item.appendChild(document.createTextNode(ch.recipient));root.appendChild(item);});
  }
  D.operations.forEach(mode=>{$('mode-'+mode.id).addEventListener('click',()=>{state.mode=mode.id;updateText();render();});});
  $('same-rates').addEventListener('change',e=>{state.equalize=e.target.checked;updateText();render();});
  $('show-labels').addEventListener('change',e=>{state.labels=e.target.checked;render();});
  $('show-g02').addEventListener('change',e=>{state.g02=e.target.checked;render();});
  $('play').addEventListener('click',()=>{state.playing=!state.playing;$('play').textContent=state.playing?'Pause':'Play';});
  $('time').addEventListener('input',e=>{state.time=Number(e.target.value);state.playing=false;$('play').textContent='Play';render();});
  $('source-citations').textContent='G02: '+D.claims[0].statement+' G03: '+D.claims[1].statement+' G04 (context only): '+D.claims[2].statement+' Sources: '+D.textual_sources.map(s=>s.label).join('; ')+'.';
  window.__encodingStudy={getState:()=>({...state}),setMode:id=>{if(D.operations.some(x=>x.id===id)){state.mode=id;updateText();render();}}};
  function tick(now){const dt=Math.min(.07,Math.max(0,(now-state.last)/1000));state.last=now;
    if(state.playing){state.time=(state.time+dt)%16;$('time').value=state.time;render();}
    requestAnimationFrame(tick);
  }
  updateText();render();requestAnimationFrame(tick);
})();
