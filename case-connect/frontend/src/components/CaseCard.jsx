// frontend/src/components/CaseCard.jsx
import React from 'react';

const CaseCard = ({ caseData }) => {
  if (!caseData) {
    return null;
  }

  console.log('CaseCard received data:', caseData);
  const { dataset, similarity, metadata } = caseData || {};
  const { file_path, sections } = metadata || {};
  const { full_text } = sections || {};

  // Extract the title from file_path
  const title = file_path ? file_path.split('/').pop().replace('.htm', '') : 'No Title';

  // Display the date if available
  const date = metadata && metadata.date ? metadata.date : 'Unknown Date';

  return (
    <div className="bg-white p-6 rounded-lg shadow-sm border mb-4 hover:shadow-md transition-shadow">
      <div className="flex justify-between items-start mb-3">
        <div>
          <h3 className="font-semibold text-lg text-gray-900">{title}</h3>
          <p className="text-sm text-gray-500">{dataset}</p>
        </div>
        <span className="text-sm text-gray-500">{date}</span>
      </div>

      <p className="text-sm text-gray-700 mb-3">
        {full_text ? full_text.slice(0, 300) + '...' : 'No Summary Available'}
      </p>

      {similarity !== undefined && (
        <p className="text-sm text-gray-500">Similarity: {similarity.toFixed(2)}</p>
      )}
    </div>
  );
};

export default CaseCard;
