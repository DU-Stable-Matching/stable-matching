import React, { useState } from 'react';
import ResumeUpload from './ResumeUpload.tsx';

interface RankFormProps {
    placesList: string[];
}

const RankForm: React.FC<RankFormProps> = ({ placesList }) => {
    const [ranks, setRanks] = useState<number[]>(Array(placesList.length).fill(0));
    const [paragraph, setParagraph] = useState('');
    const [resume, setResume] = useState<File | null>(null);

    const handleRankChange = (index: number) => (event: React.ChangeEvent<HTMLSelectElement>) => {
        const newRanks = [...ranks];
        newRanks[index] = parseInt(event.target.value, 10);
        setRanks(newRanks);
    };

    const handleParagraphChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
        console.log(event.target.value);
        setParagraph(event.target.value);
    };

    const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        // Handle form submission logic here
        console.log({ ranks, paragraph, resume });
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-6">
            <ResumeUpload />
            <div>
                <h2 className="text-xl font-semibold text-dark-green">Rank Your Top Places to Work</h2>
                <div className="mt-4 space-y-4">
                    {placesList.map((place, idx) => (
                        <div key={idx} className="flex items-center space-x-4">
                            <span className="w-32 text-dark-green">{place}</span>
                            <select
                                value={ranks[idx]}
                                onChange={handleRankChange(idx)}
                                className="mt-1 block pl-3 pr-10 py-2 border border-cool-gray rounded-md focus:outline-none focus:ring-dark-green focus:border-dark-green sm:text-sm"
                            >
                                <option value={0}>Select rank</option>
                                {Array.from({ length: placesList.length }, (_, i) => i + 1).map((num) => (
                                    <option key={num} value={num}>{num}</option>
                                ))}
                            </select>
                        </div>
                    ))}
                </div>
            </div>

            <div>
                <label htmlFor="paragraph" className="block text-sm font-medium text-dark-green">
                    Short Paragraph
                </label>
                <textarea
                    id="paragraph"
                    rows={4}
                    value={paragraph}
                    onChange={handleParagraphChange}
                    className="mt-1 block w-full shadow-sm border border-cool-gray rounded-md p-2 focus:ring-dark-green focus:border-dark-green sm:text-sm"
                />
            </div>

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

export default RankForm;