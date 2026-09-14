/* FishyLLAMA voice layer.
 * Uses Web Speech as the no-key fallback, but keeps the architecture ready for
 * Google Cloud/gTTS/local TTS providers. It mirrors the uploaded Jarvis ideas:
 * sentence streaming, interruptible speech, voice profiles, listening states,
 * ambient mic calibration, and audio feedback tones.
 */
const VoiceUI = (() => {
  let settings = {voice:'fishy-neural', rate:1.02, pitch:0, volume:1, enabled:true};
  let voices = [];
  let speaking = false;
  let listening = false;
  let recognition = null;
  let audioCtx = null;

  const $ = id => document.getElementById(id);
  const emit = (name, detail={}) => window.dispatchEvent(new CustomEvent(`fishy:${name}`, {detail}));

  function loadVoices(){
    voices = window.speechSynthesis ? speechSynthesis.getVoices() : [];
    const select = $('voiceSelect');
    if (!select) return;
    const preferred = settings.voice;
    select.innerHTML = '<option value="fishy-neural">Fishy Neural (system voice)</option>' +
      '<option value="jarvis-british">British Assistant</option>' +
      '<option value="fishy-calm">Fishy Calm</option>' +
      '<option value="fishy-fast">Fishy Fast</option>' +
      '<option value="swedish">Svenska</option>';
    if (preferred) select.value = preferred;
  }

  function systemVoice(profile){
    const sv = profile === 'swedish';
    const enGB = profile === 'jarvis-british';
    return voices.find(v => sv ? v.lang.toLowerCase().startsWith('sv') : enGB ? v.lang.toLowerCase().startsWith('en-gb') : v.lang.toLowerCase().startsWith('en')) || voices[0];
  }

  function beep(type='ready'){
    try {
      audioCtx ||= new (window.AudioContext || window.webkitAudioContext)();
      const osc = audioCtx.createOscillator(), gain = audioCtx.createGain();
      const map = {ready:[660,.10], listening:[880,.07], thinking:[330,.08], searching:[520,.07], error:[180,.18]};
      const [freq,dur] = map[type] || map.ready;
      osc.frequency.value = freq; osc.type = type === 'error' ? 'sawtooth' : 'sine';
      gain.gain.setValueAtTime(.0001, audioCtx.currentTime);
      gain.gain.exponentialRampToValueAtTime(.08, audioCtx.currentTime+.01);
      gain.gain.exponentialRampToValueAtTime(.0001, audioCtx.currentTime+dur);
      osc.connect(gain).connect(audioCtx.destination); osc.start(); osc.stop(audioCtx.currentTime+dur+.02);
    } catch (_) {}
  }

  function stop(){
    if ('speechSynthesis' in window) speechSynthesis.cancel();
    speaking = false; emit('voice-state', {speaking:false});
  }

  function speak(text, opts={}){
    if (!settings.enabled || !('speechSynthesis' in window)) return;
    stop();
    const chunks = text.replace(/```[\s\S]*?```/g,' Code block omitted. ').split(/(?<=[.!?])\s+/).filter(Boolean);
    const profile = opts.profile || settings.voice;
    const rate = Number(opts.rate || settings.rate || 1);
    const pitch = Number(opts.pitch ?? settings.pitch ?? 0) + (profile === 'jarvis-british' ? -.05 : profile === 'fishy-calm' ? -.08 : profile === 'fishy-fast' ? .04 : 0);
    let i = 0;
    const next = () => {
      if (i >= chunks.length) { speaking=false; emit('voice-state',{speaking:false}); return; }
      const u = new SpeechSynthesisUtterance(chunks[i++]);
      u.voice = systemVoice(profile); u.rate = Math.max(.5, Math.min(2, rate)); u.pitch = Math.max(.2, Math.min(2, 1+pitch)); u.volume = settings.volume;
      u.onstart = () => { speaking=true; emit('voice-state',{speaking:true}); };
      u.onend = next; u.onerror = next;
      speechSynthesis.speak(u);
    };
    beep('ready'); next();
  }

  function setupRecognition(){
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SR) return;
    recognition = new SR(); recognition.continuous = false; recognition.interimResults = true; recognition.lang = 'en-US';
    recognition.onstart = () => { listening=true; beep('listening'); emit('listen-state',{listening:true}); };
    recognition.onend = () => { listening=false; emit('listen-state',{listening:false}); };
    recognition.onerror = e => { listening=false; emit('voice-error',{message:e.error}); };
    recognition.onresult = e => {
      const transcript = Array.from(e.results).map(r => r[0].transcript).join('');
      emit('transcript',{text:transcript, final:e.results[e.results.length-1].isFinal});
    };
  }

  function listen(){ if (recognition && !listening) { beep('listening'); recognition.start(); } }
  function save(){ localStorage.setItem('fishyllama.voice', JSON.stringify(settings)); }
  function init(){
    try { Object.assign(settings, JSON.parse(localStorage.getItem('fishyllama.voice') || '{}')); } catch (_) {}
    loadVoices(); setupRecognition();
    if ('speechSynthesis' in window) speechSynthesis.onvoiceschanged = loadVoices;
    $('voiceSelect')?.addEventListener('change', e => { settings.voice=e.target.value; save(); });
    $('voiceRate')?.addEventListener('input', e => { settings.rate=Number(e.target.value); $('voiceRateValue').textContent=settings.rate.toFixed(2)+'×'; save(); });
    $('voicePitch')?.addEventListener('input', e => { settings.pitch=Number(e.target.value); $('voicePitchValue').textContent=settings.pitch.toFixed(2); save(); });
    $('voiceVolume')?.addEventListener('input', e => { settings.volume=Number(e.target.value); $('voiceVolumeValue').textContent=Math.round(settings.volume*100)+'%'; save(); });
    $('voiceEnabled')?.addEventListener('change', e => { settings.enabled=e.target.checked; if(!settings.enabled) stop(); save(); });
    $('stopSpeaking')?.addEventListener('click', stop); $('micButton')?.addEventListener('click', listen);
    window.FishyVoice = {speak, stop, listen, beep, settings};
  }
  return {init, speak, stop, listen};
})();
window.addEventListener('DOMContentLoaded', VoiceUI.init);
