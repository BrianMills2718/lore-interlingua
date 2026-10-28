"""Assemble an integrated, art-directed offline film from Experiment 012's scene,
retaining its persistent worlds and Earth illustration while extending the
source-scoped operations and figurative surface imagery of Experiment 011.

This file is an editorial animation build, NOT an interlingua-to-film compiler.
"""
from pathlib import Path
import re, json

ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent/'012-ray-of-creation'/'film.html'
if not BASE.exists():BASE=ROOT.parent/'Gurdjieff_Film_012'/'film.html'
s=BASE.read_text()

def repl_func(source,name,replacement):
    start=source.index('function '+name+'(')
    brace=source.index('{',start)
    d=0
    for k in range(brace,len(source)):
        if source[k]=='{':d+=1
        elif source[k]=='}':
            d-=1
            if d==0:
                return source[:start]+replacement+source[k+1:]
    raise ValueError(name)

def repl_array(source, const_name, new_literal):
    start=source.index('const '+const_name+'=')
    end=source.index('];',start)+2
    return source[:start]+ 'const '+const_name+'='+new_literal+';'+source[end:]

DURATION=176
cues=[
 (0,10,'THE LIVING INTERVAL',"Gurdjieff's Ray of Creation, as recorded by P. D. Ouspensky."),
 (10,22,'ONE SELECTED RAY','Seven successive world orders—not a beam of physical light.'),
 (22,38,'THE LAW OF THREE','Active, passive and neutralizing forces meet: three roles in every phenomenon.'),
 (38,52,'ORDERS OF LAWS','The numbers count governing orders of forces, not named laboratory rules.'),
 (52,65,'A DEEPENING ORDER','Lower worlds bear more laws; the teaching calls their life more mechanical.'),
 (65,79,'THE PLANETARY WORLD','A selected world of planets belongs to the larger order.'),
 (79,93,'THE LAW OF SEVEN','The cosmic octave has an interval between the planets and Earth.'),
 (93,106,'THE LIVING INTERMEDIARY','Organic life fills that interval and receives planetary influences.'),
 (106,119,'THE SENSITIVE FILM','Plants, animals and people form Earth’s living organ of perception.'),
 (119,132,'DIFFERENT LIVING RECEIVERS','Grassland and a human gathering receive different influences, in this account.'),
 (132,144,'RECEPTION AND MEDIATION','Influence reaches life; a distinct living response moves inward to Earth.'),
 (144,156,'WHAT IS BEING TRANSMITTED?','The source calls these planetary influences; their physical nature is unspecified.'),
 (156,170,'RADIATION OUTWARD','Life also radiates differently toward Sun, planets and Moon.'),
 (170,176.1,'ONE CONNECTED COSMOLOGY','Hierarchy, interval, living mediation and reciprocal radiations belong together.')
]
clock=[dict(at=a,to=b,title=title,line=line) for a,b,title,line in cues]
s=repl_array(s,'clockData',json.dumps(clock,ensure_ascii=False,separators=(',',':')))
s=s.replace('T=124,TAU=',f'T={DURATION},TAU=')
s=s.replace('max="124"','max="176"').replace('0:00 / 2:04','0:00 / 2:56').replace(' / 2:04`',' / 2:56`')
s=s.replace('<title>The Ray of Creation — Lore Interlingua / Gurdjieff</title>','<title>The Living Interval — Gurdjieff / Lore Interlingua</title>')
s=s.replace('Animated source-scoped visual treatment of Gurdjieff\'s seven worlds and progressively increasing orders of laws','The Living Interval: continuous illustrated cosmology of Gurdjieff with seven worlds, the Law of Three, Law of Seven, and organic-life mediation')
s=s.replace('Gurdjieff via P. D. Ouspensky. Selected ray: Absolute → All Worlds → All Suns → Sun → Planets → Earth → Moon. Law counts are source-scoped; paths, motion and constraint patterns are illustrative, not astronomical measurements.', 'Gurdjieff via P. D. Ouspensky. The Ray of Creation, Law of Three, cosmic octave, and organic life are shown within one persistent world. The symbols for laws and influences are interpretive metaphors—not identified cosmic substances or physical laws.')

