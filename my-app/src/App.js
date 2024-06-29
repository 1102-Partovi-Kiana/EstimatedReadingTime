import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [file, setFile] = useState(null);
  const [readingTime, setReadingTime] = useState('');

  const handleFileChange = (event) => {
    console.log('File changed:', event.target.files[0]);
    setFile(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!file) {
      console.log('No file selected');
      return;
    }
    console.log('Submitting file:', file);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://127.0.0.1:5001/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      console.log('Response:', response.data);
      setReadingTime(response.data.reading_time);
    } catch (error) {
      console.error('Error uploading file:', error);
    }
  };

  return (
    <div className="App">
      <h1>Upload a Text File to Calculate Reading Time</h1>
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={handleFileChange} />
        <button type="submit">Upload</button>
      </form>
      {readingTime && <p>Estimated reading time: {readingTime}</p>}
    </div>
  );
}

export default App;
