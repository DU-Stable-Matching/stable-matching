// src/pages/AdminPreferences.tsx

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import TopBar from '../components/TopBar.tsx';
import RankForm from '../components/AdminRankForm.tsx';

interface Applicant {
  // whatever other fields you get...
  name: string;
}

const AdminPreferences: React.FC = () => {
  const [nameList, setNameList] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchNames = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/get_all_applicants/');
        console.log('Response:', response);
        // pull the array out of response.data.body
        const applicants = response.data;
        console.log('Fetched applicants:', applicants);
        // map just the name field
        setNameList(applicants.map(a => a.name));
      } catch (err) {
        console.error('Failed to load applicants', err);
      } finally {
        setLoading(false);
      }
    };

    fetchNames();
  }, []);

  if (loading) {
    return (
      <>
        <TopBar />
        <div className="min-h-screen flex items-center justify-center">
          Loading applicants…
        </div>
      </>
    );
  }

  return (
    <>
      <TopBar />
      <div className="min-h-screen bg-periwinkle flex flex-col items-center p-4 pt-24">
        <div className="w-full max-w-2xl bg-white shadow-md rounded-lg p-6 border-t-4 border-dark-green">
          <h1 className="text-3xl font-extrabold mb-6 text-center text-dark-green">
            Admin Preferences
          </h1>
          <RankForm nameList={nameList} />
        </div>
      </div>
    </>
  );
};

export default AdminPreferences;
