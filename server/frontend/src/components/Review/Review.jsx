import React, { useState, useEffect } from 'react';
import './Review.css';

const Review = ({ dealerId }) => {
    const [formData, setFormData] = useState({
        name: '',
        review: '',
        purchase: false,
        purchase_date: '',
        car_make: '',
        car_model: '',
        car_year: ''
    });
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState('');
    const [carMakes, setCarMakes] = useState([]);

    useEffect(() => {
        fetchCarMakes();
    }, []);

    const fetchCarMakes = async () => {
        try {
            const response = await fetch('/djangoapp/get_cars/');
            const data = await response.json();
            if (response.ok) {
                setCarMakes(data.CarModels || []);
            }
        } catch (error) {
            console.error('Error fetching car makes:', error);
        }
    };

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: type === 'checkbox' ? checked : value
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setMessage('');

        try {
            const reviewData = {
                ...formData,
                dealership: dealerId
            };

            const response = await fetch('/djangoapp/add_review/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(reviewData)
            });

            const data = await response.json();

            if (response.ok) {
                setMessage('Review submitted successfully!');
                setFormData({
                    name: '',
                    review: '',
                    purchase: false,
                    purchase_date: '',
                    car_make: '',
                    car_model: '',
                    car_year: ''
                });
            } else {
                setMessage(data.error || 'Failed to submit review');
            }
        } catch (error) {
            setMessage('Network error. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const uniqueMakes = [...new Set(carMakes.map(car => car.CarMake))];

    return (
        <div className="review-container">
            <div className="container mt-4">
                <div className="row justify-content-center">
                    <div className="col-md-8">
                        <div className="card shadow">
                            <div className="card-header bg-primary text-white">
                                <h3 className="mb-0">Post a Review</h3>
                                <p className="mb-0">Share your experience with this dealership</p>
                            </div>
                            <div className="card-body">
                                {message && (
                                    <div className={`alert ${message.includes('successfully') ? 'alert-success' : 'alert-danger'}`}>
                                        {message}
                                    </div>
                                )}

                                <form onSubmit={handleSubmit}>
                                    <div className="mb-3">
                                        <label htmlFor="name" className="form-label">Your Name *</label>
                                        <input
                                            type="text"
                                            className="form-control"
                                            id="name"
                                            name="name"
                                            value={formData.name}
                                            onChange={handleChange}
                                            required
                                            placeholder="Enter your full name"
                                        />
                                    </div>

                                    <div className="mb-3">
                                        <label htmlFor="review" className="form-label">Review *</label>
                                        <textarea
                                            className="form-control"
                                            id="review"
                                            name="review"
                                            rows="4"
                                            value={formData.review}
                                            onChange={handleChange}
                                            required
                                            placeholder="Share your experience with this dealership..."
                                        />
                                    </div>

                                    <div className="mb-3 form-check">
                                        <input
                                            type="checkbox"
                                            className="form-check-input"
                                            id="purchase"
                                            name="purchase"
                                            checked={formData.purchase}
                                            onChange={handleChange}
                                        />
                                        <label className="form-check-label" htmlFor="purchase">
                                            I purchased a vehicle from this dealership
                                        </label>
                                    </div>

                                    {formData.purchase && (
                                        <div className="purchase-details">
                                            <div className="row">
                                                <div className="col-md-6 mb-3">
                                                    <label htmlFor="purchase_date" className="form-label">Purchase Date</label>
                                                    <input
                                                        type="date"
                                                        className="form-control"
                                                        id="purchase_date"
                                                        name="purchase_date"
                                                        value={formData.purchase_date}
                                                        onChange={handleChange}
                                                    />
                                                </div>
                                                <div className="col-md-6 mb-3">
                                                    <label htmlFor="car_year" className="form-label">Car Year</label>
                                                    <input
                                                        type="number"
                                                        className="form-control"
                                                        id="car_year"
                                                        name="car_year"
                                                        value={formData.car_year}
                                                        onChange={handleChange}
                                                        min="1990"
                                                        max="2025"
                                                        placeholder="e.g., 2023"
                                                    />
                                                </div>
                                            </div>
                                            <div className="row">
                                                <div className="col-md-6 mb-3">
                                                    <label htmlFor="car_make" className="form-label">Car Make</label>
                                                    <select
                                                        className="form-select"
                                                        id="car_make"
                                                        name="car_make"
                                                        value={formData.car_make}
                                                        onChange={handleChange}
                                                    >
                                                        <option value="">Select a make</option>
                                                        {uniqueMakes.map(make => (
                                                            <option key={make} value={make}>{make}</option>
                                                        ))}
                                                    </select>
                                                </div>
                                                <div className="col-md-6 mb-3">
                                                    <label htmlFor="car_model" className="form-label">Car Model</label>
                                                    <select
                                                        className="form-select"
                                                        id="car_model"
                                                        name="car_model"
                                                        value={formData.car_model}
                                                        onChange={handleChange}
                                                        disabled={!formData.car_make}
                                                    >
                                                        <option value="">Select a model</option>
                                                        {carMakes
                                                            .filter(car => car.CarMake === formData.car_make)
                                                            .map(car => (
                                                                <option key={car.CarModel} value={car.CarModel}>
                                                                    {car.CarModel}
                                                                </option>
                                                            ))
                                                        }
                                                    </select>
                                                </div>
                                            </div>
                                        </div>
                                    )}

                                    <button 
                                        type="submit" 
                                        className="btn btn-primary btn-lg w-100"
                                        disabled={loading}
                                    >
                                        {loading ? (
                                            <>
                                                <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                                                Submitting...
                                            </>
                                        ) : (
                                            'Submit Review'
                                        )}
                                    </button>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Review;