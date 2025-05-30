import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Upload.css';

function Upload() {
  const [file, setFile] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const { getRootProps, getInputProps } = useDropzone({
    accept: 'image/*',
    maxFiles: 1,
    onDrop: acceptedFiles => {
      setFile(acceptedFiles[0]);
    }
  });

  const handleSubmit = async () => {
  if (!file) return;
  
  setIsLoading(true);
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await axios.post('http://localhost:5000/predict', formData);
    
    // Read file for preview
    const reader = new FileReader();
    reader.onloadend = () => {
      navigate('/results', { 
        state: { 
          prediction: {
            ...response.data,
            image: response.data.image || reader.result
          }
        } 
      });
    };
    reader.readAsDataURL(file);

  } catch (error) {
    console.error('Error:', error);
    alert('Error processing image. Please try again.');
  } finally {
    setIsLoading(false);
  }
};

  return (
    <div className="upload-container">
      <h2>Upload Plant Image</h2>
      <div {...getRootProps({ className: 'dropzone' })}>
        <input {...getInputProps()} />
        {file ? (
          <div className="preview-container">
            <img 
              src={URL.createObjectURL(file)} 
              alt="Preview" 
              className="image-preview"
            />
            <p>{file.name}</p>
          </div>
        ) : (
          <p>Drag & drop an image here, or click to select</p>
        )}
      </div>
      <button 
        className="submit-button"
        onClick={handleSubmit}
        disabled={!file || isLoading}
      >
        {isLoading ? 'Processing...' : 'Identify Plant'}
      </button>
    </div>
  );
}

export default Upload;