import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { useUserStore } from '../userState';

interface Match {
  name: string;
  ra_needed: number;
  admin_name: string;
}

const ApplicantDashboard: React.FC = () => {
  const userID = useUserStore(state => state.userID);
  const setUserID = useUserStore(state => state.setUserID);
  const navigate = useNavigate();
  const [match, setMatch] = useState<Match | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios
      .get<Match>(`http://127.0.0.1:8000/api/user_algorithm/${userID}`)
      .then(res => {
        setMatch(res.data);
      })
      .catch(err => {
        console.error('Error fetching match:', err);
        setMatch(null);
      })
      .finally(() => setLoading(false));
  }, [userID]);

  const handleLogout = () => {
    // Clear the user state and redirect back to the home page
    setUserID(null);
    navigate('/');
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-periwinkle p-4">
        <p className="text-lg text-dark-green">Loading...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-periwinkle p-6">
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-3xl font-extrabold text-dark-green">Applicant Dashboard</h1>
        <button
          onClick={handleLogout}
          className="px-3 py-1 bg-transparent border-dark-green border-2 text-dark-green rounded-md hover:bg-dark-green hover:text-white transition-colors"
        >
          Logout
        </button>
      </div>
      <hr className="border-t-2 border-dark-green my-6 w-full" />

      {match ? (
        <div className="max-w-md mx-auto bg-white shadow-lg rounded-2xl p-6 space-y-4">
          <h2 className="text-2xl font-bold text-primary-dark">Match Details</h2>
          <p><strong>Building:</strong> {match.name}</p>
          <p><strong>RAs Needed:</strong> {match.ra_needed}</p>
          <p><strong>Assigned Admin:</strong> {match.admin_name}</p>
        </div>
      ) : (
        <div className="max-w-md mx-auto bg-white shadow-lg rounded-2xl p-6">
          <h2 className="text-xl font-semibold text-primary-dark mb-2">Waiting for Match</h2>
          <p>Waiting for admins and other applicants to submit preferences.</p>
        </div>
      )}
    </div>
  );
};

export default ApplicantDashboard;
