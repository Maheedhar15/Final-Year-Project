import React, { useState } from 'react';
import Select from 'react-select';
import { BsArrowRight, BsCheckLg } from 'react-icons/bs';
import '../index.css';

function Dropdown(props) {
  const [isOpen, setIsOpen] = useState(false);
  const [Selected, setSelected] = useState(false);
  const [Label, setLabel] = useState('');

  const options = [
    { value: 'framingham', label: 'Framingham Dataset' },
    { value: 'keel', label: 'KEEL Heart Disease Dataset' },
    { value: 'Cleveland', label: 'Cleveland Dataset' },
  ];

  const handleDataChange = (selectedOption) => {
    props.setSelectedModel(selectedOption['value']);
    setLabel(selectedOption['label']);
    setSelected(true);
    setIsOpen(false);
  };
  return (
    <div className="flex duration-300 w-[220px]">
      <div className=" mt-[20px]">
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="text-[#fff] font-poppins px-[10px] py-[10px] border-[1px] border-[#7EFF66] rounded-[10px]"
        >
          {Selected ? Label : 'Framingham Dataset'}
        </button>
        {isOpen && (
          <div className="flex flex-col">
            <Select
              className="basic-single w-[400px] font-poppins text-[#000]"
              placeholder={props.SelectedModel}
              name={props.SelectedModel}
              options={options}
              value={props.SelectedModel}
              onChange={handleDataChange}
            />
          </div>
        )}
      </div>
    </div>
  );
}

export default Dropdown;
