import './App.css';
import React, { useState } from 'react';

function App() {
  const [code, setCode] = useState('');
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setCode(e.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      let res = await fetch('http://localhost:5000/api/code', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          code,
        }),
      });
      let data = await res.json();
      if (res.status === 200) {
        setError('');
        console.log('SUCCESS', data);
      } else {
        setError(data.message);
      }
    } catch (e) {
      console.log('ERROR', e);
    }
  };
  return (
    <div className="App">
      <div className="App-container">
        <form onSubmit={handleSubmit} className="Code-editor">
          <p className="Text-title">Code Editor</p>
          <textarea type="text" className="Code-input" value={code} onChange={handleChange} />
          <button type="submit" className="Code-submit">
            Submit Code
          </button>
        </form>
        <div className="Code-output">
          <p className="Text-title">Output</p>
          <div className="Output-area">
            {error && <p className="Error-message">{error}</p>}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
