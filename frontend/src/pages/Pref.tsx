import React from 'react';
import TopBar from '../components/TopBar.tsx';
import RankForm from '../components/Rankform.tsx';

const Reast: React.FC = () => {
  return (
    <>
      <TopBar />
      <div className="min-h-screen bg-periwinkle flex flex-col items-center p-4 pt-24">
        <div className="w-full max-w-2xl bg-white shadow-md rounded-lg p-6 border-t-4 border-dark-green">
          <h1 className="text-3xl font-extrabold mb-6 text-center text-dark-green">
            User Preferences
          </h1>
          <RankForm
            placesList={[
              'Google',
              'Amazon',
              'Microsoft',
              'Apple',
              'Meta',
              'Netflix',
              'Tesla',
            ]}
          />
        </div>
      </div>
    </>
  );
};

export default Reast;
