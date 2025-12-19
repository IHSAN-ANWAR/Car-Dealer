import React, { useState } from 'react';
import './Login.css';

const Login = () => {
    const [formData, setFormData] = useState({
        userName: '',
        password: ''
    });
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState('');

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setMessage('');

        try {
            const response = await fetch('/djangoapp/login/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();

            if (response.ok) {
                setMessage('Login successful!');
                // Redirect to home page or dashboard
                window.location.href = '/';
            } else {
                setMessage(data.error || 'Login failed. Please check your credentials.');
            }
        } catch (error) {
            setMessage('Network error. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="login-container">
            <div className="container mt-5">
                <div className="row justify-content-center">
                    <div className="col-md-5">
                        <div className="card shadow">
                            <div className="card-header bg-primary text-white text-center">
                                <h3>Sign In</h3>
                                <p className="mb-0">Welcome back! Please sign in to your account</p>
                            </div>
                            <div className="card-body">
                                {message && (
                                    <div className={`alert ${message.includes('successful') ? 'alert-success' : 'alert-danger'}`}>
                                        {message}
                                    </div>
                                )}
                                
                                <form onSubmit={handleSubmit}>
                                    <div className="mb-3">
                                        <label htmlFor="userName" className="form-label">Username</label>
                                        <input
                                            type="text"
                                            className="form-control"
                                            id="userName"
                                            name="userName"
                                            value={formData.userName}
                                            onChange={handleChange}
                                            required
                                            placeholder="Enter your username"
                                        />
                                    </div>

                                    <div className="mb-3">
                                        <label htmlFor="password" className="form-label">Password</label>
                                        <input
                                            type="password"
                                            className="form-control"
                                            id="password"
                                            name="password"
                                            value={formData.password}
                                            onChange={handleChange}
                                            required
                                            placeholder="Enter your password"
                                        />
                                    </div>

                                    <button 
                                        type="submit" 
                                        className="btn btn-primary w-100"
                                        disabled={loading}
                                    >
                                        {loading ? (
                                            <>
                                                <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                                                Signing in...
                                            </>
                                        ) : (
                                            'Sign In'
                                        )}
                                    </button>
                                </form>

                                <div className="text-center mt-3">
                                    <p>Don't have an account? <a href="/register">Sign up here</a></p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Login;