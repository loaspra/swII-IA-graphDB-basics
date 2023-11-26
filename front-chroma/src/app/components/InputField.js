import { useState } from 'react';

const InputField = () => {
  const [value, setValue] = useState('');

  const handleChange = (event) => {
    setValue(event.target.value);
  };

  return (
    <input
      type="text"
      value={value}
      onChange={handleChange}
      placeholder="Enter a movie name"
      className="neumorphism-input"
    />
  );
};

export default InputField;