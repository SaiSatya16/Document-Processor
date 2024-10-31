import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Toaster } from "./components/ui/toaster";
import Navbar from './components/layout/Navbar';
import DocumentUpload from './pages/DocumentUpload';
import About from './pages/About';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<DocumentUpload />} />
            <Route path="/about" element={<About />} />
          </Routes>
        </main>
        <Toaster />
      </div>
    </Router>
  );
}

export default App;