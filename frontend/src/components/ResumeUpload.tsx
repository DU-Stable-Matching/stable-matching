import React, { useState } from 'react';

const ResumeUpload: React.FC = () => {
    const [resumeFile, setResumeFile] = useState<File | null>(null);

    const handleResumeChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0];
        if (file) {
            setResumeFile(file);
            console.log('Selected file:', file.name);
        }
    };

    const handleSubmit = (event: React.FormEvent) => {
        event.preventDefault();
        if (resumeFile) {
            // Handle file upload logic here
            console.log('Uploading file:', resumeFile);
        } else {
            console.log('No file selected');
        }
    };

    return (
            <div>
                <label htmlFor="resume" className="block text-sm font-medium text-gray-700">
                    Upload Resume
                </label>
                <input
                    id="resume"
                    type="file"
                    accept=".pdf,.doc,.docx"
                    onChange={handleResumeChange}
                    className="mt-1 block w-full text-sm text-gray-900"
                />
            </div>

    );
};

export default ResumeUpload;