camera_js=r'''function cameraAt(tt){const K=[
[0,665,1420,.234],[8,663,1420,.242],
[14,644,140,.81],[21,800,400,.78],
[30,875,532,.86],[38,735,710,.75],
[45,432,984,1.01],[52,580,1190,.85],
[59,792,1430,1.15],[65,628,1580,.85],
[72,444,1843,1.10],[79,593,1990,.80],
[87,635,2090,.83],[93,717,2170,1.08],
[101,752,2279,1.50],[109,670,2210,1.79],
[118,646,2175,2.04],[126,850,2225,2.05],
[133,780,2286,1.64],[144,751,2314,1.40],
[149,674,2195,.91],[156,643,2100,.41],
[168,643,2100,.40],[175,650,1438,.237],[176,650,1438,.237]
];for(let i=0;i<K.length-1;i++){let a=K[i],b=K[i+1];if(tt<=b[0]){let u=ease((tt-a[0])/(b[0]-a[0]));return{x:mix(a[1],b[1],u),y:mix(a[2],b[2],u),s:mix(a[3],b[3],u)}}}return{x:650,y:1438,s:.237};}'''
s=repl_func(s,'cameraAt',camera_js)

selected_js=r'''function drawSelectedRay(tt,cam){
 for(let i=0;i<worlds.length-1;i++){
  let a=worlds[i],b=worlds[i+1],A=[a.x,a.y+23],D=[b.x,b.y-20],B=[a.x+85,a.y+177],P2=[b.x-95,b.y-188];
  if((a.y+b.y)/2<cam.y-950/cam.s||(a.y+b.y)/2>cam.y+950/cam.s)continue;
  // Stable selection line, NOT a stream. The octave interval is annotated elsewhere.
  let rr=i===4?.57:1;bezier(A,B,P2,D,C.gold,13,.021*rr);
  bezier(A,B,P2,D,C.gold,1.2,.22*rr);
  for(let k=-1;k<=1;k+=2){let R=[a.x+200*k,a.y+330],Q=[a.x+150*k,a.y+145];
   bezier([a.x,a.y+18],[a.x+68*k,a.y+145],Q,R,C.violet,.85,.045);}
 }
}'''
s=repl_func(s,'drawSelectedRay',selected_js)

