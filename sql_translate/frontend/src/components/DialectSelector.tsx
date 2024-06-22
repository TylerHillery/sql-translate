import React, { useEffect, useState } from "react";

interface DialectSelectorProps {
  onSelect: (dialect: string) => void;
  defaultValue: string;
}

const DialectSelector: React.FC<DialectSelectorProps> = ({
  onSelect,
  defaultValue,
}) => {
  const [dialects, setDialects] = useState<string[]>([]);
  const [selectedDialect, setSelectedDialect] = useState<string>(defaultValue);

  useEffect(() => {
    fetch("http://localhost:8000/dialects")
      .then((response) => response.json())
      .then((data) => {
        setDialects(data);
        if (!data.includes(defaultValue)) {
          setSelectedDialect(data[0]); // Set the first dialect as selected if defaultValue is not in the list
          onSelect(data[0]); // Notify the parent about the initial selection
        } else {
          setSelectedDialect(defaultValue); // Set the default value if it exists in the list
          onSelect(defaultValue); // Notify the parent about the initial selection
        }
      })
      .catch((err) => console.log(err));
  }, [onSelect, defaultValue]);

  const handleSelectChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const selectedValue = event.target.value;
    setSelectedDialect(selectedValue);
    onSelect(selectedValue); // Notify the parent about the change
  };

  return (
    <select value={selectedDialect} onChange={handleSelectChange}>
      {dialects.map((dialect, index) => (
        <option key={index} value={dialect}>
          {dialect}
        </option>
      ))}
    </select>
  );
};

export default DialectSelector;
