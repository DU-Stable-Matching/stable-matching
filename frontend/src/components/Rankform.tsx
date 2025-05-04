import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Reorder } from 'framer-motion';
import ResumeUpload from './ResumeUpload.tsx';
import axios from 'axios';
import { useUserStore } from '../userState.ts';

interface RankFormProps {
  placesList: string[];
}

interface UploadResponse {
  filename: string;
}

const DraggableRankingCards: React.FC<RankFormProps> = ({ placesList }) => {
  const navigate = useNavigate();
  const [items, setItems] = useState<string[]>([...placesList]);
  const [paragraph, setParagraph] = useState('');
  const [resume, setResume] = useState('');
  const [isFirstTime, setIsFirstTime] = useState(false);
  const [error, setError] = useState('');
  const userID = useUserStore((state) => state.userID);

  const handleParagraphChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setParagraph(e.target.value);
  };

  const onUpload = async (file: File) => {
    const formData = new FormData();
    formData.append('resume', file, file.name);
    setResume(file.name);
    try {
      const resp = await axios.post<UploadResponse>(
        `http://127.0.0.1:8000/api/upload_resume/${userID}`,
        formData
      );
      console.log('Uploaded file:', resp.data.filename);
    } catch (err: any) {
      console.error('Upload failed:', err);
      throw err;
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!resume) {
      setError('Please upload your resume before submitting.');
      return;
    }
    if (paragraph.trim().length < 100) {
      setError('Your paragraph must be at least 100 characters long.');
      return;
    }
    setError('');

    const payload = {
      id: userID,
      is_returner: !isFirstTime,
      why_ra: paragraph,
      preferences: items.map((place, index) => ({
        building_name: place,
        rank: index + 1,
      })),
    };

    try {
      await axios.post('http://127.0.0.1:8000/api/apply', payload);
      // redirect after successful submission
      navigate('/dashboard');
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

      {/* Resume Upload */}
      <ResumeUpload onUpload={onUpload} />

      {/* First-time Applicant Radio */}
      <div className="mt-4">
        <span className="text-sm font-medium text-dark-green">First-time applicant?</span>
        <div className="mt-1 flex items-center space-x-6">
          <label className="inline-flex items-center">
            <input
              type="radio"
              name="firstTime"
              value="yes"
              checked={isFirstTime}
              onChange={() => setIsFirstTime(true)}
              className="form-radio h-4 w-4 text-dark-green"
            />
            <span className="ml-2 text-dark-green">Yes</span>
          </label>
          <label className="inline-flex items-center">
            <input
              type="radio"
              name="firstTime"
              value="no"
              checked={!isFirstTime}
              onChange={() => setIsFirstTime(false)}
              className="form-radio h-4 w-4 text-dark-green"
            />
            <span className="ml-2 text-dark-green">No</span>
          </label>
        </div>
      </div>

      {/* Ranking Section */}
      <div>
        <h2 className="text-xl font-semibold text-dark-green">
          Rank Your Top Places to Work
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

      {/* Paragraph Section */}
      <div>
        <label
          htmlFor="paragraph"
          className="block text-sm font-medium text-dark-green"
        >
          Short Paragraph
        </label>
        <textarea
          id="paragraph"
          rows={4}
          value={paragraph}
          onChange={handleParagraphChange}
          className="mt-1 block w-full shadow-sm border border-cool-gray rounded-md p-2 focus:ring-dark-green focus:border-dark-green sm:text-sm"
          placeholder="At least 100 characters…"
        />
        {/* <p className="text-sm text-gray-500 mt-1">{paragraph.length} / 100 characters</p> */}
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