life_js=r'''
// LIVING SURFACE: inherited semantically and artistically from Experiment 011.
// Forms are animals, plants, and people, not a generic phosphorescent ring.
function lifeGrass(i,tt){c.save();c.rotate(.03*Math.sin(tt*.59+i));for(let j=-2;j<=2;j++){
 let h=12+(i+j+95)%5*4;let col=j%2?C.mint:'#c3b48c';c.strokeStyle=col;c.lineWidth=1.35;c.beginPath();c.moveTo(j*2.5,0);
 c.quadraticCurveTo(j*2.4-2,-h*.5,j*3.1,-h);c.stroke();}c.restore();}
function lifePlant(i,tt){let h=25+(i%5)*5;c.save();c.rotate(.035*Math.sin(tt*.33+i));
 c.strokeStyle=i%4===0?'#b1a47a':'#83baa0';c.lineWidth=2.3;c.beginPath();c.moveTo(0,4);c.quadraticCurveTo(-3,-h*.46,1,-h);c.stroke();
 for(let j=0;j<4;j++){let y=-h*(.19+j*.19),side=j%2?1:-1;let dx=side*(7+j*.8);
 c.beginPath();c.moveTo(0,y);c.quadraticCurveTo(dx*1.4,y-4,dx,y-13);c.quadraticCurveTo(dx*.7,y-5,0,y+1);c.fillStyle=j%3===0?'#cfbd86':j%3===1?'#77a78b':'#aac7a2';c.fill();}
 disc(1,-h,1.8,'#dfcca2');c.restore();}
function lifeTree(i,tt){c.save();c.rotate(.018*Math.sin(tt*.25+i));let h=48+(i%4)*9;c.lineCap='round';
 c.strokeStyle='#9c8c6e';c.lineWidth=5;c.beginPath();c.moveTo(0,2);c.bezierCurveTo(2,-h*.35,-2,-h*.63,0,-h);c.stroke();
 for(let j=0;j<7;j++){let yy=-h*(.48+j*.075),side=j%2?1:-1,dx=side*(17+(j%3)*4);
 c.lineWidth=1.8;c.beginPath();c.moveTo(0,yy+5);c.quadraticCurveTo(dx*.55,yy-7,dx,yy-17);c.stroke();
 disc(dx,yy-17,5.8+(j%2)*2.3,rgba(j%3===0?'#b6bb8e':j%3===1?'#81b199':'#6f9f8b',.87));
 disc(dx-5,yy-21,3.8,rgba('#c2c6a3',.60));}
 c.restore();}
function lifeHuman(i,tt){c.save();c.translate(0,.6*Math.sin(tt*.55+i*1.3));c.rotate(.016*Math.sin(tt*.31+i));
 const col=['#ac9d89','#99b1a5','#b59277','#a7a4b0'][i%4];
 disc(0,-26,5.5,'#dabf99');c.fillStyle=col;c.beginPath();c.moveTo(-6,-18);c.quadraticCurveTo(0,-23,6,-18);c.lineTo(7,-7);c.lineTo(-7,-7);c.closePath();c.fill();
 c.strokeStyle='#c1bbae';c.lineWidth=2;c.lineCap='round';c.beginPath();c.moveTo(-3,-7);c.lineTo(-4,2);c.moveTo(3,-7);c.lineTo(4,2);
 c.moveTo(-6,-17);c.lineTo(-11,-9);c.moveTo(6,-17);c.lineTo(11,-10);c.stroke();c.restore();}
function lifeDeer(tt){c.save();c.rotate(.013*Math.sin(tt*.48));c.fillStyle='#c7ac83';c.strokeStyle='#c7ac83';c.lineCap='round';
 c.beginPath();c.ellipse(0,-14,16,7,0,0,TAU);c.fill();
 c.beginPath();c.moveTo(11,-18);c.lineTo(19,-29);c.lineTo(29,-34);c.lineTo(36,-31);c.lineTo(34,-27);c.lineTo(27,-25);c.lineTo(20,-11);c.fill();
 c.lineWidth=2.6;for(let xx of [-9,1,11]){c.beginPath();c.moveTo(xx,-10);c.lineTo(xx+2,0);c.stroke();}
 c.strokeStyle='#d7c29f';c.lineWidth=1.4;c.beginPath();c.moveTo(26,-34);c.lineTo(23,-49);c.moveTo(23,-45);c.lineTo(15,-49);c.moveTo(24,-43);c.lineTo(33,-48);c.stroke();
 disc(32,-30,1.1,'#1c2a33');c.restore();}
function livingSurface(w,tt){const{x,y,r}=w;
 let glow=ease((tt-86)/8); // always living; light response gains emphasis with the camera.
 c.save();c.strokeStyle=rgba('#accda1',.28+.17*glow);c.lineWidth=4;
 c.beginPath();c.arc(x,y,r+4,-2.94,-.20);c.stroke();c.restore();
 for(let i=0;i<60;i++){let a=mix(-2.92,-.22,i/59),xx=x+Math.cos(a)*(r+3),yy=y+Math.sin(a)*(r+3);
 c.save();c.translate(xx,yy);c.rotate(a+Math.PI/2);
 if(a< -2.21){if(i%4===0)lifeTree(i,tt);else lifePlant(i,tt)}
 else if(a< -1.33){if(i%2===0)lifeGrass(i,tt);if(i%5===0)lifePlant(i,tt)}
 else if(a< -.55){if(i%2===0)lifeHuman(i,tt);else if(i%5===0)lifeGrass(i,tt)}
 else{if(i%4===0)lifeTree(i,tt);else lifePlant(i,tt)}c.restore();
 }
 if(tt>=108&&tt<136){let a=ease((tt-108)/3)*(1-ease((tt-133)/3));
 text('GRASSLAND',x-70,y-r-60,'12px system-ui','#cbd6af','center',a*.85);
 text('HUMAN GATHERING',x+112,y-r-60,'12px system-ui','#dbc3c0','center',a*.86);}
 let a=-2.43;c.save();c.translate(x+Math.cos(a)*(r+5),y+Math.sin(a)*(r+5));c.rotate(a+Math.PI/2);c.scale(.77,.77);lifeDeer(tt);c.restore();
 // A clearly selective metaphor of Earth's 'organ of perception'; the globe has no literal eye.
 let sig=ease((tt-132)/5)*(1-ease((tt-163)/5));if(sig>.005){c.save();c.globalAlpha=.33*sig;
 let ey=y+r*.19,ex=x+8;c.strokeStyle='#d7e4bc';c.lineWidth=1.35;c.beginPath();c.moveTo(ex-65,ey);c.quadraticCurveTo(ex,ey-47,ex+65,ey);
 c.quadraticCurveTo(ex,ey+46,ex-65,ey);c.stroke();ring(ex,ey,16,'#d7e4bc',1.4,.75);disc(ex,ey,4,'#d7e4bc');c.restore();}
}
function interpBezier(A,B,P2,D,u){return cubic(A,B,P2,D,u)}
function movingGlyph(x,y,col,kind,alpha=1,r=2.5){c.save();c.globalAlpha=alpha;gradientDisc(x,y,r*6,col,.20);
 if(kind==='circle')disc(x,y,r,col);
 else if(kind==='diamond'){c.translate(x,y);c.rotate(Math.PI/4);c.fillStyle=col;c.fillRect(-r,-r,r*2,r*2)}
 else if(kind==='ring'){ring(x,y,r+1,col,1.5,.93)}c.restore();}
function sourceInfluences(tt){if(tt<79)return;let fade=ease((tt-79)/6);let p=worlds[4],w=worlds[5],R=w.r;
 const entries=[{src:[p.x-98,p.y-20],a:-2.37,col:C.teal},{src:[p.x-14,p.y+42],a:-1.63,col:C.teal},{src:[p.x+50,p.y-64],a:-.84,col:C.violet}];
 for(let j=0;j<entries.length;j++){let z=entries[j],dst=[w.x+Math.cos(z.a)*(R+6),w.y+Math.sin(z.a)*(R+6)];
 let A=z.src,D=dst,B=[mix(A[0],D[0],.38)-48,mix(A[1],D[1],.42)+40],P=[mix(A[0],D[0],.65)+42,mix(A[1],D[1],.67)-30];
 for(let k=0;k<12;k++){let u=((tt*.086+j*.23+k/12)%1);let pos=interpBezier(A,B,P,D,u);movingGlyph(...pos,z.col,'circle',fade*(.23+.8*ease(Math.min(u,1-u)*5)),2.05);}
 let pulse=.65+.35*Math.sin(tt*.95+j*1.4);gradientDisc(...dst,30,z.col,.18*pulse*fade);
 }
}
function mediatedResponse(tt){if(tt<93)return;let alpha=ease((tt-93)/7),w=worlds[5],R=w.r;
 const sets=[-2.37,-2.05,-1.72,-1.47,-1.18,-.92,-.7];
 for(let j=0;j<sets.length;j++){let a=sets[j],skin=[w.x+Math.cos(a)*(R+3),w.y+Math.sin(a)*(R+3)],core=[w.x+Math.cos(a)*R*.50,w.y+Math.sin(a)*R*.50];
 let phase=.5+.5*Math.sin(tt*.72+j*1.7);gradientDisc(...skin,23,j>4?C.violet:C.mint,alpha*.08+alpha*phase*.12);
 let u=(tt*.22+j*.16)%1;if(u<.79){let at=u/.79,pos=[mix(skin[0],core[0],at),mix(skin[1],core[1],at)];movingGlyph(...pos,j>4?'#cfb8d1':'#b7e3bb','circle',alpha*(1-ease((u-.62)/.2)),2.9);}
 }
}
function outgoingRadiations(tt){if(tt<143)return;let alpha=ease((tt-143)/9),earth=worlds[5],R=earth.r;
 const out=[{a:-2.17,to:worlds[3],col:C.violet,type:'diamond',B:[505,1910],P:[540,1550]},
 {a:-1.10,to:worlds[4],col:'#a1bed9',type:'ring',B:[835,2040],P:[595,1880]},
 {a:.52,to:worlds[6],col:C.gold,type:'circle',B:[1010,2480],P:[820,2660]}];
 for(let i=0;i<3;i++){let z=out[i],A=[earth.x+Math.cos(z.a)*(R+7),earth.y+Math.sin(z.a)*(R+7)],D=[z.to.x,z.to.y];
 // Equal normalized timing across recipient classes. Difference of kind remains graphic, not kinetic physics.
 for(let k=0;k<14;k++){let u=(tt*.095+k/14+i*.08)%1;let p=interpBezier(A,z.B,z.P,D,u);
 movingGlyph(...p,z.col,z.type,alpha*(.35+.65*Math.sin(Math.PI*u)),2.5);}
 gradientDisc(...D,z.to.r*.72,z.col,.06*alpha*(.65+.35*Math.sin(tt*.22+i)));
 }
}
function sourceGeometry(tt){
 // Three-force roles are indicated in a research-style graphic attached to the selected world,
 // not asserted to be three colored substances occupying an actual astronomical location.
 if(tt>=20&&tt<=39){let w=worlds[1],alpha=ease((tt-20)/3)*(1-ease((tt-36)/3));
 let a0=-Math.PI/2;const labels=['ACTIVE','PASSIVE','NEUTRALIZING'];const cols=['#e3cba5','#a5d5c4','#c6b0d8'];
 for(let i=0;i<3;i++){let a=a0+i*TAU/3,rr=206,px=w.x+Math.cos(a)*rr,py=w.y+Math.sin(a)*rr,
 B=[mix(px,w.x,.55),mix(py,w.y,.55)-16],P=[mix(px,w.x,.83),mix(py,w.y,.83)+17];
 let n=clamp(((tt-21)*.135+i*.23)%1,0,1);let pos=interpBezier([px,py],B,P,[w.x,w.y],n);
 movingGlyph(...pos,cols[i],'circle',alpha*.9,3.1);
 c.save();c.globalAlpha=alpha*.92;text(labels[i],px,py+(i===0?-18:18),'12px system-ui',cols[i],'center');c.restore();}
 gradientDisc(w.x,w.y,64,C.paper,alpha*(.08+.12*(.5+.5*Math.sin(tt*.67))));
 }
}
function octaveInterval(tt){if(tt<76||tt>106)return;let a=ease((tt-76)/4)*(1-ease((tt-103)/3));
 const x=668,y=2050;
 c.save();c.globalAlpha=a;line(x-79,y,x-19,y,C.gold,2,.74);line(x+19,y,x+79,y,C.gold,2,.74);
 ring(x,y,15,C.gold,1,.5);
 text('OCTAVE INTERVAL',x,y-37,'15px Georgia',C.gold,'center',.94);
 text('PLANETS  /  ORGANIC LIFE  /  EARTH',x,y+30,'11px system-ui',C.paper,'center',.72);
 c.restore();}
'''
insert_loc=s.index('function moon(')
s=s[:insert_loc]+life_js+'\n'+s[insert_loc:]

