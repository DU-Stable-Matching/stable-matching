import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { useUserStore } from '../userState.ts';

interface MatchApplicant {
  name: string;
  email: string;
  year_in_college?: number;
  is_returner?: boolean;
  why_ra?: string;
  resume_path?: string;
}

const AdminDashboard: React.FC = () => {
  const navigate = useNavigate();
  const userID = useUserStore(state => state.userID);
  const [match, setMatch] = useState<MatchApplicant | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios
      .get<{ match: MatchApplicant }>(
        `http://127.0.0.1:8000/api/admin_algorithm/${userID}`
      )
      .then(res => {
        setMatch(res.data);
      })
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  }, [userID]);

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
        <h1 className="text-3xl font-extrabold text-dark-green">Admin Dashboard</h1>
        <button
          onClick={() => navigate('/')}
          className="px-3 py-1 bg-transparent border-dark-green border-2 text-dark-green rounded-md hover:bg-dark-green hover:text-white transition-colors"
        >
          Logout
        </button>
      </div>

      <hr className="border-t-2 border-dark-green my-6 w-full" />

      {match ? (
        <div className="max-w-md mx-auto bg-white shadow-lg rounded-2xl p-6 space-y-2">
          <h2 className="text-2xl font-bold text-primary-dark">Match Found</h2>
          <p>
            <strong>Name:</strong> {match.name}
          </p>
          <p>
            <strong>Email:</strong>{' '}
            <a
              href={`mailto:${match.email}`}
              className="text-blue-500 hover:underline"
            >
              {match.email}
            </a>
          </p>
          {match.year_in_college !== undefined && (
            <p>
              <strong>Year in College:</strong> {match.year_in_college}
            </p>
          )}
          {match.is_returner !== undefined && (
            <p>
              <strong>Returner:</strong> {match.is_returner ? 'Yes' : 'No'}
            </p>
          )}
          {match.why_ra && (
            <p>
              <strong>Why RA:</strong> {match.why_ra}
            </p>
          )}
          {match.resume_path && (
            <p>
              <strong>Resume:</strong>{' '}
              <a
                href={`http://127.0.0.1:8000/api/applicant/resume/${match.resume_path}`}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-500 hover:underline"
              >
                Download
              </a>
            </p>
          )}
        </div>
      ) : (
        <div className="max-w-md mx-auto bg-white shadow-lg rounded-2xl p-6">
          <h2 className="text-xl font-semibold text-primary-dark">
            Waiting for Preferences
          </h2>
          <p>Waiting for applicants and other admins to submit preferences.</p>
        </div>
      )}
    </div>
  );
};

export default AdminDashboard;
