import React, { useState } from 'react';
import '../App.css'; 

function TranslationDisplay() {
  const [customerText, setCustomerText] = useState('');
  const [agentText, setAgentText] = useState('');
  const [customerTranslation, setCustomerTranslation] = useState('');
  const [agentTranslation, setAgentTranslation] = useState('');

  const handleAudioUpload = (e, isCustomer) => {
    const formData = new FormData();
    formData.append('audio', e.target.files[0]);

    const url = isCustomer
      ? 'http://127.0.0.1:8000/api/process-customer-audio/'
      : 'http://127.0.0.1:8000/api/process-agent-audio/';

    fetch(url, {
      method: 'POST',
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        if (isCustomer) {
          setCustomerText(data.spanish_text);
          setCustomerTranslation(data.english_text);
          playAudio(data.english_audio_url);
        } else {
          setAgentText(data.english_text);
          setAgentTranslation(data.spanish_text);
          playAudio(data.spanish_audio_url);
        }
      });
  };

  const playAudio = (audioUrl) => {
    const audio = new Audio(audioUrl);
    audio.play();
  };

  return (
    <div className="translation-display">
      {/* <h1>Customer Service Translator</h1> */}

      <div className="upload-section">
        <h3>Upload Customer Audio (Spanish)</h3>
        <input type="file" accept="audio/*" onChange={(e) => handleAudioUpload(e, true)} />
      </div>

      <div className="upload-section">
        <h3>Upload Agent Audio (English)</h3>
        <input type="file" accept="audio/*" onChange={(e) => handleAudioUpload(e, false)} />
      </div>

      <div className="translations">
        <div className="text-block">
          <h4>Customer's Spanish Text:</h4>
          <p>{customerText}</p>
          <h4>Translated English Text:</h4>
          <p>{customerTranslation}</p>
        </div>
        <div className="text-block">
          <h4>Agent's English Text:</h4>
          <p>{agentText}</p>
          <h4>Translated Spanish Text:</h4>
          <p>{agentTranslation}</p>
        </div>
      </div>

      <div className="audio-player">
        <audio controls>
          <source src="http://127.0.0.1:8000/media/customer_audio.wav" type="audio/wav" />
          Your browser does not support the audio element.
        </audio>
      </div>
    </div>
  );
}

export default TranslationDisplay;
