import React from 'react';

function SubmitButton({ onSubmit }) {
  const handleClick = () => {
    onSubmit();
  };

  return (
    <button className="submit-button" onClick={handleClick}>
      Get Recommendations
    </button>
  );
}

export default SubmitButton;