# The Earth was originally a small cameo. Replace it with the same persistent world
# carrying the richer living cast of Film 011; world-space coords are unchanged.
earth_js=r'''function earth(w,tt){const{x,y,r}=w;gradientDisc(x,y,r*1.85,C.mint,.17);
 c.save();c.beginPath();c.arc(x,y,r,0,TAU);c.clip();
 if(EARTH_TEXTURE.complete&&EARTH_TEXTURE.naturalWidth){c.drawImage(EARTH_TEXTURE,x-r,y-r,2*r,2*r)}
 else{let g=c.createRadialGradient(x-r*.4,y-r*.4,0,x,y,r);g.addColorStop(0,'#4b8490');g.addColorStop(1,'#173148');disc(x,y,r,g);}
 c.restore();ring(x,y,r,C.mint,1.25,.42);
 livingSurface(w,tt);
}'''
s=repl_func(s,'earth',earth_js)
# Append operation rendering into persistent world viewport after bodies have been drawn.
s=s.replace(' drawName(w,i,tt,a);\n }\n c.restore();}',
''' drawName(w,i,tt,a);
 }
 sourceGeometry(tt);octaveInterval(tt);sourceInfluences(tt);mediatedResponse(tt);outgoingRadiations(tt);
 c.restore();}''')
