import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Reorder } from 'framer-motion';
import axios from 'axios';
import { useUserStore } from '../userState';

interface RankFormProps {
  nameList: string[];
}

const DraggableRankingCards: React.FC<RankFormProps> = ({ nameList }) => {
  const navigate = useNavigate();
  const [items, setItems] = useState<string[]>([...nameList]);
  const [error, setError] = useState('');
  const userID = useUserStore((state) => state.userID);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    // Build payload in required format
    const payload = {
      admin_id: userID,
      list_of_rankings: items.map((applicantName, index) => ({
        applicant_name: applicantName,
        rank: index + 1,
      })),
    };

    console.log('Submitting payload:', payload);

    try {
      await axios.post('http://127.0.0.1:8000/api/admin_rank/', payload);
      navigate('/admin_dashboard');
    } catch (err: any) {
      console.error('Submit failed:', err);
      setError('Submission failed. Please try again later.');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {error && (
        <div className="p-3 bg-red-100 border border-red-400 text-red-700 rounded">
          {error}
        </div>
      )}

      {/* Ranking Section */}
      <div>
        <h2 className="text-xl font-semibold text-dark-green">
          Rank Your Top Names
        </h2>
        <Reorder.Group
          axis="y"
          values={items}
          onReorder={setItems}
          className="mt-4 space-y-4"
        >
          {items.map((item) => (
            <Reorder.Item
              key={item}
              value={item}
              whileDrag={{ scale: 1.02 }}
              className="p-4 bg-white shadow border-2 border-gray-300 rounded-lg cursor-grab"
            >
              {item}
            </Reorder.Item>
          ))}
        </Reorder.Group>
      </div>

      {/* Submit Button */}
      <div>
        <button
          type="submit"
          className="w-full py-2 px-4 bg-dark-green text-white font-medium rounded-md hover:bg-myrtle-green focus:outline-none focus:ring-2 focus:ring-dark-green"
        >
          Submit
        </button>
      </div>
    </form>
  );
};

export default DraggableRankingCards;
