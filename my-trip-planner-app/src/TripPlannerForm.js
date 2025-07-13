// src/TripPlannerForm.js
import React, { useState } from 'react';

function TripPlannerForm() {
  // State for form inputs
  const [origin, setOrigin] = useState('');
  const [cities, setCities] = useState('');
  const [dateRange, setDateRange] = useState('');
  const [interests, setInterests] = useState('');

  // State for API response, loading, and error
  const [tripPlan, setTripPlan] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (event) => {
    event.preventDefault(); // Prevent default form submission behavior

    setLoading(true); // Indicate loading
    setError(null);    // Clear previous errors
    setTripPlan(null); // Clear previous trip plan

    // Construct the request body matching your FastAPI's TripRequest Pydantic model
    const requestBody = {
      origin: origin,
      cities: cities,
      date_range: dateRange, // Ensure this matches 'date_range' in your Pydantic model
      interests: interests,
    };

    try {
      const response = await fetch('http://localhost:8000/plan_trip', { // Your FastAPI endpoint
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody), // Send the data as a JSON string
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setTripPlan(data.trip_plan); // Assuming your FastAPI returns `{"status": "success", "trip_plan": "..."}`
    } catch (err) {
      console.error("Error planning trip:", err);
      setError(err.message);
    } finally {
      setLoading(false); // End loading
    }
  };

  return (
    <div style={{ maxWidth: '800px', margin: '20px auto', padding: '20px', border: '1px solid #ccc', borderRadius: '8px', boxShadow: '2px 2px 10px rgba(0,0,0,0.1)' }}>
      <h1>Plan Your AI-Powered Trip</h1>
      <form onSubmit={handleSubmit} style={{ display: 'grid', gap: '15px' }}>
        <div>
          <label htmlFor="origin" style={{ display: 'block', marginBottom: '5px' }}>Origin:</label>
          <input
            type="text"
            id="origin"
            value={origin}
            onChange={(e) => setOrigin(e.target.value)}
            required
            style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ddd' }}
          />
        </div>
        <div>
          <label htmlFor="cities" style={{ display: 'block', marginBottom: '5px' }}>Cities to visit (comma-separated):</label>
          <input
            type="text"
            id="cities"
            value={cities}
            onChange={(e) => setCities(e.target.value)}
            required
            style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ddd' }}
          />
        </div>
        <div>
          <label htmlFor="dateRange" style={{ display: 'block', marginBottom: '5px' }}>Date Range (e.g., "July 1st to July 10th"):</label>
          <input
            type="text"
            id="dateRange"
            value={dateRange}
            onChange={(e) => setDateRange(e.target.value)}
            required
            style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ddd' }}
          />
        </div>
        <div>
          <label htmlFor="interests" style={{ display: 'block', marginBottom: '5px' }}>Interests (e.g., "museums, food, hiking"):</label>
          <input
            type="text"
            id="interests"
            value={interests}
            onChange={(e) => setInterests(e.target.value)}
            required
            style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ddd' }}
          />
        </div>
        <button
          type="submit"
          disabled={loading}
          style={{
            padding: '10px 20px',
            backgroundColor: '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
            fontSize: '16px',
            opacity: loading ? 0.7 : 1
          }}
        >
          {loading ? 'Planning Trip...' : 'Generate Trip Plan'}
        </button>
      </form>

      {error && (
        <div style={{ color: 'red', marginTop: '20px', padding: '10px', border: '1px solid red', borderRadius: '4px' }}>
          <h3>Error:</h3>
          <p>{error}</p>
        </div>
      )}

      {tripPlan && (
        <div style={{ marginTop: '30px', padding: '20px', backgroundColor: '#f9f9f9', border: '1px solid #eee', borderRadius: '8px' }}>
          <h2>Your Trip Plan:</h2>
          {/* We'll use dangerouslySetInnerHTML to render the markdown content.
              Be careful with this if the content is not trusted, as it can expose to XSS.
              For AI-generated content, it's generally acceptable for user's own consumption.
              Alternatively, use a markdown renderer library like 'react-markdown'.
          */}
          <div dangerouslySetInnerHTML={{ __html: tripPlan.replace(/\n/g, '<br>') }} />
        </div>
      )}
    </div>
  );
}

export default TripPlannerForm;