# Visually softer law ornament: still a hypothesis, avoid 96 objects. Existing source 012 motif retained.
# Caption overlay at lower quarter; space for mature, readable copy.
cap_js=r'''function uiCaption(tt){let cue=clockData.find(q=>tt>=q.at&&tt<q.to)||clockData.at(-1),a=ease((tt-cue.at)/.70)*(1-ease((tt-(cue.to-.7))/.80));
 if(tt>=156&&tt<170){
 // Keep Sun, planets and Moon unobscured during the integrated outward relation.
 let g=c.createLinearGradient(0,515,0,720);g.addColorStop(0,'rgba(2,9,17,0)');g.addColorStop(.4,'rgba(2,9,17,.85)');g.addColorStop(1,'rgba(2,9,17,.97)');c.fillStyle=g;c.fillRect(0,515,535,205);
 c.save();c.globalAlpha=a;text(cue.title,72,578,'29px Georgia',C.paper,'left');
 text('Life radiates differently toward the Sun,',72,618,'17px Georgia',C.paper,'left');
 text('planets and Moon.',72,643,'17px Georgia',C.paper,'left');c.restore();
 }else{
 let shade=c.createLinearGradient(0,498,0,720);shade.addColorStop(0,'rgba(2,9,17,0)');shade.addColorStop(.42,'rgba(2,9,17,.69)');shade.addColorStop(1,'rgba(2,9,17,.99)');c.fillStyle=shade;c.fillRect(0,498,1280,222);
 c.save();c.globalAlpha=a;text(cue.title,72,577,'30px Georgia',C.paper,'left');text(cue.line,72,618,'18px Georgia',C.paper,'left');c.restore();}
 line(74,547,194,547,C.gold,2,.58);
 text('GURDJIEFF  /  THE LIVING INTERVAL',71,39,'bold 13px system-ui',C.paper,'left',.88);
 text('THE RAY OF CREATION  ·  A SOURCE-SCOPED VISUAL INTERPRETATION',71,62,'11px system-ui',C.cold,'left',.63);
 if(tt<8||tt>170){let A=tt<8?1-ease((tt-6.5)/1.5):ease((tt-170)/2.5);text('ONE CONTINUOUS COSMOLOGY',71,122,'20px Georgia',C.gold,'left',A*.7)}
 if(tt>=39&&tt<68){let a2=ease((tt-39)/2)*(1-ease((tt-66)/2));text('ORDERS OF LAWS ≠ PHYSICAL RULEBOOK',72,170,'11px system-ui',C.gold,'left',a2*.75);}
}'''
s=repl_func(s,'uiCaption',cap_js)
hud_js=r'''function hud(tt,cam){const y=158;
 c.save();c.fillStyle='rgba(6,15,25,.54)';c.beginPath();c.roundRect(1063,112,200,350,12);c.fill();
 text('SELECTED WORLD ORDERS',1077,137,'bold 10px system-ui',C.paper,'left',.82);
 for(let i=0;i<worlds.length;i++){let w=worlds[i],yy=y+i*42,focus=worldFocusAlpha(w,cam),hi=focus>.64;
 line(1087,yy,1087,yy+38,C.gold,1,.18);
 disc(1087,yy,hi?3.8:2.4,rgba(hi?C.gold:C.cold,hi?.95:.35));
 text(String(w.laws).padStart(2,'0'),1102,yy,'bold 13px system-ui',hi?C.gold:C.cold,'left',hi?.95:.65);
 let short=['Absolute','All Worlds','All Suns','Sun','Planets','Earth','Moon'][i];
 text(short,1135,yy,'12px Georgia',C.paper,'left',hi?.95:.62);}
 c.restore();}'''
