import React from 'react';
import { Link } from 'react-router-dom';

const Policies: React.FC = () => {
    return (
        <div className="text-white text-xs py-8 space-x-8 justify-center flex w-full items-center px-8">
            <span>© 2024 OptiMatch. All rights reserved.</span>
            <Link to="/privacy-policy">Privacy Policy</Link>
            <Link to="/terms-of-service">Terms of Service</Link>
            <Link to="/cookie-settings">Cookie Settings</Link>
        </div>
    );
};

export default Policies;