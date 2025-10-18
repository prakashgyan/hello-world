import React from 'react';
import FileUpload from './components/FileUpload';
import Flashcard from './components/Flashcard';
import Stats from './components/Stats';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Flashcard App</h1>
      </header>
      <main>
        <FileUpload />
        <Flashcard />
        <Stats />
      </main>
    </div>
  );
}

export default App;
