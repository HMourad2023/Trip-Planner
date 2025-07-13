// src/App.js
import React from 'react';
import './App.css'; // Assuming you have some basic CSS or can create one
import TripPlannerForm from './TripPlannerForm';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        {/* You can add a header or navigation here */}
      </header>
      <main>
        <TripPlannerForm />
      </main>
    </div>
  );
}

export default App;