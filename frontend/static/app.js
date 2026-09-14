const chat = document.querySelector('#chat'), form = document.querySelector('#form'), input = document.querySelector('#input'), provider = document.querySelector('#provider');
const messages = [];
const $ = id => document.getElementById(id);

function add(role, text, meta='') {
  const e=document.createElement('article'); e.className='msg '+role;
  e.innerHTML=`<div class="msg-head"><b>${role==='user'?'YOU':'FISHYLLAMA'}</b><span>${meta}</span></div><p></p>`;
  e.querySelector('p').textContent=text; chat.appendChild(e); chat.scrollTop=chat.scrollHeight; return e;
}
function setState(state){
  $('voiceState').textContent=state.toUpperCase(); $('voiceOrb').dataset.state=state;
  document.body.dataset.state=state;
}
function speakAssistant(text){ if(window.FishyVoice) window.FishyVoice.speak(text); }

window.addEventListener('fishy:voice-state', e => setState(e.detail.speaking?'speaking':'ready'));
window.addEventListener('fishy:listen-state', e => setState(e.detail.listening?'listening':'ready'));
window.addEventListener('fishy:voice-error', () => setState('error'));
window.addEventListener('fishy:transcript', e => { $('liveTranscript').textContent=e.detail.text; if(e.detail.final){ input.value=e.detail.text; $('liveTranscript').textContent=''; form.requestSubmit(); } });

$('settingsButton').onclick=()=>{$('settingsPanel').classList.add('open');$('backdrop').classList.add('show');$('settingsPanel').setAttribute('aria-hidden','false')};
$('closeSettings').onclick=$('backdrop').onclick=()=>{$('settingsPanel').classList.remove('open');$('backdrop').classList.remove('show');$('settingsPanel').setAttribute('aria-hidden','true')};
$('clearChat').onclick=()=>{messages.length=0;chat.innerHTML='';setState('ready')};
$('micButton2').onclick=$('micButton').onclick=()=>window.FishyVoice?.listen();
$('stopSpeaking').onclick=()=>window.FishyVoice?.stop();
provider.onchange=()=>{$('engineLabel').textContent=provider.value.toUpperCase();};
$('voiceSelect')?.addEventListener('change',e=>{$('voiceLabel').textContent=e.target.options[e.target.selectedIndex].text.split(' (')[0].toUpperCase()});

input.addEventListener('keydown',e=>{if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();form.requestSubmit()}});
form.addEventListener('submit',async e=>{
  e.preventDefault(); const text=input.value.trim(); if(!text)return; input.value=''; $('liveTranscript').textContent='';
  messages.push({role:'user',content:text}); add('user',text); setState('thinking');
  const load=add('assistant','Thinking…','ROUTING');
  try{
    const r=await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({messages,provider:provider.value,model:'auto'})});
    const d=await r.json(); if(!r.ok) throw Error(d.detail||'Request failed');
    load.querySelector('p').textContent=d.content; load.querySelector('.msg-head span').textContent=`${d.provider} • ${d.model}`;
    messages.push({role:'assistant',content:d.content}); $('modeLabel').textContent='RESPONSE';
    speakAssistant(d.content); setState('speaking');
  }catch(err){load.querySelector('p').textContent='Error: '+err.message;load.classList.add('error');setState('error');window.FishyVoice?.beep('error')}
});

(async()=>{try{const r=await fetch('/api/health');const d=await r.json();$('statusDot').textContent=d.status.toUpperCase();}catch(_){$('statusDot').textContent='OFFLINE';$('statusDot').classList.remove('online')}})();