s=repl_func(s,'hud',hud_js)
# A zero-variance per-frame draw promise, used by headless renderer.
s=s.replace('let cam=cameraAt(t);cosmicLayer(t,cam);grain(t);uiCaption(t);hud(t,cam);','let cam=cameraAt(t);cosmicLayer(t,cam);grain(t);uiCaption(t);hud(t,cam);')
s=s.replace("window.renderDuration=T;","window.renderDuration=T;window.FILM_013_CUES=clockData;")
# A safety comment distinguishing foreground annotations from actual cosmos.
s=s.replace('let t=0,playing=true,last=performance.now();','let t=0,playing=true,last=performance.now();\n// Film 013 builds meaning cumulatively; captions name unmeasured mechanisms as unmeasured.')
(ROOT/'film.html').write_text(s)
(ROOT/'cues.json').write_text(json.dumps(clock,indent=2,ensure_ascii=False)+'\n')

def fmt(x):
    ms=int(round(x*1000));return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
sub=[]
for i,(a,b,title,line) in enumerate(cues,1):
    sub.extend([str(i),fmt(a)+' --> '+fmt(min(b,DURATION)),title+' — '+line,''])
(ROOT/'captions.srt').write_text('\n'.join(sub))
print('Wrote film.html',len(s),'bytes',len(cues),'caption units')
