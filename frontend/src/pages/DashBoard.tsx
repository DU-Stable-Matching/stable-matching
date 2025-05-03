import React from 'react';

const DashBoard: React.FC = () => (
  <div className="min-h-screen flex flex-col items-center justify-center bg-periwinkle p-4">
    <h1 className="text-4xl font-bold text-dark-green mb-4">Under Construction</h1>
    <p className="text-lg text-dark-green mb-8">
      We're working hard to bring you a new experience. Stay tuned!
    </p>
    <img
      src={require("../assets/img/worker-bro.png")}
      alt="Under Construction"
      className="max-w-xs"
    />
  </div>
);

export default DashBoard;
