import React, { useState, useRef } from "react";

export default function LensPage() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [imageFile, setImageFile] = useState(null);
  const inputFileRef = useRef(null);  


  // Trigger hidden file input for upload
  const handleUploadClick = () => {
    inputFileRef.current.click();
  };

  // Set preview & file
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      const imageURL = URL.createObjectURL(file);
      setSelectedImage(imageURL);
      setImageFile(file);
    }
  };

  // Send to backend
  const handleSendToBackend = async () => {
    if (!imageFile) return alert("No image selected!");

    const formData = new FormData();
    formData.append("file", imageFile); //"image"

    try {
      const res = await fetch("http://127.0.0.1:8000/detect-attributes", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();

      if (!data.category || !data.attributes) {
        alert("Detection failed.");
        return;
      }

      const urlRes = await fetch("http://127.0.0.1:8000/generate-url", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          category: data.category,
          attributes: data.attributes,
        }),
      });

      const urlData = await urlRes.json();
      if (urlData.url) {
        window.location.href = urlData.url;
      } else {
        alert("URL generation failed.");
      }

    } catch (e) {
      alert("Error: " + e.message);
    }
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.heading}>Visual Search Lens</h1>
      <p style={styles.subheading}>Choose how you'd like to input an image:</p>

      {/* Upload & Camera Buttons */}
      <div style={styles.buttonContainer}>
        <button onClick={handleUploadClick} style={styles.button}>Upload Image</button>
        <input
          type="file"
          accept="image/*"
          ref={inputFileRef}
          style={{ display: "none" }}
          onChange={handleFileChange}
        />

        <label htmlFor="cameraInput" style={styles.button}>Take a Photo</label>
        <input
          type="file"
          accept="image/*"
          capture="environment"
          id="cameraInput"
          style={{ display: "none" }}
          onChange={handleFileChange}
        />
      </div>

      {/* Preview + Send Button */}
      {selectedImage && (
        <div style={{ marginTop: "2rem", textAlign: "center" }}>
          <h3 style={styles.subheading}>Preview:</h3>
          <img
            src={selectedImage}
            alt="Preview"
            style={{ maxWidth: "100%", height: "auto", borderRadius: "12px" }}
          />
          <div style={{ display: "flex", justifyContent: "center" }}>
            <button onClick={handleSendToBackend} style={styles.sendButton}>
              Send Image
            </button>
          </div>
        </div>
      )}

    </div>
  );
}

// Inline styles with responsiveness
const styles = {
  container: {
    padding: "1.5rem",
    fontFamily: "system-ui, sans-serif",
    textAlign: "center",
  },
  heading: {
    fontSize: "1.8rem",
    marginBottom: "0.5rem",
  },
  subheading: {
    fontSize: "1rem",
    marginBottom: "1rem",
  },
  buttonContainer: {
    display: "flex",
    flexDirection: "column", // Stack by default (mobile-first)
    gap: "0.75rem",
    alignItems: "center",
  },
  button: {
    padding: "0.8rem 1.2rem",
    fontSize: "1rem",
    borderRadius: "8px",
    border: "1px solid #0071dc",
    backgroundColor: "#0071dc",
    color: "white",
    width: "100%",
    maxWidth: "240px",
  },
  sendButton: {
  padding: "0.75rem 1.5rem",
  fontSize: "1rem",
  backgroundColor: "#28a745",
  color: "white",
  border: "none",
  borderRadius: "8px",
  cursor: "pointer",
  marginTop: "1rem",
  },
  resultPrompt: {
    fontSize: "1rem",
    marginBottom: "1rem",
  },
  objectButtonContainer: {
    display: "flex",
    flexWrap: "wrap",
    justifyContent: "center",
    gap: "0.75rem",
  },
  objectButton: {
    padding: "0.6rem 1rem",
    fontSize: "0.9rem",
    borderRadius: "6px",
    border: "1px solid #ccc",
    backgroundColor: "#f0f0f0",
    cursor: "pointer",
  },
};