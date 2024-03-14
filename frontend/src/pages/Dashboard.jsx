import { useState } from 'react';
import Dropdown from '../Components/Dropdown';
import Reveal from '../Components/Reveal';
import { FaHandHoldingHeart } from 'react-icons/fa';
import { AiOutlineUser } from 'react-icons/ai';
import { BiInfoCircle } from 'react-icons/bi';
import FraminghamDataset from './FraminghamDataset';
import KEELDataset from './KEELDataset';
import '../index.css';
import ClevelandDataset from './ClevelandDataset';
import { toast } from 'react-hot-toast';
import { Toaster } from 'react-hot-toast';

function Dashboard() {
  const [SelectedModel, setSelectedModel] = useState('framingham');
  const [LegendToggle, setLegendToggle] = useState(false);

  const handleInfo = () => {
    toast.success(
      'There are three datasets available, choose the one that best fits the data that you have',
      {
        duration: 4000,
        position: 'top-center',
      }
    );
  };
  return (
    <>
      <Toaster />
      <div className="main">
        <div className="px-[5px] py-[5px] flex w-full">
          <FaHandHoldingHeart className="fill-[#7EFF66] w-[50px] h-[50px] ml-[10px] mt-[10px]" />
          <span className="font-poppins text-[24px] font-bold text-center align-middle mt-[20px] ml-[15px]">
            HeartSolutions
          </span>

          <div className="justify-end items-end self-end align-self-end ml-[1620px]">
            <button>
              <AiOutlineUser className="fill-[#fff] px-[3px] py-[5px] mt-[20px] w-[40px] h-[40px] border-[1px] border-[#7EFF66] rounded-[20px]" />
            </button>
          </div>
        </div>

        <Reveal>
          <h1 className="font-poppins text-center justify-center ml-[20px] mt-[40px] text-[#7EFF66]">
            Select Model
          </h1>
        </Reveal>
        <div className="card ml-[20px] flex">
          <Dropdown
            SelectedModel={SelectedModel}
            setSelectedModel={setSelectedModel}
          />
          <button onClick={() => handleInfo()}>
            <BiInfoCircle className="w-[30px] h-[30px] fill-[#7EFF66] text-[#fff] mt-[18px]" />
          </button>
        </div>
        <div>
          {SelectedModel == 'framingham' ? (
            <FraminghamDataset />
          ) : SelectedModel == 'keel' ? (
            <KEELDataset />
          ) : (
            <ClevelandDataset />
          )}
        </div>
      </div>
    </>
  );
}

export default Dashboard;
