import React, { useState } from 'react';
import '../index.css';
import Reveal from '../components/Reveal';
const KEELDataset = () => {
  const [KData, setKData] = useState({
    age: '',
    gender: '',
    height: '',
    weight: '',
    ap_hi: '',
    alco: '',
    active: '',
    smoke: '',
    ap_lo: '',
    gluc: '',
    cholestrol: '',
  });

  const handleDataChange = (event) => {
    const { name, value } = event.target;
    setKData({ ...KData, [name]: value });
  };

  const handlePredict = async () => {
    await axios
      .post('https://maheedhar.pythonanywhere.com/predict_keel', KData)
      .then((res) => {
        if (res.data.value == '0') {
          toast.success(res.data.prediction, {
            duration: 4000,
            position: 'top-center',
          });
        } else {
          toast.error(res.data.prediction, {
            duration: 4000,
            position: 'top-center',
          });
        }
      });
  };

  return (
    <Reveal>
      <div className="mt-[40px] ml-[20px]">
        <div className="grid-cols-2 grid gap-[40px]">
          <div className=" flex gap-[20px]">
            <span className="input-text">Gender:</span>
            <div className="border-2 border-[#7EFF66] rounded">
              <input
                type="text"
                className="box-text"
                required={true}
                value={KData.gender}
                name="gender"
                onChange={(e) => handleDataChange(e)}
              />
            </div>
          </div>
          <div className=" flex gap-[20px]">
            <span className="input-text">Age:</span>
            <div className="border-2 border-[#7EFF66] rounded">
              <input
                type="number"
                className="box-text"
                required={true}
                value={KData.age}
                name="age"
                onChange={(e) => handleDataChange(e)}
              />
            </div>
          </div>
          <div className=" flex gap-[20px]">
            <span className="input-text">Are you a current Smoker:</span>
            <div className="border-2 border-[#7EFF66] rounded">
              <input
                type="text"
                className="box-text"
                required={true}
                value={KData.smoke}
                name="smoke"
                onChange={(e) => handleDataChange(e)}
              />
            </div>
          </div>
          <div className=" flex gap-[20px]">
            <span className="input-text">Weight(in kg):</span>
            <div className="border-2 border-[#7EFF66] rounded">
              <input
                type="number"
                className="box-text"
                required={true}
                value={KData.weight}
                name="weight"
                onChange={(e) => handleDataChange(e)}
              />
            </div>
          </div>
          <div className=" flex gap-[20px]">
            <span className="input-text">Height(in cm):</span>
            <div className="border-2 border-[#7EFF66] rounded">
              <input
                type="number"
                className="box-text"
                required={true}
                value={KData.height}
                name="height"
                onChange={(e) => handleDataChange(e)}
              />
            </div>
          </div>
          <div className=" flex gap-[20px]">
            <span className="input-text">
              Enter your glucose levels in the range of 1 to 3:
            </span>
            <div className="border-2 border-[#7EFF66] rounded">
              <input
                type="number"
                className="box-text"
                required={true}
                value={KData.cholestrol}
                name="cholestrol"
                onChange={(e) => handleDataChange(e)}
              />
            </div>
          </div>
          <div className=" flex gap-[20px]">
            <span className="input-text">Systolic Blood Pressure:</span>
            <div className="border-2 border-[#7EFF66] rounded">
              <input
                type="number"
                className="box-text"
                required={true}
                value={KData.ap_hi}
                name="ap_hi"
                onChange={(e) => handleDataChange(e)}
              />
            </div>
          </div>
          <div className=" flex gap-[20px]">
            <span className="input-text">Diastolic Blood Pressure:</span>
            <div className="border-2 border-[#7EFF66] rounded">
              <input
                type="number"
                className="box-text"
                required={true}
                value={KData.ap_lo}
                name="ap_lo"
                onChange={(e) => handleDataChange(e)}
              />
            </div>
          </div>
          <div className=" flex gap-[20px]">
            <span className="input-text">Do you consume alcohol:</span>
            <div className="border-2 border-[#7EFF66] rounded">
              <input
                type="text"
                className="box-text"
                required={true}
                value={KData.alco}
                name="alco"
                onChange={(e) => handleDataChange(e)}
              />
            </div>
          </div>
          <div className=" flex gap-[20px]">
            <span className="input-text">Are you active(Y/N):</span>
            <div className="border-2 border-[#7EFF66] rounded">
              <input
                type="text"
                className="box-text"
                required={true}
                value={KData.active}
                name="active"
                onChange={(e) => handleDataChange(e)}
              />
            </div>
          </div>
          <div className=" flex gap-[20px]">
            <span className="input-text">Enter your glucose level :</span>
            <div className="border-2 border-[#7EFF66] rounded">
              <input
                type="number"
                className="box-text"
                required={true}
                value={KData.gluc}
                name="gluc"
                onChange={(e) => handleDataChange(e)}
              />
            </div>
          </div>
        </div>
        <div>
          <button className="font-poppins py-[10px] px-[10px] bg-[#7EFF66] border-[1px] border-[#fff] text-[#000] rounded-[10px] font-semibold text-[18px] ml-[700px] mt-[60px]">
            Predict
          </button>
        </div>
      </div>
    </Reveal>
  );
};

export default KEELDataset;
