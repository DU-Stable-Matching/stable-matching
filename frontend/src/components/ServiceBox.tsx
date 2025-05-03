import React from 'react';
import { Link } from 'react-router-dom';
import { FaBox } from 'react-icons/fa';

interface ServiceBoxProps {
  title: string;
  description: string;
  buttonText: string;
  link?: string;
}

const ServiceBox: React.FC<ServiceBoxProps> = ({ title, description, buttonText, link }) => {
  const content = (
    <button className="mt-4 px-4 py-2 bg-dark-green text-white rounded-md hover:bg-myrtle-green transition-colors">
      {buttonText}
    </button>
  );

  return (
    <div className="space-y-8 text-white">
      <FaBox color="white" size={30} />
      <h2 className="text-xl font-semibold">{title}</h2>
      <p className="text-base">{description}</p>
      {link ? <Link to={link}>{content}</Link> : content}
    </div>
  );
};

export default ServiceBox;