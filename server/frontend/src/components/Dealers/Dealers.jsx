import React, { useState, useEffect } from 'react';
import './Dealers.css';

const Dealers = () => {
    const [dealers, setDealers] = useState([]);
    const [filteredDealers, setFilteredDealers] = useState([]);
    const [selectedState, setSelectedState] = useState('');
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    const states = [
        { code: '', name: 'All States' },
        { code: 'CA', name: 'California' },
        { code: 'TX', name: 'Texas' },
        { code: 'NY', name: 'New York' },
        { code: 'FL', name: 'Florida' },
        { code: 'KS', name: 'Kansas' }
    ];

    useEffect(() => {
        fetchDealers();
    }, []);

    useEffect(() => {
        filterDealers();
    }, [dealers, selectedState]);

    const fetchDealers = async () => {
        try {
            setLoading(true);
            const response = await fetch('/djangoapp/get_dealers/');
            const data = await response.json();
            
            if (response.ok) {
                setDealers(data.dealers || []);
            } else {
                setError('Failed to load dealers');
            }
        } catch (err) {
            setError('Network error occurred');
        } finally {
            setLoading(false);
        }
    };

    const filterDealers = () => {
        if (!selectedState) {
            setFilteredDealers(dealers);
        } else {
            setFilteredDealers(dealers.filter(dealer => dealer.st === selectedState));
        }
    };

    const handleStateChange = (e) => {
        setSelectedState(e.target.value);
    };

    if (loading) {
        return (
            <div className="dealers-container">
                <div className="container mt-5">
                    <div className="text-center">
                        <div className="spinner-border text-primary" role="status">
                            <span className="visually-hidden">Loading...</span>
                        </div>
                        <p className="mt-2">Loading dealers...</p>
                    </div>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="dealers-container">
                <div className="container mt-5">
                    <div className="alert alert-danger text-center">
                        <h4>Error</h4>
                        <p>{error}</p>
                        <button className="btn btn-primary" onClick={fetchDealers}>
                            Try Again
                        </button>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="dealers-container">
            <div className="container mt-4">
                <div className="row mb-4">
                    <div className="col-md-8">
                        <h2>Car Dealerships</h2>
                        <p className="text-muted">Find trusted dealerships near you</p>
                    </div>
                    <div className="col-md-4">
                        <label htmlFor="stateFilter" className="form-label">Filter by State:</label>
                        <select 
                            id="stateFilter"
                            className="form-select" 
                            value={selectedState}
                            onChange={handleStateChange}
                        >
                            {states.map(state => (
                                <option key={state.code} value={state.code}>
                                    {state.name}
                                </option>
                            ))}
                        </select>
                    </div>
                </div>

                <div className="row">
                    {filteredDealers.length === 0 ? (
                        <div className="col-12">
                            <div className="text-center py-5">
                                <h4>No dealers found</h4>
                                <p>Try selecting a different state or check back later.</p>
                            </div>
                        </div>
                    ) : (
                        filteredDealers.map(dealer => (
                            <div key={dealer.id} className="col-md-6 col-lg-4 mb-4">
                                <div className="card dealer-card h-100">
                                    <div className="card-body">
                                        <h5 className="card-title">{dealer.full_name}</h5>
                                        <p className="card-text">
                                            <strong>Address:</strong> {dealer.address}<br/>
                                            <strong>City:</strong> {dealer.city}, {dealer.st}<br/>
                                            <strong>ZIP:</strong> {dealer.zip}
                                        </p>
                                        <div className="d-grid gap-2">
                                            <a 
                                                href={`/dealer/${dealer.id}`} 
                                                className="btn btn-primary"
                                            >
                                                View Details
                                            </a>
                                            <a 
                                                href={`/dealer/${dealer.id}/reviews`} 
                                                className="btn btn-outline-primary"
                                            >
                                                View Reviews
                                            </a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        ))
                    )}
                </div>

                {filteredDealers.length > 0 && (
                    <div className="row mt-4">
                        <div className="col-12 text-center">
                            <p className="text-muted">
                                Showing {filteredDealers.length} of {dealers.length} dealerships
                                {selectedState && ` in ${states.find(s => s.code === selectedState)?.name}`}
                            </p>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default Dealers;